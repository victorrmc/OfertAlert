from celery import Celery

celery = Celery('index', backend='rpc://', broker='pyamqp://')