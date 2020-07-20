import os.path
import logging
import logging.config
import requests
import urllib
import json
from datetime import datetime

def initialize_logger():
    """

    :return: logger object
    """
    log_file = os.path.dirname(__file__) + '/../utils/log.conf'
    logging.config.fileConfig(fname=log_file, disable_existing_loggers=False)
    return logging

def send_whatsapp_msg(mobile, url, name, doc_url):
    headers = {'Cache-Control': 'no-cache', 'Content-Type': 'application/x-www-form-urlencoded',
               'apikey': '8e455564878b4ca2ccb7b37f13ef9bfa', 'cache-control': 'no-cache'}
    message = {"type":"text","text":"Dear Candidate, Based on information provided by you, we are sending you, your resume. Please find the document attached. => "+url+" \n Also find editable format document of your resume "+doc_url}
    '''message = {"type": "file",
               "caption": "Dear Candidate, Based on information provided by you, we are sending you, your resume. Please find the document attached. => ",
               "url": url,
               "filename":name}'''
    message = urllib.parse.quote(json.dumps(message))
    print(message)
    params = 'channel=whatsapp&source=917834811114&destination='+'91'+str(mobile)
    params +='&message='+message+'&src.name=SakshamHaryana'
    result = requests.request("POST", 'https://api.gupshup.io/sm/api/v1/msg', data=params, headers=headers)
    print(result.__dict__ )
    error = None
    if result.status_code != 200:
        error = 'Unable to send msg'
        print(result.__dict__)
    return error, result

def send_mail(email, url, custom_fields, file_name, template_id):
    data = {'EMAIL': email, 'SUBJECT': 'Resume'}
    data['SEND_CONFIGURATION_ID'] = 4
    if url:
        attachments = []
        attachment = {"filename": file_name,"href": url}
        attachments.append(attachment)
        #data['ATTACHMENTS'] = attachments

    data['TAGS'] = custom_fields
    print(data)
    resp = requests.post(
        'http://139.59.2.20:3000/api/templates/' + str(template_id) +
        '/send?access_token=42fdc4d67d5983700635ddb4ff99fdc0c3e6198b', json=data)
    print(resp.__dict__)
    error = None
    if resp.status_code != 200:
        error = 'Unable to send msg'

    return error, resp

def info_log(logger, msg, raw_data):
    if all(raw_key in raw_data for raw_key in ("INSTANCEID", "FORMID")) and \
            raw_data['INSTANCEID'] and raw_data['FORMID']:
        logger(
            "%s - instance id %s - Form id %s", msg,
            raw_data['INSTANCEID'], raw_data['FORMID'])
    else:
        logger(msg)

def print_log(msg, raw_data):
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if all(raw_key in raw_data for raw_key in ("INSTANCEID", "FORMID")) and \
            raw_data['INSTANCEID'] and raw_data['FORMID']:
        print(
            "{} - {} - instance id {} - Form id {}".format(dt_string, msg,
            raw_data['INSTANCEID'], raw_data['FORMID']))
    else:
        print("{} - {} ".format( dt_string, msg))

def call_healthcheck_url(url):
    resp = requests.get(url)
    print(resp.__dict__)
    error = None
    if resp.status_code != 200:
        error = 'Unable to call healthcheck'

    return error, resp
