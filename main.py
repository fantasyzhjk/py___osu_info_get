"""查看可以先把能折叠的全部折叠，注释写在外边了"""
from json import load as json_load
from json import loads as json_loads
from requests import post, get
from platform import system
from os import system as sysrun

"""-------------------------------各种def-------------------------------"""

# zh神写的清屏
def clearscreen():
    if(system()=='Windows'):
        sysrun("cls") #Windows系统
    elif(system()=='Linux'):
        sysrun('clear') #Linux系统
    else:
        pass


# 获取基本信息
def getbasicinfo(a):
    data = json_load(open('data/basicinfo.json'))
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


# 获取token
def get0token(id, pw):
    # 获取新token
    url = 'https://osu.ppy.sh/oauth/token'
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}
    body = {"grant_type": "client_credentials",
            "client_id": id, "client_secret": pw, "scope": "public"}
    index = post(url, headers=headers, json=body, timeout=300)
    tokenjsontext = index.text
    jsonn = json_loads(tokenjsontext)
    tokena = jsonn['access_token']
    return tokena


# 获取铺面信息
def getbeatmap(bid, accesstoken):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               'Authorization': 'Bearer ' + accesstoken}
    beatmap_url_to_get = 'https://osu.ppy.sh/api/v2/beatmaps/' + bid
    beatmap_url_get_result = get(url=beatmap_url_to_get, headers=headers)
    beatmap_get_result = beatmap_url_get_result.text
    beatmap_json = json_loads(beatmap_get_result)
    out = ("铺面名称：{beatmapset[title]}\n"
    "艺术家：{beatmapset[artist]}\n"
    "铺面作者：{beatmapset[creator]}\n"
    "铺面作者id：{beatmapset[user_id]}\n"
    "试听链接：https:{beatmapset[preview_url]}\n"
    "总游玩数：{beatmapset[play_count]}\n"
    "\n"
    "Bid：{id}\n"
    "Sid：{beatmapset_id}\n"
    "铺面模式：{mode}\n"
    "状态：{status}\n"
    "难度：{difficulty_rating}\n"
    "难度名：{version}\n"
    "有无故事板：{beatmapset[storyboard]}\n"
    "有无视频：{beatmapset[video]}\n"
    "该难度总游玩数：{playcount}\n"
    "该难度总pass数：{passcount}\n"
    "最后更新：{last_updated}\n"
    "Rank时间：{beatmapset[ranked_date]}\n"
    "铺面url：{url}\n"
    "铺面tags：{beatmapset[tags]}\n"
    "\n"
    "单note数：{count_circles}\n"
    "滑条数：{count_sliders}\n"
    "转盘数：{count_spinners}\n"
    "\n"
    "总长度：{total_length}\n"
    "去除休息段的长度：{hit_length}\n"
    "\n"
    "AR：{ar}\n"
    "OD：{accuracy}\n"
    "CS：{cs}\n"
    "bpm：{bpm}\n"
    "HP：{drain}\n"
    "最大连击：{max_combo}").format(**beatmap_json)
    return out


# 搜索玩家
def searchUser(username, accesstoken):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               'Authorization': 'Bearer ' + accesstoken}
    params = {'mode': 'user', 'query': username}
    user_url_to_get = 'https://osu.ppy.sh/api/v2/search'
    user_url_get_result = get(url=user_url_to_get, headers=headers, params=params)
    user_get_result = user_url_get_result.text
    user_json = json_loads(user_get_result)
    if user_json['user']['data'] == []:
        raise RuntimeError('咱们找不到这人，要不要看看有没有输错啥')
    return user_json['user']['data'][0]['id']


