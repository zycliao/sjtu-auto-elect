# _*_coding:utf-8_*_
import time
import argparse
from autoelectbrowser import AutoElectBrowser


def main():
    args = parse_argument()
    browser = AutoElectBrowser(args.username, args.password,
                               args.course_code, args.teacher_re)
    browser.login()
    browser.elect_site()
    browser.jump_to_list()

    while True:
        browser.course_arrange()
        print('-------time:' + time.strftime('%H:%M:%S', time.localtime(time.time())) + '-------')
        check_result = 0
        try:
            check_result += browser.check_is_empty()
        except IndexError:
            browser.elect_site()
            time.sleep(5)
            browser.jump_to_list()
            continue
        if check_result:
            browser.submit()
            print(u'*******选课成功 ' + time.strftime('%H:%M:%S', time.localtime(time.time())) + '*******')
            break
        else:
            browser.return_page()
    print("Finished!")


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, default='')
    parser.add_argument('--password', type=str, default='')
    parser.add_argument('--course_code', type=str, default='MU901')
    parser.add_argument('--teacher_re', type=str, default=u'385290([\s\S]*)满')
    parser.add_argument('--elect_type', type=str, default='qx',
                        help=u"海选：hx\n抢选：qx\n第三轮选课：dsl")
    parser.add_argument('--course_type', type=str, default='bx',
                        help=u"必修：bx\n人文通识：ts")
    return parser.parse_args()


if __name__ == '__main__':
    main()
