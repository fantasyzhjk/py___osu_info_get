"""查看可以先把能折叠的全部折叠，注释写在外边了"""
import json
import time
import requests
import os

"""-------------------------------各种def-------------------------------"""


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
def get0token(id, pw):
    tokenfile = json.load(open('data/token.json'))
    datenow = time.strftime("%Y-%m-%d")
    if tokenfile['getdate'] != datenow or tokenfile['token'] == '0000000000':
        # 获取新token
        url = 'https://osu.ppy.sh/oauth/token'
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Connection': 'close'}
        body = {"grant_type": "client_credentials", "client_id": id, "client_secret": pw, "scope": "public"}
        index = requests.post(url, headers=headers, json=body, timeout=300)
        tokenjsontext = index.text
        jsonn = json.loads(tokenjsontext)
        if tokenjsontext == """{"error': 'Client authentication failed'}""":
            input('oauth身份验证失败，请去个人资料的设置界面检查oauth程序的id与密钥是否与basic.info内的一致\n按下回车退出')
            exit(0)
        else:
            tokena = jsonn['access_token']
            # 写入token.json
            tokenWhichIsJson = {'token': tokena, 'getdate': datenow}
            whichToWrite = json.dumps(tokenWhichIsJson)
            tokenjson = open('data/token.json', mode='w')
            tokenjson.write(whichToWrite)
    else:
        file = json.load(open('data/token.json'))
        tokena = file['token']
    return tokena


# 获取铺面信息
def getbeatmap(bid, accesstoken):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               'Authorization': 'Bearer ' + accesstoken, 'Connection': 'close'}
    beatmap_url_to_get = 'https://osu.ppy.sh/api/v2/beatmaps/' + bid
    beatmap_url_get_result = requests.get(url=beatmap_url_to_get, headers=headers)
    beatmap_get_result = beatmap_url_get_result.text
    beatmap_json = json.loads(beatmap_get_result)
    out = """-------------------------------------------------------
    铺面名称：{beatmapset[title]}
    艺术家：{beatmapset[artist]}
    铺面作者：{beatmapset[creator]}
    铺面作者id：{beatmapset[user_id]}
    试听链接：https:{beatmapset[preview_url]}
    总游玩数：{beatmapset[play_count]}
    
    Bid：{id}
    Sid：{beatmapset_id}
    铺面模式：{mode}
    状态：{status}
    难度：{difficulty_rating}
    难度名：{version}
    有无故事板：{beatmapset[storyboard]}
    有无视频：{beatmapset[video]}
    该难度总游玩数：{playcount}
    该难度总pass数：{passcount}
    最后更新：{last_updated}
    Rank时间：{beatmapset[ranked_date]}
    铺面url：{url}
    铺面tags：{beatmapset[tags]}
    
    单note数：{count_circles}
    滑条数：{count_sliders}
    转盘数：{count_spinners}
    
    总长度：{total_length}
    去除休息段的长度：{hit_length}
    
    AR：{ar}
    OD：{accuracy}
    CS：{cs}
    bpm：{bpm}
    HP：{drain}
    最大连击：{max_combo}
    
    -------------------------------------------------------
    """.format(**beatmap_json)
    return out


# 获取玩家信息
def getuser(userid, accesstoken):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               'Authorization': 'Bearer ' + accesstoken, 'Connection': 'close'}
    user_url_to_get = 'https://osu.ppy.sh/api/v2/users/' + userid + '/osu'
    user_url_get_result = requests.get(url=user_url_to_get, headers=headers)
    user_get_result = user_url_get_result.text
    user_json = json.loads(user_get_result)
    # print (user_json) 好家伙zh牛逼
    out = """-------------------------------------------------------
{username}
总PP：{statistics[pp]}
游戏排名：{statistics[global_rank]}
游戏次数：{statistics[play_count]}
准确率：{statistics[hit_accuracy]}%
Rank分数：{statistics[ranked_score]}
总分数：{statistics[total_score]}
-------------------------------------------------------
    """.format(**user_json)
    return out


"""-------------------------------程序主体-------------------------------"""

# 获取最基本的信息
oauthpw = getbasicinfo('pw')
oauthid = getbasicinfo('id')
username = getbasicinfo('name')
userid = getbasicinfo('userid')
token = get0token(oauthid, oauthpw)

# 选择功能
functionselect = str(input('''选择你要用的功能，然后回车
1.查询特定铺面
2.查询玩家信息
你的选择：'''))

clearaaaaa = os.system("cls")  # 清屏

if functionselect == '1':
    bid = str(input('请输入铺面的bid：'))
    output = getbeatmap(bid, token)
    print(output)
elif functionselect == '2':
    playerselect = str(input('1.你自己\n2.其他玩家'))
    if playerselect == '1':
        playertoget = userid
    elif playerselect == '2':
        playertoget = str(input('请输入玩家id(注意，是id)：'))
    else:
        input('参数错误，请重新运行')
        exit(0)
    output = getuser(playertoget, token)
    print(output)

input('回车键退出')
