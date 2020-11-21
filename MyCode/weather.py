# -*- coding: utf8 -*-
import requests
import json

def get_iciba_everyday():
    icbapi = 'http://open.iciba.com/dsapi/'  #下载.PY文件可见
    eed = requests.get(icbapi)
    bee = eed.json()  #返回的数据
    english = bee['content']
    zh_CN = bee['note']
    str = '【奇怪的知识】\n' + english + '\n' + zh_CN
    return str

def main():
    try:
        api = 'http://t.weather.itboy.net/api/weather/city/'
        city_code = '101190509'
        tqurl = api + city_code
        response = requests.get(tqurl)
        d = response.json()
        print(d)
        if(d['status'] == 200):
            parent = d["cityInfo"]["parent"] #省
            city = d["cityInfo"]["city"] #市
            
            update_time = d["time"] #更新时间
            
            date = d["data"]["forecast"][0]["ymd"] #日期
            
            week = d["data"]["forecast"][0]["week"] #星期
            
            weather_type = d["data"]["forecast"][0]["type"] # 天气
            
            wendu_high = d["data"]["forecast"][0]["high"] #最高温度
            
            wendu_low = d["data"]["forecast"][0]["low"] #最低温度
            print(wendu_low)
            shidu = d["data"]["shidu"] #湿度
            pm25 = str(d["data"]["pm25"]) #PM2.5
            pm10 = str(d["data"]["pm10"]) #PM10
            quality = d["data"]["quality"] #天气质量
            fx = d["data"]["forecast"][0]["fx"] #风向
            fl = d["data"]["forecast"][0]["fl"] #风力
            ganmao = d["data"]["ganmao"] #感冒指数
            tips = d["data"]["forecast"][0]["notice"] #温馨提示
            cpurl = 'https://push.xuthus.cc/send/'

            tdwt = get_iciba_everyday()+"\n------------------------------------" + "\n【今日天气】\n城市：" + parent + city + \
                   "\n日期：" + date + "\n星期：" + week + "\n天气：" + weather_type + "\n温度：" + wendu_high + " / "+ wendu_low + "\n湿度：" + \
                    shidu + "\nPM25：" + pm25 + "\nPM10：" + pm10 + "\n空气质量：" + quality + \
                   "\n风力风向：" + fx + fl + "\n感冒指数："  + ganmao + "\n温馨提示：" + tips + "\n更新时间：" + update_time
            print(tdwt)
            requests.post(cpurl, tdwt.encode('utf-8'))
    except:
        
        error = '【出现错误】\n　　今日天气推送错误，请检查服务或网络状态！'
        requests.post(cpurl, error.encode('utf-8'))
        print(error)

def main_handler(event, context):
    return main()

if __name__ == '__main__':
    main()
