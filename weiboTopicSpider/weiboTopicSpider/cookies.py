#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
import re
import rsa
import json
import base64
import binascii
import requests

myWeibo = [
    {'no': 'count', 'psw': 'password,'},
    # {'no': 'count', 'psw': 'password,'},
]

# class Userlogin:


def getCookies(weibos):
    cookies = []
    session = requests.Session()
    url_prelogin = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)"
    url_login = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)"

    resp = session.get(url_prelogin)
    json_data = re.findall(r'(?<=\().*(?=\))', resp.text)[0]
    data = json.loads(json_data)

    # Prepare the post data
    for elem in weibos:
        username = elem['no']
        password = elem['psw']
        servertime = data['servertime']
        nonce = data['nonce']
        pubkey = data['pubkey']
        print(pubkey)
        rsakv = data['rsakv']
        su = base64.b64encode(username.encode(encoding="utf-8"))
        rsaPublicKey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublicKey, 65537)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
        sp = binascii.b2a_hex(rsa.encrypt(
            message.encode(encoding="utf-8"), key))

        postdata = {
            "entry": "account",
            "gateway": "1",
            "from": "",
            "savestate": "30",
            "qrcode_flag": "true",
            "userticket": "1",
            "pagerefer": "http://my.sina.com.cn/profile/unlogin",
            "vsnf": "1",
            "vsnval": "",
            "su": su,
            "service": "sso",
            "servertime": servertime,
            "nonce": nonce,
            "pwencode": "rsa2",
            "rsakv": rsakv,
            "sp": sp,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "305",
            "returntype": "TEXT",
        }
        # The full login url
        url_login = url_login + "&_=" + str(servertime)
        resp = session.post(url_login, data=postdata)
        print(resp.content)
        json_text = resp.content.decode('gbk')
        res_info = json.loads(json_text)
        # Get the Cookie
        if res_info["retcode"] == '0':
            print("Get Cookie Success!( Account:%s )" % username)
            cookie = session.cookies.get_dict()
            cookies.append(cookie)
            print(cookies)
        else:
            print("Failed!( Reason:%s )" % info["reason"].encode("utf-8"))
    return cookies

## 第二种方法
# def getCookies(weibo):
#     """ 获取Cookies """
#     cookies = []
#     loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
#     for elem in weibo:
#         account = elem['no']
#         password = elem['psw']
#         username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
#         postData = {
#             "entry": "sso",
#             "gateway": "1",
#             "from": "null",
#             "savestate": "30",
#             "useticket": "0",
#             "pagerefer": "",
#             "vsnf": "1",
#             "su": username,
#             "service": "sso",
#             "sp": password,
#             "sr": "1440*900",
#             "encoding": "UTF-8",
#             "cdult": "3",
#             "domain": "sina.com.cn",
#             "prelt": "0",
#             "returntype": "TEXT",
#         }
#         session = requests.Session()
#         r = session.post(loginURL, data=postData)
#         jsonStr = r.content.decode('gbk')
#         info = json.loads(jsonStr)
#         if info["retcode"] == "0":
#             print("Get Cookie Success!( Account:%s )" % account)
#             cookie = session.cookies.get_dict()
#             cookies.append(cookie)
#         else:
#             print("Failed!( Reason:%s )" % info["reason"].encode("utf-8"))
#     print(cookies)
#     return cookies

cookies = getCookies(myWeibo)
