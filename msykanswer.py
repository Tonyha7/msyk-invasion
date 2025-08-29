import hashlib
import json
import re
import os
import webbrowser
import requests
import time
import base64
from rsa import core, PublicKey, transform
from colorama import init,Fore,Back,Style
# 额外功能，自行取消注释
#import msyk_message
#import msyk_learning_circle

#课件下载转PDF功能，需要pillow
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    Image = None

# 科目代码映射字典
SUBJECT_CODE_MAP = {
    "3001": "政治",
    "3002": "历史",
    "3003": "地理",
    "3006": "物理",
    "3007": "语文",
    "3008": "数学",
    "3009": "英语",
    "3011": "化学",
    "3014": "体育与健康",
    "3020": "生物",
    "3110": "通用(选考)",
    "3111": "通用(学考)",
    "3113": "信息(选考)",
    "3114": "信息(学考)",
    "9834": "语音"
}

SUBJECT_NAME_TO_CODE = {v: k for k, v in SUBJECT_CODE_MAP.items()}

# 定义科目颜色映射
SUBJECT_COLORS = {
	'政治': Fore.YELLOW,
    '历史': Fore.CYAN,
    '语文': Fore.LIGHTWHITE_EX,
    '数学': Fore.LIGHTRED_EX,
    '英语': Fore.LIGHTGREEN_EX,
    '语音': Fore.LIGHTGREEN_EX,
    '物理': Fore.LIGHTMAGENTA_EX,
    '化学': Fore.LIGHTBLUE_EX,
    '生物': Fore.LIGHTCYAN_EX,
    '地理': Fore.LIGHTYELLOW_EX,
    '体育与健康': Fore.LIGHTRED_EX,
    '通用(选考)': Fore.BLUE,
    '通用(学考)': Fore.LIGHTBLUE_EX,
    '信息(选考)': Fore.MAGENTA,
    '信息(学考)': Fore.LIGHTMAGENTA_EX,
    # 默认颜色
    '其他': Fore.LIGHTYELLOW_EX
}

init(autoreset=True)#文字颜色自动恢复
roll=1#循环
serialNumbers,answers,serialNumbersa,answersa="","","",""
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
        ProfileImport=input(Fore.CYAN+"可提供未缓存的登录信息(失败则自动执行账号密码登录):")
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
        #print(data)
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

def ljlVink_parsemsyk1(html_doc,count,url):
    html_doc.replace('\n',"")
    index=html_doc.find("var questions = ")
    index1=html_doc.find("var resource")
    if index !=-1:
        data=json.loads(html_doc[index+16:index1-7])
        #print(data)
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
            answer=" "
            return answer


def save_json(data,filename):
    filename+=".json"
    try:
        file = open(filename,'w')
        file.write(data)
        file.close()
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

#POST方案，目前以弃用
def login1():
    userName=input("用户名:")
    pwd=input("密码:")
    mac=input("mac:").upper()#mac地址要大写
    api=input("安卓API:")
    sn=input(Fore.RED + "SN(区分大小写):")
    genauth=string_to_md5(userName+pwd+"HHOO")
    dataup={"userName":userName,"auth":genauth,"macAddress":mac,"versionCode":api,"sn":sn}
    res=post("https://padapp.msyk.cn/ws/app/padLogin",dataup,1,genauth+mac+sn+userName+api)
    setAccountInform(res)

#登入已简化为GET方案，感谢 cyhLen 提供方案

