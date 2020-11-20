import requests
import time
import json
import urllib3
import datetime
urllib3.disable_warnings()

session = requests.Session()

print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(time.time()))))

ck = open('DDG_Cookie.ddg','r')
Cookie = ck.read()

headers = {
    'User-Agent': 'jdapp;Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; BAC-TL00 Build/HUAWEIBAC-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.6.4.950 UCBS/2.11.1.28 Mobile Safari/537.36 AliApp(TB/7.3.0.9) WindVane/8.3.0 1080X1812',
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://h5.m.jd.com',
    'Referer': 'https://pro.m.jd.com/mall/active/3gSzKSnvrrhYushciUpzHcDnkYE3/index.html',
    'Cookie':Cookie
}

def get_currentdate():
    # 2020-11-08T17%253A25%253A46.606
    yearMD = datetime.datetime.now().strftime('%Y-%m-%d')

    hour=datetime.datetime.now().strftime('%H')
    mi = datetime.datetime.now().strftime('%M')
    mill = datetime.datetime.now().strftime('%S')
    return ',%22currentDate%22:%22'+yearMD+'T'+hour+'%253A'+mi+'%253A'+mill+'.606%22%7D'


def get_taskList():
    url = 'https://api.m.jd.com/api?appid=jd_mp_h5&functionId=necklace_homePage&loginType=2&client=jd_mp_h5&uuid=99001026708276-ecd09f877fd9&t=1604802224643&body=%7B%7D'
    response = session.get(url,verify=False, headers=headers)
    print(response)
    if response.status_code == 200:
        response =response.json()

        res = response.get('data','').get('result','').get('taskConfigVos','')
        starIds = []
        for i in res:
            starIds.append(i.get('id',''))
        print(starIds)
        return starIds
    else:
        print('其他')

def do_click(taskid):
    url = 'https://api.m.jd.com/api?appid=jd_mp_h5&functionId=necklace_startTask&loginType=2&client=jd_mp_h5&uuid=99001026708276-ecd09f877fd9&t=1604825803194&body=%7B%22taskId%22:'+str(taskid)+get_currentdate()
    
    data=''
    response = session.post(url,data=data,headers=headers,verify=False).json()
    print(response)

def get_bubbles():
    url = 'https://api.m.jd.com/api?appid=jd_mp_h5&functionId=necklace_homePage&loginType=2&client=jd_mp_h5&uuid=99001026708276-ecd09f877fd9&t=1604802224643&body=%7B%7D'
    response = session.get(url,verify=False, headers=headers)
    print(response)
    if response.status_code == 200:
        response =response.json()

        res = response.get('data','').get('result','').get('bubbles','')
        starIds = []
        for i in res:
            starIds.append(i.get('id',''))
        print(starIds)
        return starIds
    else:
        print('其他')

def charge_bubble(bubbldid):
    url = 'https://api.m.jd.com/api?appid=jd_mp_h5&functionId=necklace_chargeScores&loginType=2&client=jd_mp_h5&uuid=99001026708276-ecd09f877fd9&t=1604827560546&body=%7B%22bubleId%22:'+str(bubbldid)+get_currentdate()
    data=''
    response = session.post(url,data=data,headers=headers,verify=False).json()
    print(response)

def sign_in():
    url = 'https://api.m.jd.com/api?appid=jd_mp_h5&functionId=necklace_sign&loginType=2&client=jd_mp_h5&uuid=99001026708276-ecd09f877fd9&t=1604828702823&body=%7B'+get_currentdate()
    data=''
    response = session.post(url,data=data,headers=headers,verify=False).json()
    print(response)

print("每日签到...")
sign_in()

print("点任务...")
tasklist = get_taskList()
for task in tasklist:
    # taskid = task.get('id','')
    print(task)
    do_click(task)
    time.sleep(2)


##收取 1.重新加载页面，获取 bubbles 
print("收取...")
bubbleids = get_bubbles()
for bubble in bubbleids:
    print(bubble)
    charge_bubble(bubble)
    time.sleep(2)

print("结束了")
input("请按回车键退出")
##
