---
name: wechat-daily-report
description: Analyze exported WeChat chat logs and generate a daily HTML report.
---

# WeChat Daily Report

Use this skill when the user wants to turn an exported WeChat chat log into a daily relationship, group, or work-summary report.

## Workflow

1. Put the exported chat text file in the project folder.
2. Run `scripts/analyze_chat.py` to create a JSON summary.
3. Add AI-written commentary manually or with another model if desired.
4. Run `scripts/generate_report.py` to create an HTML report.

## Commands

```powershell
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/analyze_chat.py --input chat.txt --output output/summary.json
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/generate_report.py --summary output/summary.json --output output/report.html
```

If Playwright is installed in the Python environment, `generate_report.py` can also export a PNG:

```powershell
& "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" scripts/generate_report.py --summary output/summary.json --output output/report.html --png output/report.png
```

