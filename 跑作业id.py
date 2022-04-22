import json
import requests
import time
from colorama import init,Fore,Back,Style
init(autoreset=True)#文字颜色自动恢复
roll=1
#post
def post(url,postdata):
    headers = {'user-agent': "okhttp/3.12.1"}
    try:
        req=requests.post(url=url,data=postdata,headers=headers)
        return req.text
    except:
        print(Fore.RED+str(postdata))
        print(Fore.RED+"网络异常 请检查代理设置")
        exit(1)

def login_offline():
    res=input("登录信息:")
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

login_offline()
dataup={"studentId":id,"subjectCode":"","homeworkType":"-1","pageIndex":"1","pageSize":"18","statu":"1","homeworkName":"","homeworkName":"","unitId":unitId}
res=post("https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList",dataup)
reslist=json.loads(res).get('sqHomeworkDtoList')#作业list
for item in reslist:
    timeArray = time.localtime ((item['endTime'])/1000)
    timePrint = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print(
        Fore.MAGENTA + str(item['id'])+" 作业类型:"+str(item['homeworkType'])+" "+str(item['homeworkName'])+" 截止时间:"+timePrint
    )

hwid=int(input(Fore.YELLOW + "请输入起始作业id:"))
hwidplus100=hwid+100
while roll == 1:
    if hwid==hwidplus100:
        print(Fore.GREEN+"已滚动100项 当前"+str(hwidplus100))
        hwidplus100+=100
    
    dataup={"homeworkId":str(hwid),"modifyNum":"0","userId":id,"unitId":unitId}
    res=post("https://padapp.msyk.cn/ws/common/homework/homeworkStatus",dataup)
    if 'isWithdrawal' in res:
        pass
        #print(str(hwid)+" 无")
    else:
        hwname=json.loads(res).get('homeworkName')
        print(Fore.MAGENTA+str(hwid)+" "+hwname)
    hwid+=1
