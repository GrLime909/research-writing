# Section: Results / Experiments / Findings

## Default Evidence Ladder

`system / workflow validation -> main result -> baseline comparison -> ablation / mechanism analysis -> application or generalization -> stress tests / failure modes`

Each subsection has a claim-first opening, then data support.

## Three Core Questions to Answer

1. **Is the method better than strong baselines?** — comparison experiments against strong and recent baselines; standard metrics on main benchmarks; fair protocol (same data split, preprocessing, evaluation settings).
2. **Which modules/design choices make the gain?** — ablation studies for each key module/design choice; remove/replace/disable variants; report delta to full model.
3. **How far can the method generalize under harder settings?** — evaluations on harder or out-of-distribution settings; stress-test scenarios; report both gains and failure modes.

## Drafting Rules

- Stay mainly in past tense.
- Report what was observed, under what conditions, with what quantitative support.
- Use statistics correctly and sparingly. Every test needs a stated hypothesis.
- Use supplementary data sparingly. If a result belongs in the main text, do not hide it in supplements.
- **Each major claim needs comparison, ablation, or stress-test evidence.** If a claim has none, mark it for follow-up rather than drafting around it.

## Results Syntax vs Discussion Syntax

Results sentences report observations:

- `was detected` / `increased` / `showed` / `enabled` / `achieved`

Do not drift into Discussion syntax (`may reflect`, `suggests`, `is likely due to`) unless the transition is intentional.

## Subsection Opening Rule

`To test [question], we [action].`

Then report the result and evidence. Keep interpretation short unless the paragraph explicitly transitions toward Discussion.

## Experiment Section Decomposition

```
Experimental Setup -> Validation Experiment 1 -> Validation Experiment 2 -> Ablation Studies
```

## Figure/Table Writing Rules

### Hard rules

1. Put caption above the table.
2. Avoid vertical lines in tabular columns.
3. Use `booktabs` style (`\toprule`, `\midrule`, `\bottomrule`) for clean structure.
4. Highlight key numbers (best/second-best) with subtle color emphasis.

### Readability rules

1. Label metric direction in column headers (e.g., `PSNR up`, `LPIPS down`).
2. Add units so values are interpretable without guessing.
3. Keep numeric precision consistent (same decimal places within a metric column).
4. Group multi-dataset results using `\multicolumn` + `\cmidrule`, not vertical separators.
5. One table, one message: do not mix unrelated results in a single table.
6. Keep caption focused on setting/protocol/notation, not long discussion.

## Experimental Rigor Checklist

- [ ] Are baselines recent and relevant?
- [ ] Are metrics sufficient and standard for this task?
- [ ] Is ablation tied to every key design claim?
- [ ] Are claims in Abstract/Introduction supported by reported numbers?
- [ ] Are limitations of evaluation scope explicitly stated?

## Common Failure Modes

- Mixing observation and interpretation in the same paragraph.
- Citing supplementary data when the result should be in the main text.
- Vague comparisons (`higher than control`) without effect size, sample size, or test.
- Per-paragraph claims without per-paragraph evidence.
- Bare "we obtain higher accuracy" without baseline + setup + statistical handling.

## Cross-Reference

For discipline-specific register adjustments, see `references/academic_writing_style.md` (Register Adjustment by Discipline table).
