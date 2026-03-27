# Refs Index（引用索引）

本目录用于管理“白皮书 / 论文 / 标准解读 / 最佳实践”等参考资料（refs），并通过统一的索引格式支持：

- 按**主题/关键词**快速定位材料
- 在回答中提供**可追溯引用**（文档名、版本、章节/页码/段落）
- 控制上下文体积：只在需要时引入**命中摘录**，而不是整篇原文

> 注意：把资料文件放在仓库里不等于会自动进入大模型上下文；只有“被引用/被摘录/被检索命中并注入”的段落才会消耗 token。

---

## 1. 索引条目格式（建议保持简短可检索）

每条 ref 建议包含以下字段（用项目内可读的“YAML 风格条目”即可，不要求严格 YAML 解析）：

- `id`：引用 ID（建议唯一、稳定）
- `title`：文档标题
- `publisher`：机构/期刊/组织（或作者）
- `year`：年份
- `type`：`standard | whitepaper | paper | guideline | blog | internal`
- `topic`：主题标签（数组）
- `keywords`：关键词（数组）
- `source`：来源定位（优先文件路径；或链接）
- `locator`：章节/页码/段落号/图表号（越精确越好）
- `summary`：一句话摘要（用于检索与筛选）
- `quote_hint`：建议摘录的关键句/段落范围（可选）
- `status`：`ready | placeholder | deprecated`

---

## 2. 引用 ID 命名建议

- `REF-ISO26262-P3-HARA-...`
- `REF-ISO21448-SOTIF-...`
- `REF-PAPER-<FirstAuthor>-<Year>-<Keyword>`
- `REF-WHITEPAPER-<Org>-<Year>-<Keyword>`

---

## 3. Refs 条目（示例 + 占位）

> 说明：本仓库目前未内置标准/论文 PDF 原文；以下条目包含“可立即用的项目内参考文件”，以及“可按需补齐的占位条目”。

### 3.1 项目内参考（可直接引用）

- id: REF-PROJ-FUSA-REFERENCE
  title: ISO 26262 与 FuSa — 参考摘录（非正式培训教材）
  publisher: The Grand FuSa Agent（项目内）
  year: 2026
  type: internal
  topic: [ISO26262, FuSa, HARA, ASIL, SOTIF, traceability]
  keywords: [Part结构, S/E/C, ASIL分解, SOTIF边界, 可追溯性]
  source: `.cursor/skills/automotive-functional-safety/reference.md`
  locator: 全文（按小节引用）
  summary: 项目内 FuSa 速查与常见误区，适合作为回答的“结构与提醒”参考。
  status: ready

- id: REF-PROJ-FUSA-EXAMPLES
  title: FuSa 问答结构示例
  publisher: The Grand FuSa Agent（项目内）
  year: 2026
  type: internal
  topic: [FuSa, answer-structure]
  keywords: [输出结构, 反例, 结论边界]
  source: `.cursor/skills/automotive-functional-safety/examples.md`
  locator: 全文（按示例段落引用）
  summary: 用于约束回答形状（结构化、保守结论、避免过度承诺）。
  status: ready

### 3.2 标准/白皮书/论文（占位：建议你补齐文件或链接）

- id: REF-ISO26262-ED2
  title: ISO 26262: Road vehicles — Functional safety（Edition 2）
  publisher: ISO
  year: 2018
  type: standard
  topic: [ISO26262, FuSa]
  keywords: [HARA, FSC, TSC, safety requirements, confirmation]
  source: （请补齐：例如 `docs/refs/sources/ISO26262-2018.pdf` 或组织内受控链接）
  locator: （按需填：Part/Clause/Page）
  summary: 功能安全核心标准，涉及概念阶段到验证确认的全过程要求与指南。
  status: placeholder

- id: REF-ISO21448
  title: ISO 21448: Road vehicles — Safety of the intended functionality（SOTIF）
  publisher: ISO
  year: 2022
  type: standard
  topic: [ISO21448, SOTIF]
  keywords: [misuse, performance limitations, triggering conditions]
  source: （请补齐：例如 `docs/refs/sources/ISO21448.pdf` 或组织内受控链接）
  locator: （按需填：Clause/Page）
  summary: 预期功能安全，覆盖无故障情况下的性能局限与误用风险分析。
  status: placeholder

