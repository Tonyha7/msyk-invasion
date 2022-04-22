#项目地址 https://bitbucket.org/tonyha7/msykinvasion/src/main/
import hashlib
import json
import requests
import webbrowser
import time
from colorama import init,Fore,Back,Style
#from bs4 import BeautifulSoup

init(autoreset=True)#文字颜色自动恢复
roll=1#循环

def ljlVink_parsemsyk(html_doc,count):
    html_doc.replace('\n',"")
    index=html_doc.find("var questions = ")
    end=index
    while 1:
        if(html_doc[end]==';'):
            break
        else :
            end+=1
    #print(html_doc[index+16:end])
    data=json.loads(html_doc[index+16:end])
    print(Fore.GREEN+count+" "+str(data[0].get('answer')))

#字符计算32位md5
def string_to_md5(string):
    md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
    return md5_val
#浏览器新窗口打开链接
def open_url(url):
    webbrowser.open_new(url)
#post
def post(url,postdata):
    headers = {'user-agent': "okhttp/3.12.1"}
    try:
        req=requests.post(url=url,data=postdata,headers=headers)
        return req.text
    except:
        print("网络异常 请检查代理设置")
        exit(1)
#login
def login():
    user=input("用户名:")
    pwd=input("密码:")
    mac=input("mac:").upper#mac地址要大写
    api=input("安卓API:")
    sn=input(Fore.RED + "SN(区分大小写):")
    dataup={"userName":user,"auth":string_to_md5(user+pwd+"HHOO"),"macAddress":mac,"versionCode":api,"sn":sn}
    res=post("https://padapp.msyk.cn/ws/app/padLogin",dataup)
    setAccountInform(res)
#获取账号信息
def setAccountInform(result):
    #成功登录 获取账号信息
    if json.loads(result).get('code')=="10000":
        #avatar=json.loads(res).get('InfoMap').get('avatarUrl')
        #open_url(avatar)#浏览器打开头像（同时测试能否正常打开浏览器）
        print(Fore.GREEN + result)
        global unitId,id
        unitId=json.loads(result).get('InfoMap').get('unitId')
        id=json.loads(result).get('InfoMap').get('id')
    #登录失败 打印原因
    else:
        print(Fore.RED + json.loads(result).get('message'))
        exit(1)

howtologin=input("输入登录信息(失败则模拟登录):")
try:
    setAccountInform(howtologin)
except:
    login()

dataup={"studentId":id,"subjectCode":"","homeworkType":"-1","pageIndex":"1","pageSize":"18","statu":"1","homeworkName":"","homeworkName":"","unitId":unitId}
res=post("https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList",dataup)
reslist=json.loads(res).get('sqHomeworkDtoList')#作业list
for item in reslist:
    timeArray = time.localtime ((item['endTime'])/1000)
    timePrint = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(
        Fore.YELLOW + str(item['id'])+" 作业类型:"+str(item['homeworkType'])+" "+str(item['homeworkName'])+" 截止时间:"+timePrint
    )
while roll == 1:
    hwid=input(Fore.YELLOW + "请输入作业id:")
    dataup={"homeworkId":hwid,"modifyNum":"0","userId":id,"unitId":unitId}
    res=post("https://padapp.msyk.cn/ws/common/homework/homeworkStatus",dataup)
    #print(Fore.CYAN+res)
    hwname=json.loads(res).get('homeworkName')
    print(Fore.MAGENTA+Back.WHITE+str(hwname))#作业名
    reslist=json.loads(res).get('resourceList')#题目list
    list_b = []
    count=1
    for item in reslist:
        #哪个鬼才把答案写js里了。。。。。。
        #req = requests.get(url="https://www.msyk.cn/webview/newQuestion/singleDoHomework?studentId="+id+"&homeworkResourceId="+str(item['id'])+"&orderNum="+str(count)+"&showAnswer=1&unitId="+unitId+"&modifyNum=1")
        #req.encoding = "utf-8"
        #html=req.text
        #print(html)
        #soup = BeautifulSoup(req.text,features="html.parser")
        #answer = soup.find("div",class_="right-part")
        #answerstrip = answer.text.strip()
        #print(str(count)+" "+str(answerstrip))
        #浏览器打开带答案的网页
        #open_url("https://www.msyk.cn/webview/newQuestion/singleDoHomework?studentId="+id+"&homeworkResourceId="+str(item['id'])+"&orderNum="+str(count)+"&showAnswer=1&unitId="+unitId+"&modifyNum=1")

        url="https://www.msyk.cn/webview/newQuestion/singleDoHomework?studentId="+id+"&homeworkResourceId="+str(item['id'])+"&orderNum="+str(count)+"&showAnswer=1&unitId="+unitId+"&modifyNum=1"
        
        vink=requests.get(url=url)
        ljlVink_parsemsyk(vink.text,str(count))

        count+=1#题号滚动
        list_b.append(item['id'])
    print(list_b)#打印题目id列表