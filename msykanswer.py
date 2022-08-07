import hashlib
import json
import re
import webbrowser
import requests
import time
from colorama import init,Fore,Back,Style
#from bs4 import BeautifulSoup

init(autoreset=True)#文字颜色自动恢复
roll=1#循环
serialNumbers,answers="",""
msykkey="DxlE8wwbZt8Y2ULQfgGywAgZfJl82G9S"

def answer_encode(answer):
    answer_code=""
    if len(answer)==1:
        return answer
    else:
        if "A" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "B" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "C" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "D" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "E" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "F" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "G" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "H" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "I" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        if "J" in answer:
            answer_code+="1"
        else:
            answer_code+="0"
        return answer_code

def ljlVink_parsemsyk(html_doc,count,url):
    html_doc.replace('\n',"")
    index=html_doc.find("var questions = ")
    index1=html_doc.find("var resource")
    if index !=-1:
        data=json.loads(html_doc[index+16:index1-7])
        if data[0].get('answer')!=None:
            answer="".join(data[0].get('answer')).lstrip("[")[:-1].replace('"','').lstrip(",").replace(',',' ')
            if(re.search(r'\d', answer)):
                open_url(url)
                print(Fore.GREEN+count+" 在浏览器中打开")
                return "wtf"
            else:
                print(Fore.GREEN+count+" "+answer)
                return answer
        else:
            print(Fore.RED+count+" "+"没有检测到答案,有可能是主观题")
            return "wtf"

def getCurrentTime():
    return int(round(time.time() * 1000))
#字符计算32位md5
def string_to_md5(string):
    md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
    return md5_val
#浏览器新窗口打开链接
def open_url(url):
    webbrowser.open_new(url)
#login
def login():
    userName=input("用户名:")
    pwd=input("密码:")
    mac=input("mac:").upper()#mac地址要大写
    api=input("安卓API:")
    sn=input(Fore.RED + "SN(区分大小写):")
    genauth=string_to_md5(userName+pwd+"HHOO")
    dataup={"userName":userName,"auth":genauth,"macAddress":mac,"versionCode":api,"sn":sn}
    res=post("https://padapp.msyk.cn/ws/app/padLogin",dataup,1,genauth+mac+sn+userName+api)
    setAccountInform(res)
#获取账号信息
def setAccountInform(result):
    #成功登录 获取账号信息
    if json.loads(result).get('code')=="10000":
        #avatar=json.loads(res).get('InfoMap').get('avatarUrl')
        #open_url(avatar)#浏览器打开头像（同时测试能否正常打开浏览器）
        print(Fore.GREEN + "===============")
        print(Fore.GREEN + result)
        print(Fore.GREEN + "===============")
        print(Fore.GREEN + "以上为登录信息，可以保存以便下次使用")
        global unitId,id
        unitId=json.loads(result).get('InfoMap').get('unitId')
        id=json.loads(result).get('InfoMap').get('id')
    #登录失败 打印原因
    else:
        print(Fore.RED + json.loads(result).get('message'))
        exit(1)
#post
def post(url,postdata,type=1,extra=''):
    time=getCurrentTime()
    key=''
    if type==1:
        key=string_to_md5(extra+str(time)+msykkey)
    elif type==2:
        key=string_to_md5(extra+id+unitId+str(time)+msykkey)
    elif type==3:
        key=string_to_md5(extra+unitId+id+str(time)+msykkey)
    postdata.update({'salt': time,'key': key})
    headers = {'user-agent': "okhttp/3.12.1"}
    try:
        req=requests.post(url=url,data=postdata,headers=headers)
        return req.text
    except:
        print(Fore.RED+str(url)+" "+str(postdata))
        print(Fore.RED+"网络异常 请检查代理设置")
        exit(1)

