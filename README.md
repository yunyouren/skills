# AI 技能集合

[中文](README.md) | [English](README.en.md)

针对 Claude Code、Codex 和 GitHub Copilot CLI 平台的 AI 助手技能精选集合。

## 概览

本仓库包含可重用的技能，旨在增强 AI 编程助手的专业能力。每个技能都遵循包含 YAML frontmatter 和 Markdown 说明的标准化格式。

## 包含的技能

### [U-skill-creator](U-skill-creator/)

一个用于创建、测试和优化 AI 助手技能的元技能。它提供：

- **交互式创建** - 带有可视化进度跟踪的引导式头脑风暴
- **多平台支持** - Claude Code, Codex, GitHub Copilot CLI
- **质量验证** - YAML、内容和风格检查
- **评估系统** - 评估、基准测试、盲测对比
- **描述优化** - 迭代改进触发准确性

### [U-neural-network-coder](U-neural-network-coder/)

使用 PyTorch 构建、训练、调试和优化神经网络。功能包括：

- 支持分类、回归、序列建模和动力系统
- 包含最佳实践的训练循环模板
- 诊断和故障排除指南
- 模型导出和部署模式

### [U-matlab-simulink-coder](U-matlab-simulink-coder/)

构建、修改和调整 MATLAB/Simulink 工作流，用于：

- 控制系统设计和仿真
- 电路仿真
- 神经常微分方程（Neural-ODE）集成
- Python-MATLAB 桥接自动化

## 安装

### Claude Code

```bash
# 如果不存在技能目录，则创建
mkdir -p ~/.claude/skills

# 创建技能软链接
ln -sf "$(pwd)/U-skill-creator" ~/.claude/skills/U-skill-creator
ln -sf "$(pwd)/U-neural-network-coder" ~/.claude/skills/U-neural-network-coder
ln -sf "$(pwd)/U-matlab-simulink-coder" ~/.claude/skills/U-matlab-simulink-coder
```

### Codex

```bash
mkdir -p ~/.codex/skills
ln -sf "$(pwd)/U-skill-creator" ~/.codex/skills/U-skill-creator
ln -sf "$(pwd)/U-neural-network-coder" ~/.codex/skills/U-neural-network-coder
ln -sf "$(pwd)/U-matlab-simulink-coder" ~/.codex/skills/U-matlab-simulink-coder
```

### GitHub Copilot CLI

```bash
mkdir -p ~/.copilot/skills
ln -sf "$(pwd)/U-skill-creator" ~/.copilot/skills/U-skill-creator
ln -sf "$(pwd)/U-neural-network-coder" ~/.copilot/skills/U-neural-network-coder
ln -sf "$(pwd)/U-matlab-simulink-coder" ~/.copilot/skills/U-matlab-simulink-coder
```

## 技能结构

每个技能遵循以下结构：

```
skill-name/
├── SKILL.md              # 必需：主要技能定义
│   ├── YAML frontmatter  # 名称、描述、版本等
│   └── Markdown content  # 说明和工作流
├── scripts/              # 可选：可执行工具脚本
├── references/           # 可选：详细文档
├── agents/               # 可选：子代理配置
└── assets/               # 可选：模板和静态文件
```

## 使用方法

AI 助手会根据 frontmatter 中的 `description` 字段自动触发技能。只需用自然语言描述您的任务，相应的技能就会被激活。

提示示例：
- "Create a new skill for database migrations"（为数据库迁移创建一个新技能） → 触发 U-skill-creator
- "Build a CNN for image classification"（构建一个用于图像分类的 CNN） → 触发 U-neural-network-coder
- "Tune a PID controller in Simulink"（在 Simulink 中调整 PID 控制器） → 触发 U-matlab-simulink-coder

## 创建新技能

使用 U-skill-creator 技能来创建新技能：

```bash
# 初始化新技能
python U-skill-creator/scripts/init_skill.py my-new-skill --path ./skills

# 验证技能
python U-skill-creator/scripts/quick_validate.py ./my-new-skill
```

## 许可证

MIT License
