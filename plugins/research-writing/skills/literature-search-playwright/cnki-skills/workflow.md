# CNKI Skills for Codex

基于 [cookjohn/cnki-skills](https://github.com/cookjohn/cnki-skills) 的 CNKI 知网文献工具包，已适配 Codex。

## 技能清单（9 个子技能）

| 技能 | 功能 | 触发方式 |
|------|------|----------|
| read `skills/cnki-search/workflow.md` | 关键词搜索，返回结构化结果 | 在知网搜... / CNKI search... |
| read `skills/cnki-advanced-search/workflow.md` | 高级搜索：作者、期刊、时间范围、来源类别(SCI/EI/CSSCI/北大核心) | 高级搜索... |
| read `skills/cnki-parse-results/workflow.md` | 解析当前搜索结果页 | 自动调用 |
| read `skills/cnki-navigate-pages/workflow.md` | 翻页与排序 | 下一页 / 按引用排序 |
| read `skills/cnki-paper-detail/workflow.md` | 提取论文完整信息（摘要、关键词等） | 查看这篇论文详情 |
| read `skills/cnki-journal-search/workflow.md` | 按名称/ISSN/CN 查找期刊 | 帮我找《XX》期刊 |
| read `skills/cnki-journal-index/workflow.md` | 查询期刊收录情况和影响因子 | XX期刊是什么级别 |
| read `skills/cnki-journal-toc/workflow.md` | 浏览期刊目录 | 看XX期刊2025年第1期 |
| read `skills/cnki-export/workflow.md` | 导出引用到 Zotero 或输出 GB/T 7714 | 导出到 Zotero |

## Agent

cnki-researcher — 统一调度全部 9 个技能，自动处理验证码检测。

## 预筛选期刊列表

cnki-journals.txt — 保留了你原有的 124 种 FMS Tier 1 & 2 中文期刊。在高级搜索中可以按这些期刊逐刊检索。

## 与 literature-search 的集成

literature-search 技能的 CNKI 部分已更新为指向此技能包。中文关键词自动路由到 CNKI。

## 前置条件

- Chrome 浏览器（手动完成知网 IP 登录）
- Zotero 桌面端（导出功能需要）
