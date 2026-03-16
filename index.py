from flask import Flask, request
import json
import datetime
import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ===================== 【全部填好！直接用】 =====================
LINE_ACCESS_TOKEN = "TXTgg7f8Xbf4+RlW37gCW27YkazQ97EmgfYJ81llDQYLAtcaOCFoz8fvqOrzPB9BD6mrQgZr+hd0xZjvMqU8giwXmpdFcDvLBDT+8zHwMIA5bCUKX+vHIuRlmL3miezINn11pHD+GF9ruXoAEvnyiwdB04t89/1O/w1cDnyilFU="
BOSS_USER_ID = "U5e32d2a8818c6780fdd59588c025621"

DIFY_API_KEY = "app-DTdkXDskAH1htz4BHZpW1j9O"
DIFY_USER = "raohe_boss"

GOOGLE_SHEET_ID = "1mmm4i_y4itduMr4h-hmVkQ32f4RlFdg5uN-G4nNYC_E"
GOOGLE_SERVICE_ACCOUNT = {
  "type": "service_account",
  "project_id": "crafty-key-490400-h4",
  "private_key_id": "8277870bf90580ffb12628d7028373ae955285ce",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDYJLwO+10MiDuJ\nN+QysetHdj4wQEu4Hcc4+x5irrl0ilZ8EX3d+NsoDE6DTV/jgotOPsz1mAA9tdsU\n81E/cHzyvZW659ycDgYYmhE3P9kBdH5YYzVI4lneffK4y8EYH5Jy1g0cXy72x+VC\nSFN8CJWACkr+UnfarbJsPiar/QBrr/v7E7B/Yihkk6Kn8kSwQu8mz2Y5d/PPi2MG\nWZMmjnhqhUH74WLrusfmesu9HIfmJ6o910o/ovazfWImMWm30b4m0HRorJZuGUUz\n6qJv5vAzK+vlThQfY20Fjh+Pju4PD/xVWmfXYR9tftIlcEDh2jgXBmwDnc7KZ0/T\nN5Rruq47AgMBAAECggEAG7GROuYwBOQLpMg5f9lWCQD4dNw4F24RUZazTPeQIYN8\nE0d2dhNlmRsCkEZAq/jU+oCHaExCc6WyXVvTpCo4iC2MWrdMh94wH8TVwdt3ZX1U\nluSXNjByTVSb3duVcQ7Sh84vPdxgOxRfpn932uOKrC4lb7KHUsiAnOfVsqGnBST5\n+TtCOhFeSCNjCklJ+PY6ZCuAHC7VFejyUtibt8lJ3e8THEzkp6aFafn9pF3A7QLJ\nvo/bdxj3Eud1W4cwrWOwjFyfcZzS1BwJ8dWa4Ak9CUZRz3DLtbF/hBJMJQw36JsC\nzC+Aj2XFAx574G7AAerq4drySGYW5EVqCjrierapqQKBgQDyMHLhEnTcXJlwuHMa\n2OldJXZqxQWWUvbqI/Q7QfvGPa+zi1Na14w3mx3Tzdqzl3T+E6frw0Yp23mMvCuJ\nWPxSo4sFhvMi/9U0y4QtKa0GI4GzUU5XXxty4C832STz45wsIe6WDPnhAWkdRoHj\nbxLwAvShVVPeV8NRz5pzWCz2JwKBgQDkeA/kJZGsM9Ptp4mFarAU9zLdZ33R9IPh\nTxWaOID2jQXQ66lZbqmEHWgjbcQ2skcHtPGhxau52rZMCi90Xhc+VFDfKJF4CUv1\nZm6rAOUoc913mitcF5b+Rl0J8GOq8G6OpcyvSEY+jCws9kPeLMhLMevsLPOHrud7\nLKbVPJ2HzQKBgEBx8e/AOIZ2wYHEIyTuuVJG6LbKjI0OsJNnU9L84OFEgt904I5Y\nswAM76fvrBWD5ObDFjjfMmlq9HIllDQtEJ9w00p6OXKDvxkYWqil4Vuz0QyFQyJu\ntWAhFY934aRgWatIsDMPauKbvHvEykVZxiFFuBDCItoUYm3/nyq4OOabAoGAfcSu\nEsyvpVkeiAwbQyuY5OGzyXfIJoTw+F3dqXkDXTYChqDEJ+woOwcpJZ+uTOHVAiQU\nhBZZ00TX54IP34JQT0qA/mfJtIeBngSWVWJ3w84Mk2N2DQsbXryDSQ5g/1+9rJ8O\nz0r9CD+HrfSfJbYHSIWhtvCD2yRoX0EUUfw9R90CgYB6NAPIKg4zLwJoQKlimOEQ\ndyasl3pW1ddpcURIlOxMAFcMYXIlrUMPl1PS7fg9GE2JkJeDnDJyJPC3z8XL2pXA\nFJUL/w22bIY2Rexk+1k6Cwwxnmwd5PKMyVUcQxBx1/ZUzcNckPJQnl5d9KdJz5ax\nLQI01W74B/SEj/gqisLXYg==\n-----END PRIVATE KEY-----\n",
  "client_email": "raohe-500@crafty-key-490400-h4.iam.gserviceaccount.com",
  "client_id": "115836904378519580039",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",  # 修正錯誤的URL
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/raohe-500%40crafty-key-490400-h4.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
# ======================================================================

# 群組規則（會自動學習新增）
GROUP_MAP = {
    "報表":"饒河點貨群拿貨記得紀錄", "上班天數":"饒河點貨群拿貨記得紀錄", "營業額":"饒河點貨群拿貨記得紀錄",
    "現場問題":"饒河現場群", "狀況":"饒河現場群", "機器":"饒河現場群",
    "包材":"饒河包材群組", "盒子":"饒河包材群組", "吸管":"饒河包材群組",
    "牛奶":"饒河牛奶群組",
    "草莓":"饒河水果廠商", "香蕉":"饒河水果廠商", "蚵仔":"饒河水果廠商", "大陸妹":"饒河水果廠商",
    "起士":"饒河起士金幣燒",
    "冰沙":"饒河冰沙茶包叫貨群", "紅茶包":"饒河冰沙茶包叫貨群",
    "蛋":"饒河農產行群組", "油":"饒河農產行群組", "玉米":"饒河農產行群組"
}

GROUP_FILE = "group_map.json"

# ------------------------------
# 工具函式
# ------------------------------
def load_json(f):
    if os.path.exists(f):
        with open(f, "r", encoding="utf-8") as fp:
            return json.load(fp)
    return []

def save_json(f, data):
    with open(f, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)

def get_user_name(uid):
    try:
        r = requests.get(f"https://api.line.me/v2/bot/profile/{uid}", 
                        headers={"Authorization":f"Bearer {LINE_ACCESS_TOKEN}"})
        return r.json().get("displayName", "未知員工")
    except Exception as e:
        print(f"獲取使用者名稱失敗：{e}")
        return "未知員工"

def reply(token, text):
    try:
        requests.post("https://api.line.me/v2/bot/message/reply",
            headers={"Content-Type":"application/json","Authorization":f"Bearer {LINE_ACCESS_TOKEN}"},
            json={"replyToken":token,"messages":[{"type":"text","text":text}]})
    except Exception as e:
        print(f"回覆訊息失敗：{e}")

def push(to, text):
    try:
        requests.post("https://api.line.me/v2/bot/message/push",
            headers={"Content-Type":"application/json","Authorization":f"Bearer {LINE_ACCESS_TOKEN}"},
            json={"to":to,"messages":[{"type":"text","text":text}]})
    except Exception as e:
        print(f"推播訊息失敗：{e}")

# ------------------------------
# 自動學習新商品
# ------------------------------
def get_group(item):
    gm = dict(load_json(GROUP_FILE))
    if item in gm:
        return gm[item]
    if item in GROUP_MAP:
        return GROUP_MAP[item]
    return None

def add_item(item, group):
    gm = dict(load_json(GROUP_FILE))
    gm[item] = group
    save_json(GROUP_FILE, list(gm.items()))

# ------------------------------
# 自動分月份：115年3月 饒河報表
# ------------------------------
def get_month_sheet(month):
    try:
        scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_SERVICE_ACCOUNT, scope)
        client = gspread.authorize(creds)
        wb = client.open_by_key(GOOGLE_SHEET_ID)
        title = f"115年 {month}月 饒河報表"
        
        try:
            sheet = wb.worksheet(title)
        except:
            sheet = wb.add_worksheet(title=title, rows="1000", cols="20")
            sheet.append_row([
                "日期","天氣","營業額","盒子","玉米","起士",
                "現場不收錢","電費","瓦斯","薪資","獎金","現場支出",
                "實收營業額","庫存","上傳者"
            ])
        return sheet
    except Exception as e:
        print(f"取得Google試算表失敗：{e}")
        return None

