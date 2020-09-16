from kombu import Queue
from datetime import timedelta
from celery.schedules import crontab

BROKER_URL = 'amqp://xxx:xxx@123.207.251.121:5672'# 指定 Broker
CELERY_RESULT_BACKEND = 'rpc://xxx:xxx@123.207.251.121:5672'# 指定 Backend
CELERY_TIMEZONE='Asia/Shanghai'# 指定时区，默认是 UTC
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_IGNORE_RESULT = True
CELERY_TIMEZONE='UTC'
# CELERY_IMPORTS = (
#     # 指定导入的任务模块
#     'app1.tasks'
# )
# CELERY_QUEUES = (
#     Queue('default', routing_key='default'),
#     Queue('worker_queue', routing_key='worker'),
# )
#
# CELERY_ROUTES = {
#     'app1.tasks.add': {'queue': 'worker_queue', 'routing_key': 'worker'},
# }
#
# # schedules
# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#          'task': 'app1.tasks.add',
#          'schedule': timedelta(seconds=30),       # 每 30 秒执行一次
#          'args': (5, 8)                           # 任务函数参数
#     }
#     # 'multiply-at-some-time': {
#     #     'task': 'celery_app.tasks.multiply',
#     #     'schedule': crontab(hour=9, minute=50),   # 每天早上 9 点 50 分执行一次
#     #     'args': (3, 7)                            # 任务函数参数
#     # }
# }