# 获取玩家信息
def getuser(userid, accesstoken):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               'Authorization': 'Bearer ' + accesstoken}
    user_url_to_get = 'https://osu.ppy.sh/api/v2/users/' + userid + '/osu'
    user_url_get_result = get(url=user_url_to_get, headers=headers)
    user_get_result = user_url_get_result.text
    user_json = json_loads(user_get_result)
    # print (user_json) 好家伙zh牛逼
    out = ("-------------------------------------------------------"
    "\n{username}\n"
    "总PP：{statistics[pp]}\n"
    "游戏排名：{statistics[global_rank]}\n"
    "游戏次数：{statistics[play_count]}\n"
    "准确率：{statistics[hit_accuracy]}%\n"
    "Rank分数：{statistics[ranked_score]}\n"
    "总分数：{statistics[total_score]}\n"
    "-------------------------------------------------------").format(**user_json)
    print(out)
    more_info_sec = str(input("想要更详细的信息？按下Y再回车吧！(也可以直接回车走人哦)"))
    if more_info_sec == 'Y' or more_info_sec == 'y':
        clear_screen = clearscreen()  # 清屏
        out = ("-------------------------------------------------------\n"
        "用户名：{username}\n"
        "用户id：{id}\n"
        "头像：{avatar_url}\n"
        "地区：{location}\n"
        "注册时间：{join_date}\n"
        "游玩模式：{playmode}\n"
        "设备：{playstyle}\n"
        "喜欢的铺面数：{loved_beatmapset_count}\n"
        "曾用名：{previous_usernames}\n"
        "最近是否活跃：{is_active}\n"
        "目前是否在线：{is_online}\n"
        "是否为撒泼特：{is_supporter}\n"
        "兴趣：{interests}\n\n"

        "等级：{statistics[level][current]}\n"
        "PP：{statistics[pp]}\n"
        "Rank分数：{statistics[ranked_score]}\n"
        "总分数：{statistics[total_score]}\n"
        "准确率：{statistics[hit_accuracy]}%\n"
        "游玩数：{statistics[play_count]}\n"
        "游玩时间：{statistics[play_time]}s\n"
        "世界排名：{statistics[global_rank]}\n"
        "国内排名：{statistics[country_rank]}\n"
        "最高连击：{statistics[maximum_combo]}x\n\n"

        "SS数：{statistics[grade_counts][ss]}\n"
        "SSH数：{statistics[grade_counts][ssh]}\n"
        "S数：{statistics[grade_counts][s]}\n"
        "SH数：{statistics[grade_counts][sh]}\n"
        "A数：{statistics[grade_counts][a]}\n"
        "-------------------------------------------------------").format(**user_json)
        print(out)
    else:
        pass
    return


# 获取玩家最近游玩
def get_user_recent(userid,accesstoken):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               'Authorization': 'Bearer ' + accesstoken}
    recent_url_to_get = 'https://osu.ppy.sh/api/v2/users/' + userid + '/scores/recent'
    # 用户选择是否包括fail的成绩
    include_fails_select = str(input('是否包括fail的成绩 Y/N (默认Y)：'))
    if include_fails_select == 'Y' or include_fails_select =='y':
        include_fails = "1"
    elif include_fails_select == 'N' or include_fails_select == 'n':
        include_fails = "0"
    else:
        include_fails = "1"
    # 用户选择查询最近游玩的数量
    limit_input = input('请输入要查询最近游玩的数量（1-10 默认1)：')
    if limit_input != '':
        limit_input = int(limit_input)
        if limit_input >= 1 and limit_input <= 10:
            limit = str(limit_input)
        else:
            limit = '1'
    else:
        limit = '1'
    params = {'include_fails': include_fails, 'mode': 'osu', 'limit': limit, 'offset':'1'}
    recent_url_get_result = get(url=recent_url_to_get, headers=headers, params=params)
    recent_get_result = recent_url_get_result.text
    recent_json = json_loads(recent_get_result)
    clearaaaa = clearscreen()
    # print(recent_json)
    if recent_json != []:
        for recent_score in recent_json:
            out = ('-------------------------------------------------------\n'
            '分数id： {id}\n'
            '玩家id： {user_id}\n'
            '玩家名： {user[username]}\n'
            '\n铺面信息：\n'
            '标题： {beatmapset[title]}\n'
            '难度： {beatmap[difficulty_rating]}\n'
            '难度名： {beatmap[version]}\n'
            '铺面sid： {beatmap[id]}\n'
            '铺面bid： {beatmapset[id]}\n'
            '游戏模式： {beatmap[mode]}\n'
            '铺面状态： {beatmap[status]}\n'
            '圈圈数： {beatmap[count_circles]}\n'
            '滑条数： {beatmap[count_sliders]}\n'
            '转盘数： {beatmap[count_spinners]}\n'
            'AR： {beatmap[ar]}\n'
            'CS： {beatmap[cs]}\n'
            'OD： {beatmap[accuracy]}\n'
            'Bpm： {beatmap[bpm]}\n'
            'HP： {beatmap[drain]}\n'
            '总长度： {beatmap[total_length]}\n'
            '去除休息时间： {beatmap[hit_length]}\n'
            '总游玩数： {beatmap[playcount]}\n'
            '总pass数： {beatmap[passcount]}\n'
            'url： {beatmap[url]}\n'
            '\n成绩：\n'
            '分数： {score}\n'
            'Acc:  {accuracy}\n'
            '最大连击： {max_combo}\n'
            'mods: {mods}\n'
            'Rank: {rank}\n'
            'pp: {pp}\n'
            '是否Perfect： {perfect}\n'
            '游玩时间： {created_at}\n'
            'Replay： {replay}\n'
            '300： {statistics[count_300]}\n'
            '100： {statistics[count_100]}\n'
            '50： {statistics[count_50]}\n'
            'miss： {statistics[count_miss]}\n'
            '-------------------------------------------------------').format(**recent_score)
            print(out)
        print('最上边的是最后游玩的成绩，往下以此类推')
    else:
        print('该玩家最近没有游玩记录')


