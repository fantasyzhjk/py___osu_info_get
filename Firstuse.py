"""第一次使用的基本设置，查看可以先把能折叠的全部折叠，注释写在外边了"""

import json
import requests
import os
import platform


def cleanscreen():
    if(platform.system()=='Windows'):
        os.system("cls") #Windows系统
    elif(platform.system()=='Linux'):
        os.system('clear') #Linux系统
    else:
        pass


def searchUser(username, accesstoken):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               'Authorization': 'Bearer ' + accesstoken}
    params = {'mode': 'user', 'query': username}
    user_url_to_get = 'https://osu.ppy.sh/api/v2/search'
    user_url_get_result = requests.get(url=user_url_to_get, headers=headers, params=params)
    user_get_result = user_url_get_result.text
    user_json = json.loads(user_get_result)
    return user_json['user']['data'][0]['id']


def get0token(id, pw):
    # 获取新token
    url = 'https://osu.ppy.sh/oauth/token'
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}
    body = {"grant_type": "client_credentials",
            "client_id": id, "client_secret": pw, "scope": "public"}
    index = requests.post(url, headers=headers, json=body, timeout=300)
    tokenjsontext = index.text
    jsonn = json.loads(tokenjsontext)
    tokena = jsonn['access_token']
    return tokena


clearaaaaa = cleanscreen()  # 清屏

print('''该程序用于设置基本信息，和初始化token.json（不初始化使用main.py的特定功能会百分百报错）

注：1.一旦设置请不要更改，否则数据会乱，如要更改用户名，请另外下载一份。
   2.该程序可以随意更改文件夹，但是要保证路径不带有中文，且移动整个文件夹
   
   按下回车开始设置''')  # 使用说明
input()


clearaaaaa = cleanscreen()  # 清屏

# 用户输入basicinfo Done
user = str(input("请输入玩家名："))
v2id = str(input("请输入你oauth程序的id："))
v2pw = str(input("请输入你oauth程序的密钥："))

print('\n正在尝试写入...')

token = str(get0token(v2id, v2pw))

userid = str(searchUser(user, token))


# 将basicinfo写入文件
basicinfo = {"user": user, "userid": userid, "v2id": v2id, "v2pw": v2pw}
basicinfo_json = json.dumps(basicinfo)
filebasicinfo = open("data/basicinfo.json", mode="w")
filebasicinfo.write(basicinfo_json)
filebasicinfo.close()

input('''\n尝试写入完成，请查看data文件夹下的basicinfo.json文件进行检查\n\n按下回车退出''')
