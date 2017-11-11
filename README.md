# SJTU自动抢课脚本
本脚本在抢选或第三轮选课阶段反复刷新人数已满课程，直到有人退课。  
## 安装
### Requirements
python2.7  
splinter  
chrome  
### chromedriver
splinter要正常运行需要浏览器驱动，这里提供一个百度云链接  
http://pan.baidu.com/s/1nu7A7rz 密码：vyvx  
将chromedriver复制到chrome.exe所在目录下（一般为C:\Program Files (x86)\Google\Chrome\Application），并将改目录加入系统环境变量PATH中，然后重启计算机。  
## 使用
该版本最初于2016年实现，由于教学信息服务网的页面更改，现在可能无法使用，未来选课时将修复。