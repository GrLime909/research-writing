---
name: literature-search
description: >
  Unified literature search for the Nature Paper Suite. Two primary engines:
  Web of Science (via wos-monitor Chrome CDP) and CNKI (via cnki-skills
  Chrome CDP). Searches pre-filtered journal lists with keyword matching,
  time-range filtering, deduplication, and export to Excel. This is the
  sole entry point for all literature searches — WOS and CNKI are internal
  components, never called directly. Use when the user needs to search for
  papers, find articles, monitor journals, or build a literature database.
  Requires institutional WOS/CNKI access via IP.
metadata:
  version: "2.0.0"
  primary_source: "Web of Science + CNKI"
  language: "English + Simplified Chinese"
---

# Literature Search — Unified WOS + CNKI Entry Point

This is the **only** literature search entry point in the Nature Paper Suite.
All literature queries, whether English or Chinese, are routed through this skill.

Two internal engines, never called directly from outside:

```
literature-search/
├── SKILL.md                    ← this file (you are here)
├── wos-monitor/                ← WOS engine (8 sub-skills, 86 journals)
│   ├── SKILL.md
│   ├── wos-journals.txt
│   ├── agents/wos-researcher.md
│   ├── skills/                 (wos-search, parse-results, navigate-pages,
│   │                            paper-detail, download, export, excel-export, dom)
│   ├── scripts/                (excel_manager.py, journal_monitor.py)
│   └── references/             (wos-api.md, wos-selectors.md, publisher-selectors.md)
└── cnki-skills/                ← CNKI engine (11 sub-skills, 124 journals)
    ├── cnki-journals.txt
    ├── agents/cnki-researcher.md
    ├── skills/                 (cnki-search, advanced-search, parse-results,
    │                            navigate-pages, paper-detail, download,
    │                            journal-search, journal-index, journal-toc,
    │                            export, excel-export)
    └── scripts/excel_manager.py
```

**Requires**: institutional WOS and CNKI access via IP. Chrome browser with
manual IP-based login completed.

---

## Pre-Step: Clarify Your Research Direction First

**This skill should NOT be the first step of your workflow.**

Before searching for literature, use `deep-research` (socratic mode) to clarify
your research question. A well-defined RQ makes literature search dramatically
more efficient and focused.

Once your direction is clear, return here to execute the search.

---

## Quick Start

Just say what you want to find. The skill auto-selects the engine:

| You say | Engine used |
|---------|-------------|
| "Search for urban resilience papers since 2024" | **WOS** (English keywords) |
| "帮我搜城市韧性的最新论文" | **CNKI** (Chinese keywords) |
| "Search WOS for climate adaptation" | **WOS** (explicit) |
| "在知网搜水资源管理" | **CNKI** (explicit) |
| "Search both WOS and CNKI for ecosystem services" | **Both** (explicit) |
| "Search arXiv for graph neural network papers" | **arXiv** (explicit opt-in) |
| "Search Google Scholar for urban governance" | **Google Scholar** (explicit opt-in) |

---

## Source Policy

WOS and CNKI are the **default** literature sources. No automatic fallback
to any other database. arXiv and Google Scholar are available only when
explicitly requested by the user.

| Source | Engine | Journals | Access |
|--------|--------|----------|--------|
| Web of Science Core Collection | `wos-monitor/` | 86 journals (wos-journals.txt) | Chrome CDP, IP login |
| CNKI (中国知网) | `cnki-skills/` | 124 journals (cnki-journals.txt) | Chrome CDP, IP login |
| arXiv (opt-in only) | Codex browsing | Preprints | Explicit: "search arXiv for ..." |
| Google Scholar (opt-in only) | Codex browsing | Broad discovery | Explicit: "search Google Scholar for ..." |

If WOS or CNKI is unavailable (IP blocked, session expired), **stop and report**
rather than falling back to another source.

---

## Language-Based Auto-Selection

When no source is specified, the engine is chosen by keyword language:

| Keyword Language | Auto-Selected Engine | Reason |
|-----------------|---------------------|--------|
| English (ASCII only) | `wos-monitor/` (WOS) | WOS indexes English journals |
| Chinese (any CJK characters) | `cnki-skills/` (CNKI) | CNKI is the primary index for Chinese journals |
| Mixed English + Chinese | Ask user, or search both engines | |
| Any | arXiv / Google Scholar | Never auto-selected; only when user explicitly says "arXiv" or "Google Scholar" |

---

## Keyword Logic

| User says | Operator | Query |
|-----------|----------|-------|
| "A B" (space only, no connector) | **OR** | A OR B |
| "A and B" | **AND** | A AND B |
| "A + B" | **AND** | A AND B |
| "A;B" / "A,B" | **OR** | A OR B |

**Default rule**: Space-separated keywords = **OR** (broader search).
Use explicit connector (and/+) for **AND**.

---

## Keyword Expansion for WOS

**Universal rule**: before every WOS search, expand each concept into
multiple English terms — regardless of whether the input was Chinese or
English. A single keyword is a single point of failure.

