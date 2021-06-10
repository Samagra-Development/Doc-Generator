"""
Plugin for getting data from sheet and generate pdf from it
"""
import json
import os
import os.path
import calendar
import time
from datetime import datetime
from urllib.parse import urlencode
import gspread
from gspread.exceptions import SpreadsheetNotFound
import requests
from requests.auth import HTTPDigestAuth
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from interface import implements
from kafka import KafkaProducer
from pdfbase.internal import PDFPlugin
from pdfbase.config import KAFKA_CREDENTIAL
from plugin.file_uploader.file_uploader import FileUploader
from utils.func import initialize_logger, send_whatsapp_msg, info_log, send_mail
from confluent_kafka import Consumer, Producer
import traceback


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


# implement interface
class HTML(implements(PDFPlugin)):
    