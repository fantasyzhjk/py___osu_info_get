"""程序主体"""
import json

def getbasicinfo(a):
    data = json.load(open('data/basicinfo.json'))
    if a == 'name':
        result = data[0]
    elif a == 'id':
        result = data[1]
    elif a == 'pw':
        result = data[2]
    else:
        print('''请检查main.py是否有错误
        此处的错误指调用getbasicinfo模块时参数是否为"id"、"name"或"pw"
        不懂请在github上提交issue''')
    return(result)