def getAnswer():
    hwid=input(Fore.YELLOW + "请输入作业id:")
    dataup={"homeworkId":int(hwid),"studentId":id,"modifyNum":0,"unitId":unitId}
    res=post("https://padapp.msyk.cn/ws/teacher/homeworkCard/getHomeworkCardInfo",dataup,2,hwid+'0')
    hwname=json.loads(res).get('homeworkName')
    print(Fore.MAGENTA+Back.WHITE+str(hwname))#作业名
    res_list=json.loads(res).get('homeworkCardList')#题目list

    question_list = []
    for question in res_list:
        global serialNumbers,answers
        serialNumber=str(question['serialNumber'])
        url="https://www.msyk.cn/webview/newQuestion/singleDoHomework?studentId="+id+"&homeworkResourceId="+str(question['resourceId'])+"&orderNum="+(question['orderNum'])+"&showAnswer=1&unitId="+unitId+"&modifyNum=1"
        #浏览器打开带答案的网页
        #open_url(url)
        vink=requests.get(url=url)
        answer=ljlVink_parsemsyk(vink.text,(question['orderNum']),url)
        question_list.append(question['resourceId'])

        if answer!="wtf":
            answer=answer_encode(answer)
            if serialNumbers=="":
                serialNumbers+=serialNumber
                answers+=answer
            else:
                serialNumbers+=";"+serialNumber
                answers+=";"+answer

    print(question_list)#打印题目id列表
    up = input(Fore.MAGENTA+"是否要提交选择答案 y/N:")
    if up=="Y" or up=="y":
        dataup={"serialNumbers":serialNumbers,"answers":answers,"studentId":id,"homeworkId":hwid,"unitId":unitId,"modifyNum":"0"}
        res=post("https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives",dataup)
        if json.loads(res).get('code')=="10000":
            print(Fore.GREEN + "自动提交选择答案成功")
    serialNumbers,answers="",""

def getUnreleasedHWID():
    EndHWID=0
    StartHWID=int(input(Fore.YELLOW + "请输入起始作业id:"))
    EndHWID=int(input(Fore.YELLOW + "请输入截止作业id(小于起始则不会停):"))
    hwidplus100=StartHWID+100
    while roll == 1:
        if StartHWID==hwidplus100:
            print(Fore.GREEN+"已滚动100项 当前"+str(hwidplus100))
            hwidplus100+=100
    
        dataup={"homeworkId":StartHWID,"modifyNum":0,"userId":id,"unitId":unitId}
        res=post("https://padapp.msyk.cn/ws/common/homework/homeworkStatus",dataup,3,str(StartHWID)+'0')
        if 'isWithdrawal' in res:
            pass
        else:
            hwname=json.loads(res).get('homeworkName')
            print(Fore.MAGENTA+str(StartHWID)+" "+hwname)
        
        if StartHWID==EndHWID:
            print(Fore.CYAN+"跑作业id结束 当前作业id为"+str(StartHWID))
            break
        StartHWID+=1

def MainMenu():
    print(Fore.MAGENTA+"1.作业获取答案(默认)\n2.跑作业id")
    Mission=input(Fore.RED + "请选择要执行的任务:")
    if Mission=="2":
        getUnreleasedHWID()
    else:
        getAnswer()

Start=input(Fore.CYAN+"输入登录信息(失败则模拟登录):")
try:
    setAccountInform(Start)
except:
    login()

dataup={"studentId":id,"subjectCode":None,"homeworkType":-1,"pageIndex":1,"pageSize":36,"statu":1,"homeworkName":None,"unitId":unitId}
res=post("https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList",dataup,2,"-11361")
reslist=json.loads(res).get('sqHomeworkDtoList')#作业list
for item in reslist:
    timeArray = time.localtime ((item['endTime'])/1000)
    timePrint = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(
        Fore.YELLOW + str(item['id'])+" 作业类型:"+str(item['homeworkType'])+" "+str(item['homeworkName'])+" 截止时间:"+timePrint
    )

while roll == 1:
    MainMenu()