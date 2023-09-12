class Config:
    SECRET_KEY = "PRUEBA"
    broker_url = 'pyamqp://'
    result_backend = 'rpc://'
    task_serializer = 'json'
    result_serializer = 'json'
    enable_utc = True
