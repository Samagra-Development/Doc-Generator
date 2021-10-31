from celery import shared_task
from ..models import *
from django_celery_beat.models import PeriodicTask, IntervalSchedule

schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS,)
PeriodicTask.objects.get_or_create(interval=schedule, name='Importing contacts', task='pdf.tasks.pdf.sch')

# One time tasks
@shared_task
def test_task(total):
    print(total*100)
    print(Pdf.objects.all().count())
    print("Task Executed")
    return total


# Scheduled Tasks
@shared_task
def sch():
    print("Scheduled Task Executed")
    return "Done"
