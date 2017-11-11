# _*_coding:utf-8_*_
from splinter import Browser
import time
import re
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException


def login(name):
    """手动输入验证码后登录，调用该函数将返回抢选界面(必修课选课)的browser对象"""
    login_url = 'http://electsys.sjtu.edu.cn/edu/login.aspx'
    browser = Browser('chrome')
    print(type(browser))
    browser.visit(login_url)
    user_name = ''
    user_password = ''
    browser.fill('user', user_name)
    browser.fill('pass', user_password)
    while browser.title != u'上海交通大学教学信息服务网－学生服务平台':
        time.sleep(0.1)
    print(browser.windows[0], browser.windows[1])
    browser.windows[1].close()
    browser.visit('http://electsys.sjtu.edu.cn/edu/student/elect/electwarning.aspx?xklc=3')
    # 1为海选，2为抢选，3为第三轮
    browser.check('CheckBox1')
    browser.find_by_name('btnContinue').first.click()
    return browser


def jump_to_list(browser, course_type='bx'):
    """从某种课程的列表跳转到指定种类的列表
    course_type：'bx'必修，'ts'通识"""
    if course_type == 'bx':
        browser.find_by_value(u'必修课').first.click()
    if course_type == 'ts':
        browser.find_by_value(u'通识课').first.click()
        browser.choose('gridGModule$ctl02$radioButton', 'radioButton')  # 选择人文
    if course_type == 'rx':
        browser.find_by_value(u'任选课').first.click()
        browser.select('OutSpeltyEP1$dpYx', '03000')
        browser.select('OutSpeltyEP1$dpNj', '2016')
        browser.find_by_value(u'查 询').first.click()


def course_arrange(browser, course_code):
    """从课程列表进入到选择教师列表"""
    while 1:
        try:
            browser.choose('myradiogroup', course_code)
            time.sleep(1.3)  # 0.6会出现刷新过于频繁
            browser.find_by_value(u'课程安排').first.click()
            if browser.title == 'messagePage':
                browser.find_by_value(u'返回').first.click()
                print(u'-------刷新过于频繁' + time.strftime('%H:%M:%S', time.localtime(time.time())) + '-------')
                time.sleep(1.2)
            else:
                break
        except StaleElementReferenceException as e:
            print(e)
            time.sleep(1)
        except WebDriverException as e:
            print(e)
            time.sleep(1)


def check_is_empty(browser, teacher_re):
    """在选择教师列表中检验人数是否未满，course_code为课程代码，teacher_name为老师名字，"""
    # print(browser.html)
    teacher_code = teacher_re.split('(')[0]
    a = re.findall(teacher_re, browser.html)
    b = a[0].split(u'满')
    # 使用([\s\S]*)findall的结果只有([\s\S]*)的部分，开头和结尾都会被删除
    if u'未' in b[0]:
        print(teacher_code + u' 人数未满 ')
        browser.choose('myradiogroup', teacher_code)
        return 1
    else:
        print(teacher_code + u' 人数满 ')
        return 0


def main():
    teacher_list_jx = [u'385290([\s\S]*)满']

    browser1 = login('cgd')
    jump_to_list(browser1, 'ts')
    while True:
        course_arrange(browser1, 'MU901')
        print('-------time:' + time.strftime('%H:%M:%S', time.localtime(time.time())) + '-------')
        check_result = 0
        try:
            for each_teacher in teacher_list_jx:
                check_result += check_is_empty(browser1, each_teacher)
        except IndexError:
            browser1.visit('http://electsys.sjtu.edu.cn/edu/student/elect/electwarning.aspx?xklc=3')
            browser1.check('CheckBox1')
            browser1.find_by_name('btnContinue').first.click()
            time.sleep(5)
            jump_to_list(browser1, 'ts')
            continue
        if check_result:
            browser1.find_by_value(u'选定此教师').first.click()
            browser1.find_by_value(u'选课提交').first.click()
            print(u'*******选课成功 ' + time.strftime('%H:%M:%S', time.localtime(time.time())) + '*******')
            break
        else:
            browser1.find_by_value(u'返 回').first.click()
    input("Finished!")


if __name__ == '__main__':
    main()
