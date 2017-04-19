## EveryClass @ CSU - A tool to know people taking same classes with you & add your classes to calendar on your phone.
每课 @ CSU - 一个查询跟你上同一节课的人、并能将你的课表导入手机、电脑日历的工具

## IMPORTANT NOTICE
Notice that this project is still under development, please DO NOT clone this repository at the moment until we finish the first beta version. You can "watch" our progress now.

## Our latest progress
I have basically finished the data_collector module. The project still has a long way to go.

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
- `db`: 数据库结构备份文件

### 源码使用指南
#### data_collector
1. 通过各种手段取得包含学生基本信息的stu_data.json，保存在data_collector目录下
2. 手动通过浏览器操作进入教务的课表查询页面，然后抓包获得 cookies，修改settings.py里的cookies字段
3. 马上运行retrieve.py，它将会按照stu_data.json里的列表从教务系统爬取课表存放在data_collector/raw_data文件夹里，这大概需要耗费10小时的时间。
4. 配置settings.py中的当前学期、数据库等信息，导入 db 中的数据库备份文件到你本地的数据库
5. 运行process_data.py，程序将会通过 Python 的 bs4 库分析raw_data文件夹里的 HTML 页面，并将课程和学生信息写入数据库
6. 英语大班课没有录入教务系统，因此单独运行english_class.py，程序会获取大班课信息然后保存到数据库

### 备注
#### data_collector
- 因为教务系统的 session 机制，在运行 retrieve_from_server.py 前请手动运行浏览器打开课表查询界面，确保此时在服务器上你的 session 已经被加入白名单

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