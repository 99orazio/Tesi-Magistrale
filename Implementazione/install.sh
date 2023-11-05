#celery -A tasks worker --pool=solo --loglevel=info
celery -A tasks worker --loglevel=info
#celery -A tasks beat -l INFO

python app.py
celery -A tasks flower --port=5566

