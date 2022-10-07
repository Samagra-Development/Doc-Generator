import json
from json import JSONDecodeError

import requests
from django.views.decorators.csrf import csrf_exempt
from requests import HTTPError
from django.http import HttpResponseRedirect

from .base.builder import Builder
from .plugins._doc.external import DOCXPlugin
from .plugins._html.external import HTMLPlugin
from .plugins._pdf.external import PDFPlugin
from .plugins._pdf_make.external import PDFMakePlugin
from .tasks.celery_tasks import *
import logging
import traceback
import os
import requests
from django.conf import settings

import jwt
# from jwt import PyJWKClient

import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup
from .utils import return_response, format_html, get_sample_data, build_pdf, return_tokens
from django.utils.datastructures import MultiValueDictKeyError
from dotenv import load_dotenv

from .models import *

load_dotenv()

logger = logging.getLogger()


# Create your views here.
def current_datetime(request):
    test_task.delay(10)
    now = datetime.datetime.now()
    logger.info("Test Logs")
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

  
@csrf_exempt
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
        try:
            if plugin == 'pdf':
                drive = PDFPlugin(config_id, data, token)
                error_text, error_code, final_data = drive.shorten_url()
            elif plugin == 'html':
                drive = HTMLPlugin(config_id, data, token)
                error_text, error_code, final_data = drive.shorten_url()
            elif plugin == 'docx':
                drive = DOCXPlugin(config_id, data, token)
                error_text, error_code, final_data = drive.shorten_url()
            elif plugin == 'pdf-make':
                drive = PDFMakePlugin(config_id, data, token)
                error_text, error_code, final_data = drive.shorten_url()
        except Exception as e:
            traceback.print_exc()
            error_code = 804
            error_text = f"Something went wrong: {e}"
        finally:
            return return_response(final_data, error_code, error_text)


@csrf_exempt
@api_view(['POST'])
def generate_pdf2(request):
    final_data = []
    error_text = error_code = None
    if request.method == 'POST':
        data = json.loads(request.body)
        token = uuid.uuid4()
        plugin = request.GET['plugin']
        Doc.objects.create(id=token, config_id=data['config_id'], plugin=plugin)
        try:
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
            return return_response(final_data, error_code, error_text)


@csrf_exempt
@api_view(['GET', 'POST'])
def register_template(request):
    final_data = []
    error_text = error_code = None
    if request.method == "GET":
        try:
            req = requests.get(f"{os.getenv('TEMPLATOR_URL')}/{request.GET['id']}")
            req.raise_for_status()
            print(req.json())
            try:
                final_data = json.loads(req.json()['body'])
            except JSONDecodeError:
                final_data = req.json()
        except Exception as e:
            traceback.print_exc()
            error_code = 804,
            error_text = f"Something went wrong!: {e}",
        return return_response(final_data, error_code, error_text)
    elif request.method == "POST":
        try:
            transformers = None
            type = request.data["type"]
            body = None
            if type == "GOOGLE_DOC":
                if 'GA-OAUTH-TOKEN' in request.headers:
                    doc_id = request.data['data']
                    meta = "GOOGLE_DOC"
                    try:
                        resp = requests.get(f'https://www.googleapis.com/drive/v3/files/{doc_id}/export', params={
                            'mimeType': 'text/html'
                        }, headers={
                            'Authorization': f"Bearer {request.headers.get('GA-OAUTH-TOKEN')}"
                        })

                        if resp.status_code == 200:
                            token = uuid.uuid4()
                            data = {"data": None, "template_id": None}
                            drive = PDFPlugin(data, token)
                            html_str = str(resp.content)
                            html_str = html_str.replace("\"", "'")
                            html_str = html_str.replace("\n", " ")
                            body = html_str
                        else:
                            raise Exception(resp.content)
                    except Exception as e:
                        traceback.print_exc()
                        error_code = 804
                        error_text = f"Something went wrong!: {e}"
                else:
                    doc_id = request.data['data']
                    meta = "GOOGLE_DOC"
                    try:
                        token = uuid.uuid4()
                        data = {"data": None, "template_id": None}
                        drive = PDFPlugin(data, token)
                        client = drive.get_client()
                        file = client.CreateFile({'id': doc_id})
                        # file.GetContentFile(f'pdf/drivefiles/{docID}.html', mimetype='text/html')
                        html_str = file.GetContentString(mimetype='text/html')
                        html_str = html_str.replace("\"", "'")
                        # soup = BeautifulSoup(html_str, 'html.parser')
                        # html_str = soup.prettify()
                        html_str = html_str.replace("\n", " ")
                        # raw_data = get_sample_data()
                        # html_str = format_html(html_str, raw_data)
                        # build_pdf(html_str, docID)
                        body = html_str
                    except Exception as e:
                        traceback.print_exc()
                        error_code = 804
                        error_text = f"Something went wrong!: {e}"
            elif type == "STRING":
                body = request.data['data']
                meta = "STRING"
            elif type == "JSON":
                body = json.dumps(request.data['data'])
                meta = "JSON"
            if 'transformers' in request.data:
                data['transformers'] = request.data['transformers']
            req = requests.post(os.getenv('TEMPLATOR_URL'), data={"transformers": transformers,
                                                                       "meta": meta,
                                                                       "body": body,
                                                                       "type": "JS_TEMPLATE_LITERALS",
                                                                       "user": os.getenv('DOC_GENERATOR_ID')})
            req.raise_for_status()
            final_data = req.json()
        except Exception as e:
            traceback.print_exc()
            error_code = 804
            error_text = f"Something went wrong!: {e}"
        print(final_data, error_code, error_text)
        return return_response(final_data, error_code, error_text)


