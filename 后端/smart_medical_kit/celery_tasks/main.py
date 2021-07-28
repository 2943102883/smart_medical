# celery入口文件
from celery import Celery

# 创建Celery实例
celery_app = Celery('map')

# 加载配置
celery_app.config_from_object('celery_tasks.config')

#从配置文件加载配置
celery_app.config_from_object('celery_tasks.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_tasks.map'])
