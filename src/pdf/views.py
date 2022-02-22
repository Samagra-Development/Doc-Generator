import json

import requests
from requests import HTTPError

from .plugins._doc.external import DOCXPlugin
from .plugins._html.external import HTMLPlugin
from .plugins._pdf.external import PDFPlugin
from .plugins._pdf_make.external import PDFMakePlugin
from .tasks.pdf import *
import logging
import traceback
import os
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from .utils import return_response, format_html, get_sample_data, build_pdf
from django.utils.datastructures import MultiValueDictKeyError

logger = logging.getLogger()


# Create your views here.
def current_datetime(request):
    test_task.delay(10)
    now = datetime.datetime.now()
    logger.info("Test Logs")
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


@api_view(['POST'])
def generate_html_str(request):
    final_data = []
    error_text = error_code = None
    if request.method == 'POST':
        doc_id = request.data['doc_id']
        try:
            # If config_id is provided then replacing config_id
            config_id = request.data['config_id']

        except KeyError:
            # If config_id is not provided then taking default google config as config_id
            config_id = 1
        try:
            raw_data = None
            drive = PDFPlugin(config_id, raw_data)
            token = drive.get_token()
            file = token.CreateFile({'id': doc_id})
            # file.GetContentFile(f'pdf/drivefiles/{docID}.html', mimetype='text/html')
            html_str = file.GetContentString(mimetype='text/html')
            soup = BeautifulSoup(html_str, 'html.parser')
            html_str = soup.prettify()
            # raw_data = get_sample_data()
            # html_str = format_html(html_str, raw_data)
            # build_pdf(html_str, docID)
            html_str = html_str.replace("\"", "'")
            html_str = html_str.replace("\n", " ")
            return HttpResponse(html_str)
        except Exception as e:
            traceback.print_exc()
            error_code = 804
            error_text = f"Something went wrong!: {e}"

    response = return_response(final_data, error_code, error_text)
    return response


@api_view(['POST'])
def generate_pdf(request):
    final_data = []
    error_text = error_code = None
    if request.method == 'POST':
        token = uuid.uuid4()
        plugin = request.GET['plugin']
        data = json.loads(request.body)
        print(data)
        config_id = data['config_id']
        raw_data = data['data']
        template_id = data['template_id']
        try:
            if plugin == 'pdf':
                drive = PDFPlugin(config_id, raw_data)
                error_text, error_code, final_data = drive.shorten_url(template_id, token)
            elif plugin == 'html':
                drive = HTMLPlugin(config_id, raw_data)
                error_text, error_code, final_data = drive.shorten_url(template_id, token)
            elif plugin == 'docx':
                drive = DOCXPlugin(config_id, raw_data)
                error_text, error_code, final_data = drive.shorten_url(template_id, token)
            elif plugin == 'pdf-make':
                drive = PDFMakePlugin(config_id, raw_data)
                error_text, error_code, final_data = drive.shorten_url(template_id, token)
        except Exception as e:
            traceback.print_exc()
            error_code = 804
            error_text = f"Something went wrong: {e}"
        finally:
            return return_response(final_data, error_code, error_text)


@api_view(['GET', 'POST'])
def register_template(request):
    if request.method == "GET":
        try:
            req = requests.get(f"http://127.0.0.1:3000/{request.GET['id']}")
            req.raise_for_status()
            print(req.json())
            return JsonResponse(
                {"Response": [{
                    "code": req.status_code,
                    "message": json.loads(req.json()['body'])
                }]},
                safe=False,
                status=200)
        except HTTPError as http_err:
            return JsonResponse(
                {"Response": [{
                    "code": req.status_code,
                    "message": req.content
                }]},
                safe=False,
                status=200)
        except Exception as e:
            return JsonResponse(
                {"error": [{
                    "code": 804,
                    "message": f"Something went wrong!: {e}"
                }]},
                safe=False,
                status=200)
    elif request.method == "POST":
        try:
            # body = json.dumps(request.json)
            req = requests.post("http://127.0.0.1:3000", data={"meta": {},
                                                               "body": request.body,
                                                               "type": "JS_TEMPLATE_LITERALS",
                                                               "user": "25bbdbf7-5286-4b85-a03c-c53d1d990a24"
                                                               })
            req.raise_for_status()
            return JsonResponse(
                {"Response": [{
                    "code": req.status_code,
                    "message": req.json()
                }]},
                safe=False,
                status=200)

        except HTTPError as http_err:
            return JsonResponse(
                {"error": [{
                    "code": request.status_code,
                    "message": http_err
                }]},
                safe=False,
                status=200)
        except ValueError:
            traceback.print_exc()
            return request.content
        except Exception as e:
            traceback.print_exc()
            return JsonResponse(
                {"error": [{
                    "code": 804,
                    "message": f"Something went wrong!: {e}"
                }]},
                safe=False,
                status=200)


data = {
    "1": "Developer",
    "17": "09-02-2022",
    "2": "Software engineer",
    "4": "D.K",
    "6": "R.V Bangalore",
    "7": "09-02-2022",
    "8": "3",
    "9": "Rahul",
    "10": "Math",
    "11": "50",
    "12": "50",
    "13": "Yes",
    "14": "Yes",
    "15": "5",
    "16": "5",
    "17": "5",
    "18": "Yes",
    "19": "Yes",
    "20": "Concept",
    "21": "Teaching way",
    "22": "Practical",
    "23": "Yes",
    "24": "3 hours",
    "25": "100%",
    "26": "100%",
    "27": "Yes",
    "28": "09-02-2022",
    "29": "Math",
    "30": "Rahul",
    "31": "50",
    "32": "50",
    "33": "Yes",
    "34": "Yes",
    "35": "5",
    "36": "5",
    "37": "5",
    "38": "Yes",
    "39": "Yes",
    "40": "Concept",
    "41": "Teaching way",
    "42": "Practical",
    "43": "Yes",
    "44": "3 hours",
    "45": "100%",
    "46": "100%",
    "47": "Yes",
    "48": "09-02-2022",
}