# ------------------------------
# 自動解析報表 + 寫入對應月份
# ------------------------------
def parse_and_save(text, name):
    lines = text.replace("：",":").split("\n")
    data = {"上傳者":name}
    
    for line in lines:
        line = line.strip()
        if "日期" in line: data["日期"] = line.split(":",1)[-1].strip()
        if "天氣" in line: data["天氣"] = line.split(":",1)[-1].strip()
        if "營業額" in line and "實收" not in line: data["營業額"] = line.split(":",1)[-1].strip()
        if "盒子" in line: data["盒子"] = line.split(":",1)[-1].strip()
        if "玉米" in line: data["玉米"] = line.split(":",1)[-1].strip()
        if "起士" in line: data["起士"] = line.split(":",1)[-1].strip()
        if "現場不收錢" in line: data["現場不收錢"] = line.split(":",1)[-1].strip()
        if "電費支出" in line: data["電費"] = line.split(":",1)[-1].strip()
        if "瓦斯支出" in line: data["瓦斯"] = line.split(":",1)[-1].strip()
        if "薪資支出" in line: data["薪資"] = line.split(":",1)[-1].strip()
        if "獎金支出" in line: data["獎金"] = line.split(":",1)[-1].strip()
        if "現場支出" in line: data["現場支出"] = line.split(":",1)[-1].strip()
        if "實收營業額" in line: data["實收營業額"] = line.split(":",1)[-1].strip()
        if "玉米罐頭" in line or "煉乳" in line or "盒子" in line:
            data["庫存"] = data.get("庫存","") + line + " "

    if "日期" in data:
        month = data["日期"].split("/")[0]
        sheet = get_month_sheet(month)
        if sheet:
            sheet.append_row([
                data.get("日期",""), data.get("天氣",""), data.get("營業額",""),
                data.get("盒子",""), data.get("玉米",""), data.get("起士",""),
                data.get("現場不收錢",""), data.get("電費",""), data.get("瓦斯",""),
                data.get("薪資",""), data.get("獎金",""), data.get("現場支出",""),
                data.get("實收營業額",""), data.get("庫存",""), data.get("上傳者","")
            ])
    return data

