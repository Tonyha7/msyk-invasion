# msyk_message.py - 美师优课消息系统模块
# 使用前请取消主程序中对本模块的注释

import requests
import json
from colorama import Fore, Style, Back
import os

def information_numget(studentId):
    """获取未读消息数量"""
    try:
        infnumget_2 = requests.get(f"https://msgapp.msyk.cn/ws/teacher/information/getInformationUnreadNum?userId={studentId}").text
        data = json.loads(infnumget_2).get('data', {})
        print(Fore.BLACK + Back.WHITE + "新消息:", Fore.BLACK + Back.WHITE + str(data.get('num', 0)))
        return data.get('num', 0)
    except Exception as e:
        print(Fore.RED + f"获取消息数量失败: {str(e)}")
        return 0

def informationlist(studentId, unitId):
    """获取消息列表"""
    pagenum = 1
    while True:
        try:
            inflistget_2 = requests.get(
                f"https://msgapp.msyk.cn/ws/student/information/informationListForStudent?userId={studentId}&type=0&pageSize=20&pageIndex={pagenum}&startTime=&endTime=&exigencyType=&subjectCodes=&title=&accessory=0"
            ).text
            
            data = json.loads(inflistget_2).get('data', {})
            informationList = data.get('informationList', [])
            uuid_list = []
            
            print(Fore.MAGENTA + f"====== 第 {pagenum} 页消息列表 ======")
            for inf_order, info in enumerate(informationList):
                i = inf_order + 1
                uuid = info.get('uuid', '')
                uuid_list.append(uuid)
                print(Fore.YELLOW + "序号:", Fore.YELLOW + str(i), 
                      Fore.YELLOW + "发送者:", Fore.YELLOW + info.get('sendUserName', ''),
                      Fore.YELLOW + "标题:", Fore.YELLOW + info.get('title', ''))
                print(Fore.BLACK + Back.WHITE + info.get('content', ''))
                print("-" * 50)
            
            print(Fore.GREEN + "当前第", pagenum, Fore.GREEN + "页")
            cho = input(Fore.MAGENTA + "1.上一页\n2.查看详情\n3.下一页\n4.返回上一级\n" + Fore.RED + "请输入需要执行的任务:")
            
            try:
                cho = int(cho)
                if cho == 1:
                    pagenum = max(1, pagenum - 1)
                elif cho == 3:
                    pagenum += 1
                elif cho == 2:
                    informationget(studentId, unitId, uuid_list)
                elif cho == 4:
                    break
                else:
                    pagenum = 1
            except ValueError:
                print(Fore.RED + "请输入有效数字")
        except Exception as e:
            print(Fore.RED + f"获取消息列表失败: {str(e)}")
            break

def informationget(studentId, unitId, uuid_list):
    """获取消息详情"""
    try:
        uuid_num1 = input(Fore.RED + "请输入序号: ")
        uuid_num2 = int(uuid_num1) - 1
        
        if uuid_num2 < 0 or uuid_num2 >= len(uuid_list):
            print(Fore.RED + "序号无效")
            return
            
        uuid_inf = uuid_list[uuid_num2]
        infget_2 = requests.get(
            f"https://msgapp.msyk.cn/ws/teacher/information/getInformationDetail?userId={studentId}&unitId={unitId}&uuid={uuid_inf}&drafts=false"
        ).text
        
        data = json.loads(infget_2).get('data', {})
        information = data.get('information', {})
        accessoryList = information.get('accessoryList', [])
        
        # 显示消息内容
        print(Fore.MAGENTA + "消息内容:")
        print(Fore.WHITE + information.get('content', ''))
        
        # 显示附件列表
        if accessoryList:
            print(Fore.MAGENTA + "\n附件列表:")
            for i, accessory in enumerate(accessoryList):
                print(Fore.YELLOW + f"{i+1}. {accessory.get('title', '无标题')}")
            
            # 询问是否下载附件
            down_choice = input(Fore.BLUE + "是否下载附件? [Y/n]: ")
            if down_choice.lower() == 'y':
                for accessory in accessoryList:
                    file_url = accessory.get('resourceUrl', '')
                    if file_url:
                        if not file_url.startswith('http'):
                            file_url = "https://msgapp.msyk.cn" + ('' if file_url.startswith('/') else '/') + file_url
                        
                        title = accessory.get('title', 'unknown_file')
                        print(Fore.GREEN + f"下载: {title}")
                        try:
                            response = requests.get(file_url, stream=True)
                            with open(title, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=8192):
                                    f.write(chunk)
                            print(Fore.GREEN + f"下载成功: {title}")
                        except Exception as e:
                            print(Fore.RED + f"下载失败: {str(e)}")
        else:
            print(Fore.YELLOW + "此消息无附件")
    except Exception as e:
        print(Fore.RED + f"获取消息详情出错: {str(e)}")

def message_menu(studentId, unitId):
    """消息系统菜单"""
    information_numget(studentId)
    informationlist(studentId, unitId)