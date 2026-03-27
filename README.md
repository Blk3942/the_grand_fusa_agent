# The Grand FuSa Agent

专注于**汽车功能安全（FuSa）**的 AI Agent 项目骨架，适用于在 Cursor 中开发、并对接大模型 API 构建运行时 Agent。

## 目标

- 支撑 **ISO 26262** 相关概念澄清、工作项拆解、检查清单与文档结构建议。
- 通过 **Rules** 固定工程与表达习惯，通过 **Skills** 注入可复用的领域工作流与参考知识。

## 目录结构

```
The_Grand_FuSa_Agent/
├── AGENTS.md                 # 协作者/Agent 行为约定
├── README.md
├── docs/
│   └── USAGE_AND_NOTES.md    # 关键文件使用说明与注意事项（必读）
├── .cursor/
│   ├── rules/                # Cursor 规则（.mdc）
│   └── skills/
│       └── automotive-functional-safety/   # SKILL.md、reference、examples
├── config/
│   └── env.example           # 环境变量示例（复制为 .env 后填写）
├── src/the_grand_fusa_agent/ # 运行时代码占位
└── requirements.txt
```

## 快速开始

1. 阅读 [`docs/USAGE_AND_NOTES.md`](docs/USAGE_AND_NOTES.md)。
2. 在 Cursor 中打开本文件夹；规则与项目技能会自动参与上下文（视 Cursor 版本与设置而定）。
3. 若开发可执行 Agent：复制 `config/env.example` 为 `.env` 并填入 API 密钥；创建虚拟环境后 `pip install -r requirements.txt`。

## 免责声明

本仓库中的说明与生成内容**不构成**正式的安全评估、认证或法律责任依据。量产与认证请以 OEM/Tier1 流程及具备资质的审核为准。
