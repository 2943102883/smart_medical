# Celery配置文件

# 指定消息队列为Redis
broker_url = "redis://120.78.168.67/10"
CELERY_RESULT_BACKEND = "redis://120.78.168.67/0"
CELERY_TIMEZONE = 'Asia/Shanghai'
