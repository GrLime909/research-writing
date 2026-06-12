---
name: academic-paper
description: "Academic writing pipeline combining 12-agent workflow's 12-agent full workflow (literature search, structure design, argumentation, citation compliance, bilingual abstract, peer review, formatting) with nature-writing's precision drafting toolkit (8-step workflow, one-sentence argument, verb-evidence calibration, paragraph job classification, terminology ledger, reader 5-question sequence, self-review audit). 10 modes, 5 paper types with type-specific argument chains, 4-axis fragment loading, journal-specific constraints."
version: "1.0.0"
author: "Adapted from academic-paper v3.2.0 + nature-writing v1.0.0"
status: active
data_access_level: redacted
task_type: open-ended
---

# Fused Academic Writer

This skill merges `academic-paper` (ARS v3.2.0) and `nature-writing` (v1.0.0) into a single precision drafting system. It retains academic-paper's full 12-agent pipeline while replacing its Phase 4 drafting core with nature-writing's 8-step workflow, paragraph discipline, and evidence-first stance.

## Architecture Overview

```
Phase 0: CONFIG        -> intake_agent (+ axis detection + terminology ledger)
Phase 1: RESEARCH      -> literature_strategist_agent
Phase 2: ARCHITECTURE  -> structure_architect_agent (+ paragraph job mapping)
Phase 3: ARGUMENTATION -> argument_builder_agent
Phase 4: DRAFTING      -> draft_writer_agent_fused (8-step workflow, verb calibration, paragraph discipline)
Phase 5a: CITATIONS    -> citation_compliance_agent
Phase 5b: ABSTRACT     -> abstract_bilingual_agent
Phase 6: PEER REVIEW   -> peer_reviewer_agent (+ self-review audit)
Phase 7: FORMAT        -> formatter_agent
```

## Quick Start

**Minimal command:**
```
Write a paper on the impact of AI on higher education quality assurance
```

**Nature-style precision drafting:**
```
Draft the introduction for my paper on [topic]. Here are my results: [evidence].
```

## Trigger Conditions

**English**: write paper, academic paper, paper outline, write abstract, revise paper, literature review paper, check citations, convert to LaTeX, draft section, write introduction, write method, write discussion, Nature-style, manuscript

**Chinese**: 写论文, 学术论文, 论文大綱, 寫摘要, 修改论文, 文獻回顧, 起草论文, 寫引言, 寫方法, 學術寫作, 科研寫作

## Routing Protocol — Fused

This skill uses a dual routing system:

### A. Full-paper workflow routing (from academic-paper)

| User intent | Route to |
|---|---|
| Complete paper from scratch | `full` mode — all phases |
| Need guided planning | `plan` mode |
| Just need an outline | `outline-only` mode |
| Have reviewer comments | `revision` or `revision-coach` mode |
| Check citations only | `citation-check` mode |
| Convert format | `format-convert` mode |
| Generate AI disclosure | `disclosure` mode |
| Need bilingual abstract | `abstract-only` mode |

### B. Precision drafting routing (fused — from nature-writing)

When the user already has evidence/results and wants to draft a specific section, route through the 4-axis fragment system. Load `manifest.yaml` and detect:

1. **paper_type**: research / methods / hypothesis / algorithmic / review (default: research)
2. **section**: abstract / intro / related-work / method / experiments / discussion / conclusion / title
3. **language**: en / zh-to-en
4. **journal**: nature / nat-comms / generic (default: generic)

Load only matching fragments. State detected axis values before drafting.

## Agent Team (13 Agents — 12 from academic-paper + 1 fused)

| # | Agent | Role | Source |
|---|---|---|---|
| 1 | `intake_agent_fused` | Configuration + axis detection + terminology ledger + handoff detection | **FUSED** |
| 2 | `literature_strategist_agent` | Search strategy, source screening, annotated bibliography | academic-paper |
| 3 | `structure_architect_agent_fused` | Structure selection, outline, paragraph job mapping per nature-writing 8-type taxonomy | **FUSED** |
| 4 | `argument_builder_agent` | Claim-evidence chains, logical flow, counter-argument handling | academic-paper |
| 5 | `draft_writer_agent_fused` | 8-step precision drafting workflow, verb-evidence calibration, paragraph discipline, unsupported-claim sweep | **FUSED** |
| 6 | `citation_compliance_agent` | Citation verification, DOI checking | academic-paper |
| 7 | `abstract_bilingual_agent` | Bilingual abstract (zh-TW + EN) | academic-paper |
| 8 | `peer_reviewer_agent` | Five-dimension scoring + nature-writing self-review audit | academic-paper |
| 9 | `formatter_agent` | LaTeX/DOCX/PDF output, citation format conversion | academic-paper |
| 10 | `socratic_mentor_agent` | Plan mode chapter-by-chapter guidance | academic-paper |
| 11 | `visualization_agent` | Publication-quality figures (matplotlib/ggplot2) | academic-paper |
| 12 | `revision_coach_agent` | Parse reviewer comments into Revision Roadmap | academic-paper |

