# _*_coding:utf-8_*_

from splinter import Browser
import time
import re
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException

website = {"login": "http://electsys.sjtu.edu.cn/edu/login.aspx",
           "hx": "http://electsys.sjtu.edu.cn/edu/student/elect/warning.aspx?&xklc=1&lb=1",
           "qx": "http://electsys.sjtu.edu.cn/edu/student/elect/warning.aspx?&xklc=2&lb=1",
           "dsl": "http://electsys.sjtu.edu.cn/edu/student/elect/warning.aspx?&xklc=3&lb=1"}


class AutoElectBrowser(object):
    def __init__(self, username, password,
                 course_code, teacher_re,
                 elect_type='qx',
                 course_type='bx',
                 browser_type='chrome', ):
        self.username = username
        self.password = password
        self.course_code = course_code
        self.teacher_re = teacher_re
        self.elect_type = elect_type
        self.course_type = course_type
        self.browser = Browser(browser_type)
        print(type(self.browser))

    def login(self):
        u"""手动输入验证码后登录，调用该函数将返回抢选界面(必修课选课)的browser对象"""
        self.browser.visit(website["login"])
        self.browser.fill('user', self.username)
        self.browser.fill('pass', self.password)
        while self.browser.title != u'上海交通大学教学信息服务网－学生服务平台':
            time.sleep(0.1)
        print(self.browser.windows[0], self.browser.windows[1])
        self.browser.windows[1].close()

    def elect_site(self):
        u"""从教学信息服务网主页面到选课页面"""
        self.browser.visit(website[self.elect_type])
        self.browser.check('CheckBox1')
        self.browser.find_by_name('btnContinue').first.click()

    def jump_to_list(self):
        u"""从某种课程的列表跳转到指定种类的列表
        course_type：'bx'必修，'ts'通识"""
        course_type = self.course_type
        browser = self.browser
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

    def course_arrange(self):
        u"""从课程列表进入到选择教师列表"""
        browser = self.browser
        course_code = self.course_code
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

    def check_is_empty(self):
        u"""在选择教师列表中检验人数是否未满，course_code为课程代码，teacher_name为老师名字，"""
        browser = self.browser
        teacher_re = self.teacher_re
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

    def submit(self):
        self.browser.find_by_value(u'选定此教师').first.click()
        self.browser.find_by_value(u'选课提交').first.click()

    def return_page(self):
        self.browser.find_by_value(u'返 回').first.click()