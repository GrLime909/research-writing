# Section: Conclusion

## Default Structure

`contribution -> decisive evidence -> implication -> boundary`

## Drafting Rules

- **No new data.** No unsupported promises.
- Restate the central contribution in one sentence. Do not summarize each Results figure.
- The implication must be narrower than or equal to the scope of the evidence.
- A bounded future-work pointer is acceptable, but generic "more work is needed" is not.

## Four-Part Close

1. This work demonstrates or establishes the main contribution.
2. The decisive evidence is named.
3. The broader implication is stated.
4. The boundary condition is clear.

## Limitation Guidance

Prefer limitations tied to task goal/setting boundaries:

- Data regime limitation (e.g., only short sequences, specific geographic scope).
- Assumption limitation (e.g., controlled viewpoints only, steady-state conditions).
- Deployment scope limitation (e.g., specific sensor setup, single institution).

Avoid framing conclusion around fixable implementation flaws unless they critically define your method's scope.

### Distinguish Limitation Types

- **Technical defect**: underperforms strong baselines on key metrics or causes unacceptable tradeoff.
- **Scope limitation**: bounded by current task setting and still competitive vs. current SOTA.

## Template

1. This paper addresses [problem] by proposing [method/approach].
2. The key idea is [core insight], which enables [main benefit].
3. Experiments/analysis show [main gains/findings] across [datasets/settings].
4. A current limitation is [scope boundary], and extending to [future setting] is an important next step.

## Overclaim Check

Before finalizing, verify:

- [ ] Does each claim trace back to evidence in this paper?
- [ ] Are mechanism words (`demonstrates`, `proves`, `establishes`) backed by the right study design?
- [ ] Is the scope of the implication narrower than or equal to the scope of the evidence?
- [ ] Is any "first" claim genuinely first within a stated scope?

## Common Failure Modes

- Summarizing each section/figure instead of synthesizing the contribution.
- Introducing new data, new citations, or new mechanisms.
- Ending with vague importance claims unsupported by the evidence.
- Confusing technical defects with scope limitations.

## Cross-Reference

For discipline-specific register adjustments, see `references/academic_writing_style.md` (Register Adjustment by Discipline table).
