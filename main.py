# _*_coding:utf-8_*_

import time
import argparse
from autoelectbrowser import AutoElectBrowser


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, default='',
                        help=u"Jaccount账号")
    parser.add_argument('--password', type=str, default='',
                        help=u"Jaccount密码")
    parser.add_argument('--course_code', type=str, default='IS209',
                        help=u"课程编号")
    parser.add_argument('--which_class', type=unicode,
                        default=u'001-(2017-2018-2)IS209(教学班)',
                        help=u"课程安排页面里的课号，如001-(2017-2018-2)IS209(教学班)，\n"
                             u"若有多个班需要同时抢，请用英文逗号分隔，\n"
                             u"若多个要抢的班同时人数未满，则将选择课程安排页面里靠前的班")
    parser.add_argument('--elect_type', type=str, default='qx',
                        help=u"选课批次\n"
                             u"海选：hx\n"
                             u"抢选：qx\n"
                             u"第三轮选课：dsl")
    parser.add_argument('--course_type', type=str, default='bx',
                        help=u"课程类型\n"
                             u"必修：bx\n"
                             u"人文通识：ts")
    parser.add_argument('--delay', type=float, default=1.5,
                        help=u"刷新时的延迟时间（秒），如果太短容易出现“过于频繁”的提示，"
                             u"如果太长会使抢课效果变差")
    return parser.parse_args()


def main():
    args = parse_argument()
    which_class = args.which_class
    which_class = which_class.split(',')
    for i in range(len(which_class)):
        which_class[i] = which_class[i].strip()
    browser = AutoElectBrowser(args.username, args.password,
                               args.course_code, which_class,
                               args.elect_type, args.course_type,
                               delay=args.delay)
    browser.login()
    browser.elect_site()
    browser.jump_to_list()

    while True:
        browser.course_arrange()
        print('-------time:' + time.strftime('%H:%M:%S', time.localtime(time.time())) + '-------')
        check_result = 0
        try:
            check_result = browser.check_is_empty()
        except IndexError:
            browser.elect_site()
            time.sleep(5)
            browser.jump_to_list()
            continue
        if check_result == 0:
            browser.submit()
            print(u'*******选课成功 ' + time.strftime('%H:%M:%S', time.localtime(time.time())) + '*******')
            break
        else:
            print u'人数满'
            browser.return_page()
    input("Finished!")


if __name__ == '__main__':
    main()
