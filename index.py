from flask import Flask, request
import json
import datetime
import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ===================== 【配置檢查！重點確認 BOSS_USER_ID】 =====================
LINE_ACCESS_TOKEN = "TXTgg7f8Xbf4+RlW37gCW27YkazQ97EmgfYJ81llDQYLAtcaOCFoz8fvqOrzPB9BD6mrQgZr+hd0xZjvMqU8giwXmpdFcDvLBDT+8zHwMIA5bCUKX+vHIuRlmL3miezINn11pHD+GF9ruXoAEvnyiwdB04t89/1O/w1cDnyilFU="
# ⚠️ 請確認這個 ID 是「老闆個人 LINE ID」（不是群組ID！）
# 查詢方式：https://developers.line.biz/console/channel/{你的ChannelID}/messaging-api/insight
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
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/raohe-500%40crafty-key-490400-h4.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
# ======================================================================

# 群組規則
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
# 新增：儲存通知記錄，方便排查
NOTIFICATION_LOG = "notification_log.json"

# ------------------------------
# 工具函式：新增日誌記錄
# ------------------------------
def log_notification(type_msg, content, status):
    """記錄通知日誌"""
    log_data = load_json(NOTIFICATION_LOG)
    log_data.append({
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": type_msg,
        "content": content,
        "status": status  # success/fail
    })
    save_json(NOTIFICATION_LOG, log_data)

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
                        headers={"Authorization":f"Bearer {LINE_ACCESS_TOKEN}"},
                        timeout=10)
        r.raise_for_status()
        return r.json().get("displayName", "未知員工")
    except Exception as e:
        print(f"獲取使用者名稱失敗：{e}")
        log_notification("get_user_name", f"UID:{uid}, Error:{str(e)}", "fail")
        return "未知員工"

def reply(token, text):
    """加強版回覆函式"""
    try:
        payload = {
            "replyToken": token,
            "messages": [{"type": "text", "text": text}]
        }
        r = requests.post(
            "https://api.line.me/v2/bot/message/reply",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
            },
            json=payload,
            timeout=15
        )
        r.raise_for_status()
        print(f"✅ 回覆成功：{text}")
        log_notification("reply", f"Token:{token}, Text:{text}", "success")
        return True
    except Exception as e:
        error_msg = f"回覆失敗：{e}，LINE回應：{r.text if 'r' in locals() else '無'}"
        print(f"❌ {error_msg}")
        log_notification("reply", f"Token:{token}, Error:{error_msg}", "fail")
        return False

def push_to_boss(text):
    """終極版推播老闆函式（多重保障）"""
    # 1. 先檢查 BOSS_USER_ID 是否合法
    if not BOSS_USER_ID or not BOSS_USER_ID.startswith("U"):
        error = f"BOSS_USER_ID 無效：{BOSS_USER_ID}（必須以U開頭的個人ID）"
        print(f"❌ {error}")
        log_notification("push", error, "fail")
        return False, error
    
    # 2. 調用 LINE Push API
    try:
        payload = {
            "to": BOSS_USER_ID,
            "messages": [{"type": "text", "text": text}]
        }
        r = requests.post(
            "https://api.line.me/v2/bot/message/push",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
            },
            json=payload,
            timeout=15
        )
        # 列印完整回應（關鍵！排查錯誤）
        print(f"LINE Push API 回應：{r.status_code} - {r.text}")
        
        if r.status_code == 200:
            print(f"✅ 推播老闆成功：{text}")
            log_notification("push", f"BOSS_UID:{BOSS_USER_ID}, Text:{text}", "success")
            return True, "推送成功"
        else:
            error = f"推播失敗：LINE返回{r.status_code}，訊息：{r.text}"
            print(f"❌ {error}")
            log_notification("push", f"BOSS_UID:{BOSS_USER_ID}, Error:{error}", "fail")
            return False, error
    except Exception as e:
        error = f"推播異常：{str(e)}"
        print(f"❌ {error}")
        log_notification("push", f"BOSS_UID:{BOSS_USER_ID}, Error:{error}", "fail")
        return False, error

# ------------------------------
# 商品識別
# ------------------------------
def extract_product_name(text):
    clean_text = text.replace("斤","").replace("包","").replace("罐","").replace(" ","").replace("要叫","").replace("我","").replace("買","").replace("訂","").replace("你有識別到","").replace("嗎","")
    # 優先匹配已知商品
    for product in GROUP_MAP.keys():
        if product in clean_text:
            return product
    # 自定義商品
    custom_products = dict(load_json(GROUP_FILE)).keys()
    for product in custom_products:
        if product in clean_text:
            return product
    return None

# ------------------------------
# Dify 對話
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
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return response.json().get("answer", "我目前無法回覆您哦")
    except Exception as e:
        error = f"Dify錯誤：{str(e)}"
        print(f"❌ {error}")
        return error

# ------------------------------
# 報表處理
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
            sheet.append_row([
                data.get("日期",""), data.get("天氣",""), data.get("營業額",""),
                data.get("盒子",""), data.get("玉米",""), data.get("起士",""),
                data.get("現場不收錢",""), data.get("電費",""), data.get("瓦斯",""),
                data.get("薪資",""), data.get("獎金",""), data.get("現場支出",""),
                data.get("實收營業額",""), data.get("庫存",""), data.get("上傳者","")
            ])
        except Exception as e:
            print(f"寫入Google試算表失敗：{e}")
    return data

