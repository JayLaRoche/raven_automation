from celery import Celery

app = Celery('backend')

app.config_from_object('backend.config', silent=True)

# Set broker and result backend
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

