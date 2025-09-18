import hashlib
import json
import re
import webbrowser
import requests
import time
import base64
import os
from rsa import core, PublicKey, transform, decrypt, PrivateKey
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

FIXED_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEqAIBAAKCAQEAndq0AWyxkp0ted7i4He7GW2YpENpXye0sSEs9z1dKE67GILj
wsg62ghhtjdDF/5Dt95Gw7VyXfXvZlmIrXXYVYmkLfz0rjpZj3gaTe/vmqEFU0pP
brkiLa38e6Bihjy3HzfaqEz25voOtP/gLJ6J4j9uKeyXQsYela/KqTFYdvT6Ac+L
t78pkB2GEfxJmqqn82yiT/Kz4aQN9rnIc06Z9M6Gn6XCwyLso33Y2LwMW4GUDek+
8dYGLJ1lCb/5LyamMfX/0odc4/yb1IomtVKwfYUlf9ThEOXSSJ5Z7o1bedOYMFbc
3jes7yZSnl+ldLBIAQ48meEngQJFSekjIA1YtwIDAQABAoIBABVaPRkoO8jqS/l9
RdE5QOzKn2gw2jMN6uo+45c6DLzkEXjaU7bIYPWXRqhgR0oakcxwW8Ajbin5l32P
xOY5156SdMvnuK1MpUq740sBlrai61Z96cq/bjkhnNKYOluQIPEvG/vCFW/fCVhA
eHFwrJQXIm63WyqkI+xd8tkeRbH0+ruay952cn4jullkAf91GKmRGUBPy0WrMJlw
05atQUNOxLsNR9tggPK9xIgmnm/LSjCrk/VIWYCuNS6Ws5d9+uPqIqvHW17ZS18N
f7l7fUDeWYBxh89guuWZ5bk17ucAaaCX0xrAOntxe9Pxx/Ru1Y/siHqGXqZi2x56
uRuAQlkCgYkAter0paMoWRP4ogmMFe+09rWvGmerP3he15JLSI9sGv6NGeLnnEAo
+uiJ7KXCyFq0MWQPFiG7P9JNtxVuWB8Dw30KCnBO/xotpVJZaQWsUSmHGT1nTKUp
PRtqA9bLOi2shI2Pcwjle9ZDIRUrrAZ3AGdNU6K0vOXmkg3F4cN1cLc4oyTqB1Rv
TQJ5AN4jHSs7o55mXx2hSkvB1AhJMoHGbm/2dgrVdbFIPcSLLEhq5kqKN1QUaTNE
HWqxLVRIB9Vc59aTARoWzmd27YntehkQLhueDfmtMibLoD2VQLUQ+DiJ1TvzG0kX
9HE5wQFJdalV11S7vali2YgiJQqjRHFbMc5uEwKBiChaEqQ/Ga8QoAEJTxp6jlB/
InUf87tjbt4wZCSXM6qVNiU80JU3Ih/tvtJQPnGEtR2TjUkieE+CzZxD07MWRhZx
wO1p1gv9+YwHRS/ngz6JkJ8HoMc+h3Q3hX+OgIvKH89TOzOQEJ80erV25bYFxRXA
1EUt/Rs9f7R7+53FZmJ3Mcf2Yzb3Aq0CeBDKorfT6EhfAK2itZUIb9i4f8LjlxGL
ldy3yg++oDytMInA2uujiw8mA9XGPlsETaLjVwQ/456KujiYpL2ZdddJRkOCv5mC
1xeaigH4voIpOBz3zWuor5+6fsOFtgqhDP/l56kHPiG/l1Sojj0GJ7qoINJYzGkI
VQKBiGS0b9tZnBW99F6U+OkNINmGRS9RKrZblPDml2h3KdtC8GljG/s59Eo0tWmB
430oa5/FuFV++LJH+AUFAc/kF64qfGrXh3kNMMebJmi79T7+gZlDdvo+7Dg4Aljo
SAAql73hRLtcvMx/tQb6GEttBoUJnl1eSG6qB/Zgviu4pCF2wTc+H50RTic=
-----END RSA PRIVATE KEY-----"""

def rsa_decrypt_data(encrypted_data):
    """使用固定的RSA私钥解密数据"""
    try:
        # Base64解码
        encrypted_bytes = base64.b64decode(encrypted_data)
        
        # 加载固定私钥
        privkey = PrivateKey.load_pkcs1(FIXED_PRIVATE_KEY.encode())
        
        # RSA解密的分段大小
        chunk_size = 256  # 2048位密钥的加密块大小
        decrypted_chunks = []
        
        # 分段解密
        for i in range(0, len(encrypted_bytes), chunk_size):
            chunk = encrypted_bytes[i:i+chunk_size]
            decrypted_chunk = decrypt(chunk, privkey)
            decrypted_chunks.append(decrypted_chunk)
        
        # 合并所有解密块并解码为字符串
        decrypted_data = b''.join(decrypted_chunks)
        return decrypted_data.decode('utf-8')
    except Exception:
        return None

def getAccountInform():
    try:
        with open("ProfileCache.txt", "r", encoding='utf-8') as f:
            encrypted_data = f.read().strip()
        
        # 尝试解密数据
        decrypted_data = rsa_decrypt_data(encrypted_data)
        if decrypted_data:
            setAccountInform(decrypted_data)
        else:
            # 如果解密失败，尝试作为明文处理
            try:
                setAccountInform(encrypted_data)
            except Exception:
                print("4")
                exit(4)  # RSA解密失败且明文解析也失败
    except FileNotFoundError:
        print("0")
        exit(0)  # ProfileCache.txt不存在
    except Exception:
        print("1")
        exit(1)  # 其他读取错误

def answer_encode(answer: str) -> str:
    """
    将多选题答案（如 "ACD"）编码成 10 位 01 串，对应 A~J 的选中状态。
    单字符答案直接原样返回。
    """
    if len(answer) == 1:          # 单选 / 判断
        return answer

    OPTIONS = "ABCDEFGHIJ"        # 10 个候选选项
    # 利用位图生成 0/1 串
    return ''.join('1' if ch in answer else '0' for ch in OPTIONS)


def public_key_decrypt(publicKey, content):
    try:
        qr_code_cipher = base64.b64decode(content)
        public_key = base64.b64decode(publicKey)
        rsa_public_key = PublicKey.load_pkcs1_openssl_der(public_key)
        cipher_text_bytes = transform.bytes2int(qr_code_cipher)
        decrypted_text = core.decrypt_int(cipher_text_bytes, rsa_public_key.e, rsa_public_key.n)
        final_text = transform.int2bytes(decrypted_text)
        final_code = final_text[final_text.index(0) + 1:]
        return final_code.decode()
    except Exception:
        return None  # 静默失败
        print('5')
        exit(5)

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
    try:
        if json.loads(result).get('code') == "10000":
            global unitId, id
            unitId = json.loads(result).get('InfoMap').get('unitId')
            id = json.loads(result).get('InfoMap').get('id')
            sign1 = public_key_decrypt(msyk_sign_pubkey, json.loads(result).get('sign')).split(':')
            if sign1 != None:
                global sign
                sign = sign1[1] + id
        else:
            print("1")
            exit(1)  # 登录失败
    except Exception:
        print("1")
        exit(1)  # 解析失败

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
        except json.JSONDecodeError:
            print("3")
            exit(3)
        if res.strip():
            try:
                code = json.loads(res).get('code')
            except json.JSONDecodeError:
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
                    if json.loads(res).get('code')!="10000":
                        print('2.1')
                middle = "y"
                if middle=="Y" or up=="y":
                    dataupp={"serialNumbers":serialNumbersa,"answers":answersa,"studentId":id,"homeworkId":int(hwid),"unitId":unitId,"modifyNum":0}
                    res=post("https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives",dataupp,2,answers+hwid+'0'+serialNumbers)
                    if json.loads(res).get('code')!="10000":
                        print('2.2')
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
                    hwtp = json.loads(res).get('homeworkType')
                    StartTime = json.loads(res).get('startTime')
                    if StartTime >= Time and str(hwtp) == "7":
                        usefulHWID_list1.append(StartHWID)
                except json.JSONDecodeError:
                    print("3")
                    exit(3)
            else:
                print("3")
                exit(3)
        if StartHWID == EndHWID:
            break
        StartHWID += 1

def MainMenu():
    for item in usefulHWID_list2:
        getAnswer(item)
    for item in usefulHWID_list1:
        getAnswer(item)
    #输出退出代码
    print("10")
    exit(10)

Start=getAccountInform()
dataup={"studentId":id,"subjectCode":None,"homeworkType":-1,"pageIndex":1,"pageSize":36,"statu":1,"homeworkName":None,"unitId":unitId}
res=post("https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList",dataup,2,"-11361")
if res.strip():
    try:
        reslist=json.loads(res).get('sqHomeworkDtoList')
    except json.JSONDecodeError:
        print("3")
        exit(3)
else:
    print("3")
    exit(3)  # res为空

for item in reslist:
    usefulHWID_list3.append(item['id'])
    if str(item['homeworkType']) == '7':
        usefulHWID_list2.append(item['id'])

DefaultHWID = max(usefulHWID_list3)
getUnreleasedHWID()
while roll == 1:
    MainMenu()