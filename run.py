import requests, json, time
from tabulate import tabulate 
import time, datetime, os
from collections import OrderedDict

def getJsonByUrl(url, addparam=[]):

    headers = {
        'Host': 'ljw.antforecast.com',
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJZCI6IjEyOTMwMzE1MDU3MTkwNzQ4MTYiLCJEZXZpY2UiOiJXWF9vWHVNdjVXeWk2ZmhvSEdBSUxpcW5HdXRSQm5VIiwibmJmIjoxNjUxMjMxNTcwLCJleHAiOjE2NTE0OTA3NzAsImlhdCI6MTY1MTIzMTU3MCwiaXNzIjoiQWRtaW5MSlRRIiwiYXVkIjoiMTI5MzAzMTUwNTcxOTA3NDgxNiJ9.bRXK2EdQHkVe8Mp2QlHqYF94TtmSNdNymEG2bl9aMB0',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x1800142f) NetType/WIFI Language/zh_CN',
        'Referer': 'https://servicewechat.com/wx53ed90a7aefc9795/79/page-frame.html',
    }

    params = [('lon', '119.99438744666699'),
        ('lat', '30.286695402075779')]+addparam

    response = requests.get(url, headers=headers, params=params)
    return response.text

urls={
    "星空":"https://ljw.antforecast.com/StarIndex/GetByLocation",
    "夕阳":"https://ljw.antforecast.com/SunsetGlow/GetExtremumByLocation",
    "朝霞":"https://ljw.antforecast.com/MorningGlow/GetExtremumByLocation"
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
lookuptb_print=OrderedDict([
    ('startTime','始'),
    ('endTime'  ,'末'),
    ('pr'       ,'概率'),
    ('qu'       ,'质量')])
num_emoji=OrderedDict({
    -1:"❌",
    15:"😳",
    40:"🥺",
    70:"🤑"
})
ltbkeys=[]
printstr=""
def intersect(lst2, lst1): 
    res=[]
    for value in lst1:
        if value in lst2:
            res.append(value)
    return res
def num_process(numstr):
    res=""
    try:
        for lim in num_emoji:
            if int(numstr)>lim:
                res=num_emoji[lim]
    except:
        pass
    return res+str(numstr)

def applyRules(jsonstr, rule):
    global printstr
    data=json.loads(jsonstr)
    for field in rule.split('.'):
        if field in data:
            data=data[field]
        else: return "[ERROR]"
    header=[lookuptb[k] for k in intersect(data[0], lookuptb)]
    header_print=[lookuptb_print[k] for k in intersect(data[0], lookuptb_print)]
    column=[k for k in intersect(data[0], lookuptb)]
    column_print=[k for k in intersect(data[0], lookuptb_print)]
    tb=[[item[k] for k in column] for item in data]
    tb_print=[[item[k] for k in column_print] for item in data]
    for tb_print_row in tb_print:
        printstr+="|".join([f"{header_print[i]} {num_process(tb_print_row[i])}" for i in range(len(column_print))])+"\n"
    return tabulate(tb, header, tablefmt="html")


while True:
    try:
        res='<p>余杭区 未来科技城</p><p>更新时间：%s</p>'%datetime.datetime.now()
        for item in urls:
        # item="夕阳"
            printstr+=f"========{item}========\n"
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
        currentYear = str(datetime.datetime.now().year)+"-"
        print(printstr.replace(currentYear,""))
    except Exception as e: 
        print("Error:", e)
        pass
    time.sleep(3600)