# 列举玩家bp
def list_user_bp(userid,accesstoken):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               'Authorization': 'Bearer ' + accesstoken}
    bp_url_to_get = 'https://osu.ppy.sh/api/v2/users/' + userid + '/scores/best'
    offset_input = input('请输入从bp几开始（范围1-100 默认bp1)：')
    if offset_input != '':
        offset_input = int(offset_input)
        if offset_input >= 1 and offset_input <= 100:
            offset = offset_input - 1
        else:
            offset = 0
    else:
        offset = 0
    # 用户选择查询bp的数量
    limit_input = input(f'请输入要查询bp的数量（从bp{offset + 1}开始,范围1-{100 - offset} 默认5)：')
    if limit_input != '':
        limit_input = int(limit_input)
        if limit_input >= 1 and limit_input <= 51:
            limit = limit_input
        elif limit_input > 51 and limit_input <= 100:
            limit = 50
            limit2 = limit_input - 51
        else:
            limit = 5
    else:
        limit = 5

    print('获取中...')
    params = {'include_fails': '1', 'mode': 'osu', 'limit': limit, 'offset': offset}
    bp_url_get_result = get(url=bp_url_to_get, headers=headers, params=params)
    bp_json = json_loads(bp_url_get_result.text)
    if 'limit2' in vars():
        params = {'include_fails': '1', 'mode': 'osu', 'limit': limit2, 'offset': offset + 51}
        bp_url_get_result = get(url=bp_url_to_get, headers=headers, params=params)
        bp_json2 = json_loads(bp_url_get_result.text)
        
    clearscreen()
    # print(bp_get_result)
    outstr = ('-------------------------------------------------------\n'
            '分数id： {id}\n\n'
            '标题： {beatmapset[title]}\n'
            '难度： {beatmap[difficulty_rating]}\n'
            '难度名： {beatmap[version]}\n'
            '铺面sid： {beatmap[id]}\n'
            '铺面bid： {beatmapset[id]}\n'
            '游戏模式： {beatmap[mode]}\n'
            '圈圈数： {beatmap[count_circles]}\n'
            '滑条数： {beatmap[count_sliders]}\n'
            '转盘数： {beatmap[count_spinners]}\n'
            'AR： {beatmap[ar]}\n'
            'CS： {beatmap[cs]}\n'
            'OD： {beatmap[accuracy]}\n'
            'Bpm： {beatmap[bpm]}\n'
            'HP： {beatmap[drain]}\n'
            '总长度： {beatmap[total_length]}\n'
            '去除休息时间： {beatmap[hit_length]}\n'
            'url： {beatmap[url]}\n'
            '分数： {score}\n'
            'Acc:  {accuracy}\n'
            '最大连击： {max_combo}\n'
            'mods: {mods}\n'
            'Rank: {rank}\n'
            'pp: {pp}\n'
            '是否Perfect： {perfect}\n'
            '游玩时间： {created_at}\n'
            'Replay： {replay}\n'
            '300： {statistics[count_300]}\n'
            '100： {statistics[count_100]}\n'
            '50： {statistics[count_50]}\n'
            'miss： {statistics[count_miss]}\n'
            '-------------------------------------------------------')
    if bp_json != []:
        for bp_score in bp_json:
            out = outstr.format(**bp_score)
            print(out)
    else:
        print('查询失败')
        return
    if 'limit2' in vars():
        if bp_json2 != []:
            for bp_score in bp_json2:
                out = outstr.format(**bp_score)
                print(out)
    print('最上边的是bp1，往下以此类推')


