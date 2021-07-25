# 準備資料
import urllib.request  # 發送連線的套件
import json  # 解讀 JSON 格式的套件
from flask import *  # 載入 flask 模組
import json
file = open("data.txt", mode="r", encoding="utf-8")
data = json.load(file)
file.close()

# 建立網站伺服器
# cmd: pip install flask

app = Flask("My Website")  # 建立一個網站應用程式物件

# 網站的網址:http://主機名稱/路徑?參數名稱=資料&參數名稱=資料&...
# 例如:https://linebot-1130.herokuapp.com/


@app.route("/")  # 指定對應的網址路徑，"/"是根目錄
def home():  # 對應的處理函式
    return render_template("home.html")    # 回應給前端的訊息

# 例如:https://linebot-1130.herokuapp.com/test.php?keyword=關鍵字


@app.route("/test.php")  # 指定對應的網址路徑
def test():  # 對應的處理函式
    # 取得網址列上的參數:keyword=request.args.get(參數名稱, 預設值)
    keyword = request.args.get("keyword", None)
    if keyword == None:
        return redirect("/")    # 導向到路徑 /
    else:    # 回應給前端的訊息
        if keyword in data:
            # return "中文: "+data[keyword]
            return render_template("result.html", result=data[keyword])
        else:
            # return "沒有翻譯"
            return render_template("result.html", result="沒有翻譯")


# 建立負責處理 LINE 訊息的網址
# 例如:https://linebot-1130.herokuapp.com/linebot
# 找到圖片的網址 :
# https://linebot-1130.herokuapp.com/static/images/檔案名稱
# https://linebot-1130.herokuapp.com/static/images/dog_origin.jpg
# https://linebot-1130.herokuapp.com/static/images/dog_preveiw.jpg


@app.route("/linebot", methods=["GET", "POST"])
def linebot():

    # 取得 LINE 傳遞過來的資料
    content = request.json  # 取得整包資訊
    event = content["events"][0]  # 發生的事件 (使用者傳遞訊息、使用者加入好友等等)
    eventType = event["type"]  # 事件的型態
    replyToken = event["replyToken"]  # 回應這個訊息，需要的鑰匙 (token)
    text = event["message"]["text"]  # 取得使用者真正傳遞的訊息文字
    # 準備回應給使用者

    if "圖片" in text:
        message = {
            "type": "image",
            "originalContentUrl": "https://fried-chicken.herokuapp.com/static/images/dog_origin.jpg",
            "previewImageUrl": "https://fried-chicken.herokuapp.com/static/images/dog_preveiw.jpg"
        }
    else:
        if text == "你是誰":
            replyText = "雞排です"
        elif text == "哈哈哈":
            replyText = "嘿嘿嘿"
        elif text == "古戰場":
            replyText = "還想逃阿，古戰場逃兵"
        elif text == "雞排":
            replyText = "好吃呦~~"
        elif "下雨" in text:
            # 抓取雨量資料
            url = "http://117.56.59.17/OpenData/API/Rain/Get?stationNo=&loginId=open_rain&dataKey=85452C1D"
            response = urllib.request.urlopen(url)
            response = response.read().decode("utf-8")
            weather = json.loads(response)
            # 準備回應
            replyText = "雨量觀測資料 : "
            stations = weather["data"]
            # 確認使用者想找的地區
            areas = ["文山", "大安", "中正", "中山", "松山",
                     "信義", "南港", "內湖", "萬華", "士林", "北投"]
            area = None  # 記錄使用者的搜尋目標
            for a in areas:
                if a in text:
                    area = a
                    break
            # 根據使用者想找的地區給資料
            if area == None:
                replyText += "沒有資料\n可以嘗試輸入:\"文山\", \"大安\", \"中正\", \"中山\", \"松山\", \"信義\",\"南港\", \"內湖\", \"萬華\", \"士林\", \"北投\" 下雨"
            else:
                for station in stations:
                    if area in station["stationName"]:
                        replyText += "\n" + \
                            station["stationName"]+" : " + \
                            str(station["rain"])+" 公厘"
        else:
            replyText = text  # "你真可愛"
        message = {"type": "text", "text": replyText}  # 單一回應訊息

    body = {  # 整包回應: 可以包含很多則訊息
        "replyToken": replyToken,
        "messages": [message]
    }
    req = urllib.request.Request("https://api.line.me/v2/bot/message/reply", headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer "+"My Channel access token"
    }, data=json.dumps(body).encode("utf8"))
    # 處理網路連線，把整包回應傳回給LINE
    # 準備連線的細節:網址、標頭、資料
    # 發出連線並取得回應
    response = urllib.request.urlopen(req)
    response = response.read().decode("utf-8")
    print(response)
    return "ok bot"


if __name__ == "__main__":  # 如果以主程式執行，立即啟動伺服器
    app.run()  # 啟動伺服器

# ctrl+c 關閉伺服器
