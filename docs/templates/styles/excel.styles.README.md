# `excel.styles.yaml` 填写说明

本说明用于指导如何填写 `docs/templates/styles/excel.styles.yaml`，以统一所有导出 `.xlsx` 的字体、对齐与封面样式。

> 适用范围：由 `scripts/render_from_yaml.py` 生成的所有 Excel 输出（如 HARA 的 `*.xlsx`）。

---

## 1. 文件结构总览

`excel.styles.yaml` 的顶层结构：

- `version`: 样式配置版本号（建议与项目模板版本一起维护）
- `workbook`: 工作簿全局默认样式
- `cover`: `Sheet: Cover` 的“真正封面页”样式
- `table`: 所有表格（含 key/value sheet 的表格部分与各 table sheet）的表头/表体样式

---

## 2. `workbook`（全局默认）

```yaml
workbook:
  default_font:
    name: Calibri
    size: 11
    bold: false
  default_alignment:
    horizontal: left
    vertical: center
    wrap_text: true
  column_auto_fit:
    enabled: true
    min_width: 10
    max_width: 60
    padding: 2
```

- **`default_font`**：默认字体设置
  - **`name`**：字体名（如 `Calibri`、`Arial`、`Microsoft YaHei`）
  - **`size`**：字号（数字）
  - **`bold`**：是否加粗（`true/false`）
- **`default_alignment`**：默认对齐
  - **`horizontal`**：`left/center/right`
  - **`vertical`**：`top/center/bottom`
  - **`wrap_text`**：是否自动换行（`true/false`）
- **`column_auto_fit`**：列宽自适应（方案 1：按文本长度近似计算）
  - **`enabled`**：是否启用（`true/false`）
  - **`min_width`**：最小列宽
  - **`max_width`**：最大列宽（避免长文本撑爆）
  - **`padding`**：额外留白（字符数）

说明：
- 当前渲染器主要对 **封面与表格区域** 应用显式样式；`workbook.default_*` 更像“默认值池”，便于未来扩展统一应用。
 - 列宽自适应会对除 `Cover` 外的所有 sheet 生效。

---

## 3. `cover`（封面页）

```yaml
cover:
  merge_range: A2:H6
  font:
    name: Calibri
    size: 24
    bold: true
  alignment:
    horizontal: center
    vertical: center
    wrap_text: true
  hide_grid_lines: true
  column_width: 18
  row_height: 28
```

字段说明：
- **`merge_range`**：合并单元格范围，用于放置大标题（必须是 Excel 范围字符串）
  - 常用：`A2:H6`（更“居中”且留白更足）
- **`font`**：封面标题字体
  - 建议字号：18–32
- **`alignment`**：封面标题对齐
  - 建议：`horizontal: center`、`vertical: center`、`wrap_text: true`
- **`hide_grid_lines`**：是否隐藏网格线（建议 `true`）
- **`column_width`**：封面页 A–H 列统一列宽（数字）
- **`row_height`**：封面页前几行统一行高（数字）

注意：
- 封面内容目前只使用 `meta.title`（按你当前规则：Cover 只保留 title）。

---

## 4. `table`（表格样式）

```yaml
table:
  header:
    font:
      name: Calibri
      size: 11
      bold: true
    alignment:
      horizontal: center
      vertical: center
      wrap_text: true
    border:
      style: thin
      color: "000000"
  body:
    font:
      name: Calibri
      size: 11
      bold: false
    alignment:
      horizontal: left
      vertical: center
      wrap_text: true
    border:
      style: thin
      color: "000000"

  outline:
    enabled: true
    style: medium
    color: "000000"
```

字段说明：
- **`header`**：表头行样式（第一行）
- **`body`**：表体样式（从第二行开始）
- **`header.border` / `body.border`**：单元格边框样式（对每个单元格四边生效）
  - **`style`**：线型（常用：`thin`、`medium`、`thick`、`dashed`、`dotted`）
  - **`color`**：RGB 十六进制字符串（不带 `#`），例如黑色 `"000000"`
- **`outline`**：表格外框（可选）
  - **`enabled`**：是否启用外框（`true/false`）
  - **`style`**：外框线型（推荐 `medium`）
  - **`color`**：外框颜色（例如 `"000000"`）

推荐实践：
- 表头：居中 + 加粗
- 表体：左对齐 + 自动换行（便于长文本）
- 边框：表头/表体用 `thin`，外框用 `medium` 便于区分表格边界

---

## 5. 常见填写示例

### 5.1 统一为微软雅黑（更适合中文）

```yaml
cover:
  font:
    name: Microsoft YaHei
    size: 24
    bold: true

table:
  header:
    font:
      name: Microsoft YaHei
      size: 11
      bold: true
  body:
    font:
      name: Microsoft YaHei
      size: 11
      bold: false
```

### 5.2 表体改为顶端对齐（更适合多行文本）

```yaml
table:
  body:
    alignment:
      vertical: top
      wrap_text: true
```

### 5.3 边框：表格细边框 + 外框加粗

```yaml
table:
  header:
    border:
      style: thin
      color: "000000"
  body:
    border:
      style: thin
      color: "000000"
  outline:
    enabled: true
    style: medium
    color: "000000"
```

---

## 6. 生效方式

修改 `excel.styles.yaml` 后，重新生成任意 Excel 输出即可生效，例如：

```bash
python scripts/render_from_yaml.py --input data/work-products/concept/hara/HARA-DMS-001.yaml --out-dir out
```

如果你同时修改了基础模板说明（`base-template.excel.md`），建议先运行：

```bash
python scripts/sync_base_templates.py
```