# 获取玩家指定bp
def get_user_bp(userid,accesstoken):
    headers = {"Accept": "application/json", "Content-Type": "application/json",
               'Authorization': 'Bearer ' + accesstoken}
    bp_url_to_get = 'https://osu.ppy.sh/api/v2/users/' + userid + '/scores/best'
    # 用户选择查询bp的数量
    offset_input = input('请输入要查询的bp（1-100 默认1)：')
    if offset_input != '':
        offset_input = int(offset_input)
        if offset_input >= 1 and offset_input <= 100:
            offset = offset_input - 1
        else:
            offset = 0
    else:
        offset = 0
    params = {'include_fails': '1', 'mode': 'osu', 'limit': 1, 'offset': offset}
    bp_url_get_result = get(url=bp_url_to_get, headers=headers, params=params)
    bp_get_result = bp_url_get_result.text
    bp_json = json_loads(bp_get_result)
    clearaaaa = clearscreen()
    # print(bp_get_result)
    # print(bp_json)
    if bp_json != []:
        out = ('-------------------------------------------------------\n'
        '分数id： {id}\n'
        '玩家id： {user_id}\n'
        '玩家名： {user[username]}\n'
        '\n铺面信息：\n'
        '标题： {beatmapset[title]}\n'
        '难度： {beatmap[difficulty_rating]}\n'
        '难度名： {beatmap[version]}\n'
        '铺面sid： {beatmap[id]}\n'
        '铺面bid： {beatmapset[id]}\n'
        '游戏模式： {beatmap[mode]}\n'
        '铺面状态： {beatmap[status]}\n'
        '圈圈数： {beatmap[count_circles]}\n'
        '滑条数： {beatmap[count_sliders]}\n'
        '转盘数： {beatmap[count_spinners]}\n'
        'AR： {beatmap[ar]}\n'
        'CS： {beatmap[cs]}\n'
        'OD： {beatmap[accuracy]}\n'
        'Bpm： {beatmap[bpm]}\n'
        'HP： {beatmap[drain]}\n'
        '总长度： {beatmap[total_length]}\n'
        '去除休息时间： {beatmap[hit_length]}\n'
        '总游玩数： {beatmap[playcount]}\n'
        '总pass数： {beatmap[passcount]}\n'
        'url： {beatmap[url]}\n'
        '\n成绩：\n'
        '分数： {score}\n'
        'Acc:  {accuracy}\n'
        '最大连击： {max_combo}\n'
        'mods: {mods}\n'
        'Rank: {rank}\n'
        'pp: {pp}\n'
        '是否Perfect： {perfect}\n'
        '游玩时间： {created_at}\n'
        'Replay： {replay}\n'
        '300： {statistics[count_300]}\n'
        '100： {statistics[count_100]}\n'
        '50： {statistics[count_50]}\n'
        'miss： {statistics[count_miss]}\n'
        '-------------------------------------------------------').format(**bp_json[0])
        print(out)
    else:
        print('查询失败')


# 获取pp+信息
def get_pp_plus(userid):    
    url = 'https://syrin.me/pp+/api/user/' + userid + '/'
    index = get(url=url)
    pp_plus = json_loads(index.text)
    return pp_plus['user_data']


