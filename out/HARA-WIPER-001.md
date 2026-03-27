---
doc_id: HARA-WIPER-001
title: 雨刮器系统（Wiper System）HARA（危害分析与风险评估）
work_product_type: hara
iso_ref:
  - ISO 26262-3
asil: 待定
status: Draft
owner: 系统安全团队（待定）
reviewers:
version: v0.1
baseline: 未基线
last_updated: 2026-03-27
---
# Change History（变更历史）

## Document Change History（文档履历）

| Version | Status | Author | Date | Approver | Approve Date | Description |
|---|---|---|---|---|---|---|
| v0.1 |  | AI Assistant | 2026-03-27 |  |  | 创建雨刮器系统 HARA 草案 |

## Template Change History（文档模板履历）

| Version | Status | Author | Date | Approver | Approve Date | Description |
|---|---|---|---|---|---|---|

# 1. General Information（一般信息）

## 1.1 Document Purpose（文档目的）

基于雨刮器系统 Item Definition，在概念阶段识别危害事件并进行风险评估（S/E/C），提出安全目标（SG）并形成向 FSC 的追溯输入。

## 1.2 Document Scope（文档范围）

系统/功能边界：
- 覆盖雨刮控制逻辑、自动雨刮（若配备）、故障检测与降级提示
- 覆盖 malfunction 引发的危害事件；对传感器性能边界与误用风险在 SOTIF 中补充
V 模型阶段：
- 概念

## 1.3 Input Document（输入文档）

| Document No. | File name | Version |
|---|---|---|
| ITEM-WIPER-001 | 雨刮器系统 Item Definition | v0.1 |

## 1.4 References（参考文档）

| Document No. | File name | Version |
|---|---|---|

# 2. Terms and Abbreviations（术语与缩略语）

## 2.1 Terms（术语）

| Term | Definition | Source |
|---|---|---|

## 2.2 Abbreviations（缩略语）

| Term | Definition |
|---|---|

# 6. 正文内容（Main Content）

## 6.1 分析范围

- 关联 Item：ITEM-WIPER-001
- 分析边界：
  - 雨刮停止/速度不足等失效对驾驶视野的影响
  - 自动雨刮（若配备）异常导致的视野与驾驶员分心风险（malfunction 维度）
- 不覆盖范围：
  - 机械结构可靠性详细分析（在系统/硬件阶段展开）
  - 纯性能不足/使用不当风险（SOTIF 另行分析）

## 6.2 场景与危害事件识别

| HE-ID | 运行场景 | malfunction（功能异常） | 危害事件 | 潜在后果 |
|---|---|---|---|---|
| HE-WIPER-001 | 高速强降雨，驾驶员依赖雨刮维持视野 | 雨刮停止或速度不足（控制失效/堵转/供电异常），未及时检测或提示不足 | 驾驶员前向视野显著受限，无法及时识别前方风险 | 偏离车道/追尾/碰撞等事故风险上升 |
| HE-WIPER-002 | 夜间大雨/眩光环境，视野需求更高 | 雨刮失效导致视野受限，且告警不明确或延迟 | 驾驶员反应不足，发生碰撞风险上升 | 伤害风险上升 |
| HE-WIPER-003 | 自动雨刮模式下，雾/毛毛雨/飞溅等边界工况 | 自动雨刮不触发或触发不足（功能失效） | 视野逐步恶化，驾驶员未及时介入 | 事故风险上升（需与 SOTIF 边界澄清） |
| HE-WIPER-004 | 自动雨刮误触发频繁（干刮/误判） | 自动雨刮误触发导致驾驶员分心或操作干预不当 | 驾驶员注意力被干扰，在复杂交通中发生风险 | 可控性下降与事故风险上升（与 SOTIF 边界相关） |

## 6.3 风险评估与 ASIL 判定

