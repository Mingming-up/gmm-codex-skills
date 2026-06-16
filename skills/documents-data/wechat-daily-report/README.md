# WeChat Daily Report Skill

This is a local, dependency-light implementation of the GitHub project idea from `siuserxiaowei/wechat-daily-report-skill`.

It reads exported WeChat chat text, summarizes the day, and generates a shareable HTML report. PNG export is optional and only runs when Playwright is available.

## Quick Start

```powershell
cd path\to\wechat-daily-report-skill
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/analyze_chat.py --input examples/sample_chat.txt --output output/summary.json
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/generate_report.py --summary output/summary.json --output output/report.html
```

Open `output/report.html` in a browser.

## Chat Format

The parser supports common exported formats such as:

```text
2026-05-25 08:30 Alice: Good morning
2026/05/25 08:31 Bob：早上好
[2026-05-25 08:32] Alice: 今天安排是什么？
```

Multiline messages are attached to the previous message.

## Optional AI Commentary

Create a plain text file and pass it with `--ai-text`:

```powershell
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/generate_report.py --summary output/summary.json --ai-text ai_summary.txt --output output/report.html
```
