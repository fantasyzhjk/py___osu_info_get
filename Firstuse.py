"""第一次使用的基本设置"""

import json

user = str(input("请输入玩家名："))
v2id = str(input("\n请输入你oauth程序的id："))
v2pw = str(input("\n请输入你oauth程序的密钥："))

basicinfo = {"user":user,"v2id":v2id,"v2pw":v2pw}

basicinfo_json = json.dumps(basicinfo)

file = open("data/basicinfo.json",mode="w")

file.write(basicinfo_json)

input('\n尝试写入完成，请查看data文件夹下的basicinfo.json文件进行检查\n\n按下回车退出')