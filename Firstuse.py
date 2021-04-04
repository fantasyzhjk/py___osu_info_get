"""第一次使用的基本设置，查看可以先把能折叠的全部折叠，注释写在外边了"""

import json
import time
import os

print('''该程序用于设置基本信息，和初始化token.json（不初始化使用main.py的特定功能会百分百报错）

注：1.一旦设置请不要更改，否则数据会乱，如要更改用户名，请另外下载一份。
   2.该程序可以随意更改文件夹，但是要保证路径不带有中文，且移动整个文件夹
   
   按下回车开始设置''')  # 使用说明
input()

clearaaaaa = os.system("cls")  # 清屏

# 用户输入basicinfo Done
user = str(input("请输入玩家名："))
v2id = str(input("请输入你oauth程序的id："))
v2pw = str(input("请输入你oauth程序的密钥："))
userid = str(input("请输入玩家的id："))


# 将basicinfo写入文件
basicinfo = {"user": user, "userid": userid, "v2id": v2id, "v2pw": v2pw}
basicinfo_json = json.dumps(basicinfo)
filebasicinfo = open("data/basicinfo.json", mode="w")
filebasicinfo.write(basicinfo_json)
filebasicinfo.close()

# 初始化token.json
datenow = time.strftime("%Y-%m-%d")
tokenjson = {'token': "0000000000", 'getdate': datenow}
tokenfile = json.dumps(tokenjson)
filetoken = open("data/token.json", mode='w')
filetoken.write(tokenfile)
filetoken.close()

input('''\n尝试写入完成，请查看data文件夹下的basicinfo.json和token.json文件进行检查\n\n按下回车退出''')
