---
name: zotero-note
description: 从 Zotero 文献生成 Obsidian 精读笔记。使用 54yyyu/zotero-mcp 的 zotero-cli 读取本地 Zotero 库，支持单篇精读、批量分类处理、frontmatter 提取、Dataview 索引刷新与 BibTeX 导出。
---
# Zotero Note

## 工具接口

本技能使用 [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) 安装出的终端命令，不再使用旧版 `zotero.py` 适配器。

| 变量           | 命令           | 用途                                                                |
| -------------- | -------------- | ------------------------------------------------------------------- |
| `ZOTERO_CLI` | `zotero-cli` | 搜索、读取 metadata、children、annotations、notes、fulltext、BibTeX |
| `ZOTERO_MCP` | `zotero-mcp` | 仅在排查问题时检查版本、配置与语义数据库状态                        |

默认前提：

- `zotero-cli` 已安装并配置完成。
- 命令示例使用通用 shell 写法；在 Windows、macOS 或 Linux 上按当前终端直接执行同名命令即可，不要在技能中写死平台路径或特定终端。
- 除非用户明确要求排查安装或配置问题，不要在每次任务开始前运行健康检查命令。
- 若当前机器的语义搜索数据库 `Document count` 为 0 或报 Chroma/HNSW 错误，除非用户明确要求，不依赖 `search --mode semantic`。

## 路径配置

使用前请设置环境变量 `ZOTERO_SUITE_VAULT_ROOT` 指向 Obsidian vault 根目录。若该变量未设置，先询问用户，不要猜测 vault 路径。

| 变量              | 相对路径                                             | 说明                |
| ----------------- | ---------------------------------------------------- | ------------------- |
| `NOTES_ROOT`    | `<VAULT_ROOT>/03-科研笔记/文献/文献笔记`                | 笔记输出目录        |
| `INDEX_ROOT`    | `<VAULT_ROOT>/03-科研笔记`                         | Dataview 索引页目录 |
| `TEMPLATE_PATH` | `<VAULT_ROOT>/08-Assets/Templates/论文精读模板.md` | 精读模板            |

文件规则：

- 批量运行产生的临时文件应放在系统临时目录；任务结束后删除不必要的中间文件。

## 模式选择

| 用户意图                                | 模式        | 执行阶段                   |
| --------------------------------------- | ----------- | -------------------------- |
| “精读这篇论文” / 提供 Item Key 或标题 | 单篇处理    | Phase A -> Phase B         |
| “处理这个分类” / 提供 Zotero 分类名   | 批量处理    | Phase C（内部循环 A -> B） |
| “导出参考文献”                        | BibTeX 导出 | Phase D                    |

## Phase A: 数据抓取

### A.1 定位 Item

优先使用用户给出的 Item Key；没有 Item Key 时再搜索标题、作者或年份。

| 已知信息  | CLI 命令                                                    |
| --------- | ----------------------------------------------------------- |
| Item Key  | 直接使用，无需查找                                          |
| 标题      | `zotero-cli search "<title>" --limit 10`                  |
| 作者+年份 | `zotero-cli search "<author> <year>" --limit 10`          |
| Citekey   | `zotero-cli search --mode citekey "<citekey>" --limit 10` |

搜索返回多个候选时，按标题、作者、年份人工比对；仍不确定时让用户确认，不要自行选择。

### A.2 获取 Metadata

```sh
zotero-cli get metadata <item_key>
```

从输出中提取：

- Item Key
- Title
- Year / Date
- Publication
- DOI
- URL
- Authors
- Tags
- Collections
- Abstract

如需 BibTeX 元数据：

```sh
zotero-cli get metadata <item_key> --output-format bibtex
```

### A.3 获取子项、批注、笔记与全文

```sh
zotero-cli get children <item_key>
zotero-cli annotations list --item-key <item_key> --pdf-extraction
zotero-cli notes list --item-key <item_key> --full
zotero-cli get fulltext <item_key>
```

