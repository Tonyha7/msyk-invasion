import hashlib
import json
import re
import webbrowser
import requests
import time
import base64
from rsa import core, PublicKey, transform
from colorama import init,Fore,Back

init(autoreset=True)#文字颜色自动恢复
roll=1#循环
serialNumbers,answers="",""
msyk_sign_pubkey= "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAj7YWxpOwulFyf+zQU77Y2cd9chZUMfiwokgUaigyeD8ac5E8LQpVHWzkm+1CuzH0GxTCWvAUVHWfefOEe4AThk4AbFBNCXqB+MqofroED6Uec1jrLGNcql9IWX3CN2J6mqJQ8QLB/xPg/7FUTmd8KtGPrtOrKKP64BM5cqaB1xCc4xmQTuWvtK9fRei6LVTHZyH0Ui7nP/TSF3PJV3ywMlkkQxKi8JBkz1fx1ZO5TVLYRKxzMQdeD6whq+kOsSXhlLIiC/Y8skdBJmsBWDMfQXxtMr5CyFbVMrG+lip/V5n22EdigHcLOmFW9nnB+sgiifLHeXx951lcTmaGy4uChQIDAQAB"

msyk_key="DxlE8wwbZt8Y2ULQfgGywAgZfJl82G9S"
headers = {'user-agent': "okhttp/3.12.1"}
sign=""

def getAccountInform():
    ReturnInform=""
    ProfileImport=""
    try:
        for line in open("ProfileCache.txt", "r",encoding='utf-8').readlines():
            line = line.strip('\n')  #去掉列表中每一个元素的换行符
            ReturnInform = ReturnInform + line
        print("检测到 ProfileCache，尝试缓存登录中。（如失败自动执行登录流程）")
        setAccountInform(ReturnInform)
    except:
        print("未检测到 ProfileCache，执行登录流程。")
        ProfileImport=input(Fore.CYAN+"可提供未缓存的登录信息(失败则自动执行设备信息登录):")
        try:
            setAccountInform(ProfileImport)
        except:
            print(Fore.RED+"错误：登录信息有误或已经失效。")
            print(Fore.WHITE)
            login()

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
def save_json(data,filename):
    filename+=".json"
    try:
        file = open(filename,'w')
        file.write(data)
        file.close
        print(Fore.MAGENTA + "保存登录信息成功 "+filename)
    except:
        print(Fore.RED + "保存登录信息失败")
def public_key_decrypt(publicKey, content):
    qr_code_cipher = base64.b64decode(content)
    public_key = base64.b64decode(publicKey)
    try:
        rsa_public_key = PublicKey.load_pkcs1_openssl_der(public_key)
        cipher_text_bytes = transform.bytes2int(qr_code_cipher)
        decrypted_text = core.decrypt_int(cipher_text_bytes, rsa_public_key.e, rsa_public_key.n)
        final_text = transform.int2bytes(decrypted_text)
        final_code = final_text[final_text.index(0) + 1:]
        return final_code.decode()
    except Exception:
        print(Fore.RED+"警告:sign解密失败!")
        return None
def getCurrentTime():
    return int(round(time.time() * 1000))
def TimeToHMS(ts:int):
    # 十三位时间戳
    return time.strftime("%H:%M:%S", time.localtime(ts/1000))
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
        #print(Fore.GREEN + "===============")
        #print(Fore.GREEN + result)
        #print(Fore.GREEN + "===============")
        save_json(result,json.loads(result).get('InfoMap').get('realName'))
        open("ProfileCache.txt","w",encoding='utf-8').write(result)
        print("ProfileCache 登录缓存已更新。(下一次优先自动读取)")
        global unitId,id
        unitId=json.loads(result).get('InfoMap').get('unitId')
        id=json.loads(result).get('InfoMap').get('id')
        
        sign1=public_key_decrypt(msyk_sign_pubkey,json.loads(result).get('sign')).split(':')
        if sign1!=None:
            signdec=','.join(sign1) 
            print(Fore.GREEN+"sign解密成功:"+signdec)
            global sign
            sign=sign1[1]+id

    #登录失败 打印原因
    else:
        print(Fore.RED + json.loads(result).get('message'))
        exit(1)
