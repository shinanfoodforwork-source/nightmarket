from flask import Flask, request
import json

app = Flask(__name__)

LINE_ACCESS_TOKEN = "TXTgg7f8Xbf4+RlW37gCW27YkazQ97EmgfYJ81llDQYLAtcaOCFoz8fvqOrzPB9BD6mrQgZr+hd0xZjvMqU8giwXmpdFcDvLBDT+8zHwMIA5bCUKX+vHIuRlmL3miezINn11pHD+GF9ruXoAEvnyiwdB04t89/1O/w1cDnyilFU="

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return "OK"

@app.route("/")
def home():
    return "查 User ID 用"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
