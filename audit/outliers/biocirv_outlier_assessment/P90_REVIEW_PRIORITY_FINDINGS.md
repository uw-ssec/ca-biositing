# P90 Review Priority Findings — Supplementary Analytical Lens

This document reports a **supplementary, additive** prioritization lens on top
of the completed BioCirV Exploratory Outlier & Variance Analysis. It reads
only existing Steps 0–10 output CSVs
(`outputs/replicate_group_summary.csv`, `outputs/method_parameter_summary.csv`,
`outputs/flagged_review_queue.csv`, and `outputs/human_review_priorities.csv`
for cross-reference only) and does **not** modify any of them, any Step 0–10
script, or the final synthesis report
(`BIOCIRV_REPLICATE_PRECISION_OUTLIER_ASSESSMENT.md`). It does **not**
recompute RSD, Dixon, 3×SD, or pooled-SD, and it does **not** introduce any
new production QC threshold.

**Terminology note:** the legacy literal CSV column `method` (present in
`replicate_group_summary.csv`) represents **sample preparation method**, not
analytical method. `flagged_review_queue.csv` already exposes the corrected
`sample_preparation_method` column name; this document uses
`sample_preparation_method` in prose and does not rename any literal column.

Output artifact produced by this analysis:
[`outputs/p90_review_priority.csv`](outputs/p90_review_priority.csv) (427
rows — see "Population chosen" below).

---

## 1. Methodology (1 paragraph)

For each of the 2712 replicate groups in `replicate_group_summary.csv` with a
defined `RSD_percent` (1955 of 2712), this analysis joins in that group's own
`analysis_type × parameter`'s `P90_RSD` and `n_RSD_defined` from
`method_parameter_summary.csv` (74 combinations), then computes: (1)
`is_at_or_above_parameter_P90` = `RSD_percent >= P90_RSD` (boolean); (2)
`RSD_to_P90_ratio` = `RSD_percent / P90_RSD`, with the ratio set to `NaN`
whenever `P90_RSD` is undefined or `<= 1e-9` (chosen as a "functionally zero"
epsilon — several `analysis_type × parameter` combinations have `P90_RSD`
computed from only 1–3 groups and can legitimately equal exactly `0.0`,
which would otherwise produce an infinite or meaningless ratio); and (3) a
purely descriptive `p90_evidence_label` of `"adequate"` (`n_RSD_defined >=
10`) or `"sparse"` (`n_RSD_defined < 10`) for that combination's `P90_RSD`
estimate. The threshold of 10 is a descriptive labeling convenience chosen
for this document only — it is explicitly **not** a new statistical rule or
production QC cutoff, and no groups or values are filtered, excluded, or
reclassified based on it.

