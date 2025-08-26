# msyk_learning_circle.py - 美师优课学习圈系统模块
# 使用前请取消主程序中对本模块的注释

import requests
import json
from colorama import Fore, Style, Back
import time
import urllib.parse

def timestamp_to_date(timestamp):
    """将13位时间戳转换为日期格式"""
    try:
        seconds = timestamp // 1000
        time_struct = time.gmtime(seconds)
        return time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
    except:
        return "日期格式错误"

def questionlist(studentId, unitId):
    """获取科目和教师信息"""
    try:
        questionlist_2 = requests.get(
            f"https://padapp.msyk.cn/ws/student/homework/studentHomework/searchSubjectInfo?studentId={studentId}&unitId={unitId}"
        ).text
        
        studentSubjectList = json.loads(questionlist_2).get('studentSubjectList', [])
        print(Fore.MAGENTA + "科目和教师信息:")
        for subject in studentSubjectList:
            name = subject.get('name', '')
            teacherName = subject.get('teacherName', '')
            code = subject.get('code', '')
            userId = subject.get('userId', '')
            print(f"{code} {Back.WHITE+Fore.MAGENTA+name} {Fore.YELLOW+teacherName} {userId}")
    except Exception as e:
        print(Fore.RED + f"获取科目信息失败: {str(e)}")

def question_privatelist(studentId, unitId):
    """获取个人问题列表"""
    try:
        print(Fore.MAGENTA + "我的问题:")
        question_privatelist_2 = requests.get(
            f"https://learningapp.msyk.cn/ws/submitQuestion/getSubmitQuestion?userId={studentId}&ownerType=1&unitId={unitId}&endQuestionType=&subjectCode=&startTime=&endTime=&onlyShowPublic=&pageIndex=1&pageSize=20"
        ).text
        
        data = json.loads(question_privatelist_2).get('data', {})
        submitQuestionList = data.get('submitQuestionList', [])
        
        for i, question in enumerate(submitQuestionList):
            questionDescribe = question.get('questionDescribe', '')
            subjectName = question.get('subjectName', '')
            uuid = question.get('uuid', '')
            print(Fore.CYAN + f"{i+1}. {Back.GREEN+Fore.MAGENTA+subjectName} - {uuid}")
            print(Fore.BLACK + Back.WHITE + questionDescribe)
            print("-" * 50)
    except Exception as e:
        print(Fore.RED + f"获取问题列表失败: {str(e)}")

def question_detail(studentId, unitId):
    """查看问题详情"""
    try:
        submitQuestionUuId = input(Fore.CYAN + "请输入问题uuid: ")
        question_detail_2 = requests.get(
            f"https://learningapp.msyk.cn/ws/chattingRecords/getChattingRecords?submitQuestionUuId={submitQuestionUuId}&unitId={unitId}&userId={studentId}"
        ).text
        
        data = json.loads(question_detail_2).get('data', {})
        chattingRecordsList = data.get('chattingRecordsList', [])
        
        print(Fore.MAGENTA + "问题对话记录:")
        for record in chattingRecordsList:
            question_detail = record.get('chatContent', '')
            creationTime = record.get('creationTime', 0)
            creationTime = timestamp_to_date(creationTime) if creationTime else "未知时间"
            realName = record.get('realName', '未知用户')
            ownerType = record.get('ownerType', 1)
            
            type_text = "老师" if int(ownerType) == 2 else "学生"
            print(f"{realName}({type_text}) {creationTime}:")
            print(f"  {question_detail}")
            print("-" * 50)
    except Exception as e:
        print(Fore.RED + f"获取问题详情出错: {str(e)}")

def question_add(studentId, unitId):
    """提交问题"""
    try:
        teacherId = input(Fore.CYAN + "请输入要提问教师的ID: ")
        subjectCode = input(Fore.CYAN + "请输入学科码: ")
        classId = input(Fore.CYAN + "请输入班级ID: ")
        content = input(Fore.YELLOW + "请输入问题描述: ")
        
        # URL编码内容
        encoded_content = urllib.parse.quote(content)
        
        response = requests.get(
            f"https://learningapp.msyk.cn/ws/submitQuestion/addSubmitQuestion?studentId={studentId}&content={encoded_content}&picUrls=[]&aduioList=[]&unitId={unitId}&homeworkName=&orderNum=0&teacherId={teacherId}&subjectCode={subjectCode}&questionId=&classId={classId}"
        )
        
        if response.status_code == 200:
            result = json.loads(response.text)
            if result.get('code') == '10000':
                print(Fore.GREEN + "问题提交成功!")
            else:
                print(Fore.RED + f"问题提交失败: {result.get('message', '未知错误')}")
        else:
            print(Fore.RED + f"网络请求失败: {response.status_code}")
    except Exception as e:
        print(Fore.RED + f"提交问题出错: {str(e)}")

def question_chatadd(studentId, unitId):
    """添加聊天内容"""
    try:
        qwerid = input(Fore.CYAN + "请输入自己的ID: ")
        ownerType = input(Fore.CYAN + "请输入自己的用户类型(1学生/2老师): ")
        submitQuestionUuIds = input(Fore.YELLOW + "请输入问题ID: ")
        content = input(Fore.GREEN + "请输入聊天内容: ")
        
        # URL编码内容
        encoded_content = urllib.parse.quote(content)
        
        response = requests.get(
            f"https://learningapp.msyk.cn/ws/chattingRecords/addChattingRecord?userId={qwerid}&ownerType={ownerType}&content={encoded_content}&picUrls=%5B%5D&aduioList=%5B%5D&submitQuestionUuIds={submitQuestionUuIds}&unitId={unitId}"
        )
        
        if response.status_code == 200:
            result = json.loads(response.text)
            if result.get('code') == '10000':
                print(Fore.GREEN + "聊天内容添加成功!")
            else:
                print(Fore.RED + f"聊天内容添加失败: {result.get('message', '未知错误')}")
        else:
            print(Fore.RED + f"网络请求失败: {response.status_code}")
    except Exception as e:
        print(Fore.RED + f"添加聊天内容出错: {str(e)}")

def learning_circle_menu(studentId, unitId):
    """学习圈菜单"""
    questionlist(studentId, unitId)
    question_privatelist(studentId, unitId)
    
    print(Fore.MAGENTA + "1.查看问题详情\n2.提问\n3.添加聊天内容\n4.返回主菜单")
    ques_choice = input(Fore.RED + "请选择需要执行的任务: ")
    
    try:
        if int(ques_choice) == 1:
            question_detail(studentId, unitId)
        elif int(ques_choice) == 2:
            question_add(studentId, unitId)
        elif int(ques_choice) == 3:
            question_chatadd(studentId, unitId)
        elif int(ques_choice) == 4:
            return
        else:
            print(Fore.RED + "无效选择")
    except ValueError:
        print(Fore.RED + "请输入有效数字")