---
name: wos-monitor
description: >
  Web of Science journal monitor and literature search. Search WOS by keywords
  within a pre-defined journal list (wos-journals.txt), extract metadata, browse
  results, view paper details, download PDFs, export to Zotero, and save to Excel.
  Uses WOS internal API via Chrome CDP. Requires institutional WOS access via IP.
---

# WOS Monitor — 外文 SCI/SSCI 期刊检索

**适用范围**: Web of Science Core Collection (WOSCC)，外文 SCI/SSCI 期刊。
**期刊列表**: `wos-journals.txt`（运行时读取，不在本文件中硬编码）。

## Sub-Skills

| 技能 | 功能 | 触发方式 |
|------|------|----------|
| wos-search | 关键词搜索（含期刊过滤 + 关键词扩展） | `read `skills/wos-search/workflow.md`` |
| wos-parse-results | 解析当前搜索结果页 | 自动调用 |
| wos-navigate-pages | 翻页与排序 | `read `skills/wos-navigate-pages/workflow.md`` |
| wos-paper-detail | 提取论文完整元数据 | `read `skills/wos-paper-detail/workflow.md`` |
| wos-download | 下载论文 PDF | `read `skills/wos-download/workflow.md`` |
| wos-export | 导出到 Zotero / RIS / BibTeX | `read `skills/wos-export/workflow.md`` |
| wos-excel-export | 导出到 Excel（含去重、翻译占位） | `read `skills/wos-excel-export/workflow.md`` |

## Journal Filtering

All searches are filtered against the journal list in `wos-journals.txt`.
The agent reads this file at runtime and constructs an `SO=(...)` clause:

```
SO=("Nature Climate Change" OR "Nature Sustainability" OR ...)
```

This clause is prepended to every WOS query. No journal list content is
hardcoded in any workflow.md — the `.txt` file is the single source of truth.

## Keyword Expansion Rule

Before every WOS search, expand each concept into multiple English terms:
1. Chinese input → translate to English + add synonyms
2. English input → add near-synonyms directly
3. Abbreviations → verify meaning + add full form + exclude false matches

Always report the expanded terms to the user before executing.

## Excel Export

Results can be exported to Excel with the following columns:
文章标题 | 作者 | 所属期刊 | 摘要 | 发表时间 | 中文标题 | 中文摘要 | 入库时间

Uses `scripts/excel_manager.py` for deduplication (by DOI, then title+journal+year).
Use `scripts/journal_monitor.py` for batch WOS API search + Excel export.

## Prerequisites

- Chrome browser (manual IP-based WOS login)
- Python 3 with `openpyxl` (`pip install openpyxl`)
- Zotero desktop (optional, for export)

## File Structure

```
wos-monitor/
├── workflow.md                  ← this file
├── wos-journals.txt             ← 86-journal list (external, editable)
├── agents/
│   └── wos-researcher.md        ← Agent orchestrator
├── skills/
│   ├── wos-search/workflow.md
│   ├── wos-parse-results/workflow.md
│   ├── wos-navigate-pages/workflow.md
│   ├── wos-paper-detail/workflow.md
│   ├── wos-download/workflow.md
│   ├── wos-export/workflow.md
│   ├── wos-excel-export/workflow.md
│   └── wos-dom.md
├── scripts/
│   ├── excel_manager.py         ← Excel read/append/dedup
│   └── journal_monitor.py       ← Batch WOS API search + Excel
└── references/
    └── wos-api.md               ← WOS internal API reference
```