@csrf_exempt
@api_view(['GET', 'POST'])
def generate_bulk(request, token=''):
    if request.method == "GET":
        error_code = error_text = final_data = None
        if token != '':
            try:
                query = Doc.objects.get(pk=token)
                print(token, query)
                final_data = query.serialize()
            except ObjectDoesNotExist:
                traceback.print_exc()
                error_text = "Wrong Token Id"
                error_code = 804
            except Exception as e:
                traceback.print_exc()
                error_code = 804
                error_text = f"Something went wrong: {e}"
        else:
            error_code = 500
            error_text = "Method Not Allowed"
        return return_response(final_data, error_code, error_text)
    if request.method == "POST":
        if token == '':
            error_code = error_text = None
            final_data = []
            try:
                raw_data = json.loads(request.body)
                for data in raw_data:
                    token = str(uuid.uuid4())
                    Doc.objects.create(id=token, config_id=data['config_id'])
                    plugin = data['plugin']
                    if plugin == 'pdf':
                        bulk_generate_task.delay(data, 'pdf', token)
                        # error_text, error_code, final_data = drive.shorten_url()
                    elif plugin == 'html':
                        bulk_generate_task.delay(data, 'html', token)
                        # error_text, error_code, final_data = drive.shorten_url()
                    elif plugin == 'docx':
                        bulk_generate_task.delay(data, 'docx', token)
                        # error_text, error_code, final_data = drive.shorten_url()
                    elif plugin == 'pdf-make':
                        bulk_generate_task.delay(data, 'pdf-make', token)
                # error_text, error_code, final_data = drive.shorten_url()
                    final_data.append(token)
            except Exception as e:
                traceback.print_exc()
                error_code = 804
                error_text = f"Something went wrong: {e}"
        else:
            error_code = 500
            error_text = "Method Not Allowed"
        return return_tokens(final_data, error_code, error_text)



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


@csrf_exempt
@api_view(['GET'])
def register_user_init(request):
    redirect_url=os.getenv('GC_REDIRECT_URL')
    scope = "https://www.googleapis.com/auth/drive openid profile email"
    url = f"https://accounts.google.com/o/oauth2/auth?client_id={settings.GC_CLIENT_ID}&redirect_uri={redirect_url}&scope={scope}&access_type=offline&response_type=code"
    print(url)
    return HttpResponseRedirect(url)


@csrf_exempt
@api_view(['GET'])
def register_user(request):
    redirect_url=os.getenv('GC_REDIRECT_URL')
    code = request.GET['code']
    url = "https://oauth2.googleapis.com/token"
    payload=f'code={code}&client_id={settings.GC_CLIENT_ID}&client_secret={settings.GC_CLIENT_SECRET}&redirect_uri={redirect_url}&grant_type=authorization_code'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    print(data)
    url = "https://www.googleapis.com/oauth2/v3/certs"
    client = jwt.PyJWKClient(url)
    pub_key = client.get_signing_key_from_jwt(data["id_token"]).key
    aud = jwt.decode(data["id_token"], options={"verify_signature": False})["aud"]
    decoded = jwt.decode(data["id_token"], pub_key, algorithms=["RS256"], audience=aud, options={"verify_exp": False})

    try:
        existing_user = Tenant.objects.filter(email=decoded["email"])
        if existing_user.count() > 0:
            existing_user.update(name=decoded["name"], email=decoded["email"], google_token=json.dumps(data))
            # return JsonResponse({"status": "User already registered"})
        else:
            Tenant.objects.create(name=decoded["name"], email=decoded["email"], google_token=json.dumps(data))

        return JsonResponse({
                "status": "User registered successfully",
                "token": data
            })
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({"status": "Exception in registering user", "error": traceback.format_exc()})