解析规则：

| 来源                  | 提取内容                           | 用途                |
| --------------------- | ---------------------------------- | ------------------- |
| `get children`      | attachment、note、PDF 子项信息     | 定位 PDF 和附属笔记 |
| `annotations list`  | 高亮、下划线、批注、页码、PDF 链接 | 原文证据与引用      |
| `notes list --full` | Zotero 独立笔记全文                | 补充阅读记录        |
| `get fulltext`      | OCR/全文索引文本                   | 批注不足时兜底      |

`get fulltext` 可能因全文过长返回 “Response size” 警告或非零退出码。遇到这种情况时，不要改用语义搜索；应先使用 metadata、annotations、notes 和可见 fulltext 片段完成笔记，并在需要原文细节的位置标注“全文过长，需分段核对 PDF”。

若批注为空，降级使用全文，并在 `Raw_Data_Buffer` 中标注：

```text
[Annotations not available via zotero-cli, using full-text]
```

### A.4 构建 Raw_Data_Buffer

整合所有提取内容为以下格式。保持原始语言，严禁在 Raw_Data_Buffer 阶段翻译、总结或套用模板。

```markdown
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

## Phase B: 分析写入

### B.1 Frontmatter 属性提取

在生成 Frontmatter 时，必须深度提炼，严禁直接大段复制摘要。每个字段必须严格遵守模板中的定义，以下是部分字段额外附加的说明：

- `study_area`（研究区/样本）：严格依据标题和摘要提取真实地名或样本范围，绝不能自行脑补常见城市。
- `data_source`（数据来源）：仅提取数据提供方、数据库名称或时间跨度，绝不能包含作者信息或摘要前言。
- `methodology`（研究方法）：必须具体到模型名称或分析工具，严禁与 `theme` 字段重复。
- `core_variable`（核心变量/指标）：提取具体自变量、因变量或评价维度，严禁堆砌 Keywords。
- `key_finding`（核心发现）：总结最重要的结论，去掉“结果表明”等废话。
- `relevance`（研究启发）：说明该文的具体闪光点，拒绝“可用于补充文献脉络”这类空泛表述。

强制校验：

- 检查 `data_source` 是否混入“摘要：”“作者：”、邮编、邮箱、基金号等无效字符；发现则重写。
- 检查 `study_area` 是否与标题、摘要中的地名冲突；发现则重写。
- Frontmatter 必填概括字段，除标题与摘要外必须为简体中文。

### B.2 模板套用与数学公式处理

模板路径：`<TEMPLATE_PATH>`

- 结论结构可灵活调整条目数，但必须采用“主要发现 + 原文引用”的成对结构。
- 引用优先使用 `annotations list` 输出中的 Zotero PDF 链接；若缺失页码，则标注“页码缺失，需回 Zotero 核对”。
- 数学公式提取规则：
  1. 如果提取到的公式仅包含孤立求和号、极短残片、无意义字母堆叠，强制判定为无效乱码，绝不强行套用 `$$...$$`。
  2. 如果公式无效或原文无公式，彻底删除对应的“公式拆解”“符号代表什么”等下级解释区块。
  3. 遇到复杂公式乱码时，仅输出 `$$\text{【公式复杂/乱码，原文公式未能准确提取】}$$`，后续拆解区块留空或删除。

### B.3 正文内容纯净度控制

填写“具体步骤”“数据来源”“样本来源”等正文分析区块时必须过滤噪声，严禁机械搬运。

学术垃圾黑名单：

- 作者姓名
- 工作单位
- 通讯地址
- 邮编
- 邮箱
- 基金项目编号
- 期刊投稿须知或排版规范

提炼规则：

- 优先从原文“数据与方法”章节提取真正的研究步骤和数据集名称。
- 如果缓存文本未包含具体数据来源，写“缓存文本未包含具体数据来源，需查阅完整正文”，不要用作者简介、基金号或摘要前言凑字数。

### B.4 写入与终检

写入路径：

```text
<NOTES_ROOT>/<分类名称>/<论文标题>.md
```

分类名称优先从 Zotero Collections 字段获取；没有分类或分类不明确时使用用户指定分类。

保存前必须检查：

1. 是否有未闭合的 `$` 符号。
2. 是否包含可用的 Zotero item 链接或 PDF 链接。

若本次写入产生新论文笔记，而不是覆盖旧文件，立即刷新 `<INDEX_ROOT>` 下 4 个 Dataview 索引页：

1. `文献索引.md`
2. `研究主题索引.md`
3. `研究方法索引.md`

## Phase C: 批量分类处理

### C.1 定位分类

先列出或搜索 Zotero collection：

```sh
zotero-cli get collections
zotero-cli collections search "<collection_name>"
```

从结果中确认目标 collection key。若出现多个同名或相近分类，必须让用户确认。

### C.2 获取分类条目

```sh
zotero-cli get collection-items <collection_key> --detail full
```

仅处理主文献条目，跳过 attachment、note 等子项。目标输出目录为：

```text
<NOTES_ROOT>/<分类名称>/
```

### C.3 断点与过滤

在目标输出目录中维护 `_ProcessLog_codex.md`。

- 若日志存在：解析 `成功` / `跳过` 的 Item Key 或标题。
- 若日志不存在：创建日志，并记录启动时间、collection key、CLI 版本。
- 待处理队列 = 分类全部主文献 - 已成功处理文献。
- 队列为空时，告知用户“该分类下所有论文已处理完毕”。

### C.4 串行处理

针对待处理队列中的每篇论文严格串行：

1. 重置当前论文分析状态。
2. 执行 Phase A 数据抓取。
3. 执行 Phase B 分析写入。
4. 每处理完一篇立即追加 `_ProcessLog_codex.md`：

```markdown
- [x] <ISO 时间> | 成功 | <ItemKey> | <标题>
```

失败时记录：

```markdown
- [ ] <ISO 时间> | 失败 | <ItemKey> | <标题> | <原因>
```

5. 若文件是首次创建，刷新 4 个 Dataview 索引页。

### C.5 输出执行报告

```text
本轮总计发现未处理文献 [X] 篇。
新增成功：[N] 篇
失败/待确认：[M] 篇
进度已同步至 _ProcessLog_codex.md，下次执行将自动跳过已成功条目。
```

## Phase D: BibTeX 导出

单篇导出：

```sh
zotero-cli get bibtex <item_key>
```

分类导出时，先用 `zotero-cli get collection-items <collection_key> --detail full` 获取主文献 Item Key，再逐篇执行 `zotero-cli get bibtex <item_key>`，合并写入：

```text
<NOTES_ROOT>/<分类名称>/references_codex.bib
```

写入前如果已有 `references.bib` 或 `references_codex.bib`，必须先备份为：

```text
references_codex_backup_YYYYMMDD.bib
```

## 常见问题

| 症状                                 | 处理                                                                            |
| ------------------------------------ | ------------------------------------------------------------------------------- |
| `zotero-cli config` 显示非本地模式 | 停止任务，提示用户切回`ZOTERO_LOCAL=true`；不要自行改配置，也不要改用 Web API |
| `zotero-cli library list` 读不到库 | 提示用户确认 Zotero 数据路径和本地库配置                                        |
| 语义搜索报 Chroma/HNSW 错误          | 不使用`search --mode semantic`，改用标题、作者、collection 检索               |
| 批注为空                             | 使用`get fulltext` 兜底，并在 Raw_Data_Buffer 标注来源                        |
| collection 名称不唯一                | 停止并让用户确认 collection key                                                 |

## 与其他技能集成

```text
zotero-note + academic-paper -> 在 academic-paper Phase 1 中引用 <NOTES_ROOT>/<分类>/references_codex.bib
zotero-note + obsidian-cli   -> 通过 Obsidian CLI 刷新 vault 内 Dataview 索引
```
