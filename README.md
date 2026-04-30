# 企业级自动化代码审计与重构中枢 (DeepCode Audit)

这是一个基于 Multi-Agent 协作架构的自动化代码审查系统，旨在通过 AI 模拟资深架构师和安全专家的 Review 过程，提升研发效能。

## 核心架构
- **Architect Agent**: 负责代码全局意图分析。
- **Reviewer Agent**: 负责静态逻辑与代码规范检查。
- **Security Agent**: 专注于潜在漏洞（如注入、越权）的挖掘。
- **Developer Agent**: 基于反馈进行自动代码重构与修复。

## 快速启动
1. 安装依赖: `pip install -r requirements.txt`
2. 配置文件: 将 `.env.example` 重命名为 `.env` 并填写有效的 API 配置。
3. 启动系统: `streamlit run app.py`

## 适用场景
- CI/CD 流程中的自动 Code Review。
- 存量老旧系统的安全性普查。
- 自动化代码重构建议。
