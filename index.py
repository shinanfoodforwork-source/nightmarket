from flask import Flask, request
import requests

app = Flask(__name__)

# 你的設定
LINE_ACCESS_TOKEN = "TXTgg7f8Xbf4+RlW37gCW27YkazQ97EmgfYJ81llDQYLAtcaOCFoz8fvqOrzPB9BD6mrQgZr+hd0xZjvMqU8giwXmpdFcDvLBDT+8zHwMIA5bCUKX+vHIuRlmL3miezINn11pHD+GF9ruXoAEvnyiwdB04t89/1O/w1cDnyilFU="
DIFY_API_KEY = "app-DTdkXDskAH1htz4BHZpW1j9O"
DIFY_APP_ID = "hw0v7PE2F6BzEEXD"
BOSS_LINE_USER_ID = "這裡替換成周老闆的LINE User ID"

# 商品對應群組
GOODS_GROUP_MAP = {
    "點心盒": "饒河包材群組",
    "吸管": "饒河包材群組",
    "500杯": "饒河包材群組",
    "700杯": "饒河包材群組",
    "牛奶": "饒河牛奶群組",
    "草莓": "饒河水果廠商",
    "大陸妹": "饒河水果廠商",
    "蚵仔": "饒河水果廠商",
    "金幣燒起士": "饒河起士金幣燒",
    "綠豆冰沙": "饒河冰沙茶包叫貨群",
    "紅茶包": "饒河冰沙茶包叫貨群",
    "綠茶包": "饒河冰沙茶包叫貨群",
    "仙草汁": "饒河冰沙茶包叫貨群",
    "冬瓜塊": "饒河冰沙茶包叫貨群",
    "蛋": "饒河農產行群組",
    "油": "饒河農產行群組",
}

def line_send(to, text):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": to,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(url, headers=headers, json=data)

def call_dify(user_id, text):
    url = f"https://api.dify.ai/v1/chat-messages"
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": {},
        "query": text,
        "user": user_id,
        "response_mode": "blocking"
    }
    try:
        res = requests.post(url, json=payload, headers=headers)
        return res.json().get("answer", "處理中，請稍候")
    except:
        return "系統處理中"

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    for event in body.get("events", []):
        if event.get("type") != "message" or event["message"].get("type") != "text":
            continue
        
        text = event["message"]["text"]
        user_id = event["source"]["userId"]
        chat_id = event["source"].get("groupId", user_id)

        if "@心安" in text:
            ai_answer = call_dify(user_id, text)
            line_send(chat_id, ai_answer)
            line_send(BOSS_LINE_USER_ID, f"【員工叫貨】\n來自群組：{chat_id}\n內容：{text}\n請回覆：同意 / 拒絕")

        if user_id == BOSS_LINE_USER_ID and "同意" in text:
            for item, group in GOODS_GROUP_MAP.items():
                if item in text:
                    line_send(group, f"自動叫貨：{item}")
                    line_send(chat_id, f"✅ 老闆同意，已送至【{group}】")
                    break
    return "OK"

@app.route("/")
def home():
    return "夜市自動化機器人運作中"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)