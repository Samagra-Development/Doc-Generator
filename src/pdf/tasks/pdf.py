from celery import shared_task

from ..base.builder import Builder
from ..models import *
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# One time tasks
from ..plugins._doc.external import DOCXPlugin
from ..plugins._html.external import HTMLPlugin
from ..plugins._pdf.external import PDFPlugin
from ..plugins._pdf_make.external import PDFMakePlugin


@shared_task
def test_task(total):
    print(total * 100)
    print(Doc.objects.all().count())
    print("Task Executed")
    return total


@shared_task
def bulk_generate_task(data, plugin, token):
    config_id = data['config_id']
    if plugin == 'pdf':
        builder = Builder(PDFPlugin(data, token), data, token)
        err_code, err_msg, data = builder._process()
        if err_code is not None:
            print("Failed to process Builder")
        else:
            final_data = data
        # error_text, error_code, final_data = drive.shorten_url()
    elif plugin == 'html':
        builder = Builder(HTMLPlugin(data, token), data, token)
        err_code, err_msg, data = builder._process()
        if err_code is not None:
            print("Failed to process Builder")
        else:
            final_data = data
        # error_text, error_code, final_data = drive.shorten_url()
    elif plugin == 'docx':
        builder = Builder(DOCXPlugin(data, token), data, token)
        err_code, err_msg, data = builder._process()
        if err_code is not None:
            print("Failed to process Builder")
        else:
            final_data = data
        # error_text, error_code, final_data = drive.shorten_url()
    elif plugin == 'pdf-make':
        builder = Builder(PDFMakePlugin(data, token), data, token)
        err_code, err_msg, data = builder._process()
        if err_code is not None:
            print("Failed to process Builder")
        else:
            final_data = token


# Scheduled Tasks
@shared_task
def sch():
    schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.SECONDS, )
    PeriodicTask.objects.get_or_create(interval=schedule, name='Importing contacts', task='pdf.tasks.pdf.sch')
    print("Scheduled Task Executed")
    return "Done"


@shared_task
def update_step_choice(id, step):
    doc = Doc.objects.get(pk=id)
    doc.step = step
    doc.save()


@shared_task
def update_status_choice(id, status):
    doc = Doc.objects.get(pk=id)
    doc.step = status
    doc.save()
