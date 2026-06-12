# FUSION.md — Fused Academic Writer

## 融合来源

| 来源 | 版本 | 原始职能 |
|---|---|---|
| `academic-paper` (ARS) | v3.2.0 | 12-Agent 完整论文生产流水线 |
| `nature-writing` (nature-skills) | v1.0.0 | 单 Agent 精密写作工匠工具 |

---

## 一、为什么要融合

两个技能代表了学术写作的两种方法，各自有对方不具备的优势：

**academic-paper 的优势**（广度）：
- 覆盖"只有话题"到"格式化 PDF"的全流程
- 12 个 Agent 分阶段协作，每阶段有明确定义的可交付物
- 文献检索、引用验证、模拟评审、格式转换——这些写作之外的环节一个不少

**academic-paper 的短板**：
- Phase 4（drafting）只有一个相对简单的 `writing_quality_check`——检查 AI 用词、em dash、段落长度——但没有系统化的写作方法论
- 不区分段落任务类型，没有动词-证据强度对标
- 缺少跨章节的术语一致性机制
- 没有从读者视角设计的论证顺序检查

**nature-writing 的优势**（深度）：
- 8 步写作工作流以"一句话论证"为起点，每一步有明确的单一职责
- 8 种段落任务分类（context/gap/approach/result/comparison/mechanism/implication/limitation）
- 动词-证据强度对标表（show → demonstrate → suggest → indicate → may → could）
- 无支撑绝对性措辞扫描（first/unique/unprecedented/...）
- 术语账本（跨章节术语一致性）
- 读者 5 问题序列（Relevance → Novelty → Trust → Reuse → Meaning）
- 论文类型特化的论证链和起草顺序

**nature-writing 的短板**：
- 假设用户已有 claim/evidence/boundary——不能从零开始
- 没有文献检索、引用验证、格式转换等功能
- 没有模拟评审机制
- 没有多 Agent 协作流水线

**融合的逻辑**：用 academic-paper 的流水线作为骨架，把 nature-writing 的精密切削工具嵌入到 drafting 阶段。

---

## 二、融合点详解

### 融合点 1：draft_writer_agent → draft_writer_agent_fused（核心融合）

**融合了什么**：
- 将 nature-writing 的 8 步写作工作流完整嵌入 academic-paper 的 Phase 4
- 替换原有的 `writing_quality_check` 为 nature-writing 的段落纪律体系

**为什么**：
academic-paper 的 Phase 4 原来做的事情是"按提纲逐节写草稿 + 写作质量检查"。这个质量检查只覆盖了表面问题（AI 用词、em dash 过多、段落长度单一），但没有触及写作的**结构性质量**——论证是否围绕一个核心主张、动词强度是否对标证据、每段是否只做一件事、段落内部的句子是否有显式逻辑关系。

nature-writing 的 8 步工作流从"建立一句话论证"开始，强制在写任何句子之前先理清论文的核心主张。然后逐层下钻：选架构 → 分段落任务 → 从证据向外起草 → 标定动词 → 清除绝对性措辞 → 检查段落流。这是一个从抽象到具体的精密过程。

**具体实现**：
`agents/draft_writer_agent_fused.md` 完整实现了 nature-writing 的 8 步流程，同时保留了 academic-paper 的字数追踪和学科语域调整能力。输出格式融合了双方的 output-format 规范（Draft + Section outline + Claim-evidence map + Assumptions + Why this structure）。

---

### 融合点 2：intake_agent → intake_agent_fused

**融合了什么**：
- 在 academic-paper 的 Phase 0 配置面谈中增加了 nature-writing 的 4 轴检测（paper_type / section / language / journal）
- 增加了术语账本（Terminology Ledger）的建立步骤
- 增加了 nature-writing 的 intake 要求（core claim / evidence / boundary 必须在开始前确认）

**为什么**：
academic-paper 的 intake_agent 原来收集的信息是"论文类型、学科、期刊、引用格式、输出格式、语言、字数"——这些都是**形式配置**。nature-writing 的 stance.md 要求的是**内容配置**——core claim（论证核心）、evidence（支撑证据）、boundary（边界）。

融合后的 intake_agent 在一开始就同时收集形式配置和内容配置。paper_type 轴的 5 种类型（research/methods/hypothesis/algorithmic/review）替代了 academic-paper 原有的 6 种 paper structure patterns，因为前者不仅提供结构模板，还提供**类型特化的论证链**和**起草顺序**——例如 research paper 的论证链是 `field-scale need → unresolved bottleneck → proposed move → decisive evidence → broader implication → boundary`，起草顺序是 Results → Introduction → Title → Discussion → Methods → Abstract。

