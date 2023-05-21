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
from .plugins._template.external import TemplatePlugin
from .plugins._pdf_make.external import PDFMakePlugin
from .tasks.celery_tasks import *
import logging
import traceback
import os
import requests

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
        Doc.objects.create(
            id=token, config_id=data['config_id'], plugin=plugin)
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
            req = requests.get(
                f"{os.getenv('TEMPLATOR_URL')}/{request.GET['id']}")
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
            access_token = None
            transformers = None
            type = request.data["type"]
            body = None
            if type == "GOOGLE_DOC":
                if 'GA-OAUTH-TOKEN' in request.headers:
                    access_token = request.headers.get('GA-OAUTH-TOKEN')
                    if not 'GA-OAUTH-REFRESHTOKEN' in request.headers:
                        raise Exception('Refresh token missing')

                    doc_id = request.data['data']
                    meta = "GOOGLE_DOC"
                    try:
                        resp = requests.get(f'https://www.googleapis.com/drive/v3/files/{doc_id}/export', params={
                            'mimeType': 'text/html'
                        }, headers={
                            'Authorization': f"Bearer {access_token}"
                        })

                        if resp.status_code == 200:
                            token = uuid.uuid4()
                            data = {"data": None, "template_id": None}
                            drive = PDFPlugin(data, token)
                            html_str = str(resp.text)
                            html_str = html_str.replace("\"", "'")
                            html_str = html_str.replace("\n", " ")
                            body = html_str
                        elif resp.status_code == 401:
                            status, data = refresh_gc_token(
                                request.headers.get('GA-OAUTH-REFRESHTOKEN'))
                            if status == 200:
                                access_token = data['access_token']
                                # repeat request
                                r = requests.post(request.build_absolute_uri(), headers={
                                    'GA-OAUTH-TOKEN': access_token,
                                    'GA-OAUTH-REFRESHTOKEN': request.headers.get('GA-OAUTH-REFRESHTOKEN'),
                                }, data=request.data)
                                return return_response(
                                    r.json()[
                                        'data'] if 'data' in r.json() else None,
                                    r.json()[
                                        'error'][0]['code'] if 'error' in r.json() else None,
                                    r.json()['error'][0]['message'] if 'error' in r.json() else None)
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
            final_data = {
                **req.json(),
                **{
                    'access_token': access_token
                }
            }
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


@csrf_exempt
@api_view(['POST'])
def generate_by_template(request):
    final_data = []
    error_text = error_code = None
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data['token']
        plugin = request.GET['plugin']
        Doc.objects.create(
            id=token, config_id=data['config_id'], plugin=plugin)
        try:
            if plugin == 'pdf':
                builder = Builder(TemplatePlugin(data, token), data, token)
                err_code, err_msg, data = builder._process()
                if err_code is not None:
                    raise Exception("Failed to process Builder")
                else:
                    final_data = data
                # error_text, error_code, final_data = drive.shorten_url()
            # TODO: Impl other plugins
            # elif plugin == 'html':
            #     builder = Builder(HTMLPlugin(data, token), data, token)
            #     err_code, err_msg, data = builder._process()
            #     if err_code is not None:
            #         raise Exception("Failed to process Builder")
            #     else:
            #         final_data = data
            #     # error_text, error_code, final_data = drive.shorten_url()
            # elif plugin == 'docx':
            #     builder = Builder(DOCXPlugin(data, token), data, token)
            #     err_code, err_msg, data = builder._process()
            #     if err_code is not None:
            #         raise Exception("Failed to process Builder")
            #     else:
            #         final_data = data
            #     # error_text, error_code, final_data = drive.shorten_url()
            # elif plugin == 'pdf-make':
            #     builder = Builder(PDFMakePlugin(data, token), data, token)
            #     err_code, err_msg, data = builder._process()
            #     if err_code is not None:
            #         raise Exception("Failed to process Builder")
            #     else:
            #         final_data = data
                # error_text, error_code, final_data = drive.shorten_url()
            else:
                final_data = "Plugin Not Supported"
        except Exception as e:
            traceback.print_exc()
            error_code = 804
            error_text = f"Something went wrong: {e}"
        finally:
            return return_response(final_data, error_code, error_text)


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
    url = f"https://accounts.google.com/o/oauth2/auth"
    url += f"?client_id={os.getenv('GC_CLIENT_ID')}"
    url += f"&redirect_uri={os.getenv('GC_REDIRECT_URL')}"
    url += f"&scope={os.getenv('GC_SCOPES')}"
    url += f"&access_type=offline"
    url += f"&response_type=code"
    return HttpResponseRedirect(url)


@csrf_exempt
@api_view(['GET'])
def register_user(request):
    final_data = []
    error_text = error_code = None

    try:
        if 'error' in request.GET:
            raise Exception(request.GET['error'])
        elif not 'code' in request.GET:
            raise Exception('Authorization code is missing')

        url = "https://oauth2.googleapis.com/token"
        payload = {
            'code': request.GET['code'],
            'client_id': os.getenv('GC_CLIENT_ID'),
            'client_secret': os.getenv('GC_CLIENT_SECRET'),
            'redirect_uri': os.getenv('GC_REDIRECT_URL'),
            'grant_type': 'authorization_code'
        }
        response = requests.post(url, json=payload)
        data = response.json()

        if response.status_code != 200:
            raise Exception(response.text)

        decoded = decode_id_token(data['id_token'])

        user = Tenant.objects.filter(email=decoded["email"]).first()
        if user:
            google_token = {**json.loads(user.google_token), **data}
            user.name = decoded["name"]
            user.email = decoded["email"]
            user.google_token = json.dumps(google_token)
            user.save()
        else:
            user = Tenant.objects.create(
                name=decoded["name"], email=decoded["email"], google_token=json.dumps(data))

        final_data = json.loads(user.google_token)
    except Exception as e:
        traceback.print_exc()
        error_code = 804
        error_text = f"Something went wrong!: {e}"
    finally:
        return return_response(final_data, error_code, error_text)


def decode_id_token(jwttoken):
    url = "https://www.googleapis.com/oauth2/v3/certs"
    client = jwt.PyJWKClient(url)
    pub_key = client.get_signing_key_from_jwt(jwttoken).key
    aud = jwt.decode(jwttoken, options={
                     "verify_signature": False})["aud"]
    return jwt.decode(jwttoken, pub_key, algorithms=["RS256"], audience=aud, options={"verify_exp": False})


def refresh_gc_token(refresh_token):
    url = "https://oauth2.googleapis.com/token"
    payload = {
        'client_id': os.getenv('GC_CLIENT_ID'),
        'client_secret': os.getenv('GC_CLIENT_SECRET'),
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(url, json=payload)
    data = response.json()

    if response.status_code == 200:
        resp = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers={
            'Authorization': f"Bearer {data['access_token']}"
        })
        if (resp.status_code == 200):
            existing_user = Tenant.objects.filter(
                email=resp.json()['email']).first()
            if not existing_user:
                raise Exception('User not found')
            existing_user.google_token = json.dumps(
                {**json.loads(existing_user.google_token), **data})
            existing_user.save()
        else:
            raise Exception('Failed to update user details')
    return response.status_code, data
