# The Grand FuSa Agent — 关键文件使用说明与注意事项

本文说明仓库内 **Rules、Skills、协作文档** 的用途、修改方式与常见风险。建议新成员与配置 Agent 前完整阅读一遍。

---

## 1. 总览

| 文件/目录 | 作用 | 主要读者 |
|-----------|------|----------|
| [`AGENTS.md`](../AGENTS.md) | 仓库级行为约定（术语、结论边界、可追溯性） | 人类协作者 + Cursor Agent |
| [`.cursor/rules/*.mdc`](../.cursor/rules/) | Cursor 注入的**规则**（约束写法与领域习惯） | Cursor |
| [`.cursor/skills/automotive-functional-safety/`](../.cursor/skills/automotive-functional-safety/) | 领域 **Skill**（工作流与参考） | Cursor |
| [`README.md`](../README.md) | 项目简介与目录说明 | 所有人 |

---

## 2. Cursor Rules（`.cursor/rules/`）

### 2.1 文件列表

| 文件 | 生效范围 | 用途摘要 |
|------|----------|----------|
| `fusa-domain.mdc` | `alwaysApply: true` | 功能安全表述、结论保守、术语、中英文习惯 |
| `python-agent.mdc` | `globs: **/*.py` | Python 风格、密钥与路径、与 FuSa 工具相关的日志与数据结构提示 |

### 2.2 使用说明

- Rules 为 **Markdown + YAML frontmatter** 的 `.mdc` 文件。
- **`alwaysApply: true`**：在多数对话中会被附带；内容应**短而稳**，只放真正全局适用的约束。
- **`globs`**：仅在与匹配文件相关的上下文中附带；适合语言/技术栈专用约定。
- 修改后一般**立即**作用于后续对话；若 Cursor 版本支持规则缓存，可尝试重新打开项目或重启 Cursor。

### 2.3 注意事项

1. **不要**在 Rules 中粘贴机密客户数据或真实 VIN、零件号样本。
2. **避免单文件过长**（建议单条规则保持精炼，复杂流程放在 Skill）。
3. 新增规则时检查 **frontmatter 语法**（YAML 冒号后空格、`globs` 引号等），错误可能导致规则不加载。
4. Rules 是「约束与习惯」，**不能**替代组织内的安全计划、模板与签字流程。

---

## 3. Cursor Skills（`.cursor/skills/automotive-functional-safety/`）

### 3.1 文件列表

| 文件 | 用途 |
|------|------|
| `SKILL.md` | **必选**：`name`、`description`（触发发现）+ 工作流速查与输出模板 |
| `reference.md` | **可选**：Part 结构、ASIL/SOTIF 边界、误区、可追溯字段建议 |
| `examples.md` | **可选**：典型问答的推荐结构与反例（避免过度承诺） |

### 3.2 使用说明

- Skill 以**目录**形式存在，核心为 `SKILL.md`。
- **`description` 字段极其重要**：应用第三人称，写清 **做什么（WHAT）** 与 **何时启用（WHEN）**，并包含触发关键词（如 ASIL、HARA、FSC、ISO 26262）。
- 详细长文放在 `reference.md`，在 `SKILL.md` 中用链接引用，减少常驻上下文体积。
- 个人全局技能可放在用户目录下的 `~/.cursor/skills/`；**本仓库技能**放在项目 `.cursor/skills/` 便于团队共享。

### 3.3 注意事项

1. **勿**在 `~/.cursor/skills-cursor/` 下创建自定义技能（该目录为 Cursor 内置保留）。
2. 更新标准理解时，同步修订 `reference.md`，并在 `SKILL.md` 中避免与标准正文**矛盾**；不确定处写明「以组织采用的版本为准」。
3. Skill 给出的是**结构与检查项**，认证结论必须由项目证据与有资质的角色裁定。
4. 链接引用保持 **一层深度**（`SKILL.md` → `reference.md`），避免多层嵌套导致模型未完整读取。

---

## 4. `AGENTS.md`

### 4.1 用途

- 与 Cursor **Agent 模式**及人工协作对齐：领域边界、输出语言、安全相关代码习惯。
- 与 Rules 互补：`AGENTS.md` 偏**仓库级说明**；Rules 偏**可机读约束**。

### 4.2 注意事项

- 修改 `AGENTS.md` 后，建议在 `README.md` 或本文档中若有关联说明一并更新。
- 若团队使用多种 IDE，可将相同原则摘要复制到内部 Wiki，避免仅依赖 Cursor。

---

## 5. 运行时代码与配置（占位）

| 路径 | 说明 |
|------|------|
| `config/env.example` | 环境变量模板；复制为 `.env` 后本地填写，**勿提交** `.env` |
| `src/the_grand_fusa_agent/` | Python 包占位，可扩展为 API 客户端、编排、RAG 管道等 |
| `requirements.txt` | 最小依赖；按实际集成增补 |

### 注意事项

- 任何连接大模型 API 的实现须遵守公司 **AUP、数据出境、日志留存** 政策。
- 若处理客户文档，默认假设为**保密信息**，不得发往未授权模型或日志系统。

---

## 6. 维护建议（Checklist）

- [ ] 标准升版或组织模板变更后：更新 `reference.md` 与相关 Rules 中的表述。
- [ ] 新增工具脚本：检查 `python-agent.mdc` 是否需补充约定。
- [ ] 季度回顾：`description` 是否仍能覆盖团队真实提问方式（触发词是否够）。

---

## 7. 免责声明

仓库内文档与 AI 生成内容用于**辅助学习与工程起草**，不构成法律咨询、认证承诺或事故责任判断依据。
