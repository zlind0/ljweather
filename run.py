import requests, json, time
from tabulate import tabulate 
import time, datetime, os
from collections import OrderedDict

def getJsonByUrl(url, addparam=[]):

    headers = {
        'Host': 'ljw.antforecast.com',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.14(0x17000e2e) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx53ed90a7aefc9795/46/page-frame.html',
        'Accept-Language': 'zh-cn',
    }

    params = [('lon', '118.963261'),
        ('lat', '32.156684')]+addparam

    response = requests.get(url, headers=headers, params=params)
    return response.text

urls={
    "星空":"https://ljw.antforecast.com/xiaochengxu/2ccda10545154737b6f9e7c909665307/StarIndex/GetByLocation",
    "夕阳":"https://ljw.antforecast.com/xiaochengxu/2ccda10545154737b6f9e7c909665307/SunsetGlow/GetExtremumByLocation",
    "朝霞":"https://ljw.antforecast.com/xiaochengxu/2ccda10545154737b6f9e7c909665307/MorningGlow/GetExtremumByLocation"
}
rules={
    "星空":"result.data",
    "夕阳":"result.data",
    "朝霞":"result.data",
}

lookuptb=OrderedDict([
    ('time'     ,'日期'),
    ('date'     ,'日期'),
    ('pr'       ,'概率'),
    ('qu'       ,'质量'),
    ('maxpr'    ,'最大概率'),
    ('minpr'    ,'最小概率'),
    ('maxqu'    ,'最大质量'),
    ('minqu'    ,'最小质量'),
    ('startTime','开始时间'),
    ('endTime'  ,'结束时间')])
ltbkeys=[]
def intersect(lst2, lst1): 
    res=[]
    for value in lst1:
        if value in lst2:
            res.append(value)
    return res
def applyRules(jsonstr, rule):
    data=json.loads(jsonstr)
    for field in rule.split('.'):
        if field in data:
            data=data[field]
        else: return "[ERROR]"
    header=[lookuptb[k] for k in intersect(data[0], lookuptb)]
    column=[k for k in intersect(data[0], lookuptb)]
    tb=[[item[k] for k in column] for item in data]
    return tabulate(tb, header, tablefmt="html")

while True:
    try:
        res='<p>南京市栖霞区栖霞山</p><p>更新时间：%s</p>'%datetime.datetime.now()
        for item in urls:
        # item="夕阳"
            stars=getJsonByUrl(urls[item])
            tb=applyRules(stars, rules[item])
            res+="<h1>%s</h1>"%item
            res+=tb
        with open('index.html') as f:
            page=f.read()
        if not os.path.exists('src'):
            os.mkdir('src')
        with open('src/index.html','w') as f:
            f.write(page.replace('CONTENIDO', res))
        print("Success:", datetime.datetime.now())
    except Exception as e: 
        print("Error:", e)
        pass
    time.sleep(3600)