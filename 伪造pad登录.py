import hashlib
import json
import requests
import webbrowser

def string_to_md5(string):
    md5_val = hashlib.md5(string.encode('utf8')).hexdigest()
    return md5_val

def open_url(url):
    webbrowser.open_new(url)

def post(postdata,ua):
    headers = {'user-agent': ua}
    try:
        req=requests.post(url="https://padapp.msyk.cn/ws/app/padLogin",data=postdata,headers=headers)
        return req.text
    except:
        print("网络异常")
        exit(1)

user=input("用户名:")
pwd=input("密码:")
mac=input("mac:").upper
api=input("安卓API:")
sn=input("SN(区分大小写):")
dataup={"userName":user,"auth":string_to_md5(user+pwd+"HHOO"),"macAddress":mac,"versionCode":api,"sn":sn}
res=post(dataup,"okhttp/3.12.1")

if json.loads(res).get('code')=="10000":
    avatar=json.loads(res).get('InfoMap').get('avatarUrl')
    open_url(avatar)
    print(res)
    exit(0)
else:
    print(json.loads(res).get('message'))
    exit(1)