# Section: Methodology / Methods

## Default Structure

`task formulation -> overview (pipeline / system / approach) -> per-module detail -> implementation notes -> assumptions and boundary`

## Pre-Writing Checklist

Before drafting Method, confirm:

- [ ] Task formulation: inputs, outputs, scope.
- [ ] Overview figure / pipeline diagram: does one exist? It anchors the section.
- [ ] Notation: defined once and consistent.
- [ ] Reproducibility scope: code, weights, data — what will be released.

## The Three-Element Pattern (per module)

Each module in a pipeline should answer three questions:

### 1. Module Design
- Describe representation/network/data-structure details.
- Describe the forward process clearly: given input -> step 1 -> step 2 -> step 3 -> output.

### 2. Motivation of This Module
- Explain why this module is needed.
- Use problem-driven logic: because problem X exists, we design module Y.
- Typical openings: `A remaining challenge is...`, `However, we...`, `Previous methods have difficulty in...`

### 3. Technical Advantages
- Explain why this module has technical advantage over alternatives.
- Tie advantage to measurable behavior when possible.

If any element is missing, the module reads as a black box. Flag the gap.

## Method Writing Workflow

1. Draw the pipeline figure sketch.
2. Use the sketch to organize subsection structure.
3. For each subsection, plan three parts: motivation, module design, technical advantages.
4. **Write module design first** to build a concrete backbone.
5. Add motivation and technical advantages afterward.

## Overview Subsection

1. One to two sentences for task setting.
2. One to two sentences for core contribution.
3. If pipeline/framework is novel, point to overview figure.
4. Tell readers what each subsequent subsection covers.

## Clarity Checks (three levels)

### Logic-level
After finishing, summarize the Method writing logic. Check whether the summary is smooth and easy to follow.

### Paragraph-level
- The first sentence of each paragraph should make readers immediately understand what this paragraph is about.
- One paragraph delivers one message.

### Sentence-level
- Check whether the **motivation** of each sentence is explicit: why is this content needed?
- Check sentence-to-sentence flow.
- Check term consistency — avoid changing key terms back and forth.

## Forbidden Vague Phrases

Never leave:

- `under standard conditions`
- `using routine methods`
- `data were analyzed statistically`
- `the method was validated`
- `samples were randomly assigned` (without saying how)

Replace with the actual reproducible information.

## Implementation Details

Include hyperparameters (layer count, feature dimensions), coordinate transforms/normalization, and other practical details. Place them near the end of Method or in a dedicated Implementation Details section.

## Common Failure Modes

- Mixing design rationale with evaluation results in the same paragraph.
- Every performance claim without specifying dataset, metric, baseline, and conditions.
- Marketing verbs (`leverages`, `enables`, `empowers`) without concrete information.
- Omitting failure modes the experiments revealed — reviewers trust papers that report their own limits.
- Hiding concrete method design behind abstract insights to look novel.

## Diagnostics Before Finalizing

- Can a peer re-implement from what is written?
- Is every module's motivation problem-driven?
- Are all symbols defined on first use and consistent throughout?
- Does the section flow match the pipeline figure?

## Cross-Reference

For discipline-specific register adjustments, see `references/academic_writing_style.md` (Register Adjustment by Discipline table).