This applies to ALL WOS searches:
- Chinese keywords → translate to English + add synonyms
- English keywords → add near-synonyms (no translation needed)
- Abbreviations → verify meaning + add full form + exclude false matches

### Step 1: Translate (if input is Chinese)

Convert each Chinese concept to its primary English academic term.
Do NOT translate word-for-word — use established terminology in the field.

### Step 2: Expand synonyms (always, for every concept)

For each English concept, generate 2-4 search terms:
- the primary term (from translation or user input)
- a narrower or more specific synonym
- a broader or adjacent synonym
- an alternative phrasing commonly used in the target journals

Combine synonyms for the same concept with **OR**.

### Step 3: Handle abbreviations (when applicable)

If any English term has a known academic abbreviation:

1. Include the abbreviation in the OR group: `"Lorenz asymmetry coefficient" OR "LAC"`
2. Check whether this abbreviation is ambiguous (shared with unrelated concepts).
   For example, `LAC` can mean:
   - Lorenz Asymmetry Coefficient
   - Latin America and the Caribbean
   - Lactate
   - Local Area Coverage
3. If ambiguous, add a **NOT exclusion** to filter out the false meaning:
   ```
   TS=("Lorenz asymmetry coefficient" OR ("LAC" NOT ("Latin America" OR Caribbean OR lactate)))
   ```
4. If the abbreviation is unambiguous in the target literature, no NOT is needed.

**Abbreviation disambiguation table** (check before search):

| Abbreviation | Possible meanings | When searching for... | Add NOT for... |
|-------------|-------------------|----------------------|----------------|
| LAC | Lorenz asymmetry coefficient / Latin America and Caribbean / Lactate | Lorenz asymmetry | "Latin America", Caribbean, lactate |
| ML | Machine learning / Maximum likelihood / Milliliter | Machine learning | "maximum likelihood" (if relevant) |
| AI | Artificial intelligence / Artificial insemination | Artificial intelligence | Usually unambiguous in CS journals |

When in doubt, check the abbreviation on the target journal's typical usage
or add the NOT exclusion. A narrower result is better than a noisy one.

### Example 1: Chinese input → translation + synonyms + abbreviation

**Input**: 在WOS中搜索洛伦兹不对称系数评估生态系统

**Auto-expansion**:
| Chinese | English synonyms + abbreviation | Exclusion |
|---------|-------------------------------|-----------|
| 洛伦兹不对称系数 | "Lorenz asymmetry coefficient", "Lorenz asymmetry", "LAC" | NOT ("Latin America" OR Caribbean) |
| 生态系统 | "ecosystem", "ecological system", "ecosystem service*" | — |

**Final WOS query**:
```
TS=("Lorenz asymmetry coefficient" OR "Lorenz asymmetry" 
    OR ("LAC" NOT ("Latin America" OR Caribbean OR lactate)))
AND TS=(ecosystem* OR "ecological system" OR "ecosystem service*")
AND TS=(evaluat* OR assess* OR effect* OR measur*)
```

**User confirmation**:
```
Keyword expansion:
  洛伦兹不对称系数 → "Lorenz asymmetry coefficient" / "Lorenz asymmetry" / "LAC"
    ⚠ "LAC" is ambiguous — excluding "Latin America", Caribbean, lactate
  生态系统 → ecosystem* / "ecological system" / "ecosystem service*"
  评估/效果 → evaluat* / assess* / effect* / measur*

Search now?
```

### Example 2: English input → synonyms only (no translation)

**Input**: Search WOS for water governance resilience

**Auto-expansion**:
| English | Synonyms | Exclusion |
|---------|----------|-----------|
| water governance | "water governance", "water management", "integrated water resource management" | — |
| resilience | "resilience", "adaptive capacity", "robustness" | — |

**Final WOS query**:
```
TS=("water governance" OR "water management" OR "integrated water resource management")
AND TS=("resilience" OR "adaptive capacity" OR "robustness")
```

### Reasoning

WOS topic search matches only what you type. Authors use different terms
for the same concept — "urban resilience" in one paper, "city resilience"
in another, "urban adaptive capacity" in a third. Multiple synonyms cast a
wider net without sacrificing precision because the journal filter already
narrows the domain. Abbreviation disambiguation prevents noise from
homographic abbreviations.

**Always report the expansion to the user before executing.**

---

## WOS Engine (wos-monitor/)

### Internal Structure

```
wos-monitor/
├── SKILL.md                     ← WOS entry point
├── wos-journals.txt             ← 86-journal list (external, editable)
├── agents/
│   └── wos-researcher.md        ← Agent orchestrator
├── skills/
│   ├── wos-search/SKILL.md      ← Search + journal filter (reads wos-journals.txt)
│   ├── wos-parse-results/SKILL.md
│   ├── wos-navigate-pages/SKILL.md
│   ├── wos-paper-detail/SKILL.md
│   ├── wos-download/SKILL.md
│   ├── wos-export/SKILL.md
│   └── wos-excel-export/SKILL.md
├── scripts/
│   ├── excel_manager.py         ← Excel read/append/dedup
│   └── journal_monitor.py       ← Batch WOS API search + Excel
└── references/
    ├── wos-api.md               ← WOS internal API reference
    ├── wos-selectors.md         ← WOS page CSS selectors
    └── publisher-selectors.md   ← Publisher page selectors
```


