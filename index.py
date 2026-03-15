from flask import Flask, request
import json  # 修正：導入 → import

app = Flask(__name__)

LINE_ACCESS_TOKEN = "TXTgg7f8Xbf4+R1W37gCW27YkazQ97EmgfYJ8111DQYLAtcaOCFoz8fvqOrzPB9BD6mrQgZr+hd0xZjvMqU8giwXmpdFcDvLBDT+8zHwMIA5bCUKX+vHIuRlmL3miezINn11pHD+GF9ruXoAEvnyiwdB04t89/1O/w1cDnyilFU="

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return "OK"  # 修正：返回 → return

@app.route("/")
def home():
    return "查用戶ID使用"

if __name__ == "__main__":  # 修正：如果 → if
    app.run(host="0.0.0.0", port=80)
