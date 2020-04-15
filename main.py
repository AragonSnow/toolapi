# -*- encoding: utf-8 -*-
from flask import Flask, render_template, request,redirect,session, Response
import requests
import json
import os
import datetime
import time
import re
import pytz
from dateutil.parser import parse
import jsonpath

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/', methods=['GET', 'POST'])
def form():
    return render_template('index.html')

@app.route('/timestamp', methods=['GET', 'POST'])
def timestamp():
    Rtv = {}
    try:
        ts = request.args.get("ts", default="")
        t = request.args.get("t", default="now")
        type = request.args.get("form", default="%Y-%m-%d %H:%M:%S")
        cst_tz = pytz.timezone('Asia/Shanghai')  

        if (ts):
            # 时间戳转北京时间
            Rtv["时间戳"] =  ts
            Rtv["时间"]  = datetime.datetime.fromtimestamp(int(ts), cst_tz).strftime(type)  
        else:
            # 北京时间转时间戳
            if (re.search('now', t, re.IGNORECASE)):
                Rtv["时间戳"] =  int(time.time())
                Rtv["时间"] = datetime.datetime.fromtimestamp(Rtv["时间戳"], cst_tz).strftime(type)
            else:
                if (request.args.get("form")):
                    Rtv["时间戳"] = int(time.mktime(time.strptime(t, type)))
                else:
                     d = parse(t , ignoretz=True)
                     d = d.astimezone(timezone(timedelta(hours=0)))                     
                     Rtv["时间戳"] = int(d.timestamp())
                Rtv["时间"] = t
        Rtv["状态"] = "OK"
    except Exception as e:
        Rtv["状态"] = str(e)

    return Response(json.dumps(Rtv, ensure_ascii=False, indent=4), mimetype='application/json')

@app.route('/jsondata', methods=['GET', 'POST'])
def jsondata():
    # 从json数据里取值并返回,需要懂jsonpath的用法
    Rtv = {}
    ds = request.args.get("data", default="")
    p = request.args.get("p", default="")
    try:
        ds = json.loads(ds)
        temp = {}
        data = jsonpath.jsonpath(ds,expr=p)
        if (data):
            for cnt in range (1, len(data)+1):
                temp[cnt] = data[cnt - 1]
            Rtv["数据"] = temp
            Rtv["状态"] = "OK"
        else:
            Rtv["状态"] = "没匹配到数据"
    except Exception as e:
        Rtv["状态"] = str(e)
        
    return Response(json.dumps(Rtv, ensure_ascii=False, indent=4), mimetype='application/json')

@app.route('/regex', methods=['GET', 'POST'])
def regex():
    # 字符串正则匹配后返回结果
    Rtv = {}
    ds = request.args.get("data", default="")
    p = request.args.get("p", default="")

    try:
        temp = {}
        data = re.findall(p, ds, re.IGNORECASE)
        if (len(data) > 0):
            for cnt in range (0, len(data)):
                temp[cnt+1] = data[cnt]
            Rtv["数据"] = temp
            Rtv["状态"] = "OK"
        else:
            Rtv["状态"] = "没匹配到数据"
    except Exception as e:
        Rtv["状态"] = str(e)

    return Response(json.dumps(Rtv, ensure_ascii=False, indent=4), mimetype='application/json')


port = int(os.getenv('PORT', 80))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=False)