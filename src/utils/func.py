import os.path
import logging
import logging.config
import requests
import urllib
import json
def initialize_logger():
    """

    :return: logger object
    """
    log_file = os.path.dirname(__file__) + '/../utils/log.conf'
    logging.config.fileConfig(fname=log_file, disable_existing_loggers=False)
    return logging

def send_whatsapp_msg(mobile, url, name):
    headers = {'Cache-Control': 'no-cache', 'Content-Type': 'application/x-www-form-urlencoded',
               'apikey': 'c2ed3ece4e7c40eac0af0e012866e090', 'cache-control': 'no-cache'}
    message = {"type":"text","text":"Your resume is here => "+url}
    message = urllib.parse.quote(json.dumps(message))
    print(message)
    params = 'channel=whatsapp&source=917834811114&destination='+'91'+str(mobile)
    params +='&message='+message+'&src.name='+name
    result = requests.request("POST", 'https://api.gupshup.io/sm/api/v1/msg', data=params, headers=headers)
    print(result)
    error = None
    if result.status_code != 200:
        error = 'Unable to send msg'
        print(result.__dict__)
    return error

def send_mail(email, url, name, file_name):
    data = {'EMAIL': email, 'SUBJECT': 'Resume'}
    data['SEND_CONFIGURATION_ID'] = 4
    attachments = []
    attachment = {"filename": file_name,"href": url}
    attachments.append(attachment)
    data['ATTACHMENTS'] = attachments
    print(data)
    resp = requests.post(
        'http://139.59.2.20:3000/api/templates/' + str(4) +
        '/send?access_token=42fdc4d67d5983700635ddb4ff99fdc0c3e6198b', json=data)
    print(resp)

def info_log(logger, msg, raw_data):
    if all(raw_key in raw_data for raw_key in ("INSTANCEID", "FORMID")) and \
            raw_data['INSTANCEID'] and raw_data['FORMID']:
        logger(
            "%s - instance id %s - Form id %s", msg,
            raw_data['INSTANCEID'], raw_data['FORMID'])
    else:
        logger(msg)