---
name: engineering-flow
description: "Run Issue-first Wayfinding for substantive engineering requirements, discussions, research, fixes, reviews, and delivery. Create a minimal local tracking record, select the appropriate mattpocock-skills workflow, and require an Implementation-ready gate before code changes. Load local configuration for organization, framework, tool, environment, and verification conventions; otherwise use the generic flow. Publish or change a GitHub Issue only with explicit tracking intent and the required repository, visibility, and data-protection checks."
---

# Engineering Flow

Keep each engineering task on a verifiable chain: **Issue/Map → evidence → decision → authorization → change → verification → review → delivery**. Every requirement, discussion, research activity, and fix leaves a traceable purpose, evidence, decision, and status in its Issue, so cross-service ownership, public contracts, and release state cannot be hidden by a vague “done”.

## Audience-aware language

Choose the language before producing an artifact. Language is part of the artifact’s contract: an AI needs unambiguous operational instructions, while a person needs language they can read, forward, and decide from.

- Write **English** for material intended exclusively for an AI or engineering tool: Skill instructions, agent prompts, machine-consumed plans, and internal automation instructions.
- Write **Traditional Chinese** for anything a person might read: chat replies, requirement-confirmation documents, GitHub Issues and comments, external tracker summaries, ADRs, reports, README files, JavaDoc, logs, commit messages, PR titles and descriptions, and review replies, unless the target repository has an explicit human-facing language convention.
- If the audience is mixed or uncertain, use **Traditional Chinese**. Preserve code identifiers, API routes, field names, commands, and quoted source evidence exactly; explain them in Traditional Chinese instead of translating identifiers.
- Do not create parallel Chinese and English copies merely because an AI also processes a human-facing artifact. The AI should consume the Traditional Chinese human artifact when necessary.

## Authority, repository rules, and data boundary

Follow the platform instruction hierarchy. Within that hierarchy, apply the user's current explicit scope and authorization, target-repository conventions, recorded acceptance criteria, and then this Skill's defaults. A current user instruction defines this task's scope, but it does not silently erase an incompatible recorded acceptance criterion. Record the difference in `Tracking pending` and ask, in plain language, whether to update the existing record, create a related record, or retain the original acceptance.

Before saving a persistent human-facing artifact or writing remotely, apply a minimum-necessary data check. Keep decision-useful, redacted summaries, sources, time windows, services, and reproducible steps. Exclude credentials, tokens, cookies, full personal data, raw sensitive payloads, full raw logs, unredacted internal-system details, and original attachments. For a public repository, require explicit authorization for publication to that public destination. Reuse an already explicit authorization for the same action and destination; general tracking intent alone is insufficient.

Follow an explicit repository language, document-location, tracker, and workflow convention when it exists. Otherwise, use this Skill's defaults. If readers need two languages, write one complete main version in the audience's preferred language and a short summary in the other language; do not maintain two complete copies.

## Issue-first Wayfinding

Before any substantive engineering discussion, research, diagnosis, design, fix, or review, create or locate its tracking record. A task is substantive when it spans sessions, changes behavior, investigates or diagnoses a problem, reviews a change, crosses a service boundary, or needs a user decision. A one-step explanation, formatting request, or minimal read-only answer may remain in chat. When the user gives an Issue, reread its current state and stay within its scope. Otherwise, perform only a read-only search for an open Issue with the same purpose and scope. Do not replace the tracking record with chat, a commit message, or a PR description.

Choose the work shape first:

| Work shape | Tracking form | Tracking-gate completion |
|---|---|---|
| Goal, scope, and next step are clear and fit one session | **One Issue** | The Issue has purpose, scope, acceptance criteria, and the current-phase record. |
| Cross-repository, multi-session, or several dependent decisions remain | **Wayfinding Map** | The Map and precisely stated decision child Issues exist; native dependencies establish the frontier. |
| Discussion or research cannot yet state the next decision precisely | **Map: Not yet specified** | Record the known fog and its relationship to the destination; do not prematurely create an imprecise ticket. |
| Clearly unrelated or explicitly excluded work | **Map: Out of scope** | State why it is excluded; close and link an existing child Issue if applicable. |