def login():
    userName=input("用户名:")
    password=input("密码:")
    pwd=string_to_md5(userName+password+"HHOO")
    loginurl='https://padapp.msyk.cn/ws/app/padLogin?userName='+userName+'&auth='+pwd
    login_first = requests.get(loginurl).text
    setAccountInform(login_first)

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
    #增加输入要求提示
    while True:
        hwid_input = input(Fore.YELLOW + "请输入作业id:")
        try:
            hwid = int(hwid_input)
            break
        except ValueError:
            print(Fore.RED + "作业ID必须是数字，请重新输入")
    hwid = str(hwid)
    dataup={"homeworkId":int(hwid),"studentId":id,"modifyNum":0,"unitId":unitId}
    res=post("https://padapp.msyk.cn/ws/teacher/homeworkCard/getHomeworkCardInfo",dataup,2,hwid+'0')
    dataupp = {"homeworkId": hwid, "modifyNum": 0, "userId": id, "unitId": unitId}
    ress = post("https://padapp.msyk.cn/ws/common/homework/homeworkStatus", dataupp, 3, str(hwid) + '0')

    #print(ress)
    if ress.strip():
        try:
            hwtp = json.loads(ress)
            hwtp = json.loads(ress).get('homeworkType')
        except json.JSONDecodeError as e:
            print("JSON格式错误:", e)
        if res.strip():
            try:
                code = json.loads(res).get('code')
            except json.JSONDecodeError as e:
                print("JSON格式错误:", e)
            if str(hwtp) == "7":
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
                global serialNumbers,answers,serialNumbersa,answersa
                for question in res_list:
                    serialNumber=str(question['serialNumber'])
                    print(Fore.BLUE+serialNumbers)
                    #print(Fore.RED+serialNumber)
                    url="https://www.msyk.cn/webview/newQuestion/singleDoHomework?studentId="+id+"&homeworkResourceId="+str(question['resourceId'])+"&orderNum="+(question['orderNum'])+"&showAnswer=1&unitId="+unitId+"&modifyNum=1"
                    #浏览器打开带答案的网页
                    #open_url(url)
                    vink=requests.get(url=url)
                    #print(vink)
                    answer=ljlVink_parsemsyk(vink.text,(question['orderNum']),url)
                    #print(Fore.GREEN+answer)
                    question_list.append(question['resourceId'])

                    answer = answer_encode(answer)
                    if serialNumbersa == "":
                        serialNumbersa += serialNumber
                        answersa += answer
                    else:
                        serialNumbersa += ";" + serialNumber
                        answersa += ";" + answer

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

                middle = input(Fore.YELLOW+"是否要为主观题提交假图片 y/N:")
                if middle=="Y" or up=="y":
                    dataup={"serialNumbers":serialNumbersa,"answers":answersa,"studentId":id,"homeworkId":int(hwid),"unitId":unitId,"modifyNum":0}
                    res=post("https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives",dataup,2,answers+hwid+'0'+serialNumbers)
                    if json.loads(res).get('code')=="10000":
                        print(Fore.GREEN + "自动提交主观题提交假图片成功")

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
                
            elif str(hwtp) == "5":
                resourceList = json.loads(ress).get('resourceList')  # 材料文件列表
                hwname = json.loads(res).get('homeworkName')
                print(Fore.MAGENTA + Style.BRIGHT + str(hwname))  # 作业名
                print(Fore.MAGENTA + Style.NORMAL + "材料文件:")
                materialRelasFiles, materialRelasUrls = [], []
                for file in resourceList:
                    # 检查资源类型，如果是5，则是PPT
                    if file.get('resourceType') == 5:
                        ppt_resource_id = file['resourceUrl']  # 资源ID
                        res_title = file['resTitle']
                        print(Fore.YELLOW + "检测到PPT文件:", Fore.CYAN + Back.WHITE + res_title)
                        download_choose = input(Fore.BLUE + "是否要下载该PPT文件？[Y/n]")
                        if download_choose == 'Y' or download_choose == 'y':
                            success = download_ppt(ppt_resource_id, res_title)
                            if success:
                                print(Fore.WHITE + "PPT处理完成")
                            else:
                                print(Fore.RED + "PPT处理失败")
                        else:
                            print(Fore.WHITE + "已取消下载")
                    else:
                        # 其他类型的资源，按照原来的方式处理
                        file_url = "https://msyk.wpstatic.cn/" + file['resourceUrl']
                        materialRelasFiles.append(file['resTitle'])
                        materialRelasUrls.append(file_url)
                        print(Fore.GREEN + "\t" + file['resTitle'] + " " + file_url)
                    
                # 保留原来的下载选项（针对非PPT资源）
                if 'materialRelasUrls' in locals() and materialRelasUrls:
                    down = input(Fore.BLUE + "是否要下载非PPT文件 y/N:")
                    if down == "Y" or down == "y":
                        for url, file in zip(materialRelasUrls, materialRelasFiles):
                            with open(file, "wb") as f, requests.get(url) as res:
                                f.write(res.content)
                serialNumbers, answers = "", ""


            else:
                # print(ress)
                resourceList = json.loads(ress).get('resourceList')  # 材料文件列表
                materialRelasUrls, materialRelasFiles, = [], []
                hwname = json.loads(res).get('homeworkName')
                print(Fore.MAGENTA + Style.BRIGHT + str(hwname))  # 作业名
                print(Fore.MAGENTA +Style.NORMAL+ "材料文件:")
                for file in resourceList:
                    file_url = "https://msyk.wpstatic.cn/" + file['resourceUrl']
                    materialRelasFiles.append(file['resTitle'])
                    materialRelasUrls.append(file_url)
                    print(Fore.GREEN + "\t" + file['resTitle'] + " " + file_url)
                down = input(Fore.BLUE + "是否要下载文件 y/N:")
                if down == "Y" or down == "y":
                    for url, file in zip(materialRelasUrls, materialRelasFiles):
                        with open(file, "wb") as f, requests.get(url) as res:
                            f.write(res.content)
                serialNumbers, answers = "", ""
        else:
            Choice = input("ress为空，是否重新解析(默认是，否请输入1):")
            if Choice == "1":
                print("The program will be ended.")

