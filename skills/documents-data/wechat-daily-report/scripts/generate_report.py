#!/usr/bin/env python3
import argparse
import html
import json
from pathlib import Path


def bar(value, maximum):
    width = 0 if maximum == 0 else max(6, round(value / maximum * 100))
    return f'<span class="bar"><span style="width:{width}%"></span></span>'


def render(summary, ai_text=""):
    participants = summary.get("participants", [])
    hours = summary.get("hourly_distribution", [])
    words = summary.get("top_words", [])
    samples = summary.get("sample_messages", [])
    max_participant = max([item["messages"] for item in participants] or [0])
    max_hour = max([item["messages"] for item in hours] or [0])
    date_range = summary.get("date_range", {})
    title_date = date_range.get("start") or "WeChat"
    if date_range.get("end") and date_range.get("end") != title_date:
        title_date = f"{title_date} to {date_range.get('end')}"

    participant_rows = "\n".join(
        f"<li><strong>{html.escape(item['name'])}</strong>{bar(item['messages'], max_participant)}<span>{item['messages']}</span></li>"
        for item in participants
    )
    hour_rows = "\n".join(
        f"<li><strong>{item['hour']}:00</strong>{bar(item['messages'], max_hour)}<span>{item['messages']}</span></li>"
        for item in hours
    )
    word_tags = "\n".join(
        f"<span>{html.escape(item['word'])}<b>{item['count']}</b></span>" for item in words
    )
    sample_rows = "\n".join(
        f"<article><p>{html.escape(item['text'])}</p><small>{html.escape(item['timestamp'])} · {html.escape(item['sender'])}</small></article>"
        for item in samples
    )
    ai_block = ""
    if ai_text.strip():
        ai_block = f"""
        <section>
          <h2>AI Summary</h2>
          <p class="ai">{html.escape(ai_text.strip()).replace(chr(10), '<br>')}</p>
        </section>
        """

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WeChat Daily Report</title>
  <style>
    :root {{ color-scheme: light; --ink:#17212b; --muted:#667085; --line:#e6e8ec; --accent:#18a058; --warm:#ff9f1c; --soft:#f6f8fb; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; color:var(--ink); background:#eef2f5; }}
    main {{ width:min(760px, 100%); margin:0 auto; background:white; min-height:100vh; }}
    header {{ padding:34px 26px 24px; background:linear-gradient(135deg, #e8fff3, #fff7e7); border-bottom:1px solid var(--line); }}
    h1 {{ margin:0 0 8px; font-size:30px; letter-spacing:0; }}
    h2 {{ margin:0 0 14px; font-size:18px; }}
    p {{ line-height:1.72; }}
    .subtitle {{ margin:0; color:var(--muted); }}
    .metrics {{ display:grid; grid-template-columns:repeat(3, 1fr); gap:10px; padding:18px 18px 0; }}
    .metric {{ padding:16px; border:1px solid var(--line); border-radius:8px; background:var(--soft); }}
    .metric b {{ display:block; font-size:25px; margin-bottom:4px; }}
    .metric span, small {{ color:var(--muted); }}
    section {{ padding:22px 26px; border-top:1px solid var(--line); }}
    ul {{ list-style:none; padding:0; margin:0; display:grid; gap:12px; }}
    li {{ display:grid; grid-template-columns:96px 1fr 44px; align-items:center; gap:12px; }}
    .bar {{ display:block; height:10px; background:#edf0f3; border-radius:999px; overflow:hidden; }}
    .bar span {{ display:block; height:100%; background:linear-gradient(90deg, var(--accent), var(--warm)); border-radius:999px; }}
    .tags {{ display:flex; flex-wrap:wrap; gap:9px; }}
    .tags span {{ padding:8px 10px; border:1px solid var(--line); border-radius:999px; background:white; }}
    .tags b {{ margin-left:6px; color:var(--accent); }}
    article {{ padding:14px 0; border-bottom:1px solid var(--line); }}
    article:last-child {{ border-bottom:0; }}
    article p {{ margin:0 0 6px; white-space:pre-wrap; }}
    .ai {{ margin:0; padding:16px; background:#fff9ed; border-left:4px solid var(--warm); border-radius:6px; }}
    @media (max-width: 560px) {{
      h1 {{ font-size:25px; }}
      .metrics {{ grid-template-columns:1fr; }}
      li {{ grid-template-columns:78px 1fr 34px; gap:8px; }}
      header, section {{ padding-left:18px; padding-right:18px; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>WeChat Daily Report</h1>
      <p class="subtitle">{html.escape(title_date)} · generated {html.escape(summary.get('generated_at', ''))}</p>
    </header>
    <div class="metrics">
      <div class="metric"><b>{summary.get('message_count', 0)}</b><span>Messages</span></div>
      <div class="metric"><b>{len(participants)}</b><span>Participants</span></div>
      <div class="metric"><b>{summary.get('character_count', 0)}</b><span>Characters</span></div>
    </div>
    {ai_block}
    <section>
      <h2>Participants</h2>
      <ul>{participant_rows}</ul>
    </section>
    <section>
      <h2>Hourly Activity</h2>
      <ul>{hour_rows}</ul>
    </section>
    <section>
      <h2>Top Words</h2>
      <div class="tags">{word_tags}</div>
    </section>
    <section>
      <h2>Notable Messages</h2>
      {sample_rows}
    </section>
  </main>
</body>
</html>"""


def export_png(html_path, png_path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright is not installed in this Python environment.") from exc

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 760, "height": 1200}, device_scale_factor=2)
        page.goto(Path(html_path).resolve().as_uri(), wait_until="networkidle")
        page.screenshot(path=str(png_path), full_page=True)
        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Generate a WeChat daily HTML report.")
    parser.add_argument("--summary", required=True, help="Path to summary JSON from analyze_chat.py.")
    parser.add_argument("--output", required=True, help="Path to write HTML report.")
    parser.add_argument("--ai-text", help="Optional plain text AI commentary.")
    parser.add_argument("--png", help="Optional PNG screenshot output path. Requires Playwright.")
    args = parser.parse_args()

    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    ai_text = Path(args.ai_text).read_text(encoding="utf-8") if args.ai_text else ""
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(summary, ai_text), encoding="utf-8")
    print(f"Wrote {output}")
    if args.png:
        png_path = Path(args.png)
        png_path.parent.mkdir(parents=True, exist_ok=True)
        export_png(output, png_path)
        print(f"Wrote {png_path}")


if __name__ == "__main__":
    main()