**Population chosen for the output CSV:** all 427 rows of the existing
Step 9/10 `flagged_review_queue.csv`, joined 1:1 on `replicate_group_id` with
the P90-relative fields above. This population was chosen (rather than "all
1955 RSD-defined groups") because the task's primary deliverable is a
priority lens **within the existing human-review backlog** — every row in
`flagged_review_queue.csv` already has `RSD_percent` defined (see §2 below),
so no queue rows are lost, and the resulting CSV stays small and directly
actionable for reviewers already working from Step 9/10's queue. Step 3's
broader (outside-queue) context is reported as summary statistics below,
not as an additional CSV, per the task's "keep this focused and small"
instruction.

---

## 2. Queue-focused results (the 427-row `flagged_review_queue.csv`)

### 2a. RSD-definition coverage within the queue

| Metric | Value |
| --- | --- |
| Total rows in `flagged_review_queue.csv` | 427 |
| Rows with `RSD_percent` defined | **427 (100%)** |
| Rows with `RSD_percent` undefined (would be Dixon-only/3×SD-only rows lacking RSD) | 0 |

All 427 flagged rows happen to have a defined `RSD_percent`, even rows whose
`flag_category` is `Dixon_only` or `3xSD_only` — those flags were computed
alongside RSD, not in place of it, for every replicate group in this dataset
(`n_replicates` is always ≥ 2, sufficient to define RSD). This is a
consequence of the existing pipeline's grouping design, not an artifact of
this analysis.

### 2b. At-or-above the combination's own P90_RSD

| Metric | Value |
| --- | --- |
| Rows at-or-above their own `analysis_type × parameter`'s `P90_RSD` | **143** |
| As % of the 427 RSD-defined queue rows | **33.5%** |
| As % of all 427 queue rows | **33.5%** (same, since RSD is defined for all) |

### 2c. Breakdown by `analysis_type`

| `analysis_type` | Rows in queue | RSD-defined | At-or-above own P90_RSD | % of RSD-defined at-or-above |
| --- | --- | --- | --- | --- |
| xrf | 254 | 254 | 60 | 23.6% |
| icp | 62 | 62 | 36 | **58.1%** |
| compositional | 52 | 52 | 29 | **55.8%** |
| proximate | 59 | 59 | 18 | 30.5% |

**Reading:** `icp` and `compositional` flagged rows are disproportionately
likely to also sit at-or-above their own parameter's P90 — i.e., among
already-flagged rows, these two `analysis_type`s skew toward the most
extreme end of their parameter's own RSD distribution more often than `xrf`
does (even though `xrf` contributes the largest raw count of flagged rows,
254 of 427, most of those are flagged for reasons — largely `Dixon_only` —
that don't necessarily coincide with being in the parameter's own worst
decile).

### 2d. Top `analysis_type × parameter` combinations contributing P90-priority cases within the 427 queue

| analysis_type | parameter | n at-or-above P90 (within queue) |
| --- | --- | --- |
| compositional | xylan | 7 |
| compositional | glucose | 6 |
| compositional | xylose | 6 |
| compositional | glucan | 6 |
| proximate | volatile solids | 6 |
| proximate | ash | 6 |
| xrf | cu | 5 |
| xrf | ba | 5 |
| xrf | mn | 5 |
| xrf | ca | 5 |
| icp | ti | 4 |
| xrf | rb | 4 |
| xrf | sr | 4 |
| icp | al | 3 |
| icp | fe | 3 |

All `P90_RSD` values behind this table are labeled `"adequate"` evidence
(`n_RSD_defined >= 10`) except where noted in §4.

### 2e. Most extreme individual review candidates by `RSD_to_P90_ratio`

Top 15 `replicate_group_id`s in the 427-row queue, ranked by how far above
their own combination's P90_RSD they sit:

| replicate_group_id | analysis_type | parameter | RSD_percent | P90_RSD | RSD_to_P90_ratio | evidence | flag_category |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 433 | proximate | volatile solids | 297.59 | 7.92 | **37.6×** | adequate | RSD_only |
| 2584 | icp | ca | 134.97 | 5.62 | 24.0× | adequate | RSD_and_3xSD |
| 2583 | icp | mg | 139.74 | 6.53 | 21.4× | adequate | RSD_and_3xSD |
| 2059 | xrf | s | 131.66 | 9.21 | 14.3× | adequate | all_three |
| 2582 | icp | k | 133.80 | 10.20 | 13.1× | adequate | RSD_and_3xSD |
| 2073 | xrf | k | 64.61 | 4.98 | 13.0× | adequate | RSD_and_Dixon |
| 2043 | xrf | ca | 59.39 | 5.97 | 9.9× | adequate | RSD_and_Dixon |
| 703 | proximate | ash | 105.43 | 14.17 | 7.4× | adequate | RSD_and_Dixon |
| 996 | xrf | la | 161.26 | 22.84 | 7.1× | adequate | all_three |
| 2578 | icp | na | 682.75 | 103.08 | 6.6× | adequate | RSD_only |
| 2585 | icp | zn | 141.42 | 21.41 | 6.6× | adequate | RSD_only |
| 992 | xrf | ba | 160.90 | 24.46 | 6.6× | adequate | all_three |
| 2589 | icp | mn | 89.64 | 13.75 | 6.5× | adequate | RSD_and_3xSD |
| 2581 | icp | s | 120.73 | 22.09 | 5.5× | adequate | RSD_and_3xSD |
| 2580 | icp | fe | 139.77 | 26.42 | 5.3× | adequate | RSD_and_3xSD |

**Cross-reference with Step 10's `human_review_priorities.csv` (context only,
no modification):**

- **Priority 1 (`experiment_id = 47`)** overlaps with 5 of these top-15 IDs:
  992, 996, 2043, 2059, 2073.