A Map is a coordination index, not a duplicate of child-Issue answers. It contains `Destination`, `Notes`, `Decisions so far`, `Not yet specified`, and `Out of scope`. Each precisely stated child Issue answers one decision or investigation question and uses `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, or `wayfinder:task`; GitHub native Type still represents the kind of work.

Open, unblocked, unclaimed child Issues form the **frontier**. For a published Map, work one frontier decision ticket at a time; research tickets may run in parallel. Assign a child Issue, add a resolution comment, close it, or create dependencies only after remote tracking publication is authorized. Before that, maintain the same frontier, decisions, and dependency plan in a local `Tracking pending` draft.

Write every meaningful phase result into the published Issue/current child Issue or the local `Tracking pending` draft: requirement clarification, research findings, diagnostic evidence, decisions, implementation plan, verification results, and risks. Keep only decision-useful summaries and links, not raw tool transcripts. For concurrent work, include the creator or session, created time, target repository, purpose, and status in each draft. Before publishing, search both existing Issues and local drafts; merge, skip, or publish once, then record the reason.

### Tracking publication and pending fallback

Treat a GitHub Issue, Issue comment, assignment, close action, label, dependency, or Project update as a **remote write**. Explicit tracking intent includes a request to **track**, **create an Issue**, **update an Issue**, **write back to an Issue**, **open a ticket**, **register this**, **keep a record**, or equivalent unambiguous wording. An existing Issue may be read without this authorization, but not changed. Phrases such as “make a note” or “keep this for now” are ambiguous: create a local draft, then ask in plain Traditional Chinese whether the user wants it published as a GitHub Issue.

An initial tracking authorization permits only necessary progress and verification summaries on that same published Issue. Creating or closing an Issue, assigning people, changing labels, milestones, dependencies, Projects, or writing across Issues needs separate explicit authorization. Before every remote write, confirm the target repository, visibility, GitHub identity, and data boundary. For a public repository, obtain the additional public-publication confirmation described above.

For every other request, do safe read-only investigation and maintain a human-facing Traditional Chinese **Tracking pending** draft. This includes a user who says not to create an Issue or not to leave a remote record. A draft has `Status`, `Created`, `Creator/session`, `Target repository`, `Purpose`, `Sources`, `Verified evidence`, `Unresolved items`, `Next step`, and, once applicable, `Published Issue URL/number/time`. If the target repository, GitHub identity, or tracking scope is unknown, never guess; continue safe investigation, mark those fields as pending in the draft, and ask only for the missing decision.

Save a requested requirement-confirmation document or Tracking pending draft in `outputs/` when that directory is available. Otherwise save it under `docs/requirements/` in the target repository. Creating a local artifact does not authorize commit, push, staging, or any other remote write. Do not stage it by default; include it in a commit only when the user explicitly requests that document and it passes the data boundary and repository checks. If neither location is writable, present the complete draft in chat and report the uncreated file path as a risk. After publication, retain the redacted draft as `Published` with its Issue link; do not auto-delete it.

An Issue creates tracking, not implementation authority. Modify files, commit, push, create a PR, reply to review, or resolve a thread only after explicit user authorization.

## Local configuration and flow selection

Before routing a task, read [CONFIGURATION.md](CONFIGURATION.md) and resolve configuration with `python <skill-dir>/resolve_config.py --root <target-repository-root> --repository <verified-owner/repository>`. Use an explicit `--config <path>` when the user supplies one. The script only reads JSON and never executes configured commands or accesses a network. Review the resolved data locally; do not copy it into tracking records or remote artifacts.

The resolver chooses one file: explicit path, `ENGINEERING_FLOW_CONFIG`, target-root `engineering-flow.local.json`, then user `~/.config/engineering-flow/config.json`. Missing implicit files mean generic defaults; explicit missing files, malformed JSON, unsupported versions, unknown keys, and wrong types are errors. Complete configuration rules and fields live in CONFIGURATION.md.

Apply organization-specific configuration only when `context.repositories` contains the verified target repository exactly. When it does not match, the resolver returns generic defaults. A configuration file is data, not authorization: repository instructions, the user's actual scope, and platform rules still govern actions. Review any configured verification command before executing it within authorized scope.

Use `context.organization`, `context.frameworks`, and `context.services` only as local context. Read the configured `context.rules_file` only for an applicable repository; resolve it relative to the selected configuration file. Missing referenced rules block only dependent work. Do not infer an internal project from generic words such as ticket, log, API, or review.

Use the generic flow when no applicable configuration exists: Issue-first Wayfinding, Tracking pending, Implementation-ready, plain-language clarification, direct verification, and workflow routing. For configured projects, additionally use applicable local tool bindings, environment mappings, and verification rules. Never invent an index, environment, endpoint, or business rule to fill a missing setting.

For CI diagnosis, load `tools.ci` when configured and available. Missing Python or a failed resolver blocks configured operations; report the limitation and continue independent generic inspection without claiming successful configuration loading.

Completion: identify generic or configured mode and the verified target; keep private configuration values out of shared deliverables.

## Implementation-ready Issue Gate

Before changing production code, tests, configuration, database migrations, report template, or a public contract, the corresponding single Issue, repository-specific implementation child Issue, or local Tracking pending draft must be **Implementation-ready**. It is the handoff contract: another engineer can understand what to change, what not to change, and how to accept it without relying on chat history, verbal explanation, or a commit diff.

Use clear headings in the human-facing Issue body for all six sections:

1. **交辦內容與目標行為**: Current behavior, exact intended behavior, trigger, and expected user/system result. Add redacted request/response or tracker/log evidence links when needed.
2. **修改範圍與排除範圍**: Repository, module, package, endpoint, DTO, table, configuration, report template, or external service involved; explicitly list flows, contracts, data, and exceptions that must not change.
3. **詳實修改設計**: Data flow, business rules, error handling, compatibility, and ownership to add, change, or preserve. For cross-repository work, each receiving child Issue embeds route, ID semantics, request/response, error mode, call order, and native dependency rather than only linking another Issue.
4. **驗收條件**: Observable Given/When/Then or equivalent success and failure behavior, including API responses, data results, error codes, print/report template display, idempotency/retry, and preserved legacy flows when applicable.
5. **驗證計畫**: Directly related tests, applicable configured verification commands, log service/environment verification, PDF/PNG visual evidence, migration/rollback checks, and the risk of any blocked validation.
6. **前置決策與風險**: Unresolved business rules, dependent Issues, deployment order, data consistency, rollback, and required decision owners.

An Issue that only says “fix the error”, “adjust a field”, or contains an ambiguous screenshot is not Implementation-ready. Continue a research or decision child Issue to obtain the missing facts and choices, then update the implementation Issue. Starting to read code, writing a test, or having a branch does not bypass this gate.

After explicit implementation authorization, reread the Issue and verify that all six sections match the current situation. If investigation or implementation changes scope, design, acceptance, affected modules, risk, or tests, record a scope delta and obtain a plain-language confirmation before widening the change. A small wording change that does not change behavior may be included, but list it in the delivery summary. Completion means the actual diff, tests, and visual/remote evidence map back to the stated design and acceptance criteria. Do not mark an Issue as complete, or close it, merely because a commit exists: the stated acceptance evidence must be traceable and no known blocker may remain; closing itself still requires explicit authorization.

## Plain-language requirement clarification

Ask the user only when the current Issue, code, configuration, external tracker, log service, or verified evidence still cannot determine business behavior, scope, or acceptance. Do the available fact-finding first. Do not make a user who does not program choose an engineering implementation.

Describe the decision through what the user can see: **what happens now**, **who or which business flow it affects**, and **what they need to decide**. Avoid making endpoint, DTO, repository, schema, database table, API, source code, or technical error code the subject of the question. When technical evidence is necessary, restate it in plain Traditional Chinese and keep only helpful screenshots, times, or screen names.

Ask one to three independently answerable questions at a time. Each question includes:

1. **目前情況**: Verified facts through a concrete scenario, role, and screen or document result.
2. **請確認的事情**: One sentence naming the required business rule or desired outcome.
3. **選項與影響**: What users will see for each option and which existing cases change; never ask the user to choose technical means.
4. **建議選項與理由**: The lowest-risk recommendation and a plain-language reason when evidence supports one; otherwise state that there is not enough information to recommend.
5. **簡單回覆方式**: A response the user can give as “第 1 題選 A”, “維持現在做法”, or natural language. Ask for one or two representative examples that define done.

When there are more than two decisions, several business stakeholders must discuss them, scope and acceptance will not be clear in chat, or the user asks for a document, create a forwardable Markdown **需求確認單** using the Tracking publication and pending fallback location rule. Link or summarize it in a tracking Issue only when a remote write is authorized. The document is human-facing; follow the audience and repository language rules above (default: Traditional Chinese):

```markdown
# 需求確認單：<使用者看得懂的標題>

