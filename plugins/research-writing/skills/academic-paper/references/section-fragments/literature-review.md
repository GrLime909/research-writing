# Section: Literature Review / Related Work

## Default Structure

`topic scope -> representative methods grouped by mechanism -> limitation tied to this paper -> distinction`

## Grouping Principle

**Group by technical topic and mechanism, not by publication year or author.** A paragraph titled "Graph-based approaches" with three contrasting methods is stronger than three single-paper paragraphs.

## Topic Design

Use 2-4 focused topics:

1. Task-specific mainstream methods.
2. Methods closest to your core idea.
3. Auxiliary techniques your method builds on.

## Paragraph Template

Each Related Work / Literature Review paragraph should contain:

1. **Topic sentence**: define scope of this topic.
2. **Representative methods**: one compact summary of the paradigm.
3. **Limitation tied to your target challenge**: the exact gap your paper addresses.
4. **Transition sentence**: leads to your method or the next topic.

## Independent Section vs Folded into Introduction

| Scenario | Choice |
|----------|--------|
| CS/ML conference style | Separate Related Work section |
| Nature-family style | Fold into Introduction |
| Social sciences / education | Often separate Literature Review chapter |
| User's target venue decides | Ask if unclear |

## Drafting Rules

- Each subsection ends with a limitation that **this paper addresses**. If a subsection's limitation does not connect back to your contribution, the subsection probably does not belong.
- Avoid both extremes: do not bash prior work, do not flatter it. State what prior work showed and where its scope ended.
- Cite the source you actually read. Do not chain-cite review papers as if they were primary sources.
- Compare mechanisms, assumptions, and failure modes. Do not just list results.
- Emphasize the exact gap your method fills. Do not make Related Work a citation dump.
- Do not hide strongest baselines.

## For Thematic Literature Reviews (standalone)

When the paper is a literature review (not just a Related Work section), use a different approach:

- **Not a survey list.** Replace `Author A reported X. Author B reported Y.` with synthesis grouped by mechanism, method, or conclusion.
- Define scope precisely: which sub-area, which time window, which inclusion criteria. Vague scopes invite reviewer pushback.
- Position your own stance carefully. A review can take a view, but must show reasoning, not assert it.
- Use connectives that signal logical relation: `in contrast`, `building on this`, `the remaining disagreement is`. Avoid generic `furthermore`, `additionally`.
- The closing section should leave the reader with a usable map of the field, not a summary of what was just read.

## Common Failure Modes

- Listing papers chronologically without a thematic or mechanistic organizing principle.
- Failing to connect each subsection's limitation back to this paper's contribution.
- Using Related Work as a dumping ground for tangentially relevant citations.
- Bashing prior work instead of fairly positioning it.
- Omitting the strongest competing baselines.

## Diagnostics Before Finalizing

- Are all strongest/recent competitors covered?
- Is each topic connected to your problem setting?
- Is your difference explained in technical terms, not marketing terms?
- Is citation coverage complete for all core claims?

## Cross-Reference

For discipline-specific register adjustments, see `references/academic_writing_style.md` (Register Adjustment by Discipline table).
