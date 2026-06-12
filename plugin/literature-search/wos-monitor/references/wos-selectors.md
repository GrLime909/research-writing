# WOS Page Selectors and Search Patterns

This file documents the Web of Science UI structure for browser automation.
Codex loads this at runtime when executing WOS searches.

---

## Browser Setup

**Chrome (via Chrome CDP):**
The Chrome plugin provides CDP at http://127.0.0.1:9222 by default.
No separate Chrome launch needed.

**Firefox** (alternative for from-scratch mode):
```bash
# macOS
/Applications/Firefox.app/Contents/MacOS/firefox --remote-debugging-port=9223
# Windows
"C:\Users\grlime\AppData\Local\Mozilla Firefox\firefox.exe" --remote-debugging-port=9223
```

**Chrome / Edge** (standalone, for from-scratch mode):
```bash
chrome --remote-debugging-port=9223 --user-data-dir=~/wos-chrome-profile
```

---

## WOS Page URLs

| Page | URL Pattern |
|------|------------|
| Advanced Search | `https://www.webofscience.com/wos/alldb/advanced-search` |
| Basic Search | `https://www.webofscience.com/wos/alldb/basic-search` |
| Summary / Results | `https://webofscience.clarivate.cn/wos/alldb/summary/<session-id>/<sort>/<page>` |
| Full Record | `https://webofscience.clarivate.cn/wos/alldb/full-record/<id>` |

Note: `webofscience.clarivate.cn` is the Chinese WOS portal. The international
portal (`www.webofscience.com`) uses the same page structure and selectors.

---

## Building the Search Query

WOS field tags for advanced search:

| Tag | Field | Usage |
|---|---|---|
| `SO` | Publication Title | `SO=("Nature Energy")` -- exact journal filter |
| `TS` | Topic (title, abstract, author keywords, Keywords Plus) | `TS=("solid electrolyte")` -- our main search target |
| `TI` | Title only | Narrower than TS. Use only if user explicitly wants title-only. |
| `PY` | Year Published | `PY=(2025-2026)` -- year range only |

### Query Construction (from-scratch mode)

For keywords split by semicolons into OR groups, space-separated terms within a group are AND:

```
SO=("Journal Name") AND (TS=("term1 term2") OR TS=("term3") OR TS=("term4"))
```

Example for "solid electrolyte;SEI" in Nature Energy:

```
SO=("Nature Energy") AND (TS=("solid electrolyte") OR TS=("SEI"))
```

Multiple journals: run separate searches per journal. WOS does not support
OR across different SO values in a single query well.

### Time Range

Use the WOS UI date picker for time filtering. Both WOS and CNKI filter by year only.
For year ranges, use `PY=(2025-2026)` in the query or the UI year picker.

---

## URL Mode: Results Summary Page (Pre-Filtered)

When starting from a pre-filtered WOS summary URL, the page already has
journal and time filters applied. We only need to add keyword filtering.

### "Search within results" / Refine Panel

After navigating to the pre-filtered summary URL, locate the refine panel
on the left sidebar or top of results:

| Element | Selector | Notes |
|---------|----------|-------|
| Refine panel container | `div.refine-panel` or `app-refine-panel` | Left sidebar on desktop |
| "Search within results" input | `input[placeholder*="Search within"]` or `input.refine-search` | Text input for keyword filter |
| "Search within results" (alt) | `app-search-within-results input` | WOS component-based selector |
| Refine search submit | `button.refine-search-btn` or button near the input | Click to apply filter |
| Refine by Topic link | `a[data-refine*="TS"]` or link containing "Topic" | Alternative: click predefined refine options |

### Refine Query Format

When entering keywords into the "Search within results" input, use the same
TS= format as advanced search:

```
TS=("urban resilience") OR TS=("climate adaptation")
```

Or for simple single-group keywords:

```
TS=("urban resilience")
```

### After Refine

The page reloads with filtered results. The URL typically updates to include
a `qid` parameter. Parse results the same way as from-scratch mode.

---

## Results List Page (After Search or Refine)

