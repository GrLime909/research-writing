# Section Writing Router

Routing index for the per-section writing guidance fragment system. Used by `draft_writer_agent`, `socratic_mentor_agent`, `abstract_bilingual_agent`, and `structure_architect_agent` to load the appropriate writing guidance on demand.

## Loading Protocol

Execute these three steps in order when starting a writing task:

1. **Load paper-type argument chain** — read the file from `references/paper-type-chains/` that matches the `paper_type` field in the Paper Configuration Record.
2. **Load section fragment** — read the file from `references/section-fragments/` that matches the current section being written.
3. **Deep reference** (if needed) — follow the "Cross-Reference" or "Deeper reference" pointers within the loaded fragment to access more detailed guidance.

---

## Paper Type Axis

Load one file based on the Paper Configuration Record's `paper_type` field:

| paper_type value | Argument chain file |
|-----------------|-------------------|
| `imrad` | `references/paper-type-chains/imrad.md` |
| `literature-review` | `references/paper-type-chains/literature-review.md` |
| `theoretical` | `references/paper-type-chains/theoretical.md` |
| `case-study` | `references/paper-type-chains/case-study.md` |
| `policy-brief` | `references/paper-type-chains/policy-brief.md` |
| `conference` | `references/paper-type-chains/conference.md` |

The argument chain file provides: the overall paper argument structure, recommended drafting order, and section-by-section guidance at the paper level.

---

## Section Axis

Load one file based on the current section being written:

| Current section | Fragment file |
|----------------|---------------|
| Introduction | `references/section-fragments/introduction.md` |
| Literature Review / Related Work | `references/section-fragments/literature-review.md` |
| Methodology / Methods | `references/section-fragments/methodology.md` |
| Results / Findings / Experiments | `references/section-fragments/results.md` |
| Discussion | `references/section-fragments/discussion.md` |
| Conclusion | `references/section-fragments/conclusion.md` |
| Abstract | `references/section-fragments/abstract.md` |
| Title | `references/section-fragments/title.md` |

The section fragment provides: paragraph movement (结构推进逻辑), drafting rules (起草规则), common failure modes (常见失败模式), and diagnostics (诊断检查).

---

## Cross-Reference Map

This table shows which existing reference files complement (not replace) the section fragments:

| Section fragment | Complementary existing references |
|-----------------|----------------------------------|
| `introduction.md` | `references/academic_writing_style.md` (register), `references/paper_structure_patterns.md` (structure) |
| `literature-review.md` | `references/academic_writing_style.md` (register), `references/paper_structure_patterns.md` (thematic review structure) |
| `methodology.md` | `references/academic_writing_style.md` (register), `references/statistical_visualization_standards.md` (figures) |
| `results.md` | `references/statistical_visualization_standards.md` (chart decision trees), `references/academic_writing_style.md` (register) |
| `discussion.md` | `references/academic_writing_style.md` (hedging language), `references/writing_judgment_framework.md` (reader's journey) |
| `conclusion.md` | `references/academic_writing_style.md` (register) |
| `abstract.md` | `references/abstract_writing_guide.md` (bilingual format, keywords, 5-component model) |
| `title.md` | `references/academic_writing_style.md` (register) |

---

## Usage by Agent

### draft_writer_agent (Phase 4 / Phase 6 revision)

1. In Pre-Writing Setup (Step 1): load the paper-type argument chain.
2. In Section-by-Section Writing (Step 2): load the section fragment before each section.
3. In Self-review (Step 2.6): run the section fragment's diagnostics checklist.

### socratic_mentor_agent (Plan mode)

1. When guiding a chapter: load the section fragment to inform "writing direction hints".
2. When designing questions: reference the fragment's "pre-writing checklist" and "common failure modes".

### abstract_bilingual_agent (Phase 5b)

1. Load `references/section-fragments/abstract.md` for structural diagnostics before drafting.
2. Continue using `references/abstract_writing_guide.md` as the authoritative bilingual format reference.

### structure_architect_agent (Phase 2)

1. Load the paper-type argument chain to inform section ordering and evidence mapping.
