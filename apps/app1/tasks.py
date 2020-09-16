import time
from celery import task
from celery import shared_task
#异步任务:shared_task()
#周期性任务:task()


@shared_task()
def add(x, y):
    time.sleep(2)
    return x + y