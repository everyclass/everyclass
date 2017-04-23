## EveryClass @ CSU - A tool to know people taking same classes with you & add your classes to calendar on your phone.
每课 @ CSU - 一个查询跟你上同一节课的人、并能将你的课表导入手机、电脑日历的工具

To use this python programme, you need to use Python 3.5.0.


## IMPORTANT NOTICE 重要提示

Notice that this project is still under development, please DO NOT fork this repository at the moment until we finish the first beta version. You can "watch" our progress now.

这个项目尚未完成最初版本，请不要fork这个仓库直到我完成第一个完整的测试版。你可以先 Watch 关注项目进度：）

## Our latest progress 最新进度

#### Apr 19
Basically finished the data_collector module. The project still has a long way to go.

----
For English readme please scroll down.


## Chinese 中文

### 介绍
EveryClass 是由就读于中南大学的 Frederic 主持创建的一个 Python 项目。它有两个基本功能：
- 查询跟你上同一节课的人的名字、学院、班级
- 生成你的课表ics文件，你可以将其导入到手机和电脑的日历（支持iOS、Mac、安卓），不用每次还单独打开课程格子看课表了
如果你是中南大学的学生，直接访问 http://every.admirable.one 即可使用本程序的功能，无需阅读下面的内容；如果你来自其他大学，你可以邀请小伙伴们克隆这个项目并创建适用于自己的学校的分支。

### 文件目录
- `data_collector`: 从教务管理系统采集数据的程序
- `server`: 用于提供查询的网站前后端
- `sql`: 建库SQL命令


### 源码使用指南

#### data_collector 数据采集器


##### 数据库和基础设置
- 配置settings.py中的当前学期、数据库等信息；
- 修改 sql/everyclass.sql 内的学期信息，然后将其拷贝到data_collector目录中，运行predefined.py，按照提示导入数据库

##### 学生信息采集
- 通过各种手段取得包含学生基本信息的stu_data.json，保存在data_collector目录下（格式参见stu_data_sample.json，出于对本校学生信息的保护，恕不直接提供stu_data.json文件）

##### 教务数据获取和处理
- 手动通过浏览器操作进入教务的课表查询页面，然后抓包获得 cookies，修改settings.py里的COOKIE_JW字段
- 马上运行retrieve.py，它将会按照stu_data.json里的列表从教务系统爬取课表存放在data_collector/raw_data文件夹里，这大概需要耗费10小时的时间
- 运行process_data.py，程序将会通过 Python 的 bs4 库分析raw_data文件夹里的 HTML 页面，并将课程和学生信息写入数据库

##### 英语大班课单独导入
- 英语大班课没有录入教务系统，因此单独运行english_class.py，程序会获取大班课信息然后保存到数据库
- 如果无法获取数据请先抓包获得 cookies 然后填入settings.py的COOKIE_ENG字段


#### server 查询服务端



### 备注

#### data_collector
- 因为教务系统有非常严格的 session 机制，在每次运行 retrieve.py 前请务必先确认你此时通过浏览器能正常访问课表查询界面，然后将 cookies 填入settings.py

#### server
等待补充


## English

### Introduction
EveryClass is a programme started by Frederic at CSU. It's written in Python. It has two basic functions:
- Show you the list that people study in the same class with you, including their faculties and the classes they in
- Generate an `.ics` file which could be imported to your calendar on your mobile phone, Mac, etc


### Folders
- `data_collector`: Python programme used to fetch and process data from our educational administration system.
- `server`: source files of the website used to query information, including front-end and back-end.
- `db`: the structure of database of the website above