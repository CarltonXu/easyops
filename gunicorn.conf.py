# 并行工作进程数量
workers = 5
# 指定每个工作者的线程数
threads = 2
# 工作模式协程
worker_class = "gevent"
# 设置最大并发量
worker_connections = 2000
# 设置守护进程，将进程交给supervisor管理
daemon = "false"
# 监听服务地址端口
bind = "0.0.0.0:80"
# 设置进程文件目录
pidfile = "/var/run/gunicorn.pid"
# 设置访问日志和错误信息日志路径
accesslog = "/var/log/easyops/gunicorn_access.log"
errorlog = "/var/log/easyops/gunicorn_error.log"
# 设置日志记录水平
loglevel = "warning"