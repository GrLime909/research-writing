---
name: wos-excel-export
description: Export WOS search results to Excel with deduplication. Columns include title, authors, journal, abstract, pub date, and placeholder columns for Chinese translation.
argument-hint: "[--output path.xlsx] [--translate]"
user-invocable: true
disable-model-invocation: false
---

# WOS Excel Export

Export WOS search results to Excel. Deduplicates by DOI, then (title + journal + year).
Output columns: 文章标题 | 作者 | 所属期刊 | 摘要 | 发表时间 | 中文标题 | 中文摘要 | 入库时间

## Steps

### Step 1: Collect Papers

Gather paper data from the current search session. Each paper should have:
```json
{
  "title": "Paper title",
  "authors": "LastName, Initials; ...",
  "journal": "Journal name",
  "abstract": "Abstract text",
  "pub_date": "2026-01-15",
  "doi": "10.xxxx/xxxxx"
}
```

### Step 2: Run Excel Export Script

```bash
python scripts/excel_manager.py --output OUTPUT.xlsx --action append
```

Pipe the JSON paper data via stdin:
```bash
echo '[{...papers...}]' | python scripts/excel_manager.py --output papers.xlsx
```

Or save to a temp file and pass via --input:
```bash
python scripts/excel_manager.py --output papers.xlsx --input /tmp/wos_papers.json
```

### Step 3: Report

```
Excel export report:
- Output: [absolute path to Excel]
- New papers saved: N
- Duplicates skipped: N
- Total in Excel: N
```

## Translation

The columns 中文标题 and 中文摘要 are placeholders. Translation can be done
separately or via the `--translate` flag if a translation API is configured.

## Deduplication Logic

1. If DOI is present → `doi:{lowercase_doi}` 
2. Fallback → `combo:{normalized_title}|{journal}|{year}`
