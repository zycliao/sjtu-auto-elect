# SJTU自动抢课脚本
本脚本在抢选或第三轮选课阶段反复刷新人数已满课程，直到有人退课。  
## 安装
### Requirements
python2.7  
splinter  
chrome  
BeautifulSoup
### chromedriver
splinter要正常运行需要浏览器驱动，这里提供一个百度云链接  
http://pan.baidu.com/s/1nu7A7rz 密码：vyvx  
将chromedriver复制到chrome.exe所在目录下（一般为C:\Program Files (x86)\Google\Chrome\Application），并将改目录加入系统环境变量PATH中，然后重启计算机。  
## 使用
目前在windows7系统下测试必修课，通识课正常  
限选课由于各专业差异巨大，需要手动修改方可实现  
任选课暂未实现  
### 使用示例
```
# 抢选操作系统课程
python main.py --username laowang --password 123456 --course_code IS206 --which_class 001-(2017-2018-1)IS206(教学班),001-(2017-2018-2)IS206(教学班) --elect_type qx --course_type bx --delay 1.0
# 各参数的具体含义可使用如下代码查询
python main.py -h
```