################第一次重启#################
            else:
                dataup = {"homeworkId": int(hwid), "studentId": id, "modifyNum": 0, "unitId": unitId}
                res = post("https://padapp.msyk.cn/ws/teacher/homeworkCard/getHomeworkCardInfo", dataup, 2, hwid + '0')
                dataupp = {"homeworkId": hwid, "modifyNum": 0, "userId": id, "unitId": unitId}
                ress = post("https://padapp.msyk.cn/ws/common/homework/homeworkStatus", dataupp, 3, str(hwid) + '0')

                # print(ress)
                if ress.strip():
                    try:
                        hwtp = json.loads(ress)
                        hwtp = json.loads(ress).get('homeworkType')
                    except json.JSONDecodeError as e:
                        print("JSON格式错误:", e)
                    if res.strip():
                        try:
                            code = json.loads(res).get('code')
                        except json.JSONDecodeError as e:
                            print("JSON格式错误:", e)
                        if str(hwtp) == "7":
                            materialRelasList, analysistList = json.loads(res).get('materialRelas'), json.loads(
                                res).get('analysistList')
                            materialRelasUrls, analysistUrls, materialRelasFiles, analysistFiles = [], [], [], []
                            hwname = json.loads(res).get('homeworkName')
                            print(Fore.MAGENTA + Back.WHITE + str(hwname))  # 作业名
                            res_list = json.loads(res).get('homeworkCardList')  # 题目list

                            if len(materialRelasList) == 0:
                                print(Fore.RED + "没有材料文件")
                            else:
                                print(Fore.MAGENTA + "材料文件:")
                                for file in materialRelasList:
                                    if str(file['resourceUrl']).lower().startswith('http'):
                                        file_url = file['resourceUrl']
                                    elif str(file['resourceUrl']).lower().startswith('//'):
                                        file_url = "https://msyk.wpstatic.cn" + file['resourceUrl']
                                    elif str(file['resourceUrl']).lower().startswith('/'):
                                        file_url = "https://msyk.wpstatic.cn" + file['resourceUrl']
                                    else:
                                        file_url = "https://msyk.wpstatic.cn/" + file['resourceUrl']
                                    materialRelasFiles.append(file['title'])
                                    materialRelasUrls.append(file_url)
                                    print(Fore.GREEN + "\t" + file['title'] + " " + file_url)

                            if len(analysistList) == 0:
                                print(Fore.RED + "没有答案文件")
                            else:
                                print(Fore.MAGENTA + "答案文件:")
                                for file in analysistList:
                                    if str(file['resourceUrl']).lower().startswith('http'):
                                        file_url = file['resourceUrl']
                                    elif str(file['resourceUrl']).lower().startswith('//'):
                                        file_url = "https://msyk.wpstatic.cn" + file['resourceUrl']
                                    elif str(file['resourceUrl']).lower().startswith('/'):
                                        file_url = "https://msyk.wpstatic.cn" + file['resourceUrl']
                                    else:
                                        file_url = "https://msyk.wpstatic.cn/" + file['resourceUrl']
                                    analysistFiles.append(file['title'])
                                    analysistUrls.append(file_url)
                                    print(Fore.GREEN + "\t" + file['title'] + " " + file_url)

                            question_list = []
                            for question in res_list:
                                serialNumber = str(question['serialNumber'])
                                url = "https://www.msyk.cn/webview/newQuestion/singleDoHomework?studentId=" + id + "&homeworkResourceId=" + str(
                                    question['resourceId']) + "&orderNum=" + (
                                      question['orderNum']) + "&showAnswer=1&unitId=" + unitId + "&modifyNum=1"
                                # 浏览器打开带答案的网页
                                # open_url(url)
                                vink = requests.get(url=url)
                                answer = ljlVink_parsemsyk(vink.text, (question['orderNum']), url)
                                question_list.append(question['resourceId'])

                                answer = answer_encode(answer)
                                if serialNumbersa == "":
                                    serialNumbersa += serialNumber
                                    answersa += answer
                                else:
                                    serialNumbersa += ";" + serialNumber
                                    answersa += ";" + answer

                                if answer != "wtf":
                                    answer = answer_encode(answer)
                                    if serialNumbers == "":
                                        serialNumbers += serialNumber
                                        answers += answer
                                    else:
                                        serialNumbers += ";" + serialNumber
                                        answers += ";" + answer

                            print(question_list)  # 打印题目id列表
                            up = input(Fore.MAGENTA + "是否要提交选择答案 y/N:")
                            if up == "Y" or up == "y":
                                dataup = {"serialNumbers": serialNumbers, "answers": answers, "studentId": id,
                                          "homeworkId": int(hwid), "unitId": unitId, "modifyNum": 0}
                                res = post("https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives",
                                           dataup, 2, answers + hwid + '0' + serialNumbers)
                                if json.loads(res).get('code') == "10000":
                                    print(Fore.GREEN + "自动提交选择答案成功")

                            middle = input(Fore.YELLOW + "是否要为主观题提交假图片 y/N:")
                            if middle == "Y" or up == "y":
                                dataup = {"serialNumbers": serialNumbersa, "answers": answersa, "studentId": id,
                                          "homeworkId": int(hwid), "unitId": unitId, "modifyNum": 0}
                                res = post("https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives",
                                           dataup, 2, answers + hwid + '0' + serialNumbers)
                                if json.loads(res).get('code') == "10000":
                                    print(Fore.GREEN + "自动提交主观题提交假图片成功")

                            if len(analysistList) != 0 or len(materialRelasList) != 0:
                                down = input(Fore.BLUE + "是否要下载文件 y/N:")
                                if down == "Y" or down == "y":
                                    for url, file in zip(materialRelasUrls, materialRelasFiles):
                                        with open(file, "wb") as f, requests.get(url) as res:
                                            f.write(res.content)
                                    for url, file in zip(analysistUrls, analysistFiles):
                                        with open(file, "wb") as f, requests.get(url) as res:
                                            f.write(res.content)
                            serialNumbers, answers = "", ""
                        elif str(hwtp) == "5":
                            # print(ress)
                            resourceList = json.loads(ress).get('resourceList')  # 材料文件列表
                            materialRelasUrls, materialRelasFiles, = [], []
                            hwname = json.loads(res).get('homeworkName')
                            print(Fore.MAGENTA + Style.BRIGHT + str(hwname))  # 作业名
                            print(Fore.MAGENTA + Style.NORMAL + "材料文件:")
                            for file in resourceList:
                                file_url = "https://msyk.wpstatic.cn/" + file['resourceUrl']
                                materialRelasFiles.append(file['resTitle'])
                                materialRelasUrls.append(file_url)
                                print(Fore.GREEN + "\t" + file['resTitle'] + " " + file_url)
                            down = input(Fore.BLUE + "是否要下载文件 y/N:")
                            if down == "Y" or down == "y":
                                for url, file in zip(materialRelasUrls, materialRelasFiles):
                                    with open(file, "wb") as f, requests.get(url) as res:
                                        f.write(res.content)
                            serialNumbers, answers = "", ""


                        else:
                            # print(ress)
                            resourceList = json.loads(ress).get('resourceList')  # 材料文件列表
                            materialRelasUrls, materialRelasFiles, = [], []
                            hwname = json.loads(res).get('homeworkName')
                            print(Fore.MAGENTA + Style.BRIGHT + str(hwname))  # 作业名
                            print(Fore.MAGENTA + Style.NORMAL + "材料文件:")
                            for file in resourceList:
                                file_url = "https://msyk.wpstatic.cn/" + file['resourceUrl']
                                materialRelasFiles.append(file['resTitle'])
                                materialRelasUrls.append(file_url)
                                print(Fore.GREEN + "\t" + file['resTitle'] + " " + file_url)
                            down = input(Fore.BLUE + "是否要下载文件 y/N:")
                            if down == "Y" or down == "y":
                                for url, file in zip(materialRelasUrls, materialRelasFiles):
                                    with open(file, "wb") as f, requests.get(url) as res:
                                        f.write(res.content)
                            serialNumbers, answers = "", ""
                    else:
                        print("ress仍然为空，美师优课是傻逼")
                else:
                    print("res为空，美师优课是傻逼")

    else:
        Choice = input("ress为空，是否重新解析(默认是，否请输入1):")
        if Choice == "1":
            print("The program will be ended.")

        ################第二次重启#################
        else:
            dataup = {"homeworkId": int(hwid), "studentId": id, "modifyNum": 0, "unitId": unitId}
            res = post("https://padapp.msyk.cn/ws/teacher/homeworkCard/getHomeworkCardInfo", dataup, 2, hwid + '0')
            dataupp = {"homeworkId": hwid, "modifyNum": 0, "userId": id, "unitId": unitId}
            ress = post("https://padapp.msyk.cn/ws/common/homework/homeworkStatus", dataupp, 3, str(hwid) + '0')

            # print(ress)
            if ress.strip():
                try:
                    hwtp = json.loads(ress)
                    hwtp = json.loads(ress).get('homeworkType')
                except json.JSONDecodeError as e:
                    print("JSON格式错误:", e)
                if res.strip():
                    try:
                        code = json.loads(res).get('code')
                    except json.JSONDecodeError as e:
                        print("JSON格式错误:", e)
                    if str(hwtp) == "7":
                        materialRelasList, analysistList = json.loads(res).get('materialRelas'), json.loads(
                            res).get('analysistList')
                        materialRelasUrls, analysistUrls, materialRelasFiles, analysistFiles = [], [], [], []
                        hwname = json.loads(res).get('homeworkName')
                        print(Fore.MAGENTA + Back.WHITE + str(hwname))  # 作业名
                        res_list = json.loads(res).get('homeworkCardList')  # 题目list

                        if len(materialRelasList) == 0:
                            print(Fore.RED + "没有材料文件")
                        else:
                            print(Fore.MAGENTA + "材料文件:")
                            for file in materialRelasList:
                                if str(file['resourceUrl']).lower().startswith('http'):
                                    file_url = file['resourceUrl']
                                elif str(file['resourceUrl']).lower().startswith('//'):
                                    file_url = "https://msyk.wpstatic.cn" + file['resourceUrl']
                                elif str(file['resourceUrl']).lower().startswith('/'):
                                    file_url = "https://msyk.wpstatic.cn" + file['resourceUrl']
                                else:
                                    file_url = "https://msyk.wpstatic.cn/" + file['resourceUrl']
                                materialRelasFiles.append(file['title'])
                                materialRelasUrls.append(file_url)
                                print(Fore.GREEN + "\t" + file['title'] + " " + file_url)

                        if len(analysistList) == 0:
                            print(Fore.RED + "没有答案文件")
                        else:
                            print(Fore.MAGENTA + "答案文件:")
                            for file in analysistList:
                                if str(file['resourceUrl']).lower().startswith('http'):
                                    file_url = file['resourceUrl']
                                elif str(file['resourceUrl']).lower().startswith('//'):
                                    file_url = "https://msyk.wpstatic.cn" + file['resourceUrl']
                                elif str(file['resourceUrl']).lower().startswith('/'):
                                    file_url = "https://msyk.wpstatic.cn" + file['resourceUrl']
                                else:
                                    file_url = "https://msyk.wpstatic.cn/" + file['resourceUrl']
                                analysistFiles.append(file['title'])
                                analysistUrls.append(file_url)
                                print(Fore.GREEN + "\t" + file['title'] + " " + file_url)

                        question_list = []
                        for question in res_list:
                            serialNumber = str(question['serialNumber'])
                            url = "https://www.msyk.cn/webview/newQuestion/singleDoHomework?studentId=" + id + "&homeworkResourceId=" + str(
                                question['resourceId']) + "&orderNum=" + (
                                      question['orderNum']) + "&showAnswer=1&unitId=" + unitId + "&modifyNum=1"
                            # 浏览器打开带答案的网页
                            # open_url(url)
                            vink = requests.get(url=url)
                            answer = ljlVink_parsemsyk(vink.text, (question['orderNum']), url)
                            question_list.append(question['resourceId'])

                            answer = answer_encode(answer)
                            if serialNumbersa == "":
                                serialNumbersa += serialNumber
                                answersa += answer
                            else:
                                serialNumbersa += ";" + serialNumber
                                answersa += ";" + answer

                            if answer != "wtf":
                                answer = answer_encode(answer)
                                if serialNumbers == "":
                                    serialNumbers += serialNumber
                                    answers += answer
                                else:
                                    serialNumbers += ";" + serialNumber
                                    answers += ";" + answer

                        print(question_list)  # 打印题目id列表
                        up = input(Fore.MAGENTA + "是否要提交选择答案 y/N:")
                        if up == "Y" or up == "y":
                            dataup = {"serialNumbers": serialNumbers, "answers": answers, "studentId": id,
                                      "homeworkId": int(hwid), "unitId": unitId, "modifyNum": 0}
                            res = post("https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives",
                                       dataup, 2, answers + hwid + '0' + serialNumbers)
                            if json.loads(res).get('code') == "10000":
                                print(Fore.GREEN + "自动提交选择答案成功")

                        middle = input(Fore.YELLOW + "是否要为主观题提交假图片 y/N:")
                        if middle == "Y" or up == "y":
                            dataup = {"serialNumbers": serialNumbersa, "answers": answersa, "studentId": id,
                                      "homeworkId": int(hwid), "unitId": unitId, "modifyNum": 0}
                            res = post("https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives",
                                       dataup, 2, answers + hwid + '0' + serialNumbers)
                            if json.loads(res).get('code') == "10000":
                                print(Fore.GREEN + "自动提交主观题提交假图片成功")

                        if len(analysistList) != 0 or len(materialRelasList) != 0:
                            down = input(Fore.BLUE + "是否要下载文件 y/N:")
                            if down == "Y" or down == "y":
                                for url, file in zip(materialRelasUrls, materialRelasFiles):
                                    with open(file, "wb") as f, requests.get(url) as res:
                                        f.write(res.content)
                                for url, file in zip(analysistUrls, analysistFiles):
                                    with open(file, "wb") as f, requests.get(url) as res:
                                        f.write(res.content)
                        serialNumbers, answers = "", ""
                    elif str(hwtp) == "5":
                        # print(ress)
                        resourceList = json.loads(ress).get('resourceList')  # 材料文件列表
                        materialRelasUrls, materialRelasFiles, = [], []
                        hwname = json.loads(res).get('homeworkName')
                        print(Fore.MAGENTA + Style.BRIGHT + str(hwname))  # 作业名
                        print(Fore.MAGENTA + Style.NORMAL + "材料文件:")
                        for file in resourceList:
                            file_url = "https://msyk.wpstatic.cn/" + file['resourceUrl']
                            materialRelasFiles.append(file['resTitle'])
                            materialRelasUrls.append(file_url)
                            print(Fore.GREEN + "\t" + file['resTitle'] + " " + file_url)
                        down = input(Fore.BLUE + "是否要下载文件 y/N:")
                        if down == "Y" or down == "y":
                            for url, file in zip(materialRelasUrls, materialRelasFiles):
                                with open(file, "wb") as f, requests.get(url) as res:
                                    f.write(res.content)
                        serialNumbers, answers = "", ""


                    else:
                        # print(ress)
                        resourceList = json.loads(ress).get('resourceList')  # 材料文件列表
                        materialRelasUrls, materialRelasFiles, = [], []
                        hwname = json.loads(res).get('homeworkName')
                        print(Fore.MAGENTA + Style.BRIGHT + str(hwname))  # 作业名
                        print(Fore.MAGENTA + Style.NORMAL + "材料文件:")
                        for file in resourceList:
                            file_url = "https://msyk.wpstatic.cn/" + file['resourceUrl']
                            materialRelasFiles.append(file['resTitle'])
                            materialRelasUrls.append(file_url)
                            print(Fore.GREEN + "\t" + file['resTitle'] + " " + file_url)
                        down = input(Fore.BLUE + "是否要下载文件 y/N:")
                        if down == "Y" or down == "y":
                            for url, file in zip(materialRelasUrls, materialRelasFiles):
                                with open(file, "wb") as f, requests.get(url) as res:
                                    f.write(res.content)
                        serialNumbers, answers = "", ""
                else:
                    print("ress仍然为空，美师优课是傻逼")
            else:
                print("res为空，美师优课是傻逼")
                
