# 介绍
该项目名为书香盈袖网，是纸质图书共享网站，以提高国民阅读量为主要宗旨。实现了用户注册与登录、书籍查询及预览、收货地址添加、图书借阅归还操作、书籍评论操作等基本功能。同时还具备浏览历史搜索、用户个性分析、消息提醒等创新功能。此外，网站首次引入信用功能，系统根据用户信用等级刷新用户可借书本最大数量及可借书本最大时长等信息，在很大程度上增强用户守信意识。
# 使用说明
## 环境安装
首先安装Python3版本，安装成功后进入项目requirements.txt同级目录下，运行pip install –r requirements.txt命令，安装软件需要的各种包。
## 连接数据库
在本机MySQL数据库中创建book_1数据库，修改settings.py文件中的数据库信息。
## 创建数据表
在manage.py同级目录下执行 python manage.py makemigrations，系统会生成创建数据表文件，接着执行python manage.py migrate 执行生成的文件，生成数据表。
接着找到软件系统下数据文件夹中的数据，将这些数据导入数据库
## 运行项目
在manage.py同级目录下执行python manage.py runserver 代码，运行项目。
运行成功后，在浏览器中输入网址127.0.0.1:8000即可显示网站。
# 注意
该网站用到了Linux中的定时任务模块。如果想要启动定时任务功能，需要在安装了crontab模块的Linux环境下使用。
展示当前定时任务：python manage.py crontab show
添加定时任务：python manage.py crontab add
删除定时任务：python manage.py crontab remove


