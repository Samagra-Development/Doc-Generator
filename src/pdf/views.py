from django.http import HttpResponse
import datetime
from .tasks.pdf import *
import logging

logger = logging.getLogger()


def current_datetime(request):
    test_task.delay(10)
    now = datetime.datetime.now()
    logger.info("Test Logs")
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)