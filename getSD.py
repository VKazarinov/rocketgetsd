from flask import Flask, request, jsonify
import re
import requests
import json
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        sd = request.json['text'].split(" ")
    sdrequest = sd[1]
	# api-endpoint
    URL = "" + sdrequest
        # location given here
    ApiKey = ""
        # defining a params dict for the parameters to be sent to the API
    PARAMS = {'TECHNICIAN_KEY':ApiKey}
        # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    msg = data['request']['description']
    subject = data['request']['subject']
#    technician = data['request']['technician']['name']
#    technician = json.dumps(technician)
    msgformat = re.sub("<[^>]*>|&nbsp;|\r\n|\n|\r", "", msg)
    msgformatcut = re.sub(r"(?i)(..)Уважением.*$|From[^\n]+gt;|", "", msgformat)
    imgsearch = re.search(r"(.)inlineimages[^\n]+.(png|jpg)", msg)
    response = jsonify({"text":"**Запрос:** "+sdrequest + "\n\n**Тема:** " + subject + "\n\n**Описание:** " + msgformatcut + "\n\n**Запрос доступен по ссылке** https://help.hoff.ru/WorkOrder.do?woMode=viewWO&woID=" + sdrequest })
    response.status_code = 200
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

app.run(host='0.0.0.0', port=8000)
