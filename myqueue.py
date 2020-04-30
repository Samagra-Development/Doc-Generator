import os, threading
from time import sleep
import pickle, os.path
import random, string, json
import urllib.request, urllib
from urllib.request import urlopen
from urllib.parse import urlencode, quote_plus
import requests
from requests.auth import HTTPDigestAuth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.cloud import storage
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update, create_engine
from app import db, create_app
from app.models import pdfData, outputTable

app = create_app()
app.app_context().push()

# These are the scopes for accessing spreadsheets. If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive'
]

##########################################################
#                                                        #
#             Project functions start here               #
#                                                        #
##########################################################


def random_name(leng, ntype):
    gen_name = ''.join(
        random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
        for _ in range(leng)) + ntype
    return gen_name


def getSessionCookie():
    error = cookie = None
    r = requests.get(
        app.config['SESSIONCOOKIEBASEURL'],
        auth=HTTPDigestAuth(app.config['ODKUSERNAME'],
                            app.config['ODKPASSWORD']),
        timeout=10)  # Sending the digest authorization request
    headers = str(r.headers)

    if r.status_code == 200:  # Check if request is OK
        startIndex = headers.find('JSESSIONID=')
        endIndex = headers.find(';')
        sessionCookie = headers[
            startIndex + 11:
            endIndex]  # Getting the value of json cookie from the string
        if len(sessionCookie) == 32:  # Making sure got the cookie value right
            cookie = sessionCookie  # Saving the cookie value
        else:
            error = "No session cookie found"
    else:
        error = "Authorization error"

    return error, cookie