- **Priority 2 (`experiment_id = 43`)** overlaps with 8 of these top-15 IDs:
  2578, 2580, 2581, 2582, 2583, 2584, 2585, 2589 — i.e., **all 8 `icp` rows
  in the top-15 by ratio fall inside Step 10's already-selected `experiment_id
  = 43` packet.**
- **Priority 3 (`proximate × ash`)** overlaps with 1: 703.
- **Priority 4 (`proximate × volatile solids`)** overlaps with 1: 433 (the
  single most extreme ratio in the entire queue).

This confirms the P90-relative lens is largely **consistent with and
reinforcing** of Step 10's existing priorities — 14 of the top 15
ratio-ranked groups already fall inside a Step 10-selected packet — while
also surfacing a finer-grained ranking *within* those packets (e.g.,
replicate_group_id 433 and the `icp x experiment_id=43` cluster are among
the single most extreme individual cases, information not visible at Step
10's packet-level granularity).

---

## 3. Step 3 — broader context (computed, not deferred)

This turned out to be a simple filter on the same merged table, so it was
computed rather than deferred:

| Metric | Value |
| --- | --- |
| RSD-defined replicate groups OUTSIDE the 427-row flagged queue | 1528 |
| Of those, at-or-above their own parameter's `P90_RSD` | **82 (5.4%)** |

**Reading:** by construction, roughly 10% of RSD-defined groups sit at or
above a P90 threshold in the overall population; the fact that only 5.4% of
*unflagged* groups clear their own parameter's P90 (vs. 33.5% of *flagged*
groups) indicates the existing Step 9 flagging logic (RSD>20 / Dixon /
3×SD) and the P90-relative view are correlated but not redundant — the 82
unflagged-but-P90+ groups represent a small pool of additional context that
was not surfaced by the original candidate rules, but this document does not
recommend adding them to any review queue; that decision is explicitly out
of scope here.

---

## 4. Evidence-sufficiency caveat

Not all `P90_RSD` values rest on equally strong evidence. Of the 74
`analysis_type × parameter` combinations in `method_parameter_summary.csv`:

| Evidence label | n combinations | Threshold |
| --- | --- | --- |
| `adequate` | 45 | `n_RSD_defined >= 10` |
| `sparse` | **29** | `n_RSD_defined < 10` |

The `n_RSD_defined >= 10` threshold is a **descriptive labeling convenience
only** — it is not a new production QC cutoff, and no data is excluded or
reclassified because of it. Sparse-evidence combinations include several
`xrf` trace elements with `n_RSD_defined` of 0–3 (e.g., `xrf/ag`, `xrf/bi`,
`xrf/cd`, `xrf/cr` have `n_RSD_defined = 0`, meaning `P90_RSD` is undefined
and no ratio/flag can be computed for those combinations at all), plus a
handful of `ultimate` parameters (`carbon`, `dm`, `oxygen`, `sulfur`, each
`n_RSD_defined = 1`) whose `P90_RSD = 0.0` and are therefore also excluded
from ratio computation by the epsilon rule in §1. Every row in
`outputs/p90_review_priority.csv` carries a `p90_evidence_label` column so
reviewers can immediately see when a `P90_RSD` comparison rests on a
thin (sparse) base rather than treating all P90 comparisons as equally
reliable. None of the 427 queue rows' own `analysis_type × parameter`
combinations fell into a `P90_RSD`-undefined (0 `n_RSD_defined`) bucket, so
all 427 queue rows do have a computable `is_at_or_above_parameter_P90` /
`RSD_to_P90_ratio` value; several of the queue's contributing combinations
(e.g., `compositional/arabinan`, `compositional/arabinose`, `xrf/nd`,
`xrf/y`, `xrf/zr`, `xrd/crystallinity`) are nonetheless labeled `sparse`
(n_RSD_defined 2–9) and should be read with that caveat in mind.

---

## 5. Explicit framing statement

**P90 review priority ≠ new QC flag ≠ bad data.**

This P90-relative view is an **additional prioritization lens** layered on
top of the existing Step 9 statistical-flag backlog (427 rows) and Step 10's
human-review priority queue (7 targets, 90.6% coverage). It does not
replace, filter, or reweight either of those outputs. A replicate group
sitting above its own parameter's P90_RSD is simply relatively more variable
than 90% of other technical-replicate groups measuring the same
`analysis_type × parameter` — this is descriptive context to help a reviewer
decide where to look first within an already-large backlog, not a
determination that the underlying measurements are invalid, wrong, or
should be excluded from any downstream analysis.

---

## 6. Files touched

**Created (this analysis only):**
- [`outputs/p90_review_priority.csv`](outputs/p90_review_priority.csv) — 427 rows.
- This document, `P90_REVIEW_PRIORITY_FINDINGS.md`.

**Not modified (verified):** `outputs/flagged_review_queue.csv`,
`outputs/human_review_priorities.csv`, `outputs/replicate_group_summary.csv`,
`outputs/method_parameter_summary.csv`, `STEP10_FINDINGS.md`,
`BIOCIRV_REPLICATE_PRECISION_OUTLIER_ASSESSMENT.md`, and all Step 0–10
scripts — all read-only inputs to this analysis. The temporary compute
script used to generate `p90_review_priority.csv`'s numbers was deleted
after use and is not part of the repository.