| HE-ID | S | E | C | ASIL | 判定依据简述 |
|---|---|---|---|---|---|
| HE-WIPER-001 | 待定 | 待定 | 待定 | 待定 | 需结合高速暴露度与驾驶员在强降雨视野受限时的可控性数据确定 |
| HE-WIPER-002 | 待定 | 待定 | 待定 | 待定 | 夜间强降雨与眩光可能提高严重度与可控性难度 |
| HE-WIPER-003 | 待定 | 待定 | 待定 | 待定 | 与功能边界与驾驶员介入行为相关，需澄清 ISO 26262 / SOTIF 分工 |
| HE-WIPER-004 | 待定 | 待定 | 待定 | 待定 | 误触发带来的驾驶员分心与操作后果需数据支持 |

## 6.4 安全目标（Safety Goals）

| SG-ID | 安全目标描述 | 来源 HE-ID | ASIL | 安全状态（Safe State） |
|---|---|---|---|---|
| SG-WIPER-001 | 系统应在雨刮失效（停止/速度不足）时及时检测并向驾驶员提供明确提示，使驾驶员能够采取补救措施以维持安全驾驶。 | HE-WIPER-001 | 待定 | 提示驾驶员降低车速/靠边停车或切换手动模式（按项目定义） |
| SG-WIPER-002 | 系统应避免自动雨刮失效导致视野长期恶化；在自动模式不可用或置信度不足时应提示并引导驾驶员介入。 | HE-WIPER-003 | 待定 | 退出自动模式并提示驾驶员手动控制（待定） |
| SG-WIPER-003 | 系统应避免自动雨刮高频误触发造成驾驶员干扰；误触发检测与降级策略需可控且可解释（与 SOTIF 分工明确）。 | HE-WIPER-004 | 待定 | 降级自动模式/提示检查传感器并允许驾驶员手动接管（待定） |

## 6.5 假设、限制与边界条件

| 类型 | ID | 内容 | 影响分析 |
|---|---|---|---|
| 假设 | ASM-WIPER-HARA-001 | 驾驶员能理解故障提示并采取减速/停车等补救 | 影响可控性 C 判定 |
| 限制 | LIM-WIPER-HARA-001 | HARA 仅覆盖 malfunction 引发的危害事件；自动雨刮性能边界与误用风险在 SOTIF 中补充 | 需建立对应 SOTIF 工作成果并与安全目标边界对齐 |

## 6.6 向下游分配与追溯

| SG-ID | 分配目标（FSC/FSR） | 接收方 | 验证方法 | 证据 ID |
|---|---|---|---|---|
| SG-WIPER-001 | FSC/FSR（待建） | FSC-WIPER-001 | 分析/评审/测试 | 待定 |
| SG-WIPER-002 | FSC/FSR（待建） | FSC-WIPER-001 | 分析/评审/测试 | 待定 |

# 7. 可追溯性（Traceability）

| 条目 ID | 上游输入（父级） | 下游分解（子级） | 验证方法 | 证据 ID |
|---|---|---|---|---|
| HARA-WIPER-001 | ITEM-WIPER-001 | FSC-WIPER-001（待建） | 评审 | SYS-REV-WIPER-HARA-001（计划） |

# 8. 待验证项（Open Verification Items）

| OVI ID | 待验证项 | 责任人 | 截止日期 | 状态 |
|---|---|---|---|---|
| OVI-WIPER-HARA-001 | 高速强降雨/夜间等关键场景的暴露度（E）与驾驶员可控性（C）数据 | 待定 | 待定 | Open |
| OVI-WIPER-HARA-002 | 自动雨刮相关风险的 ISO 26262 / SOTIF 边界划分与记录策略 | 待定 | 待定 | Open |

# 9. 评审与批准（Review and Approval）

| 角色 | 姓名 | 结论 | 日期 |
|---|---|---|---|
| 作者 | 系统安全工程师（待定） | N/A | 2026-03-27 |
| 评审者 | 功能安全工程师（待定） | 待填写 | 待填写 |
| 批准者 | 功能安全经理（待定） | 待填写 | 待填写 |

# 10. 变更记录（Change History）

| 版本 | 日期 | 变更摘要 | 变更原因 | 作者 |
|---|---|---|---|---|
| v0.1 | 2026-03-27 | 创建雨刮器系统 HARA 草案 | 概念阶段初始化 | AI Assistant |

# 11. 备注与边界声明

- 本 HARA 为草案：S/E/C 与 ASIL 定级依赖场景假设与驾驶员行为数据，需项目数据验证后冻结。
