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


port = int(os.getenv('PORT', 80))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=False)