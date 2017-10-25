import time
from celery import shared_task

celery = Celery('tasks', broker='redis://localhost:6379/0')

@shared_task
def sendmail(mail):
    print('sending mail to %s...' % mail['to'])
    time.sleep(2.0)
    print('mail sent.')
