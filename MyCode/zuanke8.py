# -*- coding:utf-8 -*-
import requests
import hashlib, re
def md5(t):
	s = t
	return hashlib.md5(s.encode('utf-8')).hexdigest()
	
def login_heart(user, pwd, phone):
	se = requests.Session()
	url = 'http://www.zuanke8.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LF0AQ&inajax=1'
	params = 'formhash=03fdfd2a&referer=http%3A%2F%2Fwww.zuanke8.com%2Fzuixin.php&loginfield=username&username='+user+'&password='+md5(pwd)+'&questionid=3&answer='+phone
	se.get('http://www.zuanke8.com/')
	headers = {
	'Host': 'www.zuanke8.com',
	'Content-Type': 'application/x-www-form-urlencoded',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 Edg/86.0.622.61',
	'Referer': 'http://www.zuanke8.com/zuixin.php'
	}
	data = se.post(url, params=params, headers=headers)
	data = se.get('http://www.zuanke8.com/re.php', headers=headers)
	try:
		msg = re.findall(r'\<a href="(.*?)" title="(.*?)"  target="_blank">(.*?)\</a>', data.text)
		return msg
	except:
		return msg
		
def server_push(msg):
    server_url = "https://sc.ftqq.com/.send"
    data = {'text': "签到完成，点击查看详细信息~",'desp': msg}
    requests.post(server_url, data=data)

def main():
    List = []
    i = 0
    msg = login_heart('', '', '')
    for x in msg:
        i += 1
        lj = '- #### [' + x[2] + '](' + x[0] + ') \n\n'
        List.append(lj)
        msg = ''.join(List)
    server_push(msg)
    with open('./msg.txt', 'a') as f:
        f.write(msg+'\n')
        
if __name__ == '__main__':
    main()
	