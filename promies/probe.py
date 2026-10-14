#!/usr/bin/env python3
"""探测飞书机器人的关键词校验：逐个候选词发一条，看哪个通过"""
import json, os, urllib.request

WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "").strip()
CANDS = ["限免", "限免软件日报", "限免软件", "日报", "通知", "Promies", "promies",
         "新码", "优惠", "推送", "白嫖", "免费", "福利", "好物", "软件",
         "码", "激活码", "限免通知", "软件限免", "限时免费", "今日限免"]

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