#PPT下载
def get_ppt_info_post(ppt_resource_id, res_source=1):
    """获取PPT文件的页面信息（POST方式）"""
    salt = getCurrentTime()
    # 生成key
    key_data = f"{ppt_resource_id}{res_source}{salt}{sign}{msyk_key}"
    key = string_to_md5(key_data)
    
    dataup = {
        "pptResourceId": ppt_resource_id,
        "resSource": res_source,
        "salt": salt,
        "sign": sign,
        "key": key
    }
    
    res = post("https://padapp.msyk.cn/ws/student/homework/studentHomework/homeworkPPTInfo", 
               dataup, type=2)
    
    if res.strip() and json.loads(res).get('code') == "10000":
        return json.loads(res).get('sqPptConvertList', [])
    return []

def download_ppt(ppt_resource_id, res_title):
    """下载PPT页面并提供PDF转换选项"""
    print(Fore.YELLOW + "文件名:", Fore.CYAN + Back.WHITE + res_title)
    
    # 获取PPT页面信息
    ppt_pages = get_ppt_info_post(ppt_resource_id)
    if not ppt_pages:
        print(Fore.RED + "无法获取PPT页面信息")
        return False
    
    print(Fore.GREEN + f"找到 {len(ppt_pages)} 页PPT")
    
    # 创建下载目录
    safe_title = re.sub(r'[<>:"/\\|?*]', '_', res_title)  # 移除文件名中的非法字符
    download_dir = f"PPT_{ppt_resource_id}_{safe_title}"
    os.makedirs(download_dir, exist_ok=True)
    
    # 下载所有页面
    success_count = 0
    for page in ppt_pages:
        page_url = "https://msyk.wpstatic.cn/" + page['path']
        page_num = page['displayNum']
        page_filename = f"{download_dir}/第{page_num:02d}页.jpg"
        
        print(Fore.CYAN + f"下载第 {page_num} 页...")
        try:
            response = requests.get(page_url, stream=True, timeout=30)
            if response.status_code == 200:
                with open(page_filename, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(Fore.GREEN + f"第 {page_num} 页下载成功")
                success_count += 1
            else:
                print(Fore.RED + f"第 {page_num} 页下载失败: HTTP {response.status_code}")
        except Exception as e:
            print(Fore.RED + f"第 {page_num} 页下载失败: {str(e)}")
    
    if success_count > 0:
        print(Fore.GREEN + f"下载完成！共成功下载 {success_count}/{len(ppt_pages)} 页")
        print(Fore.GREEN + f"文件保存在: {os.path.abspath(download_dir)}/")
        
        # 如果Pillow可用，提供PDF转换选项
        if PILLOW_AVAILABLE and success_count == len(ppt_pages):
            convert_choice = input(Fore.BLUE + "是否要转换为PDF文件？[Y/n]")
            if convert_choice == 'Y' or convert_choice == 'y':
                pdf_path = convert_ppt_to_pdf(download_dir, f"{safe_title}.pdf")
                if pdf_path:
                    print(Fore.GREEN + f"PDF转换成功: {pdf_path}")
        elif not PILLOW_AVAILABLE:
            print(Fore.YELLOW + "提示: 安装Pillow库后可以自动转换PPT为PDF")
            print(Fore.YELLOW + "命令: pip install Pillow")
        
        return True
    else:
        print(Fore.RED + "所有页面下载失败")
        return False

def convert_ppt_to_pdf(ppt_folder, output_pdf):
    """将PPT图片文件夹转换为PDF"""
    if not PILLOW_AVAILABLE:
        print(Fore.RED + "错误: Pillow库未安装，无法转换PDF")
        print(Fore.YELLOW + "请运行: pip install Pillow")
        return None
    
    try:
        # 获取所有图片文件
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png']:
            image_files.extend([f for f in os.listdir(ppt_folder) if f.lower().endswith(ext)])
        
        if not image_files:
            print(Fore.RED + f"错误: 在 '{ppt_folder}' 中没有找到图片文件")
            return None
        
        # 按数字顺序排序
        image_files.sort(key=lambda x: [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', x)])
        
        # 转换为PDF
        images = []
        for img_file in image_files:
            img_path = os.path.join(ppt_folder, img_file)
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images.append(img)
            print(Fore.CYAN + f"已加载: {img_file}")
        
        if images:
            # 确保输出路径是绝对路径
            if not os.path.isabs(output_pdf):
                output_pdf = os.path.join(os.getcwd(), output_pdf)
            
            images[0].save(output_pdf, save_all=True, append_images=images[1:])
            return output_pdf
            
    except Exception as e:
        print(Fore.RED + f"PDF转换失败: {str(e)}")
        return None
    
    return None

def getUnreleasedHWID():
    EndHWID = 0
    StartHWID = int(input(Fore.YELLOW + "请输入起始作业id:"))
    EndHWID = int(input(Fore.YELLOW + "请输入截止作业id(小于起始则不会停):"))
    hwidplus100 = StartHWID + 100
    while roll == 1:
        if StartHWID == hwidplus100:
            print(Fore.GREEN + "已滚动100项 当前" + str(hwidplus100))
            hwidplus100 += 100

        dataup = {"homeworkId": StartHWID, "modifyNum": 0, "userId": id, "unitId": unitId}
        res = post("https://padapp.msyk.cn/ws/common/homework/homeworkStatus", dataup, 3, str(StartHWID) + '0')
        # print(res)
        if 'isWithdrawal' in res:
            pass
        else:
            if res.strip():
                try:
                    hwname = json.loads(res).get('homeworkName')
                    hwtp = json.loads(res).get('homeworkType')
                    SubCode = json.loads(res).get('subjectCode')
                    subject_name = SUBJECT_CODE_MAP.get(str(SubCode), "其他")
                    color = SUBJECT_COLORS.get(subject_name, SUBJECT_COLORS['其他'])
                    StarttimeArray = time.localtime(json.loads(res).get('startTime') / 1000)
                    StarttimePrint = time.strftime("%Y-%m-%d %H:%M:%S", StarttimeArray)
                    EndtimeArray = time.localtime(json.loads(res).get('endTime') / 1000)
                    EndtimePrint = time.strftime("%Y-%m-%d %H:%M:%S", EndtimeArray)
                    print(Style.BRIGHT + Fore.BLUE + str(StartHWID) + 
                          " 作业类型:" + str(hwtp) + " " + 
                          Style.BRIGHT + color + "[" + subject_name + "]" + " " + 
                          Fore.BLUE + hwname + Style.NORMAL + 
                          Fore.RED + " 开始时间:" + Fore.BLUE + " " + StarttimePrint + 
                          Fore.RED + " 截止时间:" + Fore.BLUE + " " + EndtimePrint)
                except json.JSONDecodeError as e:
                    print("JSON格式错误:", e)
            else:
                print("res为空，跳过解析")

        if StartHWID == EndHWID:
            print(Fore.CYAN + "跑作业id结束 当前作业id为" + str(StartHWID))
            break
        StartHWID += 1

def MainMenu():
    ProfileImport = ""
    print(Fore.MAGENTA + "1.作业获取答案(默认)\n2.跑作业id\n3.切换账号\n4.退出")
    #print(Fore.MAGENTA + "5.消息系统\n6.学习圈系统")  # 取消注释以启用额外功能
    Mission = input(Fore.RED + "请选择要执行的任务:")
    if Mission == "2":
        getUnreleasedHWID()
    elif Mission == "3":
        open("ProfileCache.txt", "w", encoding='utf-8').write("")
        print(Fore.CYAN + "已清空 ProfileCache 登录缓存。")
        ProfileImport = input(Fore.CYAN + "请提供登录信息(如无则执行账号密码登录):")
        try:
            setAccountInform(ProfileImport)
        except:
            login()
    elif Mission == "4":  # 新增退出选项
        print(Fore.GREEN + "程序已退出")
        exit(0)
    #取消以下注释以启用消息系统和学习圈系统
    #elif Mission == "5":
    #    msyk_message.message_menu(id, unitId)
    #elif Mission == "6":
    #    msyk_learning_circle.learning_circle_menu(id, unitId)
    else:
        getAnswer()


Start = getAccountInform()

dataup = {"studentId": id, "subjectCode": None, "homeworkType": -1, "pageIndex": 1, "pageSize": 36, "statu": 1,"homeworkName": None, "unitId": unitId}
res = post("https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList", dataup, 2, "-11361")
if res.strip():
    try:
        reslist = json.loads(res).get('sqHomeworkDtoList')  # 作业list
    except json.JSONDecodeError as e:
        print("JSON格式错误:", e)
else:
    Choice = input("res为空，是否重新解析(默认是，否请输入1):")
    if Choice == "1":
        print("The program will be ended.")
    else:
        dataup = {"studentId": id, "subjectCode": None, "homeworkType": -1, "pageIndex": 1, "pageSize": 36, "statu": 1,
                  "homeworkName": None, "unitId": unitId}
        res = post("https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList", dataup, 2, "-11361")
        if res.strip():
            try:
                reslist = json.loads(res).get('sqHomeworkDtoList')  # 作业list
            except json.JSONDecodeError as e:
                print("JSON格式错误:", e)
        else:
            print("res仍然为空，美师优课是傻逼")
# print(res)

# 优化后的打印函数
def print_homework_item(item, timePrint):
    """作业项打印函数"""
    subject_name = str(item['subjectName'])
    # 如果科目名称在反向映射中，获取更准确的颜色
    subject_code = SUBJECT_NAME_TO_CODE.get(subject_name, "")
    if subject_code:
        # 如果有科目代码，使用科目代码映射获取科目名称（确保一致性）
        subject_name = SUBJECT_CODE_MAP.get(subject_code, subject_name)
    color = SUBJECT_COLORS.get(subject_name, SUBJECT_COLORS['其他'])  # 使用字典获取颜色，默认为其他颜色
    print(
        Fore.YELLOW + str(item['id']) + 
        " 作业类型:" + str(item['homeworkType']) + " " + 
        Style.BRIGHT + color + "[" + subject_name + "]" + 
        Style.NORMAL + Fore.YELLOW + " " + item['homeworkName'] + 
        " 截止时间:" + timePrint
    )

# 打印业类型7的作业
for item in reslist:
    if str(item['homeworkType']) == '7':
        timeArray = time.localtime(item['endTime'] / 1000)
        timePrint = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        print_homework_item(item, timePrint)

print(Fore.BLUE + "以下为阅读作业及其他作业，可能无答案且不需提交")

# 打印非作业类型7的作业
for item in reslist:
    if str(item['homeworkType']) != '7':
        timeArray = time.localtime(item['endTime'] / 1000)
        timePrint = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        print_homework_item(item, timePrint)

while roll == 1:
    MainMenu()