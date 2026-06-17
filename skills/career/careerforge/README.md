# CareerForge

来源：<https://github.com/rebecha1227-a11y/CareerForge>

CareerForge 是一套 AI 求职全链路 skills，覆盖岗位搜索、简历匹配、简历生成、求职信、模拟面试和 Offer 决策。

## Included Skills

- `job-hunt`：多平台岗位搜索、匹配筛选和 Excel 导出。
- `resume-match`：简历与 JD 的匹配度评分和优化建议。
- `resume-craft`：简历生成与优化，支持 HTML/PDF 和 Word 模板。
- `cover-letter`：邮件求职信和招聘软件打招呼消息生成。
- `mock-interview`：HR、业务主管、高管三轮模拟面试。
- `offer-decision`：多 Offer 对比、薪资谈判话术和决策报告。

## Layout

- `skills/`：6 个 Skill 本体，目录内容来自上游 `skills/`。
- `templates/word/`：`resume-craft/scripts/fill_docx.py` 生成 Word 简历时需要的模板文件。

## Install Note

手动安装到 Codex 时，将 `skills/*` 复制到 `~/.codex/skills/`。如果需要使用 `resume-craft` 的 Word 输出能力，还需要将 `templates/word/` 复制到 `~/.codex/templates/word/`。
