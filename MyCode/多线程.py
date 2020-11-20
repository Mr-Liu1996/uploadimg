from threading import Thread
from queue import Queue
import requests,time,re

requests.packages.urllib3.disable_warnings()
List = []

class SspanelQd(Thread):
    def __init__(self, user, pwd):
        Thread.__init__(self)
        # 机场地址
        self.base_url = 'https://pucloud.vip'
        self.pwd = pwd
        # 登录信息
        self.user = user
        # Server酱推送（可空）
        self.sckey = ''
        # 酷推qq推送（可空）
        self.ktkey = ''
    def run(self):
        user = self.user
        email = user.split('@')
        email = email[0] + '%40' + email[1]
        password = self.pwd

        session = requests.session()

        session.get(self.base_url, verify=False)

        login_url = self.base_url + '/auth/login'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        post_data = 'email=' + email + '&passwd=' + password + '&code='
        post_data = post_data.encode()
        response = session.post(login_url, post_data, headers=headers, verify=False)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer': self.base_url + '/user'
        }

        response = session.post(self.base_url + '/user/checkin', headers=headers, verify=False)
        msg = (response.json()).get('msg')
        #print(msg)

        info_url = self.base_url + '/user'
        response = session.get(info_url, verify=False)
        data = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime())
        """
        以下只适配了editXY主题
        """
        try:
            level = re.findall(r'\["class","(.*?)"]', response.text)[0]
            day = re.findall(r'\["vip-time","(.*)"],', response.text)[0]
            rest = re.findall(r'\["traffic","(.*?)"]', response.text)[0]
            rss = re.findall(r'\<button type="button" class="btn btn-pill btn-v2ray copy-text" data-clipboard-text="(.*?)">',response.text)[0]
            clash =  re.findall(r'\<button type="button" class="dropdown-item copy-text" data-clipboard-text="(.*?)">复制 Clash 订阅\</button>',response.text)[0]
            ms = "- 签到账号："+user+"\n- 签到信息："+str(msg)+"\n- 签到时间："+str(data)+"\n- 用户等级："+str(level)+"\n- 到期时间："+str(day)+"\n- 剩余流量："+str(rest)+'\n- 订阅链接：' +str(rss)+'\n- Clash链接：' +str(clash)+'\n --- \n'
            #print(ms)
            List.append(ms)
            
            return 
        except:
            return 

def server_send(msg):
    
    server_url = ""
    data = {
        'text': "签到完成，点击查看详细信息~",
        'desp': msg
            }
    requests.post(server_url, data=data)
def main():
    st = time.time()
    u = ['1637494149@qq.com-Aa199612','mrliupi1996@gmail.com-Aa199612','wxl1637494149@gmail.com-Aa199612','liulinatop@gmail.com-Aa199612']
    for x in u:
        us = x.split('-')[0]
        pw = x.split('-')[1]
        tk = SspanelQd(us, pw)
        tk.start()
        tk.join()
    
    msg = ''.join(List)
    en = time.time()
    ti = en - st
    msg = msg + '- 签到耗时：' + str('%.2f' %ti) + '秒'
    print(msg)
    
    server_send(msg)
# 云函数入口
def main_handler(event, context):
    main()
    
if __name__ == '__main__':
    main()