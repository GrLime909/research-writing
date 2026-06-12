---
name: zotero-note
description: 从 Zotero 文献生成 Obsidian 精读笔记。支持单篇处理和批量分类处理，自动提取 frontmatter、套用精读模板、刷新 Dataview 索引。可导出 BibTeX 供 academic-paper 使用。
---

## 路径配置

使用前请设置环境变量 `ZOTERO_SUITE_VAULT_ROOT` 指向 Obsidian vault 根目录。

| 变量 | 相对路径 | 说明 |
|------|----------|------|
| NOTES_ROOT | `<VAULT_ROOT>/03-科研笔记/文献笔记` | 笔记输出目录 |
| INDEX_ROOT | `<VAULT_ROOT>/03-科研笔记` | Dataview 索引页目录 |
| TEMPLATE_PATH | `<VAULT_ROOT>/08-Assets/Templates/论文精读模板.md` | 精读模板 |

Zotero CLI 路径：

```
ZOTERO_CLI = python3 /Users/grlime/.codex/plugins/cache/openai-curated/zotero/c6ea566d/skills/zotero/scripts/zotero.py
```

首次使用前确认 CLI 可用：

```bash
$ZOTERO_CLI status --json
```

---

## 模式选择

| 用户意图 | 模式 | 执行阶段 |
|---------|------|---------|
| "精读这篇论文" / 提供 Item Key 或标题 | **单篇处理** | Phase A → Phase B |
| "处理这个分类" / 提供 Zotero 分类名 | **批量处理** | Phase C（内部循环 A→B） |
| "导出参考文献" | **BibTeX 导出** | Phase D |

---

## Phase A: 数据抓取

### A.1 定位 Item

| 已知信息 | CLI 命令 |
|---------|---------|
| Item Key | 直接使用，无需查找 |
| 标题 | `$ZOTERO_CLI search "<title>" --json` |
| 作者+年份 | `$ZOTERO_CLI search "<author> <year>" --json` |

从 JSON 结果中提取 `itemKey`。

### A.2 获取子项（annotations + notes + attachments）

```bash
$ZOTERO_CLI children <item_key> --json
```

解析返回的 JSON，按 `itemType` 分类：

| itemType | 提取内容 | 用途 |
|----------|---------|------|
| `annotation` | `annotationText`、`annotationComment`、`annotationPageLabel`、`annotationType` | PDF 高亮、下划线、注释 |
| `note` | `note` 字段内容 | 独立笔记 |
| `attachment` | `itemKey`（记为 `<attachment_key>`） | 用于下一步获取全文 |

若 children JSON 不含 annotation 数据，降级为全文获取，并在 Raw_Data_Buffer 中标注 `[Annotations not available via CLI, using full-text]`。

### A.3 获取全文（备用）

```bash
$ZOTERO_CLI fulltext <attachment_key> --out /tmp/zotero_fulltext.md
```

### A.4 构建 Raw_Data_Buffer

整合所有提取内容为以下格式。**严守约束**：保持原始语言（英文），严禁翻译、总结或套用模板。

```
# Raw_Data_Buffer

## Metadata
- Item Key: <key>
- Title: <title>
- Year: <year>
- Publication: <journal>
- DOI: <doi>
- URL: <url>
- Authors: <author1>, <author2>
- Zotero Tags: <tag1>, <tag2>
- Collections: <path/to/collection>

## Abstract
<abstract text>

## Annotations
- [p.<page>] <highlight_text> (<zotero_pdf_link>)
- [p.<page>] <highlight_text> | Comment: <comment> (<zotero_pdf_link>)

## Notes
### <note_title>
<note content>

## Full-text Cache
<full text excerpt>
```

---

## Phase B: 分析写入

### B.1 Frontmatter 属性提取

在生成 Frontmatter 时，必须经过深度思考与提炼，**严禁直接大段复制摘要**。每个字段必须严格遵守以下定义，且**长度限制在一句话（10-30字）以内**：

* **`theme`（研究主题）**：一句话概括核心研究问题。（❌ 错误示范：复制整段摘要开头。✅ 正确示范：探讨城市创新空间生态位适宜性的评价指标与空间格局。）
* **`study_area`（研究区/样本）**：必须**严格依据标题和摘要**提取真实地名或样本范围，绝不能自行脑补常见城市。（❌ 错误示范：北京、上海等。✅ 正确示范：江苏省南京市。）
* **`data_source`（数据来源）**：仅提取**数据提供方、数据库名称或时间跨度**，绝不能包含作者信息或摘要前言！（❌ 错误示范：作者单位+邮编+摘要... ✅ 正确示范：南京市统计局数据及相关地理空间矢量数据，年份为 2020 年。）
* **`methodology`（研究方法）**：必须具体到**模型名称或分析工具**，严禁与 theme 字段重复！（❌ 错误示范：基于生态位视角探讨... ✅ 正确示范：构建 3 个维度的评价指标体系，结合 GIS 空间分析方法。）
* **`core_variable`（核心变量/指标）**：提取具体的**自变量、因变量或评价维度**，严禁堆砌论文的 Keywords！（❌ 错误示范：创新经济地理、创新生态系统。✅ 正确示范：资源生态位、环境生态位、技术生态位适宜度。）
* **`key_finding`（核心发现）**：用最精炼的语言总结最重要的结论，去掉"结果表明"等废话。
* **`relevance`（研究启发）**：说明该文的具体闪光点（如：提供了南京的对比基准 / 提供了生态位测度指标），拒绝"可用于补充文献脉络"这种正确的废话。