#post
def post(url,postdata,type=1,extra=''):
    time=getCurrentTime()
    key=''
    if type==1:
        key=string_to_md5(extra+str(time)+sign+msyk_key)
    elif type==2:
        key=string_to_md5(extra+id+unitId+str(time)+sign+msyk_key)
    elif type==3:
        key=string_to_md5(extra+unitId+id+str(time)+sign+msyk_key)
    postdata.update({'salt': time,'sign': sign,'key': key})
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
    #print(res)
    materialRelasList,analysistList = json.loads(res).get('materialRelas'),json.loads(res).get('analysistList')
    materialRelasUrls,analysistUrls,materialRelasFiles,analysistFiles=[],[],[],[]
    hwname=json.loads(res).get('homeworkName')
    print(Fore.MAGENTA+Back.WHITE+str(hwname))#作业名
    res_list=json.loads(res).get('homeworkCardList')#题目list

    if len(materialRelasList)==0:
        print(Fore.RED+"没有材料文件")
    else:
        print(Fore.MAGENTA+"材料文件:")
        for file in materialRelasList:
            if str(file['resourceUrl']).lower().startswith('http'):
                file_url=file['resourceUrl']
            elif str(file['resourceUrl']).lower().startswith('//'):
                file_url="https://msyk.wpstatic.cn"+file['resourceUrl']
            elif str(file['resourceUrl']).lower().startswith('/'):
                file_url="https://msyk.wpstatic.cn"+file['resourceUrl']
            elif str(file['title']).lower().find('.ppt'):
                #当 file 携带的 title 表明为 PPT 文件时，从 titleImg 携带的数据上获取 PPT 文件绝对路径并下载
                file_url="https://msyk.wpstatic.cn/"+file['titleImg']
            else:
                file_url="https://msyk.wpstatic.cn/"+file['resourceUrl']
            materialRelasFiles.append(file['title'])
            materialRelasUrls.append(file_url)
            print(Fore.GREEN+"\t"+file['title']+" "+file_url)

    if len(analysistList)==0:
        print(Fore.RED+"没有答案文件")
    else:
        print(Fore.MAGENTA+"答案文件:")
        for file in analysistList:
            if str(file['resourceUrl']).lower().startswith('http'):
                file_url=file['resourceUrl']
            elif str(file['resourceUrl']).lower().startswith('//'):
                file_url="https://msyk.wpstatic.cn"+file['resourceUrl']
            elif str(file['resourceUrl']).lower().startswith('/'):
                file_url="https://msyk.wpstatic.cn"+file['resourceUrl']
            else:
                file_url="https://msyk.wpstatic.cn/"+file['resourceUrl']
            analysistFiles.append(file['title'])
            analysistUrls.append(file_url)
            print(Fore.GREEN+"\t"+file['title']+" "+file_url)
            
    question_list = []
    global serialNumbers,answers
    for question in res_list:
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
        dataup={"serialNumbers":serialNumbers,"answers":answers,"studentId":id,"homeworkId":int(hwid),"unitId":unitId,"modifyNum":0}
        res=post("https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives",dataup,2,answers+hwid+'0'+serialNumbers)
        if json.loads(res).get('code')=="10000":
            print(Fore.GREEN + "自动提交选择答案成功")
            
    if len(analysistList)!=0 or len(materialRelasList)!=0:
        down = input(Fore.BLUE+"是否要下载文件 y/N:")
        if down=="Y" or down=="y":
            for url,file in zip(materialRelasUrls,materialRelasFiles):
                with open(file, "wb") as f, requests.get(url) as res:
                    f.write(res.content)
            for url,file in zip(analysistUrls,analysistFiles):
                with open(file, "wb") as f, requests.get(url) as res:
                    f.write(res.content)
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
        #print(res)
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
    ProfileImport=""
    print(Fore.MAGENTA+"1.作业获取答案(默认)\n2.跑作业id\n3.切换账号")
    Mission=input(Fore.RED + "请选择要执行的任务:")
    if Mission=="2":
        getUnreleasedHWID()
    elif Mission=="3":
        open("ProfileCache.txt","w",encoding='utf-8').write("")
        print(Fore.CYAN+"已清空 ProfileCache 登录缓存。")
        ProfileImport=input(Fore.CYAN+"请提供登录信息(如无则执行设备信息登录):")
        try:
            setAccountInform(ProfileImport)
        except:
            login()
    else:
        getAnswer()

Start=getAccountInform()

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