# 对pp+信息进行排版
def pp_plus_out(inputa):
    out = ('-------------------------------------------------------\n'
    '玩家{UserName}的pp+数据如下\n\n'
    'Total:      {PerformanceTotal:.2f}\n'
    'Aim:        {AimTotal:.2f}\n'
    'Jump:       {JumpAimTotal:.2f}\n'
    'Flow:       {FlowAimTotal:.2f}\n'
    'Precision:  {PrecisionTotal:.2f}\n'
    'Speed:      {SpeedTotal:.2f}\n'
    'Stamina:    {StaminaTotal:.2f}\n'
    'Accuracy:   {AccuracyTotal:.2f}\n'
    '-------------------------------------------------------').format(**inputa)
    return out




"""-------------------------------程序主体-------------------------------"""

print('初始化...')

# 获取最基本的信息
oauthpw = getbasicinfo('pw')
oauthid = getbasicinfo('id')
username = getbasicinfo('name')
userid = getbasicinfo('userid')
print('获取oauth token...')
token = get0token(oauthid, oauthpw)

print('Done')

clearscreen()  # 清屏

# 选择功能
functionselect = str(input('''欢迎使用，本程序98%由zh编写
（zh：？？？）（frz:你不知道这叫商业互吹吗！！！）
在此谢谢zh
zh我爱你！！！！

速度99%取决于你连接ppy的速度
pp+就是连接pp+的速度咯

接下来选择你要用的功能，然后按下回车
1.查询特定铺面
2.查询玩家信息
3.名字转id
4.获取最近游玩
5.获取并列举玩家bp
6.获取玩家指定bp
7.获取pp+ (访问很慢)

你的选择：'''))

clearscreen()  # 清屏

# 功能实现
try:
    if functionselect == '1':
        bid = str(input('请输入铺面的bid：'))
        print('尝试查询ing...')
        output = getbeatmap(bid, token)
        print(output)
    elif functionselect == '2':
        playerselect = str(input('1.你自己\n2.其他玩家\n你的选择：'))
        print('尝试查询ing...')
        if playerselect == '1':
            playertoget = userid
        elif playerselect == '2':
            playertoget = str(input('请输入玩家名或id：'))
        else:
            input('参数错误，请重新运行\n按下回车退出')
            exit(0)
        getuser(playertoget, token)
    elif functionselect == '3':
        player_to_search = str(input('请输入玩家名：'))
        print('尝试查询ing...')
        player_id = str(searchUser(player_to_search, token))
        print('玩家' + player_to_search + '的id为：' + player_id)
    elif functionselect == '4':
        playerselect = str(input('1.你自己\n2.其他玩家\n你的选择：'))
        print('尝试查询ing...')
        if playerselect == '1':
            playertoget = userid
            get_user_recent(playertoget, token)
        elif playerselect == '2':
            playertoget = str(input('请输入玩家名：'))
            get_user_recent(str(searchUser(playertoget, token)), token)
        else:
            input('参数错误，请重新运行\n按下回车退出')
            exit(0)
    elif functionselect == '5':
        playerselect = str(input('1.你自己\n2.其他玩家\n你的选择：'))
        print('尝试查询ing...')
        if playerselect == '1':
            playertoget = userid
            list_user_bp(playertoget, token)
        elif playerselect == '2':
            playertoget = str(input('请输入玩家名：'))
            list_user_bp(str(searchUser(playertoget, token)), token)
        else:
            input('参数错误，请重新运行\n按下回车退出')
            exit(0)
    elif functionselect == '6':
        playerselect = str(input('1.你自己\n2.其他玩家\n你的选择：'))
        print('尝试查询ing...')
        if playerselect == '1':
            playertoget = userid
            get_user_bp(playertoget, token)
        elif playerselect == '2':
            playertoget = str(input('请输入玩家名：'))
            get_user_bp(str(searchUser(playertoget, token)), token)
        else:
            input('参数错误，请重新运行\n按下回车退出')
            exit(0)
    elif functionselect == '7':
        print('获取中，可能需要亿点时间...(谁让他慢啊！啥时候死了都不知道！）')
        pp_plus_json = get_pp_plus(userid)
        clearscreen()  # 清屏
        print(pp_plus_out(pp_plus_json))
    else:
        raise
except Exception as e:  # 报错
    # clearscreen()  # 清屏
    print("查询出错 以下为错误信息 请提交issue")
    print(e)

input('回车键退出')

####################### 以下为zh摸鱼记录 #######################

#if (system()=='Windows'):
#    os.system("pause")
