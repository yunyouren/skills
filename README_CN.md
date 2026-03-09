# AI 技能集合

适用于 Claude Code、Codex 和 GitHub Copilot CLI 平台的 AI 助手技能合集。

## 概述

本仓库包含可复用的技能，用于增强 AI 编码助手的专项能力。每个技能都遵循标准化格式，包含 YAML 前置配置和 Markdown 指令。

## 包含技能

### [U-skill-creator](U-skill-creator/)

用于创建、测试和优化 AI 助手技能的元技能。功能包括：

- **交互式创建** - 可视化进度跟踪的引导式头脑风暴
- **多平台支持** - Claude Code、Codex、GitHub Copilot CLI
- **质量验证** - YAML、内容和风格检查
- **评估系统** - 测试、基准测试、盲审对比
- **描述优化** - 迭代式触发准确性改进

### [U-neural-network-coder](U-neural-network-coder/)

使用 PyTorch 构建、训练、调试和优化神经网络。支持：

- 分类、回归、序列建模和动力系统
- 训练循环模板与最佳实践
- 诊断与故障排除指南
- 模型导出与部署模式

### [U-matlab-simulink-coder](U-matlab-simulink-coder/)

构建、修改和调优 MATLAB/Simulink 工作流，适用于：

- 控制系统设计与仿真
- 电路仿真
- 神经网络 ODE 集成
- Python-MATLAB 桥接自动化

## 安装

### Claude Code

```bash
# 创建技能目录（如不存在）
mkdir -p ~/.claude/skills

# 链接技能
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
├── SKILL.md              # 必需：主技能定义
│   ├── YAML frontmatter  # name、description、version 等
│   └── Markdown content  # 指令和工作流
├── scripts/              # 可选：可执行工具脚本
├── references/           # 可选：详细文档
├── agents/               # 可选：子代理配置
└── assets/               # 可选：模板和静态文件
```

## 使用方法

技能由 AI 助手根据前置配置中的 `description` 字段自动触发。只需自然描述任务，相应技能将被激活。

示例提示词：
- "创建一个数据库迁移的新技能" → 触发 U-skill-creator
- "构建一个图像分类 CNN" → 触发 U-neural-network-coder
- "在 Simulink 中调优 PID 控制器" → 触发 U-matlab-simulink-coder

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