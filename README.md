## EveryClass @ CSU - A tool to import your classes to calendar on your phone and know who're taking same classes with you
每课 @ CSU - 一个能将你的课表导入手机、电脑的日历，并查询跟你上同一节课的人的工具

*To run this python programme, please use Python 3.5.0 or 3.6.0*

## Latest progress 最新进度

#### May 8, 2017
- 主体功能完成

#### Next step
- Keep collecting relationshop between prefixes of student ID and their major /继续收集学号前缀和专业对应关系信息
- Add some statistics function


----
**For English version please scroll down.**


## Chinese 中文

### 简介
EveryClass 是由就读于中南大学的 Frederic 主持创建的一个 Python 项目。它有两个基本功能：
- 查询跟你上同一节课的人的名字、学院、班级
- 生成你的课表 WebCal(iCal) 文件，你可以将其导入到手机和电脑的日历（支持iOS、Mac、安卓），让课程和你的其他日历事项在同一处展示，更便于时间管理

如果你是中南大学的学生，直接访问 https://every.admirable.one 即可使用本程序的功能，无需阅读下面的内容；如果你来自其他大学，你可以邀请小伙伴们fork这个项目并创建适用于自己的学校的分支。

### 文件目录
- `data_collector`: 从教务管理系统采集数据的程序
- `server`: 用于提供查询的网站前后端
- `sql`: 建库SQL命令


### 源码使用指南


#### 数据库和基础设置
- 配置settings.py中的当前学期、数据库等信息；
- 导入 `sql/everyclass.sql` 内的数据到mysql数据库，你可能需要修改学期信息。如果你不知道怎么导入，你可以将它拷贝到`data_collector`目录中，然后在python shell中：
```
>>> from predefined import create_tables
>>> create_tables()
```

#### 学生信息采集
- 通过各种手段取得包含学生基本信息的stu_data.json，保存在data_collector目录下（格式参见stu_data_sample.json，出于对本校学生信息的保护，恕不直接提供stu_data.json文件）

#### 教务数据获取和处理
- 手动通过浏览器操作进入教务的课表查询页面，然后抓包获得 cookies，修改`settings.py`里的`COOKIE_JW`字段（因为教务系统有非常严格的 session 机制，在每次运行 retrieve.py 前请务必先确认你此时通过浏览器能正常访问课表查询界面，然后将 cookies 填入`settings.py`）
- 马上运行`retrieve.py`，它将会按照`stu_data.json`里的列表从教务系统爬取课表存放在`data_collector/raw_data`文件夹里，这大概需要耗费10小时的时间
- 运行`process_data.py`，程序将会通过 Python 的 bs4 库分析raw_data文件夹里的 HTML 页面，并将课程和学生信息写入数据库

#### 英语大班课单独导入
- 英语大班课没有录入教务系统，因此单独运行english_class.py，程序会获取大班课信息然后保存到数据库
- 如果无法获取数据请先抓包获得 cookies 然后填入`settings.py`的`COOKIE_ENG`字段

#### 服务器端
修改 `server/config/default.py`中的设置即可访问





## English

### Introduction
EveryClass is a programme started by Frederic at CSU. It's written in Python. It has two basic functions:
- Show you the list that people study in the same class with you, including their faculties and the classes they in
- Generate an `.ics` file which could be imported to your calendar on your mobile phone, Mac, etc


### Folders
- `data_collector`: Python programme used to fetch and process data from our educational administration system.
- `server`: source files of the website used to query information, including front-end and back-end.
- `sql`: the structure of database of the website above