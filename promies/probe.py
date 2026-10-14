#!/usr/bin/env python3
"""探测飞书机器人的关键词校验：逐个候选词发一条，看哪个通过"""
import json, os, urllib.request

WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "").strip()
CANDS = ["热点", "新闻", "资讯", "热榜", "热搜", "今日热点", "TrendRadar", "trendradar",
         "头条", "热点新闻", "监控", "提醒", "每日", "报告", "简报", "快报", "播报",
         "限免日报", "免费软件", "软件日报", "羊毛", "薅羊毛", "资源", "分享", "推荐",
         "情报", "日报推送", "热点推送", "新闻推送", "今日资讯"]

def post(text):
    payload = {"msg_type": "text", "content": {"text": text}}
    data = json.dumps(payload, ensure_ascii=False).encode()
    req = urllib.request.Request(WEBHOOK, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read().decode("utf-8", "ignore")
    except Exception as e:
        return f"ERR {e}"

print("webhook 长度:", len(WEBHOOK))
ok = []
for c in CANDS:
    body = post(c)
    hit = '"code":0' in body.replace(" ", "")
    print(f"  {'✅' if hit else '❌'} {c:<12} → {body[:110]}")
    if hit:
        ok.append(c)
print("\n通过的候选:", ok)
