# WOS Internal API Reference

## Overview

WOS exposes an internal API at `/api/wosnx/core/runQuerySearch` that returns
structured NDJSON. Call it via `fetch` from any WOS page's JS context — no
form interaction needed.

## SID Extraction

The SID (session ID) is in performance resource entries:

```javascript
const sid = performance.getEntriesByType('resource')
  .filter(r => r.name.includes('SID='))
  .map(r => r.name.match(/SID=([^&]+)/)?.[1])
  .filter(Boolean)[0] || '';
```

If SID is lost (after navigating to external sites), navigate to any WOS page
first to re-establish the session.

## Search API

**Endpoint**: `POST /api/wosnx/core/runQuerySearch?SID={SID}`

**Headers**: `Content-Type: text/plain;charset=UTF-8`, `Accept: application/x-ndjson`

**Request Body**:

```json
{
  "product": "WOSCC",
  "searchMode": "general",
  "viewType": "search",
  "serviceMode": "summary",
  "search": {
    "mode": "general",
    "database": "WOSCC",
    "query": [{"rowField": "TS", "rowText": "urban resilience"}],
    "editions": ["WOS.SSCI"]
  },
  "retrieve": {
    "first": 1,
    "count": 50,
    "history": true,
    "jcr": true,
    "sort": "times-cited-descending",
    "analyzes": [],
    "locale": "en"
  },
  "eventMode": null
}
```

### Databases (`product` / `database`)

| Code | Database |
|------|----------|
| WOSCC | Core Collection |
| ALLDB | All Databases |
| MEDLINE | MEDLINE |
| PPRN | Preprint Citation Index |
| SCIELO | SciELO Citation Index |

### Editions (Core Collection only)

| Code | Edition |
|------|---------|
| WOS.SCI | SCI-EXPANDED |
| WOS.SSCI | SSCI |
| WOS.CPCI-S | CPCI-S |
| WOS.CPCI-SSH | CPCI-SSH |
| WOS.CCR-EXPANDED | CCR-EXPANDED |
| WOS.IC | IC |

Omit `editions` for all editions.

### Field Tags (`rowField`)

| Tag | Field |
|-----|-------|
| TS | Topic (title + abstract + keywords) |
| TI | Title |
| AB | Abstract |
| AU | Author |
| SO | Publication Titles |
| DO | DOI |
| PY | Year Published |
| OG | Affiliation |
| FO | Funding Agency |
| CU | Country/Region |
| SU | Research Area |
| WC | WoS Categories |
| ALL | All Fields |

For multi-condition queries, add `rowBoolean` ("AND"/"OR"/"NOT") to subsequent rows:

```json
"query": [
  {"rowField": "TS", "rowText": "urban resilience"},
  {"rowBoolean": "AND", "rowField": "PY", "rowText": "2026"}
]
```

### Sort Options

| Value | Description |
|-------|-------------|
| relevance | Relevance (default) |
| times-cited-descending | Most cited |
| date-descending | Newest first |
| date-ascending | Oldest first |
| usage-count-last-180-days-descending | Most used |

## Response Format (NDJSON)

Each line is a JSON object. Key lines:

```
{"key":"searchInfo","payload":{"RecordsFound":5462,"RecordsSearched":123456789,"QueryID":"1"}}
{"key":"records","payload":{"1":{...},"2":{...},...}}
```

### Record Structure

```javascript
rec.colluid                              // WOS:000298554300001
rec.titles.item.en[0].title              // Paper title
rec.titles.source.en[0].title            // Journal name
rec.names.author.en[].wos_standard       // Author names
rec.pub_info.pubyear                     // Year
rec.pub_info.vol / issue / page_no       // Volume, issue, pages
rec.pub_info.pubdate                     // Publication date (e.g., "2026-01-15")
rec.doi                                  // DOI
rec.citation_related.counts.WOSCC        // Citation count (Core)
rec.citation_related.counts.ALLDB        // Citation count (All DB)
rec.ref_count                            // Reference count
rec.abstract.basic.en.abstract           // Abstract (HTML)
rec.doctypes[0]                          // Document type
rec.oa                                   // Open Access flag
```

## URL-based Search (Fallback)

When the API can't be used directly, construct a search URL:

```
https://www.webofscience.com/wos/{db}/general-summary?queryJson={ENCODED_JSON}
```

`queryJson` format:
```json
[{"rowBoolean":null,"rowField":"TS","rowText":"urban resilience"}]
```

This redirects to the results page. Then extract results via DOM selectors
or re-attempt the API call (SID will be re-established).

## Pagination

Use `retrieve.first` for offset (1-based):
- Page 1: `first=1`
- Page 2: `first=51`
- Page N: `first=(N-1)*50+1`

## Rate Limits

- Max 50 records per request
- Keep 1-2 seconds between requests
- `history: false` for pagination (don't re-save to history)
