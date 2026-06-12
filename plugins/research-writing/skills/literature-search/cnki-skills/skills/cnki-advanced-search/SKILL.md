---
name: cnki-advanced-search
description: >
  【仅限中文期刊】Perform advanced search on CNKI with field filters (author, title,
  journal, date range). Source category hardcoded to 北大核心 + CSSCI. Journal list
  in cnki-journals.txt (independent of WOS wos-journals.txt).
argument-hint: "[describe search criteria in natural language]"
---

# CNKI Advanced Search (高级检索) — 中文 北大核心/CSSCI

**适用范围**: 中国知网 (CNKI)，北大核心 + CSSCI（已硬编码）。
**期刊列表**: `cnki-journals.txt` — 中文期刊名，与 WOS 的 `wos-journals.txt` 完全独立。

## Arguments

`$ARGUMENTS` describes the search criteria in natural language. Parse it to identify:
- **Subject keywords** (主题) — default field
- **Title keywords** (篇名)
- **Keywords** (关键词)
- **Author name** (作者)
- **Journal/source** (文献来源) — single journal from cnki-journals.txt
- **Date range** (时间范围)

## Steps

### 1. Navigate

→ `https://kns.cnki.net/kns/AdvSearch?classid=7NS01R8M`

### 2. Search + get results

```javascript
async () => {
  const query = "KEYWORDS";
  const fieldType = "SU";           // SU=主题, TI=篇名, KY=关键词, TKA=篇关摘, AB=摘要
  const query2 = "";
  const rowLogic = "AND";
  const sourceTypes = ["hx", "CSSCI"]; // 硬编码：北大核心 + CSSCI
  const startYear = "";
  const endYear = "";
  const author = "";
  const journal = "";               // 单本期刊名（来自 cnki-journals.txt）

  // Wait for form
  await new Promise((r, j) => {
    let n = 0;
    const c = () => { if (document.querySelector('#txt_1_value1')) r(); else if (n++ > 30) j('timeout'); else setTimeout(c, 500); };
    c();
  });

  const cap = document.querySelector('#tcaptcha_transform_dy');
  if (cap && cap.getBoundingClientRect().top >= 0) return { error: 'captcha' };

  const selects = Array.from(document.querySelectorAll('select')).filter(s => s.offsetParent !== null);

  // Source type: uncheck 全部, check 北大核心 + CSSCI
  const gjAll = document.querySelector('#gjAll');
  if (gjAll && gjAll.checked) gjAll.click();
  for (const st of sourceTypes) {
    const cb = document.querySelector('#' + st);
    if (cb && !cb.checked) cb.click();
  }

  // Row 1
  selects[0].value = fieldType;
  selects[0].dispatchEvent(new Event('change', { bubbles: true }));
  const input = document.querySelector('#txt_1_value1');
  input.value = query;
  input.dispatchEvent(new Event('input', { bubbles: true }));

  // Author / Journal / Year
  if (author) { document.querySelector('#au_1_value1').value = author; }
  if (journal) { document.querySelector('#magazine_value1').value = journal; }
  if (startYear) { selects[14].value = startYear; selects[14].dispatchEvent(new Event('change', { bubbles: true })); }
  if (endYear) { selects[15].value = endYear; selects[15].dispatchEvent(new Event('change', { bubbles: true })); }

  // Submit
  document.querySelector('div.search')?.click();

  await new Promise((r, j) => {
    let n = 0;
    const c = () => { if (document.body.innerText.includes('条结果')) r(); else if (n++ > 40) j('timeout'); else setTimeout(c, 500); };
    setTimeout(c, 2000);
  });

  const cap2 = document.querySelector('#tcaptcha_transform_dy');
  if (cap2 && cap2.getBoundingClientRect().top >= 0) return { error: 'captcha' };

  return {
    query, fieldType, sourceTypes, startYear, endYear, author, journal,
    total: document.querySelector('.pagerTitleCell')?.innerText?.match(/([\d,]+)/)?.[1] || '0',
    page: document.querySelector('.countPageMark')?.innerText || '1/1',
    url: location.href
  };
}
```

## ⚠️ 期刊列表说明

| Skill | 期刊列表 | 数据库 | 类型 |
|-------|---------|--------|------|
| `journal-monitor` | `wos-journals.txt` | Web of Science | 外文 SCI/SSCI |
| `cnki-advanced-search` | `cnki-journals.txt` | CNKI 中国知网 | 中文 北大核心/CSSCI |

两个列表完全独立，切勿混用。