## Phase 4 — Fused Precision Drafting Core

This is the primary fusion point. `draft_writer_agent_fused` replaces academic-paper's Phase 4 drafting with nature-writing's 8-step workflow:

1. **Build one-sentence argument**: `In [system], we show [advance] using [approach], supported by [evidence], with [boundary].`
2. **Build Terminology Ledger**: Extract and lock canonical terms, abbreviations, notation across all sections.
3. **Choose section architecture**: From `static/fragments/section/*.md` and `references/article-architecture.md`.
4. **Map each paragraph to one job**: context / gap / approach / result / comparison / mechanism / implication / limitation.
5. **Draft from evidence outward**: Claims near their supporting data.
6. **Calibrate verbs to evidence strength**: show > suggest > indicate > may > could.
7. **Sweep unsupported novelty**: Remove first/unique/unprecedented/comprehensive unless evidence supports.
8. **Paragraph flow check**: One paragraph, one message. First sentence = topic/claim. Explicit sentence-to-sentence relation.

### Output Format (fused)

1. `Draft:` — prose
2. `Section outline:` — 3-7 bullets
3. `Claim-evidence map:` — `Claim: ... | Evidence: ... | Status: supported / needs evidence / inferred`
4. `Assumptions or missing inputs:` — material gaps
5. `Why this structure:` — 2-4 bullets on structural choices

## Quality Standards (fused)

### From academic-paper
- Every claim must have a citation or be supported by own data
- Zero citation orphans
- Five-dimension peer review scoring
- Mandatory inclusions: Data Availability, Ethics Declaration, CRediT, COI, Funding, AI Disclosure

### From nature-writing
- Reader 5-question sequence (see `_shared/core/reader-workflow.md`)
- Verb-evidence calibration table
- Paragraph job classification (8 types)
- Terminology Ledger for cross-section consistency
- Unsupported novelty sweep
- Self-review audit before finalization (see `references/paper-review.md`)

## Checkpoint Rules (inherited from academic-paper)

1. User must confirm Paper Configuration Record before Phase 1
2. User must approve outline before Phase 3
3. Max 2 revision loops
4. Critical-severity issues block Phase 7

## Why Fusion

See [FUSION.md](FUSION.md) for the detailed rationale behind each fusion point.

## File References

### Fused agents
| Agent | File |
|---|---|
| intake_agent_fused | `agents/intake_agent_fused.md` |
| structure_architect_agent_fused | `agents/structure_architect_agent_fused.md` |
| draft_writer_agent_fused | `agents/draft_writer_agent_fused.md` |

### Original academic-paper agents (unchanged)
All other agents at `agents/*.md` — unchanged from academic-paper v3.2.0.

### nature-writing static layer
| Path | Content |
|---|---|
| `static/core/stance.md` | Default writing stance, intake requirements |
| `static/core/workflow.md` | 8-step writing workflow |
| `static/core/output-format.md` | Output format specification |
| `static/fragments/paper_type/*.md` | 5 paper-type playbooks with argument chains |
| `static/fragments/section/*.md` | 8 section-specific drafting rules |
| `static/fragments/language/*.md` | Language-specific rules (en, zh-to-en) |
| `static/fragments/journal/*.md` | Journal-specific constraints (nature, nat-comms, generic) |
| `manifest.yaml` | Axis definitions and fragment routing |

### Shared core
| Path | Content |
|---|---|
| `_shared/core/reader-workflow.md` | Reader 5-question sequence |
| `_shared/core/paper-type-taxonomy.md` | 5 paper-type definitions |
| `_shared/core/ethics.md` | Ethics declaration requirements |
| `_shared/core/terminology-ledger.md` | Terminology consistency protocol |

## Output Language
Follows user language. Academic terminology in English. Bilingual abstracts always provided. Chinese author notes produce English prose with Chinese structural notes.
