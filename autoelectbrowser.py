# _*_coding:utf-8_*_

from splinter import Browser
import time
import re
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException

website = {"login": "http://electsys.sjtu.edu.cn/edu/login.aspx",
           "hx": "http://electsys.sjtu.edu.cn/edu/student/elect/warning.aspx?&xklc=1&lb=1",
           "qx": "http://electsys.sjtu.edu.cn/edu/student/elect/warning.aspx?&xklc=2&lb=1",
           "dsl": "http://electsys.sjtu.edu.cn/edu/student/elect/warning.aspx?&xklc=3&lb=1",
           "bx": "http://electsys.sjtu.edu.cn/edu/student/elect/speltyRequiredCourse.aspx",
           "xx": "http://electsys.sjtu.edu.cn/edu/student/elect/speltyLimitedCourse.aspx",
           "ts": "http://electsys.sjtu.edu.cn/edu/student/elect/speltyCommonCourse.aspx",
           "rx": "http://electsys.sjtu.edu.cn/edu/student/elect/outSpeltyEP.aspx", }


class AutoElectBrowser(object):
    def __init__(self, username, password,
                 course_code, which_class,
                 elect_type='qx',
                 course_type='bx',
                 browser_type='chrome',
                 delay=1, ):
        self.username = username
        self.password = password
        self.course_code = course_code
        self.which_class = which_class
        self.elect_type = elect_type
        self.course_type = course_type
        self.delay = delay
        self.browser = Browser(browser_type)
        self.class_info = []
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
        course_type：'bx'必修，'rw'人文，'sk'社科，'zk'自科，'sx'数学与逻辑，'xx'限选，'rx'任选"""

        self.browser.visit(website[self.course_type])
        try:
            if self.course_type == 'xx':
                self.browser.choose('gridModule$ctl02$radioButton', 'radioButton')
            if self.course_type == 'rw':
                self.browser.choose('gridGModule$ctl02$radioButton', 'radioButton')
            if self.course_type == 'sk':
                self.browser.choose('gridGModule$ctl03$radioButton', 'radioButton')
            if self.course_type == 'zk':
                self.browser.choose('gridGModule$ctl04$radioButton', 'radioButton')
            if self.course_type == 'sx':
                self.browser.choose('gridGModule$ctl05$radioButton', 'radioButton')
            if self.course_type == 'rx':
                pass
        except ValueError as e:
            print e

    def course_arrange(self):
        u"""从课程列表进入到选择教师列表"""
        browser = self.browser
        course_code = self.course_code
        while 1:
            try:
                browser.choose('myradiogroup', course_code)
                time.sleep(self.delay)  # 0.6会出现刷新过于频繁
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
        u"""若有多个班同时人数未满，将选择列表中第一个，并返回0
        若所有班人数满，将返回-1"""
        browser = self.browser
        html = browser.html
        self.class_info = []
        soup = BeautifulSoup(html)
        table = soup.find_all('table', class_='alltab')[0].table
        all_class = table.contents[1]
        all_class = all_class.contents[1: -1]
        for c in all_class:
            each_class_info = []
            each_class = c.contents[1: -1]
            each_class_info.append(each_class[0].contents[1].contents[0].attrs['value'])
            each_class = each_class[1:]
            for ec in each_class:
                each_class_info.append(unicode(ec.string).strip())
            self.class_info.append(each_class_info)
            for wc in self.which_class:
                if wc == each_class_info[3]:
                    if each_class_info[11] == u'人数未满':
                        self.browser.choose("myradiogroup", each_class_info[0])
                        return 0
        return -1

    def submit(self):
        self.press_button(u'选定此教师')
        self.press_button(u'选课提交')

    def return_page(self):
        self.press_button(u'返 回')

    def press_button(self, name):
        self.browser.find_by_value(name).first.click()