# ------------------------------
# 主程式（終極版）
# ------------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if not data or "events" not in data:
            return "無事件數據", 400
        
        for e in data.get("events", []):
            if e.get("type") != "message" or e["message"].get("type") != "text":
                continue

            # 核心參數
            txt = e["message"]["text"].strip()
            token = e["replyToken"]
            uid = e["source"]["userId"]
            name = get_user_name(uid)
            is_boss = uid == BOSS_USER_ID
            AT_KEYWORD = "@心安夜市記錄"

            # 1. 報表處理
            if "營業額" in txt and "實收營業額" in txt:
                dt = parse_and_save(txt, name)
                reply(token, f"✅ 報表已儲存：{dt.get('日期','')}\n📝 已同步通知老闆")
                # 推播老闆 + 記錄結果
                push_msg = f"【新報表】\n員工：{name}\n日期：{dt.get('日期','')}\n營業額：{dt.get('營業額','')}\n實收：{dt.get('實收營業額','')}"
                push_success, push_msg_detail = push_to_boss(push_msg)
                # 告訴員工推送結果
                if push_success:
                    reply(token, "✅ 通知老闆成功！")
                else:
                    reply(token, f"⚠️ 通知老闆失敗：{push_msg_detail}\n請手動告知老闆！")
                continue

            # 2. 非老闆需@機器人
            if not is_boss and AT_KEYWORD not in txt:
                continue

            # 3. 清理訊息
            clean_msg = txt.replace(AT_KEYWORD, "").strip()
            if not clean_msg:
                reply(token, "💡 請輸入具體內容，例如：我要叫草莓20斤")
                continue

            # 4. 提取商品
            product = extract_product_name(clean_msg)
            
            # 5. 已知商品 → 分群 + 強制推送老闆
            if product:
                target_group = get_group(product)
                # 先回覆員工
                reply(token, f"✅ 已識別商品：{product}\n✅ 自動分群至：{target_group}\n🔄 正在通知老闆...")
                # 推播老闆（帶詳細資訊）
                push_msg = f"【叫貨確認】\n👉 員工：{name}\n👉 商品：{product}\n👉 需求：{clean_msg}\n👉 群組：{target_group}\n⏰ 時間：{datetime.datetime.now().strftime('%H:%M:%S')}"
                push_success, push_msg_detail = push_to_boss(push_msg)
                # 回覆員工推送結果
                if push_success:
                    reply(token, "✅ 通知老闆成功！老闆已收到確認訊息")
                else:
                    reply(token, f"⚠️ 通知老闆失敗！原因：{push_msg_detail}\n請手動複製以下內容告知老闆：\n{push_msg}")
                continue
            
            # 6. 未知內容（問句/新商品）
            else:
                question_words = ["為什麼","什麼","為何","沒收到","收不到","怎麼","為","識別到","嗎"]
                is_question = any(word in clean_msg for word in question_words)
                
                if is_question:
                    # 問句 → Dify回答 + 通知老闆
                    ans = chat_with_dify(clean_msg)
                    reply(token, f"💡 {ans}")
                    push_msg = f"【員工提問】\n員工：{name}\n問題：{clean_msg}\n機器人回覆：{ans}"
                    push_success, push_msg_detail = push_to_boss(push_msg)
                    if not push_success:
                        reply(token, f"⚠️ 已回覆你的問題，但通知老闆失敗：{push_msg_detail}")
                else:
                    # 新商品 → 請示老闆
                    reply(token, "✅ 新商品已請示周老闆！\n🔄 正在發送通知...")
                    push_msg = f"【新商品請示】\n員工：{name}\n需求：{clean_msg}\n請問要將此商品分到哪個群組？"
                    push_success, push_msg_detail = push_to_boss(push_msg)
                    if push_success:
                        reply(token, "✅ 已成功通知老闆，請等待回覆～")
                    else:
                        reply(token, f"⚠️ 通知老闆失敗！原因：{push_msg_detail}\n請手動告知老闆以下內容：\n{push_msg}")

        return "OK"
    except Exception as e:
        error = f"主程式出錯：{str(e)}"
        print(f"❌ {error}")
        log_notification("webhook", error, "fail")
        return "ERROR", 500

# ------------------------------
# 新增：測試推送接口（方便你排查）
# ------------------------------
@app.route("/test_push", methods=["GET"])
def test_push():
    """訪問此網址測試推播老闆功能：https://你的vercel網址/test_push"""
    test_msg = f"【測試通知】\n時間：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n測試推播功能是否正常"
    success, detail = push_to_boss(test_msg)
    if success:
        return f"<h1>✅ 測試推送成功！</h1><p>詳情：{detail}</p>"
    else:
        return f"<h1>❌ 測試推送失敗！</h1><p>原因：{detail}</p><p>請檢查：</p><ul><li>BOSS_USER_ID 是否為個人ID（以U開頭）</li><li>LINE Access Token 是否有效</li><li>LINE Bot 是否有推送權限</li></ul>"

@app.route("/")
def home():
    return """
    <h1>✅ 心安 - 夜市全自動系統（終極版）</h1>
    <p>功能：</p>
    <ul>
        <li>✅ 商品識別 + 自動分群</li>
        <li>✅ 強制推送老闆 + 結果回饋</li>
        <li>✅ 推送失敗自動提示 + 手動備份</li>
        <li>✅ 完整日誌記錄</li>
    </ul>
    <p>測試推送功能：<a href="/test_push">點擊測試</a></p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
