import hashlib
import json
import re
import os
import webbrowser
import requests
import time
import base64
import rsa
from rsa import core, PublicKey, transform
from colorama import init, Fore, Back, Style
# 额外功能，自行取消注释
# import msyk_message
# import msyk_learning_circle

# 课件下载转PDF功能，需要pillow
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    Image = None

# 科目代码映射字典
SUBJECT_CODE_MAP = {
    "0621": "问卷调查",
    "099": "其它",
    "3001": "政治",
    "3002": "历史",
    "3003": "地理",
    "3004": "思想品德",
    "3006": "物理",
    "3007": "语文",
    "3008": "数学",
    "3009": "英语",
    "3011": "化学",
    "3012": "音乐",
    "3013": "美术",
    "3014": "体育与健康",
    "3015": "通用技术",
    "3016": "艺术",
    "3017": "艺术欣赏音乐",
    "3018": "艺术欣赏美术",
    "3019": "公共卫生教育",
    "3020": "生物",
    "3021": "心理健康教育",
    "3022": "社会",
    "3023": "劳动技术",
    "3024": "科学",
    "3025": "综合实践",
    "3026": "汉语",
    "3029": "德育",
    "3037": "技术",
    "3088": "信息技术",
    "3099": "公共卫生科学",
    "3101": "文综",
    "3102": "理综",
    "3109": "高中综合",
    "3110": "通用(选考)",
    "3111": "通用(学考)",
    "3113": "信息(选考)",
    "3114": "信息(学考)",
    "3324": "物理竞赛",
    "3325": "扫除",
    "3326": "班会",
    "3327": "自习",
    "3328": "化学竞赛",
    "3567": "俄语",
    "3779": "班会",
    "3BX11": "世界文明史",
    "9834": "语音",
    "99999": "生物竞赛",
    "s926": "数学竞赛",
    "20230201": "地理1",
    "202303102": "生物1",
    "20240530": "政治1",
    "20230901": "英语1"
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

init(autoreset=True)  # 文字颜色自动恢复
roll = 1  # 循环
serialNumbers, answers, serialNumbersa, answersa = "", "", "", ""
msyk_sign_pubkey = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAj7YWxpOwulFyf+zQU77Y2cd9chZUMfiwokgUaigyeD8ac5E8LQpVHWzkm+1CuzH0GxTCWvAUVHWfefOEe4AThk4AbFBNCXqB+MqofroED6Uec1jrLGNcql9IWX3CN2J6mqJQ8QLB/xPg/7FUTmd8KtGPrtOrKKP64BM5cqaB1xCc4xmQTuWvtK9fRei6LVTHZyH0Ui7nP/TSF3PJV3ywMlkkQxKi8JBkz1fx1ZO5TVLYRKxzMQdeD6whq+kOsSXhlLIiC/Y8skdBJmsBWDMfQXxtMr5CyFbVMrG+lip/V5n22EdigHcLOmFW9nnB+sgiifLHeXx951lcTmaGy4uChQIDAQAB"

msyk_key = "DxlE8wwbZt8Y2ULQfgGywAgZfJl82G9S"
headers = {'user-agent': "okhttp/3.12.1"}
sign = ""

# 固定的RSA密钥对（用于加密ProfileCache.txt）
FIXED_PUBLIC_KEY = """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAndq0AWyxkp0ted7i4He7GW2YpENpXye0sSEs9z1dKE67GILjwsg6
2ghhtjdDF/5Dt95Gw7VyXfXvZlmIrXXYVYmkLfz0rjpZj3gaTe/vmqEFU0pPbrki
La38e6Bihjy3HzfaqEz25voOtP/gLJ6J4j9uKeyXQsYela/KqTFYdvT6Ac+Lt78p
kB2GEfxJmqqn82yiT/Kz4aQN9rnIc06Z9M6Gn6XCwyLso33Y2LwMW4GUDek+8dYG
LJ1lCb/5LyamMfX/0odc4/yb1IomtVKwfYUlf9ThEOXSSJ5Z7o1bedOYMFbc3jes
7yZSnl+ldLBIAQ48meEngQJFSekjIA1YtwIDAQAB
-----END RSA PUBLIC KEY-----"""

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

def rsa_encrypt_data(data):
    """使用固定的RSA公钥加密数据"""
    try:
        # 加载固定公钥
        pubkey = rsa.PublicKey.load_pkcs1(FIXED_PUBLIC_KEY.encode())
        # RSA加密有长度限制，需要分段处理
        max_chunk_size = 200  # 适合2048位密钥的块大小
        encrypted_chunks = []
        
        # 将数据编码为字节
        data_bytes = data.encode('utf-8')
        
        # 分段加密
        for i in range(0, len(data_bytes), max_chunk_size):
            chunk = data_bytes[i:i+max_chunk_size]
            encrypted_chunk = rsa.encrypt(chunk, pubkey)
            encrypted_chunks.append(encrypted_chunk)
        
        # 将所有加密块连接并Base64编码
        encrypted_data = b''.join(encrypted_chunks)
        return base64.b64encode(encrypted_data).decode('utf-8')
    except Exception as e:
        print(Fore.RED + f"RSA加密失败: {e}")
        return None

def rsa_decrypt_data(encrypted_data):
    """使用固定的RSA私钥解密数据"""
    try:
        # Base64解码
        encrypted_bytes = base64.b64decode(encrypted_data)
        
        # 加载固定私钥
        privkey = rsa.PrivateKey.load_pkcs1(FIXED_PRIVATE_KEY.encode())
        
        # RSA解密的分段大小
        chunk_size = 256  # 2048位密钥的加密块大小
        decrypted_chunks = []
        
        # 分段解密
        for i in range(0, len(encrypted_bytes), chunk_size):
            chunk = encrypted_bytes[i:i+chunk_size]
            decrypted_chunk = rsa.decrypt(chunk, privkey)
            decrypted_chunks.append(decrypted_chunk)
        
        # 合并所有解密块并解码为字符串
        decrypted_data = b''.join(decrypted_chunks)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        print(Fore.RED + f"RSA解密失败: {e}")
        return None

def getAccountInform():
    ReturnInform = ""
    ProfileImport = ""
    try:
        with open("ProfileCache.txt", "r", encoding='utf-8') as f:
            encrypted_data = f.read().strip()
        
        # 尝试解密数据
        decrypted_data = rsa_decrypt_data(encrypted_data)
        if decrypted_data:
            print("检测到加密的 ProfileCache，尝试缓存登录中。")
            setAccountInform(decrypted_data)
        else:
            # 如果解密失败，尝试作为明文处理
            print("检测到明文的 ProfileCache，尝试缓存登录中。")
            setAccountInform(encrypted_data)
            
    except BaseException:
        print("未检测到 ProfileCache，执行登录流程。")
        ProfileImport = input(Fore.CYAN + "可提供未缓存的登录信息(失败则自动执行账号密码登录):")
        try:
            setAccountInform(ProfileImport)
        except BaseException:
            print(Fore.RED + "错误：登录信息有误或已经失效。")
            print(Fore.WHITE)
            login()


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



def save_json(data, filename):
    filename += ".json"
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(data)
        print(Fore.MAGENTA + "保存登录信息成功 " + filename)
    except BaseException:
        print(Fore.RED + "保存登录信息失败")


def public_key_decrypt(publicKey, content):
    qr_code_cipher = base64.b64decode(content)
    public_key = base64.b64decode(publicKey)
    try:
        rsa_public_key = PublicKey.load_pkcs1_openssl_der(public_key)
        cipher_text_bytes = transform.bytes2int(qr_code_cipher)
        decrypted_text = core.decrypt_int(
            cipher_text_bytes, rsa_public_key.e, rsa_public_key.n)
        final_text = transform.int2bytes(decrypted_text)
        final_code = final_text[final_text.index(0) + 1:]
        return final_code.decode()
    except Exception:
        print(Fore.RED + "警告:sign解密失败!")
        return None


def getCurrentTime():
    return int(round(time.time() * 1000))


def TimeToHMS(ts: int):
    # 十三位时间戳
    return time.strftime("%H:%M:%S", time.localtime(ts / 1000))
# 字符计算32位md5


def string_to_md5(string):
    md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
    return md5_val
# 浏览器新窗口打开链接


def open_url(url):
    webbrowser.open_new(url)
# login

# POST方案，目前以弃用


def login_post():
    userName = input("用户名:")
    pwd = input("密码:")
    mac = input("mac:").upper()  # mac地址要大写
    api = input("安卓API:")
    sn = input(Fore.RED + "SN(区分大小写):")
    genauth = string_to_md5(userName + pwd + "HHOO")
    dataup = {
    "userName": userName,
    "auth": genauth,
    "macAddress": mac,
    "versionCode": api,
     "sn": sn}
    res = post("https://padapp.msyk.cn/ws/app/padLogin",
               dataup, 1, genauth + mac + sn + userName + api)
    setAccountInform(res)

# 登入已简化为GET方案，感谢 cyhLen 提供方案


def login():
    userName = input("用户名:")
    password = input("密码:")
    pwd = string_to_md5(userName + password + "HHOO")
    loginurl = 'https://padapp.msyk.cn/ws/app/padLogin?userName=' + \
        userName + '&auth=' + pwd
    login_first = requests.get(loginurl).text
    setAccountInform(login_first)


def normalize_url(url):
    """规范化URL"""
    if not url:
        return ""
    url = url.strip()
    if url.lower().startswith('http'):
        return url
    elif url.lower().startswith('//'):
        return "https:" + url
    elif url.lower().startswith('/'):
        return "https://msyk.wpstatic.cn" + url
    else:
        return "https://msyk.wpstatic.cn/" + url


def build_question_url(question, student_id, unit_id):
    """构建问题URL"""
    return f"https://www.msyk.cn/webview/newQuestion/singleDoHomework?studentId={student_id}&homeworkResourceId={question['resourceId']}&orderNum={question['orderNum']}&showAnswer=1&unitId={unit_id}&modifyNum=1"


def safe_filename(filename):
    """确保文件名安全"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def parse_msyk_html(html_doc, count, url, return_empty=False):
    """统一的HTML解析函数"""
    html_doc = html_doc.replace('\n', '')
    index = html_doc.find("var questions = ")
    index1 = html_doc.find("var resource")
    if index != -1 and index1 != -1:
        try:
            json_str = html_doc[index + 16:index1 - 1].strip()
            if json_str.endswith(';'):
                json_str = json_str[:-1]
            data = json.loads(json_str)
            if data and isinstance(data, list) and len(
                    data) > 0 and data[0].get('answer') is not None:
                answer = "".join(
                    data[0].get('answer')).lstrip("[").rstrip("]").replace(
        '"',
        '').replace(
            ',',
                    ' ').strip()
                
                #只有当答案包含数字但不是纯数字时才打开浏览器
                if re.search(r'\d', answer) and not re.match(r'^\d+$', answer):
                    print(Fore.YELLOW + f"检测到复杂答案，打开浏览器查看: \n{url}")
                    open_url(url)
                    print(Fore.GREEN + count + " 在浏览器中打开")
                    return "wtf"
                else:
                    print(Fore.GREEN + count + " " + answer)
                    return answer
            else:
                print(Fore.RED + count + " " + "没有检测到答案,有可能是主观题")
                return " " if return_empty else "wtf"
        except json.JSONDecodeError as e:
            print(Fore.RED + f"JSON解析错误: {e}")
            #  fallback 到原始方法
            return ljlVink_parsemsyk_fallback(
                html_doc, count, url, return_empty)
    return " " if return_empty else "wtf"


def ljlVink_parsemsyk_fallback(html_doc, count, url, return_empty=False):
    """备用的HTML解析函数（原始逻辑）"""
    html_doc = html_doc.replace('\n', "")
    index = html_doc.find("var questions = ")
    index1 = html_doc.find("var resource")
    if index != -1:
        try:
            data = json.loads(html_doc[index + 16:index1 - 7])
            if data[0].get('answer') is not None:
                answer = "".join(
                    data[0].get('answer')).lstrip("[")[
        :-
        1].replace(
            '"',
            '').lstrip(",").replace(
                ',',
                    ' ')
                
                # 同样修改逻辑，作用同上
                if re.search(r'\d', answer) and not re.match(r'^\d+$', answer):
                    open_url(url)
                    print(Fore.GREEN + count + " 在浏览器中打开")
                    return "wtf"
                else:
                    print(Fore.GREEN + count + " " + answer)
                    return answer
            else:
                print(Fore.RED + count + " " + "没有检测到答案,有可能是主观题")
                return " " if return_empty else "wtf"
        except Exception as e:
            print(Fore.RED + f"备用解析也失败: {e}")
            return " " if return_empty else "wtf"
    return " " if return_empty else "wtf"

# 获取账号信息

def setAccountInform(result):
    # 成功登录 获取账号信息
    if json.loads(result).get('code') == "10000":
        # avatar=json.loads(res).get('InfoMap').get('avatarUrl')
        # open_url(avatar)#浏览器打开头像（同时测试能否正常打开浏览器）
        # print(Fore.GREEN + "===============")
        # print(Fore.GREEN + result)
        # print(Fore.GREEN + "===============")
        save_json(result, json.loads(result).get('InfoMap').get('realName'))
        
        # 加密并保存ProfileCache.txt
        encrypted_data = rsa_encrypt_data(result)
        if encrypted_data:
            with open("ProfileCache.txt", "w", encoding='utf-8') as f:
                f.write(encrypted_data)
            print("ProfileCache 登录缓存已加密更新。")
        else:
            # 如果加密失败，保存明文
            with open("ProfileCache.txt", "w", encoding='utf-8') as f:
                f.write(result)
            print("ProfileCache 登录缓存已更新。(明文)")
        
        global unitId, id
        unitId = json.loads(result).get('InfoMap').get('unitId')
        id = json.loads(result).get('InfoMap').get('id')

        sign1 = public_key_decrypt(
    msyk_sign_pubkey,
     json.loads(result).get('sign')).split(':')
        if sign1 != None:
            signdec = ','.join(sign1)
            print(Fore.GREEN + "sign解密成功:" + signdec)
            global sign
            sign = sign1[1] + id

    # 登录失败 打印原因
    else:
        print(Fore.RED + json.loads(result).get('message'))
        exit(1)
# post


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
    except BaseException:
        print(Fore.RED + str(url) + " " + str(postdata))
        print(Fore.RED + "网络异常 请检查代理设置")
        exit(1)


def process_homework_type7(hwid, res, ress, is_retry=False):
    """处理类型7作业的公共函数"""
    global serialNumbers, answers, serialNumbersa, answersa, id, unitId
    
    if not res or not res.strip():
        print(Fore.RED + f"作业 {hwid} 获取卡片信息失败（响应为空）")
        return
    try:
        res_json = json.loads(res)
    except json.JSONDecodeError:
        print(Fore.RED + f"作业 {hwid} 返回非 JSON，可能 ID 不存在")
        return
    
    materialRelasList = res_json.get('materialRelas', [])
    analysistList     = res_json.get('analysistList', [])
    hwname            = res_json.get('homeworkName', '未命名作业')
    res_list          = res_json.get('homeworkCardList', [])
    materialRelasFiles, analysistFiles = [], []
    materialRelasUrls,  analysistUrls  = [], []

    print(Fore.MAGENTA + Back.WHITE + str(hwname))  # 作业名
    res_list = json.loads(res).get('homeworkCardList')  # 题目list

    # 统计题目类型
    has_objective_questions = False  # 是否有客观题（选择/判断/填空）
    has_subjective_questions = False  # 是否有主观题
    
    # 分析题目类型
    for question in res_list:
        questionType = question.get('questionType', 1)
        if questionType in [1, 2, 4, 5]:  # 单选、多选、填空、判断
            has_objective_questions = True
        elif questionType == 3:  # 主观题
            has_subjective_questions = True

    # 处理材料文件
    if len(materialRelasList) == 0:
        print(Fore.RED + "没有材料文件")
    else:
        print(Fore.MAGENTA + "材料文件:")
        for file in materialRelasList:
            file_url = normalize_url(file['resourceUrl'])
            materialRelasFiles.append(file['title'])
            materialRelasUrls.append(file_url)
            print(Fore.GREEN + "\t" + file['title'] + " " + file_url)

    # 处理答案文件
    if len(analysistList) == 0:
        print(Fore.RED + "没有答案文件")
    else:
        print(Fore.MAGENTA + "答案文件:")
        for file in analysistList:
            file_url = normalize_url(file['resourceUrl'])
            analysistFiles.append(file['title'])
            analysistUrls.append(file_url)
            print(Fore.GREEN + "\t" + file['title'] + " " + file_url)

    # 首先尝试使用新方法获取答案
    new_method_result = None
    if not is_retry:
        new_method_result = operation_answerget_new(id, unitId, hwid)

    # 如果新方法失败，使用旧方法获取所有题目答案
    if not new_method_result or not new_method_result.get('success', False):
        print(Fore.YELLOW + "新方法失败，使用旧方法获取答案...")
        for question in res_list:
            serialNumber = str(question['serialNumber'])
            orderNum = str(question['orderNum'])
            url = build_question_url(question, id, unitId)
            try:
                vink = requests.get(url=url, timeout=10)
                answer = parse_msyk_html(vink.text, orderNum, url)
                encoded_answer = answer_encode(answer)
            except requests.exceptions.Timeout:
                print(Fore.RED + f"题目 {orderNum} 请求超时")
                answer = "wtf"
                encoded_answer = "wtf"
            except Exception as e:
                print(Fore.RED + f"题目 {orderNum} 处理错误: {e}")
                answer = "wtf"
                encoded_answer = "wtf"

            # 添加到主观题答案列表（总是添加）
            if serialNumbersa == "":
                serialNumbersa += serialNumber
                answersa += encoded_answer
            else:
                serialNumbersa += ";" + serialNumber
                answersa += ";" + encoded_answer

            # 只将非wtf答案添加到选择题答案列表
            if answer != "wtf":
                if serialNumbers == "":
                    serialNumbers += serialNumber
                    answers += encoded_answer
                else:
                    serialNumbers += ";" + serialNumber
                    answers += ";" + encoded_answer

    # 用户交互部分
    if not is_retry:
        # 获取实际的题目类型信息（优先使用新方法的结果）
        if new_method_result and new_method_result.get('success', False):
            actual_has_objective = new_method_result.get('has_objective', False)
            actual_has_subjective = new_method_result.get('has_subjective', False)
            objective_count = new_method_result.get('objective_count', 0)
        else:
            actual_has_objective = has_objective_questions
            actual_has_subjective = has_subjective_questions
            objective_count = len(serialNumbers.split(';')) if serialNumbers else 0

        # 只有有客观题且有答案时才询问是否提交选择答案
        if actual_has_objective and objective_count > 0:
            up = input(Fore.YELLOW + "是否提交客观题答案(选择/判断/填空)?[Y/n]:")
            if up.lower() == "y":
                dataup = {
                    "serialNumbers": serialNumbers,
                    "answers": answers,
                    "studentId": id,
                    "homeworkId": int(hwid),
                    "unitId": unitId,
                    "modifyNum": 0}
                res = post(
                    "https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives",
                    dataup,
                    2,
                    answers + hwid + '0' + serialNumbers)
                if json.loads(res).get('code') == "10000":
                    print(Fore.GREEN + "客观体答案提交成功")
        elif actual_has_objective and objective_count == 0:
            print(Fore.RED + "有客观题但未获取到答案，跳过提交")

        # 只有有主观题时才询问是否提交假图片
        if actual_has_subjective:
            middle = input(Fore.YELLOW + "是否要为主观题提交假图片 [Y/n]:")
            if middle.lower() == "y":
                dataup = {
                    "serialNumbers": serialNumbersa,
                    "answers": answersa,
                    "studentId": id,
                    "homeworkId": int(hwid),
                    "unitId": unitId,
                    "modifyNum": 0}
                res = post(
                    "https://padapp.msyk.cn/ws/teacher/homeworkCard/saveCardAnswerObjectives",
                    dataup,
                    2,
                    answersa + hwid + '0' + serialNumbersa)
                if json.loads(res).get('code') == "10000":
                    print(Fore.GREEN + "主观题提交假图片成功")

        if len(analysistList) != 0 or len(materialRelasList) != 0:
            down = input(Fore.BLUE + "是否要下载文件 [Y/n]:")
            if down.lower() == "y":
                for url, file in zip(materialRelasUrls, materialRelasFiles):
                    safe_file = safe_filename(file)
                    try:
                        with open(safe_file, "wb") as f:
                            response = requests.get(url, timeout=30)
                            f.write(response.content)
                        print(Fore.GREEN + f"已下载: {safe_file}")
                    except Exception as e:
                        print(Fore.RED + f"下载失败 {file}: {e}")
                for url, file in zip(analysistUrls, analysistFiles):
                    safe_file = safe_filename(file)
                    try:
                        with open(safe_file, "wb") as f:
                            response = requests.get(url, timeout=30)
                            f.write(response.content)
                        print(Fore.GREEN + f"已下载: {safe_file}")
                    except Exception as e:
                        print(Fore.RED + f"下载失败 {file}: {e}")
    else:
        print(Fore.YELLOW + "重试模式，跳过用户交互")

    # 重置全局变量
    if not is_retry:
        serialNumbers, answers = "", ""


def operation_answerget_new(studentId, unitId, homeworkId):
    """新的答案获取方法 - 直接从API获取答案"""
    global serialNumbers, answers, serialNumbersa, answersa  # 声明使用全局变量
    
    local_serialNumbers, local_answers = "", ""  # 使用局部变量临时存储
    local_serialNumbersa, local_answersa = "", ""  # 主观题答案临时存储
    has_objective_questions = False  # 是否有客观题
    has_subjective_questions = False  # 是否有主观题
    
    try:
        # 构建请求URL
        url = f"https://padapp.msyk.cn/ws/teacher/homeworkCard/getHomeworkCardInfo?homeworkId={homeworkId}&studentId=&modifyNum=0&unitId={unitId}"
        response = requests.get(url)
        body = response.json()
        if 'homeworkCardList' not in body:
            print(Fore.RED + "API响应中没有找到homeworkCardList")
            return False
            
        homeworkCardList = body['homeworkCardList']
        for homeworkCard in homeworkCardList:
            serialNumber = homeworkCard['serialNumber']  # 提交使用的题号
            orderNum = homeworkCard['orderNum']  # 显示的题号
            answer = homeworkCard.get('answer', '')
            blankList = homeworkCard.get('blankList', [])  # 填空题答案列表
            questionType = homeworkCard.get('questionType', 1)  # 题目类型

            # 处理单选题 (questionType=1)
            if questionType == 1 and answer:
                has_objective_questions = True
                # 添加到提交字符串
                if not local_serialNumbers:
                    local_serialNumbers = str(serialNumber)
                    local_answers = str(answer)
                else:
                    local_serialNumbers += ";" + str(serialNumber)
                    local_answers += ";" + str(answer)
                # 主观题列表也添加
                if not local_serialNumbersa:
                    local_serialNumbersa = str(serialNumber)
                    local_answersa = str(answer)
                else:
                    local_serialNumbersa += ";" + str(serialNumber)
                    local_answersa += ";" + str(answer)
                print(Fore.GREEN + f"{orderNum} {answer}")
            
            # 处理多选题 (questionType=2)
            elif questionType == 2 and answer and len(answer) == 10:
                has_objective_questions = True
                # 将01串转换为选项字母
                answer_show = ''.join("ABCDEFGHIJ"[i] for i in range(10) if answer[i] == '1')
                # 添加到提交字符串
                if not local_serialNumbers:
                    local_serialNumbers = str(serialNumber)
                    local_answers = str(answer)
                else:
                    local_serialNumbers += ";" + str(serialNumber)
                    local_answers += ";" + str(answer)
                # 主观题列表也添加
                if not local_serialNumbersa:
                    local_serialNumbersa = str(serialNumber)
                    local_answersa = str(answer)
                else:
                    local_serialNumbersa += ";" + str(serialNumber)
                    local_answersa += ";" + str(answer)
                print(Fore.GREEN + f"{orderNum} {answer_show}")
                        
            # 处理主观题 (questionType=3)
            elif questionType == 3:
                has_subjective_questions = True
                # 只添加到主观题列表
                if not local_serialNumbersa:
                    local_serialNumbersa = str(serialNumber)
                    local_answersa = "wtf"  # 主观题用wtf标记
                else:
                    local_serialNumbersa += ";" + str(serialNumber)
                    local_answersa += ";wtf"
                print(Fore.RED + f"{orderNum} 未检测到答案，有可能是主观题")
                        
            # 处理填空题 (questionType=4)
            elif questionType == 4 and blankList:
                has_objective_questions = True
                answer_str = json.dumps(blankList)
                # 添加到提交字符串
                if not local_serialNumbers:
                    local_serialNumbers = str(serialNumber)
                    local_answers = answer_str
                else:
                    local_serialNumbers += ";" + str(serialNumber)
                    local_answers += ";" + answer_str
                # 主观题列表也添加
                if not local_serialNumbersa:
                    local_serialNumbersa = str(serialNumber)
                    local_answersa = answer_str
                else:
                    local_serialNumbersa += ";" + str(serialNumber)
                    local_answersa += ";" + answer_str
                
                # 显示格式化的答案（空格分隔）
                display_answer = ' '.join(blankList)
                print(Fore.GREEN + f"{orderNum} {display_answer}")
            
            # 处理判断题 (questionType=5)
            elif questionType == 5 and answer:
                has_objective_questions = True
                # 添加到提交字符串
                if not local_serialNumbers:
                    local_serialNumbers = str(serialNumber)
                    local_answers = str(answer)
                else:
                    local_serialNumbers += ";" + str(serialNumber)
                    local_answers += ";" + str(answer)
                # 主观题列表也添加
                if not local_serialNumbersa:
                    local_serialNumbersa = str(serialNumber)
                    local_answersa = str(answer)
                else:
                    local_serialNumbersa += ";" + str(serialNumber)
                    local_answersa += ";" + str(answer)
                print(Fore.GREEN + f"{orderNum} {answer}")
            
            # 其他情况
            else:
                # 如果是主观题但无法获取答案，也标记为主观题
                if questionType == 3:
                    has_subjective_questions = True
                    # 只添加到主观题列表
                    if not local_serialNumbersa:
                        local_serialNumbersa = str(serialNumber)
                        local_answersa = "wtf"
                    else:
                        local_serialNumbersa += ";" + str(serialNumber)
                        local_answersa += ";wtf"
                print(Fore.RED + f"{orderNum} 未检测到答案，有可能是主观题")

        # 更新全局变量
        serialNumbers = local_serialNumbers
        answers = local_answers
        serialNumbersa = local_serialNumbersa
        answersa = local_answersa

        if local_serialNumbers:
            # 返回题目类型信息
            return {
                'success': True,
                'has_objective': has_objective_questions,
                'has_subjective': has_subjective_questions,
                'objective_count': len(local_serialNumbers.split(';')) if local_serialNumbers else 0
            }
        else:
            return {
                'success': True,
                'has_objective': has_objective_questions,
                'has_subjective': has_subjective_questions,
                'objective_count': 0
            }
            
    except Exception as e:
        print(Fore.RED + f"新方法出错: {e}")
        import traceback
        traceback.print_exc()  # 打印详细错误信息
        return {'success': False}  # 新方法执行出错


# PPT下载


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

    res = post(
        "https://padapp.msyk.cn/ws/student/homework/studentHomework/homeworkPPTInfo",
        dataup,
        type=2)

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
    download_dir = re.sub(r'[^\w\-_\. ]', '_', f"PPT_{ppt_resource_id}_{safe_title}")
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
            convert_choice = input(Fore.BLUE + "是否要转换为PDF文件？[Y/n]:")
            if convert_choice == 'Y' or convert_choice == 'y':
                pdf_path = convert_ppt_to_pdf(
                    download_dir, f"{safe_title}.pdf")
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
            image_files.extend([f for f in os.listdir(
                ppt_folder) if f.lower().endswith(ext)])

        if not image_files:
            print(Fore.RED + f"错误: 在 '{ppt_folder}' 中没有找到图片文件")
            return None

        # 按数字顺序排序
        image_files.sort(
            key=lambda x: [
        int(c) if c.isdigit() else c.lower() for c in re.split(
            r'(\d+)', x)])

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


def getAnswer():
    
    while True:
        hwid_input = input(Fore.YELLOW + "请输入作业id:")
        try:
            hwid = int(hwid_input)
            break
        except ValueError:
            print(Fore.RED + "作业ID必须是数字，请重新输入")
    hwid = str(hwid)

    retry_count = 0
    max_retries = 2

    while retry_count <= max_retries:
        #获取作业信息
        dataup = {
            "homeworkId": int(hwid),
            "studentId": id,
            "modifyNum": 0,
            "unitId": unitId
        }
        res = post("https://padapp.msyk.cn/ws/teacher/homeworkCard/getHomeworkCardInfo",
                  dataup, 2, hwid + '0')

        #获取作业状态信息
        dataupp = {
            "homeworkId": hwid,
            "modifyNum": 0,
            "userId": id,
            "unitId": unitId
        }
        ress = post("https://padapp.msyk.cn/ws/common/homework/homeworkStatus",
                   dataupp, 3, str(hwid) + '0')

        #空响应检查
        if not ress.strip():
            if retry_count == max_retries:
                print(Fore.RED + "ress仍然为空，美师优课是傻逼")
                return
            choice = input("ress为空，是否重新解析(默认是，否请输入1):")
            if choice.strip() == "1":
                print("用户取消重试")
                return
            retry_count += 1
            continue

        if not res.strip():
            if retry_count == max_retries:
                print(Fore.RED + "res仍然为空，美师优课是傻逼")
                return
            choice = input("res为空，是否重新解析(默认是，否请输入1):")
            if choice.strip() == "1":
                print("用户取消重试")
                return
            retry_count += 1
            continue

        #处理作业
        try:
            hwtp = json.loads(ress).get('homeworkType')
        except Exception:
            hwtp = None

        if str(hwtp) == "7":
            process_homework_type7(hwid, res, ress, is_retry=(retry_count > 0))
            break
        elif str(hwtp) == "5":
            resourceList = json.loads(ress).get('resourceList', [])
            hwname = json.loads(res).get('homeworkName', "未知作业")
            print(Fore.MAGENTA + Style.BRIGHT + str(hwname))
            print(Fore.MAGENTA + Style.NORMAL + "材料文件:")
            materialRelasFiles, materialRelasUrls = [], []

            for file in resourceList:
                if file.get('resourceType') == 5:
                    ppt_resource_id = file.get('resourceUrl')
                    res_title = file.get('resTitle', "未知标题")
                    print(Fore.YELLOW + "检测到PPT文件:", Fore.CYAN + Back.WHITE + res_title)
                    download_choose = input(Fore.BLUE + "是否要下载该PPT文件？[Y/n]:")
                    if download_choose.lower() in ['y', '']:
                        success = download_ppt(ppt_resource_id, res_title)
                        print(Fore.WHITE + ("PPT处理完成" if success else "PPT处理失败"))
                else:
                    file_url = normalize_url(file.get('resourceUrl'))
                    file_title = file.get('resTitle', "未知文件")
                    materialRelasFiles.append(file_title)
                    materialRelasUrls.append(file_url)
                    print(Fore.GREEN + "\t" + file_title + " " + file_url)

            if materialRelasUrls:
                down = input(Fore.BLUE + "是否要下载非PPT文件 [Y/n]:")
                if down.lower() == "y":
                    for url, file in zip(materialRelasUrls, materialRelasFiles):
                        safe_file = safe_filename(file)
                        try:
                            with open(safe_file, "wb") as f:
                                f.write(requests.get(url, timeout=30).content)
                            print(Fore.GREEN + f"已下载: {safe_file}")
                        except Exception as e:
                            print(Fore.RED + f"下载失败 {file}: {e}")
            break
        else:
            # 其余作业统一按资源列表处理
            resourceList = json.loads(ress).get('resourceList', [])
            materialRelasFiles, materialRelasUrls = [], []
            hwname = json.loads(res).get('homeworkName', "未知作业")
            print(Fore.MAGENTA + Style.BRIGHT + str(hwname))
            print(Fore.MAGENTA + Style.NORMAL + "材料文件:")
            for file in resourceList:
                file_url = normalize_url(file.get('resourceUrl'))
                file_title = file.get('resTitle', "未知文件")
                materialRelasFiles.append(file_title)
                materialRelasUrls.append(file_url)
                print(Fore.GREEN + "\t" + file_title + " " + file_url)

            if materialRelasUrls:
                down = input(Fore.BLUE + "是否要下载文件 [Y/n]:")
                if down.lower() == "y":
                    for url, file in zip(materialRelasUrls, materialRelasFiles):
                        safe_file = safe_filename(file)
                        try:
                            with open(safe_file, "wb") as f:
                                f.write(requests.get(url, timeout=30).content)
                            print(Fore.GREEN + f"已下载: {safe_file}")
                        except Exception as e:
                            print(Fore.RED + f"下载失败 {file}: {e}")
            break
    else:
        print(Fore.RED + f"作业 {hwid} 获取失败，已跳过")



def getUnreleasedHWID():
    EndHWID = 0
    StartHWID = int(input(Fore.YELLOW + "请输入起始作业id:"))
    EndHWID = int(input(Fore.YELLOW + "请输入截止作业id(小于起始则不会停):"))
    hwidplus100 = StartHWID + 100
    while roll == 1:
        if StartHWID == hwidplus100:
            print(Fore.GREEN + "已滚动100项 当前" + str(hwidplus100))
            hwidplus100 += 100

        dataup = {
            "homeworkId": StartHWID,
            "modifyNum": 0,
            "userId": id,
            "unitId": unitId}
        res = post(
            "https://padapp.msyk.cn/ws/common/homework/homeworkStatus",
            dataup,
            3,
            str(StartHWID) +
            '0')
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
                    color = SUBJECT_COLORS.get(
                        subject_name, SUBJECT_COLORS['其他'])
                    StarttimeArray = time.localtime(
                        json.loads(res).get('startTime') / 1000)
                    StarttimePrint = time.strftime(
                        "%Y-%m-%d %H:%M:%S", StarttimeArray)
                    EndtimeArray = time.localtime(
                        json.loads(res).get('endTime') / 1000)
                    EndtimePrint = time.strftime(
                        "%Y-%m-%d %H:%M:%S", EndtimeArray)
                    print(
                        Style.BRIGHT +
                        Fore.BLUE +
                        str(StartHWID) +
                        " 作业类型:" +
                        str(hwtp) +
                        " " +
                        Style.BRIGHT +
                        color +
                        "[" +
                        subject_name +
                        "]" +
                        " " +
                        Fore.BLUE +
                        hwname +
                        Style.NORMAL +
                        Fore.RED +
                        " 开始时间:" +
                        Fore.BLUE +
                        " " +
                        StarttimePrint +
                        Fore.RED +
                        " 截止时间:" +
                        Fore.BLUE +
                        " " +
                        EndtimePrint)
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
    # print(Fore.MAGENTA + "5.消息系统\n6.学习圈系统")  # 取消注释以启用额外功能
    Mission = input(Fore.RED + "请选择要执行的任务:")
    if Mission == "2":
        getUnreleasedHWID()
    elif Mission == "3":
        # 清除ProfileCache.txt
        try:
            os.remove("ProfileCache.txt")
        except:
            pass
        print(Fore.CYAN + "已清除ProfileCache登录缓存。")
        ProfileImport = input(Fore.CYAN + "请提供登录信息(如无则执行账号密码登录):")
        try:
            setAccountInform(ProfileImport)
        except BaseException:
            login()
    elif Mission == "4":  # 新增退出选项
        print(Fore.GREEN + "程序已退出")
        exit(0)
    # 取消以下注释以启用消息系统和学习圈系统
    # elif Mission == "5":
    #    msyk_message.message_menu(id, unitId)
    # elif Mission == "6":
    #    msyk_learning_circle.learning_circle_menu(id, unitId)
    else:
        getAnswer()


Start = getAccountInform()

dataup = {
    "studentId": id,
    "subjectCode": None,
    "homeworkType": -1,
    "pageIndex": 1,
    "pageSize": 36,
    "statu": 1,
    "homeworkName": None,
     "unitId": unitId}
res = post(
    "https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList",
    dataup,
    2,
    "-11361")
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
        dataup = {
            "studentId": id,
            "subjectCode": None,
            "homeworkType": -1,
            "pageIndex": 1,
            "pageSize": 36,
            "statu": 1,
            "homeworkName": None,
            "unitId": unitId}
        res = post(
            "https://padapp.msyk.cn/ws/student/homework/studentHomework/getHomeworkList",
            dataup,
            2,
            "-11361")
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
    color = SUBJECT_COLORS.get(subject_name,
                               SUBJECT_COLORS['其他'])  # 使用字典获取颜色，默认为其他颜色
    print(
        Fore.YELLOW + str(item['id']) +
        " 作业类型:" + str(item['homeworkType']) + " " +
        Style.BRIGHT + color + "[" + subject_name + "]" +
        Style.NORMAL + Fore.YELLOW + " " + item['homeworkName'] +
        " 截止时间:" + timePrint
    )

#科目排序
major_order = {
    '语文': 0, '数学': 1, '英语': 2, '物理': 3, '化学': 4,
    '生物': 5, '政治': 6, '历史': 7, '地理': 8
}
def sort_key(item):
    name = str(item.get('subjectName', '其他'))
    return (major_order.get(name.split()[0], 9), name)

reslist.sort(key=sort_key)

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
