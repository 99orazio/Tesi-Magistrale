from celery import Celery
import celery.worker.control
import modulo
# from app import last_id
from datetime import datetime, timedelta

# Creating a celery instance with redis as message broker.
app = Celery('tasks')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'
""""
# configure the Celery beat schedule
app.conf.beat_schedule = {
    'process_run_scans_every_1_minutes': {
        'task': 'tasks.run_scans',
        'schedule': timedelta(seconds=15),
        'args': ['192.168.1.106'],
    },
}
"""

#  DEFINIZIONE DELLE FUNZIONI TASK DA IMPIEGARE CON CELERY E REDIS
@app.task
def run_scans(ip_address):
    modulo.scans(ip_address)


@app.task
def run_scans_time(ip_address, timer):
    modulo.scans_time(ip_address, timer)


@app.task
def stop():
    modulo.stop()


@app.task
def run_scan_port(ip_address, port):
    modulo.scan_port(ip_address, port)


@app.task
def run_scan_service(ip_address):
    modulo.scan_service(ip_address)


@app.task
def run_scan_os(ip_address):
    modulo.scan_os(ip_address)


@app.task
def run_scan_vuln(ip_address):
    modulo.scan_vuln(ip_address)










