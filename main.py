# -*- encoding: utf-8 -*-
from flask import Flask, render_template, request,redirect,session, Response, jsonify
import requests
import json
import os
import datetime
import time
import re
import pytz
from dateutil.parser import parse
import jsonpath
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
from Crypto import Random

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'hard to guess string'

def request_parse(req_data):
    '''解析请求数据并以json形式返回'''
    if req_data.method == 'POST':
        if (req_data.content_type.find('www-form-urlencoded') > -1):
            data = req_data.form
        elif (req_data.content_type.find('json') > -1):
            data = req_data.json
        else:
            data = req_data.form
    elif req_data.method == 'GET':
        data = req_data.args
    return data

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('./index.html')

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
        if (len(ds) > 0) and (len(p) > 0):
            for cnt in range (0, len(data)):
                temp[cnt+1] = data[cnt]
            Rtv["数据"] = temp
            Rtv["状态"] = "OK"
        else:
            Rtv["状态"] = "输入的参数为空"
    except Exception as e:
        Rtv["状态"] = str(e)

    return Response(json.dumps(Rtv, ensure_ascii=False, indent=4), mimetype='application/json')

@app.route('/convert/s264', methods=['GET', 'POST'])
def s264():
    # 字符串转base64
    Rtv = {}
    s = request.args.get("s", default="")
    b64 = request.args.get("b64", default="")

    try:
       if (s == "") and (b64 == ""):
            Rtv["状态"] = "请输入参数"
       else:
           if (b64 == ""):
               Rtv["base64"] = str(base64.b64encode(bytes(s, encoding = "utf8")), encoding = "utf-8")
               Rtv["字符串"] = s
           else:
               Rtv["base64"] = b64
               Rtv["字符串"] = str(base64.b64decode(b64), encoding = "utf-8")
           Rtv["状态"] = "OK"
    except Exception as e:
        Rtv["状态"] = str(e)

    return Response(json.dumps(Rtv, ensure_ascii=False, indent=4), mimetype='application/json')

@app.route('/string', methods=['GET', 'POST'])
def strf():
    Rtv = {}
    f = request.args.get("f", default="")
    s = request.args.get("s", default="")
    p = request.args.get("p", default="")
    t = request.args.get("t", default="")
    r = request.args.get("r", default="json")
    Rtv["原始字符串"] = s
    try:
        if (f):
            if (f.find("replace") > -1):
                Rtv["处理后字符串"] = re.sub(p, t, s)
                Rtv["状态"] = "OK"
        else:
            Rtv["处理后字符串"] = ""
            Rtv["状态"] = "请选择功能"
            
    except Exception as e:
        Rtv["处理后字符串"] = ""
        Rtv["状态"] = str(e)
    
    if (r.find("text") > -1):
        return Rtv["处理后字符串"]
    else:
        Rtv = json.dumps(Rtv, ensure_ascii=False, indent=4)
        return Response(Rtv, mimetype='application/json')
    
    
@app.route('/rsa/encode', methods=["GET","POST"])
def RSAEncode():
    try:
        res_data = request_parse(request)
        key = res_data.get("key", None)
        data = res_data.get("data", None)
        if (key) and (data):
            lines = ""
            if request.method == 'POST':
                for line in key.split("\n"):
                    if (line.find("--") < 0):
                        line = line.replace(" ", "+")
                    lines = lines+line+"\n"
            elif request.method == 'GET':
                temp = key
                temp = temp.replace("-----BEGIN PUBLIC KEY-----", "")
                temp = temp.replace("-----END PUBLIC KEY-----", "")
                lines = "-----BEGIN PUBLIC KEY-----\n"

                while(temp):
                    line = temp[0:63]
                    lines = lines+line+"\n"
                    temp = temp.replace(line, "")

                lines = lines+ "-----END PUBLIC KEY-----"
            else:
                raise Exception(u"请求方式错误")

            private_key = RSA.import_key(lines)
            cipher_rsa = PKCS1_v1_5.new(private_key)
            crypt_text = cipher_rsa.encrypt(bytes(data, encoding="utf-8"))
            crypt_text = base64.b64encode(crypt_text).decode('utf8')
            print(crypt_text)
            return crypt_text
        else:
            raise Exception("参数不完整，请确认")
    except Exception as e:
        return str(e)

@app.route('/rsa', methods=["GET","POST"])
def RSADecode():
    try:
        res_data = request_parse(request)
        key = res_data.get("key", None)
        data = res_data.get("data", None)
        func = res_data.get("f", None)
        if (key) and (data) and (func):
            lines = ""
            if request.method == 'POST':
                for line in key.split("\n"):
                    if (line.find("--") < 0):
                        line = line.replace(" ", "+")
                    lines = lines+line+"\n"
                data = data.replace(" ", "+")
            elif request.method == 'GET':
                temp = key
                temp = re.findall("-----.*?-----", temp)
                if (len(temp) == 2):
                    keytemp = key
                    for t in temp:
                        keytemp = keytemp.replace(t, "")

                    while(keytemp):
                        line = keytemp[0:63]
                        lines = lines+line+"\n"
                        keytemp = keytemp.replace(line, "")
                    
                    lines = temp[0]+"\n" + lines + temp[1]

                else:
                    return "证书格式错误"
            else:
                return "请求方式错误"

            cipher_rsa = PKCS1_v1_5.new(RSA.import_key(lines))
            if (func.find("encode") > -1):
                crypt_text = cipher_rsa.encrypt(bytes(data, encoding="utf-8"))
                crypt_text = base64.b64encode(crypt_text).decode('utf8')
                return crypt_text
            elif (func.find("decode") > -1): 
                decrypt_text = cipher_rsa.decrypt(base64.b64decode(data), Random.new().read)
                decrypt_text = decrypt_text.decode('utf8')
                return decrypt_text
            else:
                return "功能选择错误"
        else:
            return "参数不完整，请确认"
    except Exception as e:
        return str(e)

port = int(os.getenv('PORT', 80))
if __name__ == "__main__":
    app.config['JSON_AS_ASCII']=False
    app.run(host='0.0.0.0', port=port, debug=False)