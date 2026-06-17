# gmm-codex-skills

这些我平时使用 Codex 安装的一些 skills，其中有一些是我自己创建的 skills，有一些是引用了一些著名的 skills，目的主要是为了方便 Codex 使用。后续如果还增加 skills 的话，也会继续推送到这里。
这个仓库主要算是我个人使用的 skills 备份以及电脑之间的同步。

## Skills 介绍

### Core

- `skill-creator`【引用】：创建或更新 Codex skills。
- `find-skills`【自建】：查找和发现适合某类任务的 skills。
- `evaluate-suggestions`【自建】：在采纳用户建议或修改方向前，先进行判断和权衡。

### Writing & Research

- `content-research-writer`【自建】：支持带研究和引用的内容写作。
- `nature-academic-search`【自建】：学术文献检索、引用验证和多来源搜索工作流。
- `paper-write`【自建】：本科、硕士论文写作、润色、扩写、翻译和防 AIGC 等工作流。
- `patent-write`【自建】：中文发明专利撰写、改写、统稿和权利要求处理。

### Documents & Data

- `docx`【引用】：Word 文档创建、读取、编辑和格式处理。
- `pdf`【引用】：PDF 读取、拆分、合并、表单填写、OCR 和格式处理。
- `xlsx`【引用】：电子表格创建、清洗、编辑、公式、格式和转换。
- `excel-analysis`【自建】：Excel 数据分析、透视表、图表和统计处理。
- `wechat-daily-report`【自建】：分析导出的微信聊天记录，并生成日报。

### Productivity

- `file-organizer`【自建】：文件整理、归类、去重和清理工作流。

### Dev Tools

- `mcp-builder`【引用】：MCP Server 构建和工具集成指南。
- `codex-reconnecting-solve`【自建】：排查和修复 Windows 上 Codex Desktop 反复重连的问题。
- `github-repo-publisher`【自建】：在明确收到指令后，将本地项目创建为 GitHub 仓库并推送。

### Career

- `tailored-resume-generator`【自建】：根据岗位描述和个人背景生成定制化简历。
- `CareerForge`【引用】：AI 求职全链路套件，包含岗位搜索、简历匹配、简历生成、求职信、模拟面试和 Offer 决策 6 个 skills。
  - `job-hunt`：多平台岗位搜索、匹配筛选和 Excel 导出。
  - `resume-match`：简历与 JD 的匹配度评分和优化建议。
  - `resume-craft`：简历生成与优化，支持 HTML/PDF 和 Word 模板。
  - `cover-letter`：邮件求职信和招聘软件打招呼消息生成。
  - `mock-interview`：HR、业务主管、高管三轮模拟面试。
  - `offer-decision`：多 Offer 对比、薪资谈判话术和决策报告。

CareerForge 放在 `skills/career/careerforge/` 下，其中 `skills/` 是 6 个 Skill 本体，`templates/word/` 是 `resume-craft` 生成 Word 简历时需要的模板依赖。