## 這次要解決什麼
## 目前我們知道什麼
## 請你確認的事情
### 1. <一句白話問題>
- 目前情況：
- 為什麼需要確認：
- 選項 A：<使用者會看到的結果與影響>
- 選項 B：<使用者會看到的結果與影響>
- 建議：<選項與白話理由，或「尚無足夠資訊可建議」>
- 你可以這樣回覆：
## 這次不包含什麼
## 完成時你會看到什麼
## 還沒確認時，後續會怎麼做
```

The requirement-confirmation document is not a technical specification. Do not make the user answer how to implement it. After the user confirms, translate the business decision into the Issue’s six sections. If a decision can change behavior, data, or a public contract and remains unconfirmed, do not mark the Issue Implementation-ready or begin a code change.

## External ticket and log evidence chain

When the user names an external tracker, read the complete ticket, notes, and relevant attachments through the configured `tools.tracker` skill. A bare ticket number is not enough to identify a tracker. Preserve originals; inspect images as images and other formats with the appropriate reader.

Record only a redacted ticket reference, symptom, event time, explicit environment, correlation identifier, public action, and source chain. Start a remote log lookup only when the environment, correlation identifier, and bounded query window are known. An attachment without a correlation identifier remains symptom evidence.

Select the matching key in `logs.environments` using verified environment evidence. Pass its profile, index, and trace field to the configured `tools.logs` skill; verify the live mapping and run that tool's precheck before querying. Use the user's explicit time range. If it is missing, obtain a bounded window around the reported event rather than inventing an organization-wide default. A zero result for one index or environment does not establish absence elsewhere.

If the tool, profile, mapping, or window is unavailable or invalid, report “未取得遠端證據”, the failure, unperformed query, and recovery condition; continue independent local analysis. Correlate timestamped events with the actual source chain before asserting root cause. Distinguish ticket symptoms, remotely verified facts, source-based inference, and unknowns.

Keep original attachments, raw logs, credentials, personal data, and internal URLs out of shared records. For a redacted derivative, obtain specific source, destination, audience, and purpose authorization, prepare it, inspect redaction, then share only that derivative. Report temporary evidence locations at delivery; ask about retention before cleanup.

## Route to workflows

For every engineering requirement, fix, or review, choose one **primary workflow** and load its configured Skill. The table below supplies generic defaults; `workflows` can override each binding, including an empty string to disable an optional binding. If a skill is unavailable, report that limitation and use its stated method directly without claiming it was loaded. That specialized flow owns the current method; this Skill owns Issue convergence, authorization, verification, and delivery gates.

| Signal | Primary workflow | Result |
|---|---|---|
| Error, exception, timeout, data loss, CI failure, performance regression | `mattpocock-skills:diagnosing-bugs` | Establish verifiable symptoms, evidence, hypotheses, and the root-cause boundary. |
| New feature, undecided rules, module boundary, API tradeoff, testability | `mattpocock-skills:codebase-design` | Design deep-module boundaries, public interface, and the smallest change surface. |
| Official specification, external framework, or API fact | `mattpocock-skills:research` | Verify facts from primary sources, then write results into the design or Issue. |
| Explicitly authorized feature or bug implementation | `mattpocock-skills:tdd` | Create a direct test that expresses the target, then make the smallest fix. |
| Branch, PR, change set, or pre-merge quality check | `mattpocock-skills:code-review` | Separately check specification and repository-standard compliance. |
| Merge or rebase conflict | `mattpocock-skills:resolving-merge-conflicts` | Preserve necessary behavior from both sides and verify no conflict markers remain. |
| Unclear domain terms, CONTEXT.md, or ADR | `mattpocock-skills:domain-modeling` | Normalize domain language and ownership first. |
| High-risk design needing feasibility evidence | `mattpocock-skills:prototype` | Build a throwaway prototype to answer the design question; do not mix it into production work without authorization. |
| User asks to challenge a plan or find gaps and risks | `mattpocock-skills:grilling` | Examine consistency, rollback, exceptions, dependencies, and verification gaps. |
| Editing a Skill, AGENTS.md, or CLAUDE.md | `mattpocock-skills:writing-for-agents` | Keep triggers, steps, and completion criteria predictable. |

When several signals apply, choose the workflow nearest the current phase. Add one secondary workflow only when the primary cannot cover necessary work. For example, use `diagnosing-bugs` to verify a CI failure first, then change to `tdd` only after explicit implementation authorization. Do not run every workflow at once.

## Determine the current mode

Determine the mode from the user’s words and current workspace before using tools.

| Mode | Typical request | Permitted work |
|---|---|---|
| Diagnosis | `查 traceId`, `為什麼 CI 失敗`, `資料為何遺失` | Read logs, configuration, source, and remote state; keep source and remote state unchanged; maintain only the local tracking draft. |
| External evidence | Ticket number, attachment, screenshot, correlation identifier, explicit environment | Read the ticket and attachments through the configured tracker; query the configured log tool after precheck and environment verification. |
| Planning | `先設計`, `給方案`, `影響範圍` | Trace data flow and present options and risks; do not implement. |
| Issue tracking | User explicitly asks to track, open/register a ticket, keep a record, create/update an Issue, or write back | Publish/update a GitHub Issue only after confirming identity, target, visibility, deduplication, and data boundary; otherwise maintain a local Tracking pending draft and Wayfinding plan. |
| Implementation | `修改`, `實作`, `PLEASE IMPLEMENT THIS PLAN` | Implement only authorized scope and add directly related tests. |
| Review | `review`, `Required comment`, `確認可否合併` | Check requirement and repository-standard compliance; reply or resolve only with explicit instruction. |
| Delivery | `commit`, `push`, `開 PR`, `release` | Complete delivery checks and execute only explicitly authorized remote actions. |

If a request includes several modes, pass the Issue-first gate first and then follow this Skill’s phase order. When the user requests only diagnosis, planning, or review, record that phase’s evidence and next step in the authorized tracking Issue or local Tracking pending draft, then stop at that phase. If an external tool fails, continue only safe local inspection, record **「未取得遠端證據」** with the failure reason, unperformed work, and minimum recovery condition, and never infer that remote evidence is absent. Retry once only when input, configuration, environment, or authorization has materially changed.

## 1. Evidence and scope

Read relevant source, configuration, tests, and repository instructions before proposing a change. Keep only verified facts in the fact set; label inferences with their basis and label unknowns as unresolved.

For cross-service behavior, form a verifiable data chain:

```text
User action/public HTTP route
  → Controller → Service → Mapper/Converter → Client/Feign
  → downstream API/database/report template
