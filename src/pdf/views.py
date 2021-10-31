from django.http import HttpResponse
import datetime
from .tasks.pdf import *


def current_datetime(request):
    test_task.delay(10)
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)