# ------------------------------
# Dify 對話功能（修正參數錯誤）
# ------------------------------
def chat_with_dify(user_msg):
    try:
        url = "https://api.dify.ai/v1/chat-messages"
        headers = {
            "Authorization": f"Bearer {DIFY_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "inputs": {},
            "query": user_msg,
            "response_mode": "blocking",
            "user": DIFY_USER
        }
        # 修正：原本把headers和data顛倒了！
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 觸發HTTP錯誤
        return response.json().get("answer", "我目前無法回覆您哦")
    except Exception as e:
        print(f"Dify對話失敗：{e}")
        return f"對話出錯：{str(e)}"

# ------------------------------
# 主程式（修正@指令匹配）
# ------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        for e in data.get("events", []):
            if e["type"] != "message" or e["message"]["type"] != "text":
                continue

            txt = e["message"]["text"].strip()
            token = e["replyToken"]
            uid = e["source"]["userId"]
            name = get_user_name(uid)
            is_boss = uid == BOSS_USER_ID

            # 報表自動儲存
            if "營業額" in txt and "實收營業額" in txt:
                dt = parse_and_save(txt, name)
                reply(token, f"✅ 報表已儲存：{dt.get('日期','')}（自動歸類月份）")
                push(BOSS_USER_ID, f"【新報表】{name} 上傳 {dt.get('日期','')}")
                continue

            # 修正：匹配「@心安夜市記錄」而非「@心安」
            AT_KEYWORD = "@心安夜市記錄"
            if not is_boss and AT_KEYWORD not in txt:
                continue

            # 清理@標籤
            clean = txt.replace(AT_KEYWORD, "").strip()

            # 優化商品識別邏輯：逐詞比對，不是逐字
            new_item = None
            target = None
            # 拆分訊息成單詞（去除數量單位）
            words = clean.replace("斤","").replace("包","").replace("罐","").replace(" ","").replace("要叫","").split()
            for word in words:
                if len(word) < 1:
                    continue
                g = get_group(word)
                if g:
                    target = g
                else:
                    # 判斷是否是商品名（排除數字、問句）
                    if not word.isdigit() and word not in ["我","要","叫","為什麼","什麼","為何"]:
                        new_item = word

            # 新商品 → 問老闆
            if new_item and not target:
                reply(token, "✅ 新商品已請示周老闆")
                push(BOSS_USER_ID, f"---\n新商品：{new_item}\n請問要分到哪個群組？\n---")
                continue

            # 既有商品 → 自動分群
            if target:
                reply(token, f"✅ 已分群至：{target}")
                push(BOSS_USER_ID, f"---\n【叫貨】{name}\n內容：{clean}\n群組：{target}\n---")
                continue

            # Dify 智慧對話
            ans = chat_with_dify(clean)
            reply(token, ans)

        return "OK"
    except Exception as e:
        print(f"主程式出錯：{e}")
        return "ERROR", 500

@app.route("/")
def home():
    return "✅ 心安 - 夜市全自動系統（已連Google Sheets）"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)  # 開啟debug便於排查
