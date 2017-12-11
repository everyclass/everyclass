## EveryClass @ CSU - A tool to import your classes to calendar on your phone and know who're taking same classes with you
每课 @ CSU - 一个能将你的课表导入手机、电脑的日历，并查询跟你上同一节课的人的工具

**For English version please scroll down.**

## Chinese 中文

### 介绍
EveryClass 是由就读于中南大学的 Frederic 创建的一个 Python 项目。它有两个基本功能：
- 查询跟你上同一节课的人的名字、学院、班级
- 生成你的课表 WebCal(iCal) 文件，你可以将其导入到手机和电脑的日历（支持iOS、Mac、安卓），让课程和你的其他日历事项在同一处展示，更便于时间管理

如果你是中南大学的学生，直接访问 [https://every.admirable.one](https://every.admirable.one) 即可使用本程序的功能，无需阅读下面的内容；如果你来自其他大学，你可以邀请小伙伴们 fork 这个项目并创建适用于自己的学校的分支。

### 项目结构
为了使项目结构更加清晰，我们把项目中不同的模块分开到了独立的仓库：
- [EveryClass-collector](https://github.com/fr0der1c/EveryClass-collector)：数据爬取与处理模块
- [EveryClass-server](https://github.com/fr0der1c/EveryClass-server)：基于 Flask 的 web 服务


----


## English

### Introduction
Started by Frederic at Central South University, EveryClass is a Python programme which has two basic functions:
- Listing people taking same class with you, including their faculties and major info.
- Generating an `.ics` file that could be imported to calender app so you can view your daily schedule in one place(Chinese college students often use a standalone app to view their course schedule instead of calender app)

### Project Structure
We decided to separate its different module to standalone repositories for clearer structure:
- [EveryClass-collector](https://github.com/fr0der1c/EveryClass-collector)：Data crawling and processing
- [EveryClass-server](https://github.com/fr0der1c/EveryClass-server)：Web server based on Flask