### Journal-List Filtering

All WOS searches are filtered against the journal list in `wos-journals.txt`.
Two filtering methods are available:

- **"Search within results"**: After performing a topic search on WOS, use the
  "Search within results" sidebar to add journal-name constraints.
- **Advanced query**: Build a single query with `SO=(...)` clause containing
  the journal names from `wos-journals.txt`.

### Workflow (7 phases)

1. **Setup**: Load WOS URL, parse keywords and time range, load existing Excel
2. **Refine**: Add keywords via WOS sidebar "Search within results"
3. **Parse**: Extract title, authors, date, journal, DOI, WOS URL
4. **Deduplicate**: Against existing Excel by DOI or (title, journal, year)
5. **Detail**: Click through to full record for abstracts (new papers only)
6. **Translate**: Optional Chinese translation of titles/abstracts
7. **Export**: Append to Excel, report totals

---

## CNKI Engine (cnki-skills/)

### Internal Structure

```
cnki-skills/
├── cnki-journals.txt            ← 124-journal list (FMS Tier 1 & 2, external)
├── agents/
│   └── cnki-researcher.md       ← Unified agent
├── skills/
│   ├── cnki-search/             ← Keyword search
│   ├── cnki-advanced-search/    ← Field-filtered search (北大核心+CSSCI fixed)
│   ├── cnki-parse-results/      ← Parse results page into structured data
│   ├── cnki-navigate-pages/     ← Pagination and sort
│   ├── cnki-paper-detail/       ← Full paper details (abstract, keywords)
│   ├── cnki-download/           ← PDF/CAJ download
│   ├── cnki-journal-search/     ← Journal lookup by name/ISSN/CN
│   ├── cnki-journal-index/      ← Journal indexing status and impact factor
│   ├── cnki-journal-toc/        ← Browse journal table of contents
│   ├── cnki-export/             ← Export to Zotero or RIS
│   └── cnki-excel-export/       ← Export to Excel with dedup
└── scripts/
    └── excel_manager.py         ← Excel read/append/dedup
```

### Sub-skill Routing

Literature-search delegates to the appropriate cnki sub-skill based on intent:

| User intent | Sub-skill used |
|-------------|---------------|
| Keyword search | `cnki-search` |
| Author/journal/date filters | `cnki-advanced-search` |
| Parse current page | `cnki-parse-results` (auto) |
| Next/previous page | `cnki-navigate-pages` |
| Paper details | `cnki-paper-detail` |
| Export to Zotero | `cnki-export` |

### Workflow

1. Determine intent -> route to appropriate sub-skill
2. Execute search via Chrome CDP
3. Parse results into structured data
4. Deduplicate against existing Excel
5. Export and report

---

## Opt-In Sources (arXiv / Google Scholar)

arXiv and Google Scholar are available but **never auto-selected**. The user
must explicitly name the source:

| User says | Action |
|-----------|--------|
| "Search arXiv for climate adaptation preprints" | Search arXiv only |
| "Use Google Scholar to find urban governance papers" | Search Google Scholar only |
| "Search WOS and also check arXiv" | WOS primary, arXiv supplementary |

When arXiv or Google Scholar is requested:
- Results are marked as **unverified** (no institutional indexing guarantee)
- No journal-list filtering is applied
- WOS/CNKI deduplication rules still apply (mark duplicates, don't silently drop)
- Report source explicitly: "Source: arXiv (unverified)"

---

## Dual-Engine Search

When the user asks to search both WOS and CNKI:

1. Execute WOS search and CNKI search in parallel
2. Deduplicate within each engine independently
3. Report results separately (WOS section + CNKI section)
4. Do NOT cross-deduplicate between engines (different indexing systems)

---

## Integration with deep-research

When the bibliography_agent in deep-research needs to search for literature:

1. bibliography_agent formulates search terms and journal lists
2. Invokes literature-search with the terms
3. literature-search routes to WOS or CNKI based on keyword language
4. Returns annotated bibliography to synthesis_agent

---

## Safety Rules

1. Never enter credentials — WOS and CNKI login is IP-based
2. Do not bypass rate limits or CAPTCHAs
3. Keep request rates human-like: 1-2 seconds between page loads
4. Do not download PDFs or full text from WOS, CNKI, or linked publisher sites
5. If session expires, stop and report to the user
6. If Chrome is not available or WOS/CNKI tab is not open, stop and report

---

## Output Format

```text
Search report
- Engine: [WOS / CNKI / Both]
- Keywords: [...]
- Time range: [...]
- Total found: N
- Duplicates skipped: N
- New papers saved: N
- Output file: [absolute path to Excel]

Top results:
1. [Author, Year] Title. Journal. DOI.
2. ...
```
