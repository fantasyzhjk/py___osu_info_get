"""程序主体,查看可以先把能折叠的全部折叠，注释写在外边了"""
import json
import time
import requests


# 获取基本信息 Done
def getbasicinfo(a):
    data = json.load(open('data/basicinfo.json'))
    if a == 'name':
        result = data['user']
    elif a == 'userid':
        result = data['userid']
    elif a == 'id':
        result = data['v2id']
    elif a == 'pw':
        result = data['v2pw']
    else:
        print('''请检查main.py是否有错误
        此处的错误指调用getbasicinfo模块时参数是否为"id"、"name"或"pw"
        不懂请在github上提交issue''')
    return result


# 检测token.json里的token是否可用，不可用则获取token并重新写入 -ing
def gettoken(oauthid, oauthpw):
    tokenfile = json.load(open('data/token.json'))
    datenow = time.strftime("%Y-%m-%d")
    if tokenfile['getdate'] != datenow or tokenfile['token'] == '0000000000':
        # 获取新token
        url = 'https://osu.ppy.sh/oauth/token'
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        body = {"grant_type": "client_credentials", "client_id": oauthid, "client_secret": oauthpw, "scope": "public"}
        index = requests.post(url, headers=headers, data=body, timeout=300, verify=False)
        tokenjsontext = index.text
        jsonn = json.loads(tokenjsontext)
        token = jsonn['accesstoken']
        # 写入token.json
        tokenWhichIsJson = {'token': token, 'getdate': datenow}
        whichToWrite = json.dumps(tokenWhichIsJson)
        tokenjson = open('data/token.json', mode='w')
        tokenjson.write(whichToWrite)
    else:
        file = json.load(open('data/token.json'))
        token = file['token']
    return token


oauthpw = getbasicinfo('pw')
oauthid = getbasicinfo('id')
username = getbasicinfo('name')
userid = getbasicinfo('userid')

token = gettoken(oauthid, oauthpw)

print('username:' + username)
print('userid' + userid)
print('oauthid:' + oauthid)
print('oauthpw:' + oauthpw)
print('token:' + token)
