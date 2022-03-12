import traceback

from celery import shared_task

from ..base.builder import Builder
from ..models import *
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.db.models import F, Q

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
    PeriodicTask.objects.get_or_create(interval=schedule, name='Importing contacts', task='pdf.tasks.celery_tasks.sch')
    print("Scheduled Task Executed")
    return "Done"


@shared_task
def run_retries():
    retry_tasks = list(Doc.objects.filter(Q(config__retries__lte=F('tries')), Q(status='Failed'), Q(isActive=False), Q(retry=True)))
    for tasks in retry_tasks:
        try:
            plugin = tasks.plugin
            data = tasks.data
            token = tasks.id
            if plugin == 'pdf':
                builder = Builder(PDFPlugin(data, token), data, token)
                err_code, err_msg, data = builder._process()
                if err_code is not None:
                    raise Exception("Failed to process Builder")
                else:
                    final_data = data
                # error_text, error_code, final_data = drive.shorten_url()
            elif plugin == 'html':
                builder = Builder(HTMLPlugin(data, token), data, token)
                err_code, err_msg, data = builder._process()
                if err_code is not None:
                    raise Exception("Failed to process Builder")
                else:
                    final_data = data
                # error_text, error_code, final_data = drive.shorten_url()
            elif plugin == 'docx':
                builder = Builder(DOCXPlugin(data, token), data, token)
                err_code, err_msg, data = builder._process()
                if err_code is not None:
                    raise Exception("Failed to process Builder")
                else:
                    final_data = data
                # error_text, error_code, final_data = drive.shorten_url()
            elif plugin == 'pdf-make':
                builder = Builder(PDFMakePlugin(data, token), data, token)
                err_code, err_msg, data = builder._process()
                if err_code is not None:
                    raise Exception("Failed to process Builder")
                else:
                    final_data = data
                # error_text, error_code, final_data = drive.shorten_url()
        except Exception as e:
            traceback.print_exc()
            error_code = 804
            error_text = f"Something went wrong: {e}"
        finally:
            print(f"Result: {final_data}, {error_code}, {error_text}")


@shared_task
def delete_max_retries():
    failed_tasks = list(Doc.objects.filter(Q(config__retries__gt=F('tries')), Q(isActive=False), Q(retry=True)))
    for task in failed_tasks:
        print(f"Deleting object ID: {task.id}, {task.meta}", {task.data})
        task.delete()


@shared_task
def beat_task():
    print("Starting Beat Tasks")
    delete_max_retries()
    run_retries()
    print("Completed Beat Tasks")
