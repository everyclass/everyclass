## EveryClass @ CSU - A tool to know people study with you & add your classes to system's calendar
每课 @ CSU - 一个查询跟你上同一节课的人、并能将你的课表导入手机日历的工具

## Introduction 介绍
EveryClass is a programme started by Frederic. It has two basic functions:
- Show you the list that people study in the same class with you, including their faculties and the classes they in
- Generate an `.ics` file which could be imported to your calendar on your mobile phone, Mac, etc



### Folders 文件目录
- `data_collector`: Python programme used to fetch and process data from our educational administration system.
- `server`: source files of the website used to query information, including front-end and back-end.
- `db`: the structure of database of the website above

### 备注
#### data_collector
- 因为教务系统的 session 机制，在运行 retrieve_from_server.py 前请手动运行浏览器打开课表查询界面，确保此时在服务器上你的 session 已经被加入白名单

#### server
等待补充


