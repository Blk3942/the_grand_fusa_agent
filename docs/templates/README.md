# 文档模板目录（Templates）

本目录用于管理 FuSa 文档模板，采用“基础模板 + 个性模板”的模块化结构：

- 基础模板：适用于所有工作成果（work products）
- 个性模板：面向具体工作成果（如 Item Definition、HARA、FSC）

---

## 目录结构

- `_base/`：通用模板与通用章节骨架
- `work-products/`：各工作成果的专用模板
- `schemas/`：文档元数据与结构规则（供校验脚本使用）
- `styles/`：Excel/Word 输出样式配置与 Word 母版

---

## 折中方案（高稳健）：单一真源 → 多格式输出

当部分工作成果更适合用 Excel/Word 交付时，推荐使用“结构化单一真源（YAML）”作为唯一内容来源：

- **单一真源（YAML）**：`data/work-products/**/<DOC-ID>.yaml`（人工维护，不当作渲染临时目录）
- **可评审版本（MD）**：由脚本生成到 `out/`，便于 Git diff 与评审
- **交付版本（DOCX/XLSX）**：由脚本生成到 **`out/`**（仓库根目录下唯一约定导出根路径；默认 `--out-dir out`）

为避免二进制模板（`.docx/.xlsx`）进仓库造成 diff/合并困难，本项目使用**文本化模板规范（YAML）**：

- Word 基础模板规范：`_base/base.word.yaml`
- Excel 基础模板规范：`_base/base.excel.yaml`
- 工作成果输出格式约束：`work-products/formats.yaml`

运行方式（项目根目录）：

- 安装依赖：`python -m pip install -r requirements.txt`
- 校验 YAML：`python scripts/validate_fusa_yaml.py`
- 初始化 Word 母版（可选）：`python scripts/init_word_master_template.py`
- 生成多格式：
  - 指定输出格式：`python scripts/render_from_yaml.py --input data/work-products/concept/item-definition/ITEM-DMS-001.yaml --out-dir out --formats md,docx`
  - 不指定输出格式（按 `work_product_type` 默认）：`python scripts/render_from_yaml.py --input data/work-products/concept/item-definition/ITEM-DMS-001.yaml --out-dir out`
  - **默认输出目录**：`--out-dir/<doc_id>/` 下放 `*.md` / `*.docx` / `*.xlsx`，并在同目录 `uml/` 中生成 `.mmd` 与渲染后的 `.png`，Markdown 内嵌相对路径引用图片。
  - **扁平输出（旧布局）**：加 `--flat-output` 时，文档在 `--out-dir` 根目录，图表在 `uml/<doc_id>/`，避免多文档文件名冲突。
  - **UML**：在 YAML `content.diagrams` 中配置 `mermaid` 多行文本或 `source_mmd`（相对仓库根）；`placement` 控制插入位置（如 Item Definition 的 `item_architecture`、HARA 文末 `main_end`）。渲染由 `scripts/render_mermaid.py` 完成（`npx @mermaid-js/mermaid-cli`、全局 `mmdc` 或 Kroki；可选 `--offline-demo` 生成 matplotlib 示意 PNG）。
  - **Item Definition 正文字段**（与 `work-products/item-definition/template.md` 对齐）：`driving_automation`、`odd`、`vehicle_safety_strategy`、`alerts_degradation`、`function_partition`（子功能表）、`use_cases`（多用例块；未提供时回退为 `operating_scenarios` 场景表）、`functional_runtime_state`（`states`/`transitions` 表）、`foreseeable_misuse`（结构化表）、`non_functional`、`dependency_*`、`implementation.architecture_elements` / `interfaces_brief`（简表；缺省则要素回退为 in/out scope、接口回退为详细 IF 表）等。详见示例 `data/work-products/concept/item-definition/ITEM-DMS-001.yaml`。旧字段 `vehicle_safety_strategy.misuse_hmi` / `fault_handling` 已不再输出到 MD/DOCX（若仍写在 YAML 中仅作备查，请并入其他段落或删除）。

样式维护建议：

- Excel 样式统一维护在 `styles/excel.styles.yaml`
- Word 样式与母版路径维护在 `styles/word.styles.yaml`
- 需要更复杂 Word 版式时，优先编辑 `styles/word.master-template.docx`

---

## 使用约定

1. 新建文档时，先复制 `_base/base-template.md` 作为骨架。
2. 再将 `work-products/<type>/template.md` 的“个性章节”填入骨架正文。
3. 不得删除基础骨架中的共性章节（输入与参考、标准要求、假设、追溯、待验证项、评审批准、变更记录）。
4. 文档需保留可追溯字段（上游输入、下游输出、验证证据）。
5. 提交前运行结构校验脚本，防止漏填基础章节。

## 最小合规检查（模板装配后）

- [ ] 含文档头元数据（`doc_id`、`status`、`version`、`owner`）
- [ ] 含“标准要求”与“项目假设”章节
- [ ] 含“可追溯性”与“待验证项（OVI）”章节
- [ ] 含“评审与批准”与“变更记录”章节

---

## 自动校验（高稳健）

规则文件：

- `schemas/document-meta.schema.json`：front matter 字段规范
- `schemas/document-structure-rules.json`：章节与工作成果关键词规则

运行方式（项目根目录）：

- `python scripts/validate_fusa_docs.py`（默认扫描 `out/` 下已生成的 Markdown）
- 指定单文件示例：`python scripts/validate_fusa_docs.py --target out/ITEM-DMS-001/ITEM-DMS-001.md`

校验目标：

- front matter 必填字段完整
- 基础章节（H1）完整
- 按 `work_product_type` 检查专属内容关键词

---

## 命名建议

- 文档 ID：`<类型前缀>-<编号>`，例如 `HARA-001`、`FSC-003`
- 版本：`v主版本.次版本`，例如 `v1.0`
- 状态：`Draft / In Review / Approved / Obsolete`