WOS shows results in a table-like layout. After page load, wait for the
results container.

### CSS Selectors

| Field | Selector | Notes |
|---|---|---|
| Results container | `div.search-results` or `app-search-results` | Wait for this to appear |
| Result count | `span.brand-blue` or `div.results-amount` | e.g. "1,234" |
| Per-result row | `app-summary` | Each paper is one `<app-summary>` element |
| Title | `a.summary-title` or `h3.title` | Click to open full record |
| Authors | `span.author` or `div.author` within `<app-summary>` | Join with `; ` |
| Date | `span.source-date` or `span.pub-date` | e.g. "2025-05-01" or "May 2025" |
| Journal (SO) | `span.source-title` or `div.source` | The journal name |
| DOI | Text starting with `10.` inside the row, or `a[href*="doi.org"]` | WOS sometimes hides DOI in a tooltip |
| WOS Detail URL | Click the title link: `a.summary-title[href]` | Opens `/wos/alldb/full-record/...` |
| Abstract snippet | `div.abstract` or not shown on list page | WOS list pages often show NO abstract |

### Pagination

WOS paginates at 50 results per page. After collecting page N:

1. Click the right-arrow or "Next Page" button: `button[aria-label="Next Page"]`
   or `a.nextPage` or `a[aria-label="Next Page"]`
2. Wait for the `app-summary` count to change.
3. Repeat until the Next button is disabled or hidden.

If results exceed 10,000, WOS truncates. If this happens, narrow the time
range and inform the user.

---

## Full Record Page (Detail Page)

Click the title link from the results list to open. Wait for:

| Field | Selector | Notes |
|---|---|---|
| Page loaded indicator | `app-full-record` or `div.full-record` | |
| Full title | `h1.title` or `div.title` | |
| Full authors | `span.author` within the record | All authors, not truncated |
| Abstract | `div.abstract p` or `div.abstract-text` | The complete abstract text |
| DOI | `span[data-ta="doi"]` or `a[href*="doi.org"]` | |
| ISSN | `span#FullRecISN` or near the journal name | |
| Document type | `div.document-type` | Article, Review, etc. |
| Keywords (author) | `div.keywords-author span` | Optional, useful for validation |
| Keywords Plus | `div.keywords-plus span` | WOS-generated keywords |

---

## URL Mode: Chrome Plugin CDP Interaction Flow

```
1. Navigate to user''s pre-filtered WOS summary URL
2. Wait for results container to load: div.search-results or app-search-results
3. Take snapshot, identify "Search within results" input
4. Enter refine query (TS= format) into the input
5. Click the refine/search submit button
6. Wait for page reload
7. Take snapshot, parse app-summary rows
8. For pagination: click "Next Page" button, wait, snapshot, parse
9. For each new paper: click title link, wait for app-full-record, extract abstract
```

## Common WOS Quirks

1. **Session timeout**: WOS sessions expire after ~30 min of inactivity.
   If a results page returns 0 unexpectedly, the session may have expired.
   Refresh the page and check.
2. **Search syntax sensitivity**: WOS field tags are case-insensitive.
   `SO=` and `so=` both work.
3. **Exact journal name matching**: WOS matches the exact SO string.
   If `Nature Energy` returns 0, try without parentheses or check the
   WOS journal list for the exact indexed name.
4. **No abstract on list page**: Unlike ScienceDirect, WOS often shows no
   abstract on the results list. The snippet field may be empty. This is
   normal -- fetch from the full record page.
5. **CAPTCHA**: Rare on WOS via institutional IP. If it appears, stop and
   ask the user.
6. **Export limits**: WOS allows exporting up to 1,000 records at a time
   via the Export button. The script uses page-by-page parsing instead,
   which avoids this limit but is slower.
7. **Chinese vs International portal**: `webofscience.clarivate.cn` and
   `www.webofscience.com` share the same page structure. Selectors are
   identical. The session cookie works across both domains.
8. **Refine vs new search**: Using "Search within results" preserves the
   existing journal/time filters. Building a new advanced query from
   scratch loses them.