**⚠️ 强制校验机制**：在写入 Frontmatter 前，核对 `data_source` 中是否混入了类似"摘要："、"作者："、"210096"等无效字符；核对 `study_area` 是否与文章标题中的地名冲突。如发现，必须重写该字段。

### B.2 模板套用与数学公式处理

模板路径：`<TEMPLATE_PATH>`

- **结论结构**：灵活调整条目数，严格采用成对结构（主要发现 + 原文引用）。引用必须附带 `zotero://open-pdf/library/items/<pdfKey>?page=<页码>`。
- **数学公式提取规则（防乱码与胡编乱造）**：
  1. **无效公式判定**：如果提取到的公式内容仅包含孤立的求和号（`\sum`）、极短的残片（如 `ic x`）、无意义的英文字母堆叠，则**强制判定为无效乱码**。绝对禁止强行套用 `$$...$$` 输出。
  2. **连带删除机制（关键）**：如果公式被判定为无效或原文无公式，**必须彻底删除该公式对应的"公式拆解"、"符号代表什么"等所有下级解释区块**。绝对禁止为残缺符号或占位符凭空捏造解释。
  3. **占位底线**：遇乱码时，仅输出单行占位符 `$$\text{【公式复杂/乱码，原文公式未能准确提取】}$$`，后续拆解区块直接留空或删除。

### B.3 正文内容纯净度控制

在填写"具体步骤"、"数据来源"、"样本来源"等正文分析区块时，必须经过智能过滤，严禁机械搬运：

- **学术垃圾黑名单**：绝对禁止将以下内容写入笔记的任何分析字段：作者姓名、工作单位（如"XX大学XX学院"）、通讯地址、邮编、邮箱、基金项目编号（如"52008087"）、期刊投稿须知或排版规范（如"稿件内容应符合..."）。
- **提炼而非凑数**：必须从原文的"数据与方法"章节提取真正的研究步骤和数据集名称。如果在摘要或导言附近抓不到具体数据，宁可如实写"缓存文本未包含具体数据来源，需查阅完整正文"，也绝不能拿作者简介和基金号来凑字数。

### B.4 写入与终检

- **路径指定**：写入 `<NOTES_ROOT>/<分类名称>/<论文标题>.md`。分类名称从 Zotero Collections 字段或用户指定获取。
- **后置校验**：在最终保存前进行自我检查：
  1. Frontmatter 必填概括字段是否为全中文？
  2. 是否有未闭合的 `$` 符号？
  3. 是否包含有效跳转的 `zotero://select/...` 和 PDF 链接？
- 若校验通过，执行写入操作。
- **索引页刷新（新增论文时强制执行）**：若本次写入产生了新的论文笔记文件，而不是覆盖旧文件，则必须立即刷新 `<INDEX_ROOT>` 下 4 个 Dataview 索引页：
  1. `文献索引.md`
  2. `研究主题索引.md`
  3. `研究方法索引.md`
  4. `字段补全检查.md`

---

## Phase C: 批量分类处理

### C.1 任务初始化与断点读取

- **定位分类**：获取目标 Zotero 分类名称。

```bash
$ZOTERO_CLI collections --json
```

从 JSON 中找到目标分类的 key。设定目标路径为 `<NOTES_ROOT>/<分类名称>/`。

- **读取进度日志**：在该路径下查找 `_ProcessLog.md`。
  - 若存在：解析 `✅ 成功` / `⚠️ 跳过` 的 Item Key 或标题。
  - 若不存在：创建该文件。

### C.2 数据获取与任务过滤

```bash
# 获取分类下全部条目
$ZOTERO_CLI search "<分类关键词>" --json
```

- **计算差集**：全部条目 - 已处理（进度日志）= 待处理队列。
- 队列为空时告知用户"该分类下所有论文已处理完毕"。

### C.3 循环调度引擎（实时存档）

针对待处理队列中的每篇论文，**严格串行**，每处理完一篇立即更新日志：

1. **清理上下文**：重置分析状态。
2. **执行 Phase A**：数据抓取。
   - *异常捕获*：抓取失败记录 `❌ 失败（原因）` 并跳过。
3. **执行 Phase B**：分析写入。
4. **实时打卡**：追加 `_ProcessLog.md`：
   ```
   - [x] [时间戳] | ✅ 成功 | <ItemKey> | <标题>
   ```
5. **刷新 Dataview 索引**：若文件是首次创建，刷新 4 个索引页。

### C.4 输出执行报告

```
本轮总计发现未处理文献 [X] 篇。
✅ 新增成功：[N] 篇
❌ 新增失败/待确认：[M] 篇
附言：进度已实时同步至日志文件，下次执行将自动跳过已成功条目。
```

---

## Phase D: BibTeX 导出（可选）

流水线完成后，若需导出参考文献供 academic-paper 使用：

```bash
$ZOTERO_CLI export-bibtex --out <NOTES_ROOT>/<分类名称>/references.bib
```

---

## 与其他技能集成

```
zotero-note + academic-paper  -> 在 academic-paper Phase 1 中引用 <NOTES_ROOT>/<分类>/references.bib
zotero-note + obsidian-cli    -> 通过 Obsidian CLI 刷新 vault 内 Dataview 索引
```