---

### 融合点 3：structure_architect_agent → structure_architect_agent_fused

**融合了什么**：
- 在提纲设计阶段引入 nature-writing 的段落任务映射
- 每段标注其 8 种段落任务类型之一

**为什么**：
academic-paper 的 structure_architect 原来产出的是"章节标题 + 段落数 + 字数 + 证据映射"。nature-writing 要求每个段落只做一件事（context/gap/approach/result/comparison/mechanism/implication/limitation）。在提纲阶段就为每段分配任务类型，可以防止 drafting 阶段出现一个段落承载两个任务的常见问题。

---

### 融合点 4：peer_reviewer_agent（增强，不重命名）

**融合了什么**：
- 在 Phase 6 的模拟评审之后，增加 nature-writing 的 paper self-review 审计
- 使用 `references/paper-review.md` 中的拒稿风险清单和 end-of-paper 自查问题列表

**为什么**：
academic-paper 的 peer_reviewer 做的是模拟外部评审（5 维度评分）。nature-writing 的 paper-review.md 做的是内部自查——从 contribution、writing clarity、empirical effect、evaluation completeness、method design 五个拒稿维度逐项检查。两者互补：外部评审看"别人会怎么挑毛病"，内部自查看"我自己能不能先修好"。

---

### 融合点 5：读者 5 问题序列（跨阶段质量标准）

**融合了什么**：
- 将 `_shared/core/reader-workflow.md` 的读者 5 问题序列（Relevance → Novelty → Trust → Reuse → Meaning）作为贯穿所有写作阶段的质量锚点

**为什么**：
academic-paper 没有从读者视角出发的论证顺序检查。读者 5 问题序列提供了一个稳定的框架——无论哪个阶段产出的文本，最终都应该帮助读者按这个顺序回答五个问题。这特别适用于 Phase 4 drafting 和 Phase 6 review 之间的自我检查。

---

### 融合点 6：静态片段路由系统（新增能力）

**融合了什么**：
- 将 nature-writing 的 `manifest.yaml` + `static/` 片段系统完整引入
- 当用户请求起草特定章节时，通过 4 轴检测按需加载匹配的片段

**为什么**：
academic-paper 的 10 种模式覆盖了完整的论文工作流场景，但没有"我只想写引言"或"我的论文是 methods 类型"这样的精细化控制。nature-writing 的片段路由系统允许按 paper_type/section/language/journal 四个轴动态组合写作指导，每次只加载相关的片段，不浪费上下文。

---

## 三、融合后的工作流

```
用户请求
    │
    ├── "Write a full paper on [topic]" 或 "寫一篇論文"
    │   → full 模式：走 8 阶段流水线
    │   → Phase 0 使用 intake_agent_fused（轴检测 + 术语账本 + 内容配置）
    │   → Phase 2 使用 structure_architect_agent_fused（段落任务映射）
    │   → Phase 4 使用 draft_writer_agent_fused（8 步精密起草）
    │   → Phase 6 增强 self-review audit
    │
    ├── "Draft the introduction for my paper. Here are results: [data]"
    │   → 4 轴检测（paper_type=research, section=intro, language=en, journal=generic）
    │   → 加载 static/fragments/paper_type/research.md + section/intro.md + language/en.md + journal/generic.md
    │   → 跑 8 步工作流起草引言
    │
    ├── "Just need a plan" → plan mode
    ├── "Check my citations" → citation-check mode
    ├── "Reviewer comments received" → revision / revision-coach mode
    └── ...
```

---

## 四、文件清单

### 融合后新增/修改的文件

| 文件 | 类型 | 说明 |
|---|---|---|
| `SKILL.md` | 新建 | 融合路由器 |
| `FUSION.md` | 新建 | 本文件——融合文档 |
| `agents/intake_agent_fused.md` | 增强 | 融合 Phase 0 |
| `agents/structure_architect_agent_fused.md` | 增强 | 融合 Phase 2 |
| `agents/draft_writer_agent_fused.md` | 增强 | 融合 Phase 4（核心融合） |

### 从 academic-paper 继承的文件（未修改）

`agents/` 中除上述外的所有文件、`references/` 中 academic-paper 原有的 19 个文件、所有 `templates/` 文件、所有 `examples/` 文件。

### 从 nature-writing 引入的文件

`static/` 全部、`_shared/` 全部、`manifest.yaml`、`references/paper-review.md`、`references/abstract.md`、`references/paragraph-flow.md`、`references/examples/` 全部。
