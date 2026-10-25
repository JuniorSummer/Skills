---
name: delivery-readiness-review
description: Use when judging delivery progress from an issue log.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [delivery, project, analysis, issue-log]
---

# Delivery readiness from an issue log

## When to use

"客户用得怎么样 / 还有多久能交付 / 这个项目的风险在哪" and there is an issue-tracking sheet (修改点 / 问题 / 工单 / 缺陷列表).

## Procedure

### 1. Read the whole log, every tab

Tabs often split by round or by reviewer. Capture the schema first — typically 问题描述 | 修改方案 | 解决状态 | 分工(算法/后端/前端) | 备注. A **blank status is not "fine"** — it means "not yet triaged".

### 1b. Judge whether the customer is actually using it

Issue count says nothing about adoption. Infer depth from the *nature* of the reports:

- **Business-detail issues = real use** — customer-name abbreviations, ERP master-data mismatches, per-customer document habits, order-naming conventions, missing fields like the submitter. Only people placing real orders report these.
- **Only recognition/format errors, no workflow complaints = staged trial.**
- **Negotiated rules** ("the customer will standardize their naming", "cursive gets a phone call") mean a manual fallback is already in place — count the manual-override rate as the real accuracy metric.

Report adoption and delivery separately. "In real use but not converged" and "not adopted yet" are different messages with different actions.

### 2. Turn section markers into a timeline

A row whose first cell is a bare 5-6 digit number is usually an **Excel serial date used as a batch header** (an order number would be longer or prefixed). Convert with `date(1899,12,30) + timedelta(days=N)`.

This is what lets you say whether issues are still arriving or have converged — the single most useful fact in the analysis.

### 3. Quantify per batch

Count per batch and overall: 已修改 / 无需修改 / 待修改 / 空. Report the closure rate (`已修改 + 无需修改`) **and** the per-batch breakdown; a healthy overall rate can hide a newest batch that is entirely untriaged.

### 4. Cluster themes and measure recurrence

Group issues into themes by keyword, then count **how many batches each theme spans**. Recurrence — not raw volume — is the delivery risk.

Flag a theme as false closure when earlier rows say 已修改 but later batches still carry open items in the same theme. State it with the batch dates.

### 5. Classify what is left

Split open items into: functional (frontend/backend), recognition/algorithm, and customer-config/data (per-customer naming, ERP mismatch, document habits).

If the latest batches contain **no functional bugs**, the system is functionally stable and the remaining risk is generalization rather than build-out. That changes both the estimate and the mitigation.

### 6. Estimate as scenarios, never a single number

- **Functional delivery** — feature bugs cleared, accuracy at an agreed baseline. Usually the shortest path; gated on triaging the untriaged batch.
- **Full acceptance** — accuracy target met on the hard class (often handwriting/OCR). Needs data collection plus model iteration cycles, not code patches.

For each: state the precondition, the evidence supporting it, and the blocker that could push it. A range with named conditions is honest; a single date is a guess.

### 7. Recommend actions that move the end date

- Triage every unlabeled item (做 / 不做 / 客户确认) — an untriaged batch makes any schedule a guess.
- Convert 无需修改 into **customer-written confirmation**, so the item can't resurface as a defect at acceptance.
- Split delivery into phases (functional now, accuracy later) instead of one all-or-nothing date.
- Convert recurring themes from per-issue patches into **rule assets**: alias/dictionary tables, normalization tables, rule tables with unit tests. Reserve model iteration for genuinely fuzzy input.
- Define acceptance metrics (per-class accuracy, allowed manual-override rate) and measure a baseline on the last N real orders.
- Use "same-type recurrence = 0" as the internal gate — it predicts deliverability better than a count of fixed issues.

## Pitfalls

- **Declared progress is a claim, not a measurement.** The same workstream can read 80% in one cell and 30% in another; cross-check stated percentages against the log and call out the口径 conflict instead of averaging it.
- **已修改 ≠ 解决.** Cross-batch recurrence is the proof. Always check whether the newest batch re-reports an older theme before declaring closure.
- **Don't average away the newest batch.** Report it separately; it is the current velocity signal.
- **Per-customer issues are configuration debt, not algorithm debt.** When each new customer produces a fresh burst, the fix is an onboarding configuration flow (name library / material mapping / template), not more patches.
- **Big sheets truncate mid-character.** Read in chunks; streaming >60KB through a pipe can split a multi-byte character and break JSON parsing — write CLI output to a file and parse the file.
