import hashlib
import json
import re
import webbrowser
import requests
import time
import base64
from rsa import core, PublicKey, transform
from colorama import init

init(autoreset=True)  # 文字颜色自动恢复
roll = 1  # 循环
serialNumbers, answers, serialNumbersa, answersa = "", "", "", ""
msyk_sign_pubkey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAj7YWxpOwulFyf+zQU77Y2cd9chZUMfiwokgUaigyeD8ac5E8LQpVHWzkm+1CuzH0GxTCWvAUVHWfefOEe4AThk4AbFBNCXqB+MqofroED6Uec1jrLGNcql9IWX3CN2J6mqJQ8QLB/xPg/7FUTmd8KtGPrtOrKKP64BM5cqaB1xCc4xmQTuWvtK9fRei6LVTHZyH0Ui7nP/TSF3PJV3ywMlkkQxKi8JBkz1fx1ZO5TVLYRKxzMQdeD6whq+kOsSXhlLIiC/Y8skdBJmsBWDMfQXxtMr5CyFbVMrG+lip/V5n22EdigHcLOmFW9nnB+sgiifLHeXx951lcTmaGy4uChQIDAQAB"
msyk_key = "DxlE8wwbZt8Y2ULQfgGywAgZfJl82G9S"
headers = {'user-agent': "okhttp/3.12.1"}
sign = ""
usefulHWID_list1 = []
usefulHWID_list2 = []
usefulHWID_list3 = []

