# Publisher Site Selectors & URL Patterns

This file is loaded on-demand per publisher. Only read the sections for the publishers the user has journals for.

---

## Elsevier / ScienceDirect

### Journal-Level Search URL

```
https://www.sciencedirect.com/journal/{journal-slug}/search?qs={url_encoded_keywords}&date={year_start}-{year_end}&show=100
```

Alternatively, use the journal page search box in the browser.

### Search Result List Page (CSS Selectors)

| Field | Selector | Notes |
|---|---|---|
| Result container | `li.ResultItem` or `div.result-item-content` | Each paper is one item |
| Title | `h2.ResultListTitle a` or `span.srctitle-date-fields a` | Text content |
| Authors | `ol.Authors li` | Join with `; ` |
| Date | `div.srctitle-date-fields span.text-s` | e.g. "May 2025" |
| DOI | `a[href*="doi.org"]` | Extract from href |
| URL | `a.anchor-text` (the title link) | Full absolute URL |
| Abstract snippet | `div.result-item-content div.abstract` or `div.ResultContainers p` | May be truncated |

### Detail Page (CSS Selectors)

| Field | Selector |
|---|---|
| Full abstract | `div.abstract.author p` or `div.Abstracts p` |

### Quirks

- ScienceDirect may show institutional access banners. Record `access_status` based on visible badges.
- Result count is capped at ~100 per page. Use `&offset=` for pagination.
- CAPTCHA trigger: rapid paging. Always wait 3s between pages.

---

## Springer Nature / SpringerLink

### Journal-Level Search URL

```
https://link.springer.com/search?facet-journal-id={journal_id}&query={url_encoded_keywords}&facet-content-type=Article&date-facet-mode=between&facet-start-year={yyyy}&facet-end-year={yyyy}
```

### Search Result List Page (CSS Selectors)

| Field | Selector | Notes |
|---|---|---|
| Result container | `li[data-test="search-result-item"]` or `ol#results-list li` | |
| Title | `h3.title` or `a.title` | Text content |
| Authors | `span.authors` | Join with `; ` |
| Date | `time` or `span.year` | e.g. "May 2025" |
| DOI | `a[href*="doi.org"]` | |
| URL | `a.title` (href) | |
| Abstract snippet | `p.snippet` or `div.abstract-section` | |

### Detail Page (CSS Selectors)

| Field | Selector |
|---|---|
| Full abstract | `div#Abs1-content p` or `section[data-title="Abstract"] p` |

### Quirks

- Nature.com journals use a different layout than SpringerLink. Check the `search_url` field.
- SpringerLink may redirect to a login wall. If no results accessible, mark the journal as blocked.

---

## Wiley Online Library

### Journal-Level Search URL

```
https://onlinelibrary.wiley.com/action/doSearch?SeriesKey={journal_id}&AllField={url_encoded_keywords}&AfterYear={yyyy}&BeforeYear={yyyy}&ContentItemType=research-article
```

### Search Result List Page (CSS Selectors)

| Field | Selector | Notes |
|---|---|---|
| Result container | `div.item__body` or `li.sru-result` | |
| Title | `h2.issue-item__title a` or `a.publication_title` | |
| Authors | `div.comma__list` or `span.hlFld-ContribAuthor` | |
| Date | `span.epub-date` or `div.meta__details time` | |
| DOI | `a[href*="doi.org"]` | |
| URL | Title link href | |
| Abstract snippet | `div.item__body div.accordion p` | |

### Detail Page (CSS Selectors)

| Field | Selector |
|---|---|
| Full abstract | `section.article-section__abstract p` or `div.abstract-group p` |

### Quirks

- Wiley frequently shows "Full Access" / "Open Access" labels. Record these in the internal state but do not attempt to bypass paywalls.
- Some older articles have no structured abstract div. If abstract extraction fails, leave it empty.

---

## IEEE Xplore

### Journal-Level Search URL

```
https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=({url_encoded_keywords})&newsearch=true&refinements=PublicationTitle:{journal_name_encoded}&ranges={year_start}_{year_end}_Year
```

### Search Result List Page (CSS Selectors)

| Field | Selector | Notes |
|---|---|---|
| Result container | `div.List-results-items` or `xpl-results-item` | Shadow DOM may apply |
| Title | `h3.result-item-title a` or `a.fw-bold` | |
| Authors | `div.author span.text-truncate` or `span.author-preference` | |
| Date | `div.publisher-info span` or `span.pub-type-text` | |
| DOI | `a[href*="doi.org"]` | |
| URL | Title link href | |
| Abstract snippet | `div.abstract-text` or `xpl-abstract` | |

### Detail Page (CSS Selectors)

| Field | Selector |
|---|---|
| Full abstract | `div.abstract-text` or `section[aria-label="Abstract"] div.u-mb-1` |

### Quirks

- IEEE uses heavy JavaScript and may require a real browser (CDP). Simple HTTP requests often fail.
- IEEE shows CAPTCHA on aggressive access. Use 4-5 second delays.
- Shadow DOM wrappers may require JS evaluation to extract text.

---

## General Browser Automation Notes

When simple HTTP GET returns incomplete or JS-rendered pages, fall back to browser automation via CDP (Chrome DevTools Protocol). Use the same approach as Paper Harbor:

1. Open a dedicated browser profile for each publisher (separate debugging ports recommended).
2. The user must manually log in before automation starts.
3. Use `page.evaluate()` for shadow-DOM-heavy sites (IEEE).
4. For all sites: detect CAPTCHA by checking for `iframe[src*="captcha"]` or `div[class*="g-recaptcha"]`. If detected, stop that publisher immediately.