def fetchMapping(sheetID, varMapping):
    error = None
    print(sheetID, varMapping)
    try:
        SAMPLE_SPREADSHEET_ID = sheetID
        SAMPLE_RANGE_NAME = varMapping

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('instance/token.pickle'):
            with open('instance/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'instance/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('instance/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            error = "No Mapping details found"
        else:
            mappingValues = values
    except Exception as e:
        error = "Failed to fetch mapping detials"
        mappingValues = None

    return mappingValues, error


def mapData(allData, mappingValues, optionsMapping, templateId):
    mappingValues.pop(0)  # removing the header row of mapping sheet
    optionsMapping.pop(0)  # removing the header row of options sheet
    error = None
    urlgas = ''
    try:
        finalData = []  # List to hold the final values
        for row in mappingValues:
            if row[1] == 'options':
                # row[2] option value name
                # str(allData[row[2]]) option value a,b,c,d
                # optionsMapping[] the list with valuename and options value
                thisList = ''.join(
                    str(e) for e in optionsMapping)  # Converted list to string
                newList = thisList.split(str(
                    row[2]), 1)[1]  # List split to start with required string
                indexStart = newList.find(str(row[2]))  # Finding the substring
                indexEnd = newList.find("]")  # Find the stopping point
                strToCheck = newList[:
                                     indexEnd]  # The semi final string to find values from obtained
                optionValueStart = strToCheck.find(str(allData[row[2]]))
                if optionValueStart is -1:
                    allData[row[
                        2]] = 'NO_TEXT_FOUND'  # If the particular option is not found
                    finalData.append(allData[row[2]])  # Appending the received data to the final list
                else:
                    length = len(allData[row[2]])
                    optionValueEnd = strToCheck.find("'", optionValueStart)
                    optionValue = strToCheck[optionValueStart + length + 2:
                                             optionValueEnd]
                    finalData.append(
                        optionValue
                    )  # Appending the correct option to the final list
            else:
                if not allData[row[2]]:
                    allData[row[2]] = 'NO_TEXT_FOUND'  # If data is None

                finalData.append(allData[row[
                    2]])  # Appending the received data to the final list

        fileName = random_name(8,'') + random_name(8,'')  # Name of the file for Google Drive

        callSessionCookie = getSessionCookie()

        if not callSessionCookie[0]:
            sessionCookie = callSessionCookie[1]
        else:
            error = callSessionCookie[0]

        # URL of google app script
        finalDataStr = json.dumps(finalData)
        payload = {
            "fileName": fileName,
            "mylist": finalDataStr,
            "templateId": templateId,
            "sessionCookie": sessionCookie,
            "username": app.config['ODKUSERNAME'],
            "password": app.config['ODKPASSWORD']
        }  # Encoding the url with payload

        urlgas = app.config['URL'] + urlencode(payload)
    except Exception as e:
        error = "Mapping error"

    return urlgas, error


def generateFileDrive(url):
    asUrl = url
    error = documentId = fileName = pdfUrl = None
    try:
        # contents = urlopen(url, timeout=60).read()
        contents = requests.get(url, timeout=60).json()
        if contents.get("error") != "null":
            error = contents.get('error')
        print("Herer 0101", error)
        if error=="undefined":
            error = None
        documentId = contents.get("documentId")
        fileName = contents.get("fileName")
        pdfUrl = contents.get("url")
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        error = "Failed to get response from App Script"

    return documentId, fileName, pdfUrl, error


def downloadPdf(fileName, thisUrl, dirpath):
    error = None
    try:
        response = requests.get(thisUrl)
        print(dirpath + fileName)
        with open(dirpath + fileName, 'wb') as f:
            f.write(response.content)
        # downloadPdfFile = urllib.request.urlretrieve(thisUrl,
        #                                              dirpath + fileName)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        error = "Failed to download file from drive"
    return fileName, error


def upload(bucket_name, source_file_name):
    # Uploads a file to the bucket.
    fileName = app.config['DIRPATH'] + source_file_name
    error = None
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(source_file_name)  # giving input the full file name
        blob.upload_from_filename(fileName)
        os.remove(fileName)
    except Exception as e:
        error = 'File not uploaded'
        print(e)

    return error


def deleteFileDrive(file_url):
    # Google drive API to Permanently delete a file, skipping the trash.
    error = done = None
    try:
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('instance/token.pickle'):
            with open('instance/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'instance/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('instance/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)
        doc_id = file_url.split('/')
        file_id = doc_id[5]  # find file id from url here
        service.files().delete(fileId=file_id).execute()
        done = True
    except:
        error = 'Failed to delete file'

    return error, done


def getConnection():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    connection = engine.connect()
    print(connection)
    return connection


def insertOutputTable(rec_unique_id, rec_instance_id, rec_g_doc_url,
                      rec_gcs_url, rec_var_mapping_id, rec_user_name,
                      rec_application_id, rec_doc_template_id, rec_form_id,
                      rec_req_received, rec_google_doc_name, rec_pdf_version,
                      rec_gas_url, rec_udise, rec_form_submission_date, cacheCleaned):
    error = None
    try:
        dataForOutputTable = outputTable(
            unique_id=rec_unique_id,
            instance_id=rec_instance_id,
            g_doc_url=rec_g_doc_url,
            gcs_url=rec_gcs_url,
            var_mapping_id=rec_var_mapping_id,
            user_name=rec_user_name,
            application_id=rec_application_id,
            doc_template_id=rec_doc_template_id,
            form_id=rec_form_id,
            req_received=rec_req_received,
            google_doc_name=rec_google_doc_name,
            pdf_version=rec_pdf_version,
            gas_url=rec_gas_url,
            udise=rec_udise,
            form_submission_date=rec_form_submission_date,
            cache_cleaned = cacheCleaned)
        db.session.add(dataForOutputTable)  # Adds new request record to database
        db.session.commit()  # Commits all changes
        #db.session.flush()
    except:
        error = 'Values not inserted in output table'

    return error


def processQueue(qm, i, results):
    error = None
    try:
        with app.app_context():
            tries = qm.tries
            tries += 1  # Incrementing the tries
            qm.tries = tries
            getValueMapping = fetchMapping(qm.var_mapping_id,
                                                       app.config['MAPPINGDETAILS'])
            mappingError = getValueMapping[1]  # Error in fetching mapping
            mappingValues = getValueMapping[0]  # mapping values list
            getOptionsMapping = fetchMapping(qm.var_mapping_id,
                                                         app.config['OPTIONSSHEET'])
            optionsError = getOptionsMapping[1]  # Error in fetching options
            mappingOptions = getOptionsMapping[0]  # options mapping list

            if not mappingError and not optionsError:
                qm.mapping_fetched = True
                gasUrl = mapData(qm.reqd_data, mappingValues, mappingOptions,
                                    qm.doc_template_id)
                mappingErrorGas = gasUrl[1]

                if not mappingErrorGas:
                    qm.var_mapped = True
                    qm.gas_url_gen = True
                    qm.gas_url = gasUrl[0]
                    appScriptResponse = generateFileDrive(gasUrl[
                        0])  # Calling the GAS url and Getting the GAS response
                    asError = appScriptResponse[3]
                    print(appScriptResponse)
                    print(asError)

                    if not asError:
                        qm.gas_url_call = True
                        qm.google_doc_name = appScriptResponse[1]
                        qm.g_doc_url = appScriptResponse[2]
                        pdfUrl = appScriptResponse[2]
                        fileName = appScriptResponse[1] + '.pdf'
                        fileDownloaded = downloadPdf(
                            fileName, pdfUrl,
                            app.config['DIRPATH'])  # Downloading pdf
                        fileName = fileDownloaded[0]
                        fileError = fileDownloaded[1]

                        if not fileError:
                            qm.pdf_downloaded = True
                            uploadToGcs = upload(app.config['BUCKET'],fileName)  # Uploading file to GCS

                            if not uploadToGcs:
                                qm.pdf_uploaded = True
                                version = qm.pdf_version
                                version += 1
                                qm.pdf_version = version
                                qm.gcs_url = app.config['GOOGLECLOUDBASEURL'] + fileName
                                qm.current_status = 'complete'
                                qm.task_completed = True
                                deleteError = deleteFileDrive(pdfUrl)
                                if not deleteError[0]:
                                    cacheCleaned = True
                                else:
                                    cacheCleaned = False
                                # Now moving the above data to the Output table
                                insertedToOutput = insertOutputTable(
                                    qm.unique_id, qm.instance_id, qm.g_doc_url,
                                    qm.gcs_url, qm.var_mapping_id, qm.user_name,
                                    qm.application_id, qm.doc_template_id,
                                    qm.form_id, qm.req_received,
                                    qm.google_doc_name, qm.pdf_version,
                                    qm.gas_url, qm.udise,
                                    qm.form_submission_date, cacheCleaned)

                                if not insertedToOutput:
                                    qm.error_encountered = ''
                                else:
                                    qm.error_encountered = insertedToOutput
                                    qm.task_completed = False
                            else:
                                print("Error 1")
                                qm.error_encountered = 'Uploading to GCS failed'
                        else:
                            print("Error 2")
                            qm.error_encountered = fileError
                    else:
                        print("Error 3")
                        qm.error_encountered = asError
                else:
                    print("Error 4")
                    qm.error_encountered = mappingErrorGas
            else:
                print("Error 5")
                print(mappingError)
                print(optionsError)
                qm.error_encountered = str(mappingError) + str(optionsError)

        results[i] = qm

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(e)

    return error



##########################################################
#                                                        #
#               Main project flow starts                 #
#                                                        #
##########################################################

# Running this forever, but if no data is found in the database then sleep for 10 seconds and then recheck in the database

while 1:
    # Getting n (concurrency) rows from the database
    concurrency = 1
    results = [None] * concurrency
    qms = pdfData.query.filter(pdfData.tries < 500, pdfData.task_completed == False).limit(concurrency).all()
    print("unique_id values for processing - ",qms)

    if not qms:
        print("Sleeping for 10 seconds")
        sleep(10)  # If no data is found in database sleep for 10 seconds
    else:
        try:
            threads = []
            i = 0
            for qm in qms:
                processQueue(qm, i, results)
            #     threads.append(
            #         threading.Thread(
            #             target=processQueue, args=(
            #                 qm, i, results
            #             )))
            #     i += 1
            # for thread in threads:
            #     thread.start()
            # for thread in threads:
            #     thread.join()  # can also do thread.join(60) i.e. waiting for 60 seconds until process finishes.
            db.session.bulk_save_objects(results)
            db.session.commit()
            break

        except Exception as e:
            print(e)
