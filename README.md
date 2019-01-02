## EveryClass @ CSU - Personal curriculum schedule subscription & powerful information query tool for your college life at CSU
每课 @ CSU - 个人课表订阅 & 强大的信息查询工具，为你的 CSU 校园生活量身定做

**For English version please scroll down.**

## Chinese 中文

### 介绍
通过每课，你可以：
- 查询学生、教师的课表
- 查询课程详情
- 查询教室时间安排和空教室信息
- 生成你的课表 WebCal(iCal) 文件，你可以将其导入到手机和电脑的日历（支持iOS、Mac、安卓），让课程和你的其他日历事项在同一处展示，更便于时间管理

如果你是中南大学的学生，直接访问 [https://everyclass.xyz](https://everyclass.xyz) 即可使用本程序的功能，无需阅读下面的内容；如果你来自其他大学，你可以邀请小伙伴们 fork 这个项目并创建适用于自己的学校的分支。

### 代码仓库
- [everyclass-server](https://github.com/fr0der1c/EveryClass-server)：提供面向终端用户的 web 服务，基于 Flask
- [everyclass-collector](https://github.com/fr0der1c/EveryClass-collector)：数据爬取与处理模块
- [everyclass-api-server](https://github.com/AdmirablePro/everyclass-api-server)：API-server 微服务，提供数据查询


----


## English

### Introduction
Using EveryClass, you can:
- Getting a teacher or student's course schedule
- Getting rich information of a course
- Query schedule of a classroom, and see which classroom is not engaged
- Generating an `.ics` file that could be imported to calender app so you can view your daily schedule in one place(Chinese college students often use a standalone app to view their course schedule instead of calender app)

### Code Repositories
- [EveryClass-server](https://github.com/fr0der1c/EveryClass-server)：Providing web service to end user. Based on Flask.
- [EveryClass-collector](https://github.com/fr0der1c/EveryClass-collector)：Data crawling and processing
- [everyclass-api-server](https://github.com/AdmirablePro/everyclass-api-server)：API-server micro-service. Offers data querying service
