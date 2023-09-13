from celery import Celery

# Se declara la aplicación de celery
celery = Celery('index', backend='rpc://', broker='pyamqp://')