def getAccountInform():
    ReturnInform = ""
    try:
        with open("ProfileCache.txt", "r", encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip('\n')
                ReturnInform = ReturnInform + line
        setAccountInform(ReturnInform)
    except BaseException:
        print("0")
        exit(0)

def answer_encode(answer):
    answer_code = ""
    if len(answer) == 1:
        return answer
    else:
        if "A" in answer:
            answer_code += "1"
        else:
            answer_code += "0"
        if "B" in answer:
            answer_code += "1"
        else:
            answer_code += "0"
        if "C" in answer:
            answer_code += "1"
        else:
            answer_code += "0"
        if "D" in answer:
            answer_code += "1"
        else:
            answer_code += "0"
        if "E" in answer:
            answer_code += "1"
        else:
            answer_code += "0"
        if "F" in answer:
            answer_code += "1"
        else:
            answer_code += "0"
        if "G" in answer:
            answer_code += "1"
        else:
            answer_code += "0"
        if "H" in answer:
            answer_code += "1"
        else:
            answer_code += "0"
        if "I" in answer:
            answer_code += "1"
        else:
            answer_code += "0"
        if "J" in answer:
            answer_code += "1"
        else:
            answer_code += "0"
        return answer_code

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
        print("0")
        exit(0)
        return None

def ljlVink_parsemsyk(html_doc, count, url):
    html_doc.replace('\n', "")
    index = html_doc.find("var questions = ")
    index1 = html_doc.find("var resource")
    if index != -1:
        data = json.loads(html_doc[index + 16:index1 - 7])
        if data[0].get('answer') != None:
            answer = "".join(data[0].get('answer')).lstrip("[")[:-1].replace('"', '').lstrip(",").replace(',', ' ')
            if (re.search(r'\d', answer)):
                open_url(url)
                return "wtf"
            else:
                return answer
        else:
            return "wtf"

def ljlVink_parsemsyk1(html_doc, count, url):
    html_doc.replace('\n', "")
    index = html_doc.find("var questions = ")
    index1 = html_doc.find("var resource")
    if index != -1:
        data = json.loads(html_doc[index + 16:index1 - 7])
        if data[0].get('answer') != None:
            answer = "".join(data[0].get('answer')).lstrip("[")[:-1].replace('"', '').lstrip(",").replace(',', ' ')
            if (re.search(r'\d', answer)):
                open_url(url)
                return "wtf"
            else:
                return answer
        else:
            answer = " "
            return answer

def getCurrentTime():
    return int(round(time.time() * 1000))

def TimeToHMS(ts: int):
    return time.strftime("%H:%M:%S", time.localtime(ts / 1000))

def string_to_md5(string):
    md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
    return md5_val

def open_url(url):
    webbrowser.open_new(url)

def setAccountInform(result):
    if json.loads(result).get('code') == "10000":
        open("ProfileCache.txt", "w", encoding='utf-8').write(result)
        global unitId, id
        unitId = json.loads(result).get('InfoMap').get('unitId')
        id = json.loads(result).get('InfoMap').get('id')
        sign1 = public_key_decrypt(msyk_sign_pubkey, json.loads(result).get('sign')).split(':')
        if sign1 != None:
            signdec = ','.join(sign1)
            global sign
            sign = sign1[1] + id
    else:
        print("1")
        exit(1)

def post(url, postdata, type=1, extra=''):
    time = getCurrentTime()
    key = ''
    if type == 1:
        key = string_to_md5(extra + str(time) + sign + msyk_key)
    elif type == 2:
        key = string_to_md5(extra + id + unitId + str(time) + sign + msyk_key)
    elif type == 3:
        key = string_to_md5(extra + unitId + id + str(time) + sign + msyk_key)
    postdata.update({'salt': time, 'sign': sign, 'key': key})
    try:
        req = requests.post(url=url, data=postdata, headers=headers)
        return req.text
    except:
        print("1")
        exit(1)

def getAnswer(item):
    hwid = str(item)
    dataup = {"homeworkId":int(hwid),"studentId":id,"modifyNum":0,"unitId":unitId}
    res=post("https://padapp.msyk.cn/ws/teacher/homeworkCard/getHomeworkCardInfo",dataup,2,hwid+'0')
    dataupp = {"homeworkId": hwid, "modifyNum": 0, "userId": id, "unitId": unitId}
    ress = post("https://padapp.msyk.cn/ws/common/homework/homeworkStatus", dataupp, 3, str(hwid) + '0')
    if ress.strip():
        try:
            hwtp = json.loads(ress).get('homeworkType')
        except json.JSONDecodeError as e:
            print("3")
            exit(3)
        if res.strip():
            try:
                code = json.loads(res).get('code')
            except json.JSONDecodeError as e:
                print("3")
                exit(3)
            if str(hwtp) == "7":
                res_list=json.loads(res).get('homeworkCardList')
                question_list = []
                global serialNumbers,answers,serialNumbersa,answersa
                for question in res_list:
                    serialNumber=str(question['serialNumber'])
                    url="https://www.msyk.cn/webview/newQuestion/singleDoHomework?studentId="+id+"&homeworkResourceId="+str(question['resourceId'])+"&orderNum="+(question['orderNum'])+"&showAnswer=1&unitId="+unitId+"&modifyNum=1"
                    vink=requests.get(url=url)
                    answer=ljlVink_parsemsyk(vink.text,(question['orderNum']),url)
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
                up = "y"
                if up=="Y" or up=="y":
                    dataup={"serialNumbers":serialNumbers,"answers":answers,"studentId":id,"homeworkId":int(hwid),"unitId":unitId,"modifyNum":0}
                    res=post("https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives",dataup,2,answers+hwid+'0'+serialNumbers)
                    if json.loads(res).get('code')=="10000":
                        pass
                    else:
                        print("2.1")
                middle = "y"
                if middle=="Y" or up=="y":
                    dataupp={"serialNumbers":serialNumbersa,"answers":answersa,"studentId":id,"homeworkId":int(hwid),"unitId":unitId,"modifyNum":0}
                    res=post("https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives",dataupp,2,answers+hwid+'0'+serialNumbers)
                    if json.loads(res).get('code')=="10000":
                        pass
                    else:
                        print("2.2")
        else:
            print("3")
            exit(3)

def getUnreleasedHWID():
    StartHWID = DefaultHWID - 100
    EndHWID = DefaultHWID + 200
    hwidplus100 = DefaultHWID
    Time = getCurrentTime()
    while roll == 1:
        if StartHWID == hwidplus100:
            hwidplus100 += 100
        dataup = {"homeworkId": StartHWID, "modifyNum": 0, "userId": id, "unitId": unitId}
        res = post("https://padapp.msyk.cn/ws/common/homework/homeworkStatus", dataup, 3, str(StartHWID) + '0')
        if 'isWithdrawal' in res:
            pass
        else:
            if res.strip():
                try:
                    # hwname = json.loads(res).get('homeworkName')
                    hwtp = json.loads(res).get('homeworkType')
                    # SubCode = json.loads(res).get('subjectCode')
                    # StarttimeArray = time.localtime(json.loads(res).get('startTime') / 1000)
                    StartTime = json.loads(res).get('startTime')
                    if StartTime >= Time and str(hwtp) == "7":
                        usefulHWID_list1.append(StartHWID)
                except json.JSONDecodeError as e:
                    print("3")
                    exit(3)
            else:
                print("3")
                exit(3)
        if StartHWID == EndHWID:
            # print(Fore.CYAN + "跑作业id结束 当前作业id为" + str(StartHWID))
            break
        StartHWID += 1

def MainMenu():
    for item in usefulHWID_list2:
        getAnswer(item)
    # print(666)
    for item in usefulHWID_list1:
        getAnswer(item)
    # print(777)
    print("10")
    exit(10)

Start=getAccountInform()
dataup={"studentId":id,"subjectCode":None,"homeworkType":-1,"pageIndex":1,"pageSize":36,"statu":1,"homeworkName":None,"unitId":unitId}
res=post("https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList",dataup,2,"-11361")
if res.strip():
    try:
        reslist=json.loads(res).get('sqHomeworkDtoList')#作业list
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
for item in reslist:
    timeArray = time.localtime ((item['endTime'])/1000)
    timePrint = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    usefulHWID_list3.append(item['id'])
    if str(item['homeworkType']) == '7':
        usefulHWID_list2.append(item['id'])
    else:
        pass
DefaultHWID = max(usefulHWID_list3)
# print("已完成获取最大id")
getUnreleasedHWID()
# print("已完成获取id")
while roll == 1:
    MainMenu()