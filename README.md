# 1. 项目描述
项目名称：EasyOps运维项目

此项目主要基于Python Flask框架编写，前端主要是用jquery+bootstrap技术进行页面设计展示。

项目主要提供的功能如下：
1. 登陆注册
2. 添加管理主机
3. 对管理主机进行远程Ansible命令执行
4. 添加云存储
5. 数据同步，基于rclone模块进行云数据存储之间的互传

单前版本暂时支持以上几个功能，后续还会持续增加其他功能

### 1.1. 项目功能截图01-登陆注册
![](https://tva1.sinaimg.cn/large/008i3skNgy1gtx11j8298j60zk0u00tm02.jpg)
![](https://tva1.sinaimg.cn/large/008i3skNgy1gtx11y99ggj60z40u00tn02.jpg)

### 1.2. 项目功能截图01-概览页面
![概览页面](https://tva1.sinaimg.cn/large/008i3skNgy1gtx0vxs8c0j61ki0u0gmy02.jpg)

### 1.3. 项目功能截图02-主机管理
![](https://tva1.sinaimg.cn/large/008i3skNgy1gtx0x9r4gfj627w0twn1m02.jpg)

### 1.4. 项目功能截图03-存储管理
![](https://tva1.sinaimg.cn/large/008i3skNgy1gtx0xst4mzj61vb0u0di202.jpg)

### 1.5. 项目功能截图04-远程执行
![](https://tva1.sinaimg.cn/large/008i3skNgy1gtx0ydcm3xj61zq0u0acg02.jpg)

![](https://tva1.sinaimg.cn/large/008i3skNgy1gtx0yw2xcrj61ca0u00xg02.jpg)

### 1.6. 项目功能截图05-数据同步
开发中...

# 2. 项目运行

## 2.1. 初始化项目
项目使用python版本为3.6.0以上版本，请按照操作系统类型进行安装

### 2.1.1 安装python程序（CentOS示例）
[Python3.7安装指导链接](https://www.npyun.com/news/content/94.html)

### 初始化环境目录
```
# 创建虚拟python运行目录
python -m .venv venv

# 激活虚拟目录
source .venv/bin/activate
```

## 2.2. 安装依赖包
```
pip install -r requirements.txt
```

## 2.3. 建立数据库
登陆连接使用的MYSQL数据库，建立数据库及授权远程访问
```
# 创建数据库
MariaDB [(none)]> create database easyops;

# 创建数据库访问用户并添加远程访问授权
MariaDB [(none)]> grants all privileges on easyops.* to "easyops"@"%" identified by "easyopsPass";
MariaDB [(none)]> flush privileges;
```

## 2.4. 修改配置文件
```
# 修改项目根目录下的config.py配置文件
SQLALCHEMY_DATABASE_URI，修改为数据库连接URL
REDIS_HOST，修改为redis的服务地址
REDIS_PORT，修改为redis的服务端口
```

## 2.5. 初始化数据库
```
python manage.py db init
python manage.py migrate
python manage.py upgrade
```

## 2.6. 启动项目程序
```
python manage.py runserver -h <listen ipaddress> -p <port>
```

# 3. 浏览器访问
```
http://<Listen IP>:<Listen Port>
```