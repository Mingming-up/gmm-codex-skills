#!/usr/bin/env python3
import argparse
import collections
import datetime as dt
import json
import re
from pathlib import Path


MESSAGE_PATTERNS = [
    re.compile(r"^\[?(?P<date>\d{4}[-/]\d{1,2}[-/]\d{1,2})\s+(?P<time>\d{1,2}:\d{2})(?::\d{2})?\]?\s+(?P<sender>[^:：]+)[:：]\s*(?P<text>.*)$"),
    re.compile(r"^(?P<date>\d{1,2}[-/]\d{1,2}[-/]\d{4})\s+(?P<time>\d{1,2}:\d{2})(?::\d{2})?\s+(?P<sender>[^:：]+)[:：]\s*(?P<text>.*)$"),
]

STOPWORDS = {
    "the", "and", "you", "are", "for", "that", "this", "with", "have", "will",
    "今天", "然后", "可以", "我们", "一下", "一个", "这个", "那个", "收到",
}


def parse_datetime(date_text, time_text):
    for fmt in ("%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M", "%m-%d-%Y %H:%M", "%m/%d/%Y %H:%M"):
        try:
            return dt.datetime.strptime(f"{date_text} {time_text}", fmt)
        except ValueError:
            pass
    return None


def read_chat_text(path):
    data = Path(path).read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "gbk"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def parse_messages(path):
    messages = []
    current = None
    for raw_line in read_chat_text(path).splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = None
        for pattern in MESSAGE_PATTERNS:
            match = pattern.match(line)
            if match:
                break
        if match:
            timestamp = parse_datetime(match.group("date"), match.group("time"))
            if timestamp is None:
                continue
            current = {
                "timestamp": timestamp.isoformat(timespec="minutes"),
                "date": timestamp.date().isoformat(),
                "hour": timestamp.hour,
                "sender": match.group("sender").strip(),
                "text": match.group("text").strip(),
            }
            messages.append(current)
        elif current:
            current["text"] = f"{current['text']}\n{line}".strip()
    return messages


def tokenize(text):
    english = re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text.lower())
    chinese = re.findall(r"[\u4e00-\u9fff]{2,}", text)
    tokens = english + chinese
    return [token for token in tokens if token not in STOPWORDS and len(token) >= 2]


def summarize(messages):
    by_sender = collections.Counter(message["sender"] for message in messages)
    by_hour = collections.Counter(str(message["hour"]).zfill(2) for message in messages)
    by_date = collections.Counter(message["date"] for message in messages)
    words = collections.Counter()
    for message in messages:
        words.update(tokenize(message["text"]))

    total_chars = sum(len(message["text"]) for message in messages)
    longest = sorted(messages, key=lambda item: len(item["text"]), reverse=True)[:5]
    first_date = min(by_date) if by_date else None
    last_date = max(by_date) if by_date else None

    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "date_range": {"start": first_date, "end": last_date},
        "message_count": len(messages),
        "character_count": total_chars,
        "participants": [{"name": name, "messages": count} for name, count in by_sender.most_common()],
        "hourly_distribution": [{"hour": hour, "messages": by_hour[hour]} for hour in sorted(by_hour)],
        "daily_distribution": [{"date": date, "messages": by_date[date]} for date in sorted(by_date)],
        "top_words": [{"word": word, "count": count} for word, count in words.most_common(20)],
        "sample_messages": longest,
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze exported WeChat chat text.")
    parser.add_argument("--input", required=True, help="Path to exported chat text.")
    parser.add_argument("--output", required=True, help="Path to write summary JSON.")
    args = parser.parse_args()

    messages = parse_messages(args.input)
    summary = summarize(messages)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Analyzed {summary['message_count']} messages -> {output}")


if __name__ == "__main__":
    main()
