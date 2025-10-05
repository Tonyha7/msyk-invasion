import hashlib
import json
import requests
import time
import base64
from rsa import core, PublicKey, transform, decrypt, PrivateKey
from colorama import init

init(autoreset=True)
roll = 1
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
    try:
        encrypted_bytes = base64.b64decode(encrypted_data)
        privkey = PrivateKey.load_pkcs1(FIXED_PRIVATE_KEY.encode())
        chunk_size = 256
        decrypted_chunks = []
        for i in range(0, len(encrypted_bytes), chunk_size):
            chunk = encrypted_bytes[i:i+chunk_size]
            decrypted_chunk = decrypt(chunk, privkey)
            decrypted_chunks.append(decrypted_chunk)
        decrypted_data = b''.join(decrypted_chunks)
        return decrypted_data.decode('utf-8')
    except Exception:
        return None

def getAccountInform():
    try:
        with open("ProfileCache.txt", "r", encoding='utf-8') as f:
            encrypted_data = f.read().strip()
        decrypted_data = rsa_decrypt_data(encrypted_data)
        if decrypted_data:
            setAccountInform(decrypted_data)
        else:
            try:
                setAccountInform(encrypted_data)
            except Exception:
                print("4")
                exit(4)
    except FileNotFoundError:
        print("0")
        exit(0)
    except Exception:
        print("1")
        exit(1)

def answer_encode(answer: str) -> str:
    if len(answer) == 1:
        return answer
    OPTIONS = "ABCDEFGHIJ"
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
        return None
        exit(5)

def getCurrentTime():
    return int(round(time.time() * 1000))

def string_to_md5(string):
    md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
    return md5_val

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
            exit(1)
    except Exception:
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

def operation_answerget_new(id, unitId, hwid):
    serialNumbers, answers = "", ""
    try:
        url = f"https://padapp.msyk.cn/ws/teacher/homeworkCard/getHomeworkCardInfo?homeworkId={hwid}&studentId=&modifyNum=0&unitId={unitId}"
        response = requests.get(url)
        body = response.json()
        if 'homeworkCardList' not in body:
            return False
        homeworkCardList = body['homeworkCardList']
        for homeworkCard in homeworkCardList:
            serialNumber = homeworkCard['serialNumber']
            answer = homeworkCard.get('answer', '')
            blankList = homeworkCard.get('blankList', [])
            questionType = homeworkCard.get('questionType', 1)
            if questionType == 1 and answer:
                if not serialNumbers:
                    serialNumbers = str(serialNumber)
                    answers = str(answer)
                else:
                    serialNumbers += ";" + str(serialNumber)
                    answers += ";" + str(answer)
            elif questionType == 2 and answer and len(answer) == 10:
                if not serialNumbers:
                    serialNumbers = str(serialNumber)
                    answers = str(answer)
                else:
                    serialNumbers += ";" + str(serialNumber)
                    answers += ";" + str(answer)
            elif questionType == 4 and blankList:
                pass
            elif questionType == 5 and answer:
                if not serialNumbers:
                    serialNumbers = str(serialNumber)
                    answers = str(answer)
                else:
                    serialNumbers += ";" + str(serialNumber)
                    answers += ";" + str(answer)
            else:
                if not serialNumbers:
                    serialNumbers = str(serialNumber)
                    answers = "BYEBYEMSYK"
                else:
                    serialNumbers += ";" + str(serialNumber)
                    answers += ";BYEBYEMSYK"
        submit_url = f"https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives?serialNumbers={serialNumbers}&answers={answers}&studentId={id}&homeworkId={hwid}&unitId={unitId}&modifyNum=0"
        return_text = requests.get(submit_url).text
        if json.loads(return_text).get('code') == "10000":
            return True
        else:
            return False
    except Exception:
        print('2.2')
        return False

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
                pass
            except json.JSONDecodeError:
                print("3")
                exit(3)
            if str(hwtp) == "7":
                operation_answerget_new(id, unitId, hwid)
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
    exit(3)

for item in reslist:
    usefulHWID_list3.append(item['id'])
    if str(item['homeworkType']) == '7':
        usefulHWID_list2.append(item['id'])

DefaultHWID = max(usefulHWID_list3)
getUnreleasedHWID()
while roll == 1:
    MainMenu()