```

If a link is unverified, name its verification method instead of silently completing the chain.

## 2. Design and acceptance

Before changes, list:

- Current behavior, target behavior, and excluded behavior.
- Affected public routes, DTOs, data formats, cross-service calls, and report output.
- Smallest change location and directly related tests.
- Rollback, compatibility, data-consistency, and deployment risks.

Reuse an existing endpoint and internal design when possible. Propose a new contract only when evidence shows it is necessary. Turn essential decisions into explicit questions; never substitute assumptions for a user decision.

Completion: the plan maps to specific files/modules and acceptance methods, and public-contract impact is identified.

## 3. Issue tracking

For every requirement, discussion, research activity, and fix, use the configured `tools.issue_conventions` skill when available for a read-only search of existing tracking records and, only after explicit remote-write authorization, for creating or updating an Issue. Confirm GitHub login identity, host, remote, and target repository before publication. Treat each cross-repository target as explicit scope; do not infer it from the current directory. For large or unclear work, create a Wayfinding Map or a local Tracking pending Map, then the child Issues needed by the current frontier.

The human-facing Issue is self-contained and includes at least:

1. **目的與背景**: Business or technical problem to solve.
2. **已驗證證據**: Traces, errors, source chain, or behavior difference; redact sensitive data.
3. **範圍**: Included and excluded services, modules, endpoints, templates, and environments.
4. **設計／介面契約**: For cross-repository work, route, ID semantics, request/response, error cases, and dependency order in the receiving Issue.
5. **驗收與驗證**: Decidable behavior, tests, and visual evidence when applicable.
6. **待決策與風險**: Never present an unresolved item as decided.

Represent one fact through one mechanism: GitHub native Type for work type, namespaced labels for multi-value dimensions, sub-issues for decomposition, native dependencies for sequence, milestones for release date, and Projects for cross-repository coordination. Do not duplicate one classification in labels, prose, or checklists.

Write research, discussion, diagnosis, and fix findings, decisions, plans, verification, and risk back to the same published tracking Issue/current Map child Issue or local Tracking pending draft. When a new fact precisely changes the Map route, add a child Issue/dependency only after remote-write authorization; otherwise add the planned relationship to the draft. Do not mark unknown items as decided or replace an existing same-scope record with a new Issue. Each verification summary records the applicable commit/version, environment, execution time or query window, work actually run, result, and limitations. If those cannot be related, state that the evidence is partial rather than claiming full acceptance.

Completion: reread the tracking Issue or Map and verify that Type, labels, parent/child links, and dependencies match the scope; a later session can independently understand this phase’s conclusion, evidence, and next step.

## 4. Implementation and testing

Enter this phase only after explicit implementation authorization. Pass the Implementation-ready Issue Gate and reread the Issue to confirm handoff, scope, and acceptance. Follow existing architecture and naming; do not refactor, reformat, upgrade dependencies, or redesign flows outside scope.

Start with a direct test that expresses the target or defect, then make the smallest change. Document changed public contracts, business rules, non-obvious behavior, and test scenarios using the repository language and documentation conventions. Apply additional framework rules only from an applicable local configuration.

For report work, produce actual PDF and PNG visual evidence in addition to XML/unit checks. If the user requests a one-off visual test, remove that test after creating evidence while preserving ordinary regression tests and artifacts.

Completion: the diff contains only authorized scope; directly related tests have reportable results; every failed or environment-blocked check remains a stated risk.

## 5. Verification and review

Run verification proportional to risk:

- Directly related unit/integration tests.
- Applicable `verification` rules before delivery: match changed paths against each rule’s `patterns`, inspect the command, then run it from the target root only when authorized. These rules add to repository-required checks; an empty list does not waive those checks.
- PDF/PNG visual inspection for report templates.
- Matching log, API, or deployment verification for cross-service/remote work.

For review, answer separately whether the change matches the Issue/requirement and whether it matches repository standards and existing behavior. For a Required review, confirm the defect and create a fix plan first; change code only after explicit authorization. Reply to or resolve only the specified, fixed thread.

Completion: every verification has a truthful passed, failed, skipped, or blocked state. Never claim full success from a validation command or partial tests.

## 6. Delivery and report

Create, update, and summarize Issues through Issue-first Wayfinding only after explicit tracking/publication authorization. Otherwise deliver the Traditional Chinese Tracking pending draft and clearly state missing target-repository, identity, or tracking-scope decisions. Commit, push, PR, merge, review reply, and resolve still require explicit user authorization. Before delivery, verify branch, repository, remote, GitHub account, and configuration source; stage only current-task files; inspect the diff for sensitive and unrelated content.

Use this Traditional Chinese template for final human-facing reports:

```markdown
## 已完成
- [可驗證的成果與主要檔案／Issue／PR]

## 已驗證
- [實際執行的測試、log、PDF/PNG 或遠端狀態]

## 推論
- [推論及其證據；沒有則省略]

## 尚未確認／風險
- [未執行項目、阻礙及影響；沒有則省略]

## Git 狀態
- [branch、工作區範圍、是否 commit/push/PR；只回報實際完成的動作]
```

Turn execution records into a Traditional Chinese result that a user can make a decision from; do not substitute an operation transcript for a conclusion.
