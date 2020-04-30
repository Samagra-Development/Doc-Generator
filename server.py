import random, string, json
from flask import Flask, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
from app.models import pdfData, outputTable
from utils import fetch_data
import uuid
app = create_app()


def checkToken(token):
    if token == app.config['SECRET_KEY']:
        val = True
    else:
        val = False
    return val


@app.route("/", methods=['GET'])
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


# DATA COLLECTION ROUTES
## Create generic routes for getting data

## Route for Shiksha saathi, ODK forms - Class *
@app.route("/shiksha-custom", methods=['POST'])
def getPdf():
    reqData = json.loads(json.dumps(request.json))  # Converting unicodes to str and then str to dict.
    match = checkToken(reqData['token'])
    if match is True:
        # Token authenticated
        formId = reqData[
            'formId']  # Getting the form ID to distinguish between various template documents and mapping sheets
        newReqData = reqData['data'][0]  # Getting the data : [{values}]
        instanceId = newReqData['instanceID']  # Getting the instance id for searching routes

        newReqData = json.loads(json.dumps(newReqData))  # Getting the new data
        userName = newReqData['User_Name']
        formSubmissionDate = newReqData[
            '*meta-submission-date*']  # Correcting the submission date and removing the time
        endIndex = formSubmissionDate.find(str('T'))
        formSubmissionDate = formSubmissionDate[:endIndex]
        newReqData['*meta-submission-date*'] = formSubmissionDate  # Saving the corrected date in the json

        if formId == 'BPO_V1':  # Form Name - For class 9th to 12th
            applicationId = 1111
            formName = 'Class 9th to 12th School Visit Form'
            varMappingID = '1zgC-FiO7SK9Rgu2ot9_7DT2KP4-MvWHTXa5ViOuwazI'
            docTemplateID = '1DaeAzQvyOIRdREWPdvqvmfBuXIyL93fcMEU_fu3_NoQ'
        elif formId == 'CHT_V1':  # Form Name - For class 1st to 5th
            applicationId = 1111
            formName = 'Class 1st to 5th CHT School Visit Form'
            varMappingID = '1aOt6jcLc9dkzFp-_PKUIiAd9t51QZmLK3fGBF0mhTqA'
            docTemplateID = '12e8qYx2iLLJta1TatS3plYloCZisJKwPiYDR5jI9M1U'
        elif formId == 'BRCC_V1':  # Form Name - For class 1st to 8th
            applicationId = 1111
            formName = 'Class 1st to 8th School Visit Form'
            varMappingID = '10i1JIwRuImncFJLkQapvBtD5ssWxdt0lm83AbzbYuFA'
            docTemplateID = '11FQHQIKMy6cSoO6VUfx1LfsGOSQlMtVwYojaZT7SWJc'

        myDict = {}

        for k, v in newReqData.items():
            if type(v) is dict:
                for k1, v1 in v.items():
                    if k1 == "url":
                        # correcting the URLs
                        baseUrl = 'http://aggregate.cttsamagra.xyz:8080/'
                        indexStart = 0  # Finding the substring
                        indexEnd = v1.find(
                            ":8080/") + 6  # Find the stopping point
                        newv1 = v1.replace(v1[indexStart:indexEnd], baseUrl)
                        myDict[k] = newv1
            elif type(v) is float:
                myDict[k] = str(v)
            else:
                if v is None:
                    v = "NO_TEXT_FOUND"

                myDict[k] = v

        # Calculate Udise from its database and then Calculate distance from udise
        calculated_distance = 'Not available'  # Calculate using udise
        myDict['calculated_distance'] = calculated_distance

        json_data = pdfData(
            reqd_data=myDict,
            var_mapping_id=varMappingID,
            doc_template_id=docTemplateID,
            form_id=formId,
            form_name= formName,
            instance_id=instanceId,
            user_name=userName,
            application_id=applicationId,
            form_submission_date=formSubmissionDate)
        db.session.add(json_data)  # Adds new User record to database
        db.session.flush()  # Pushing the object to the database so that it gets assigned a unique id
        uniqueId = json_data.unique_id
        db.session.commit()  # Commits all changes
        status = 'submitted'
    else:
        status = 'API Authentication Error'
        uniqueId = None

    return {"status": status, "uniqueId": uniqueId}


## Route for saksham samiksha
"""
Following ODK forms are related to this route:
1. Elem mentor visit elem_men_v1
2. Elem monitor visit elem_mon_v1
3. Sec mentor visit sec_men_v1
4. Sec monitor visit sec_mon_v1
5. Elem SSA visit elem_ssa_v1
6. Sec SSA visit sec_ssa_v1
7. SAT visit sat_v2
8. SLO visit slo_v2
"""


@app.route("/saksham-custom", methods=['POST'])
def getPdfForSaksham():
    reqData = json.loads(json.dumps(request.json))  # Converting unicodes to str and then str to dict.
    match = checkToken(reqData['token'])
    if match is True:
        # Token authenticated
        formId = reqData[
            'formId']  # Getting the form ID to distinguish between various template documents and mapping sheets
        newReqData = reqData['data'][0]  # Getting the data : [{values}]
        instanceId = newReqData['instanceID']  # Getting the instance id for searching routes

        newReqData = json.loads(json.dumps(newReqData))  # Getting the new data
        userName = newReqData['username']
        formSubmissionDate = newReqData[
            '*meta-submission-date*']  # Correcting the submission date and removing the time
        endIndex = formSubmissionDate.find(str('T'))
        formSubmissionDate = formSubmissionDate[:endIndex]
        newReqData['*meta-submission-date*'] = formSubmissionDate  # Saving the corrected date in the json

        if formId == 'elem_men_v1':  # Form Name - 1. Elem mentor visit
            applicationId = 1122
            varMappingID = '1cvhb6xW1Moijgl-wq7ZOfuSUtZL5toGtlqeZIzRW28w'
            docTemplateID = '1QDXNnv5OXuU_2GdQSeIo2up7UTylaw0plvGSzaVbf_0'
        elif formId == 'elem_mon_v1':  # Form Name - 2. Elem monitor visit
            applicationId = 1122
            varMappingID = '1n0AwfxdHXU4e7BVh8UWItvQAkk-3yUyEjrMkjB_2sPk'
            docTemplateID = '1A0LXT1U7R8KoCAjwQn8B5YFRynSx_jMDGDmXTzfh4kg'
        elif formId == 'sec_men_v1':  # Form Name - 3. Sec mentor visit
            applicationId = 1122
            varMappingID = '1h_u4BQ_0EieBB2yUy7ldvO5OschZdl-0upX0rJJHFcM'
            docTemplateID = '1jLZoob9SK53jzv9Wt5eOIQtLJoXnCtUEyAfVNHHqbOI'
        elif formId == 'sec_mon_v1':  # Form Name - 4. Sec monitor visit
            applicationId = 1122
            varMappingID = '1DBa3gOn_XdLEjyJbrhc98xTG38_5s0Fcyd1g34GHetk'
            docTemplateID = '1kJ5VFexaHLn6ZfQ1aY-3i9y9hFMWJBGnHnrH0F4dKSI'
        elif formId == 'elem_ssa_v1':  # Form Name - 5. Elem SSA visit 
            applicationId = 1122
            varMappingID = '1iuRO8-w2Ap6cNEcuKkG2bIizMLytDMmOO0Q3ljeTB9E'
            docTemplateID = '1cgg7XZmlfb-HY69ym3G6mJhFYXY-_MpYtKPLe8dry3w'
        elif formId == 'sec_ssa_v1':  # Form Name - 6. Sec SSA visit 
            applicationId = 1122
            varMappingID = '1x049J4fEAfL2qSARODzI9nA12ZCZdx5T4okO6OFd5Y0'
            docTemplateID = '1I9vPRsj7yjIdzi8J4OsHDH-PVS1ALyRsE0hXh3Udsxo'
        elif formId == 'sat_v2':  # Form Name - 7. SAT visit
            applicationId = 1122
            varMappingID = '1XSwzYfKxO6x2UApJlbslOkmtgw17fPfkc25Q0LGaims'
            docTemplateID = '1ar9JQfsPbzVxsQFafi7IgVZ_RDQNfjgCtofCmhSDdnI'
        elif formId == 'slo_v2':  # Form Name - SLO visit
            applicationId = 1122
            varMappingID = '11s_HPpjnX5QJ2tZvY7pClGu97CnfBF9LZfF_0uymRTw'
            docTemplateID = '17QRs-wRdWThpTn0UC00R1sm-l2PlxkuQsyUd-WKuneM'

        myDict = {}

        for k, v in newReqData.items():
            if type(v) is dict:
                for k1, v1 in v.items():
                    if k1 == "url":
                        # correcting the URLs
                        baseUrl = 'http://aggregate.cttsamagra.xyz:8080/'
                        indexStart = 0  # Finding the substring
                        indexEnd = v1.find(
                            ":8080/") + 6  # Find the stopping point
                        newv1 = v1.replace(v1[indexStart:indexEnd], baseUrl)
                        myDict[k] = newv1
            elif type(v) is float or type(v) is int:
                myDict[k] = str(v)
            elif type(v) is list:
                myDict[k] = str(v[0])  # Converting list to str
            else:
                if v is None:
                    v = "NO_TEXT_FOUND"

                myDict[k] = v

        # Calculate Udise from its database and then Calculate distance from udise
        calculated_distance = 'Not available'  # Calculate using udise
        myDict['calculated_distance'] = calculated_distance

        json_data = pdfData(
            reqd_data=myDict,
            var_mapping_id=varMappingID,
            doc_template_id=docTemplateID,
            form_id=formId,
            instance_id=instanceId,
            user_name=userName,
            application_id=applicationId,
            form_submission_date=formSubmissionDate)
        db.session.add(json_data)  # Adds new User record to database
        db.session.flush()  # Pushing the object to the database so that it gets assigned a unique id
        uniqueId = json_data.unique_id
        db.session.commit()  # Commits all changes
        status = 'submitted'
    else:
        status = 'API Authentication Error'
        uniqueId = None

    return {"status": status, "uniqueId": uniqueId}


## Route for Covid19
@app.route("/covid-custom", methods=['GET'])
def getPdfCOVID19():

    # Get data from Google Spreadsheets
    raw_data = fetch_data()[0]
    # Create a JSON from data.
    column_names = raw_data[0]
    final_data = []
    for data in raw_data[2:]:
        single_data = dict()
        counter = 0
        for col in column_names:
            single_data[col] = data[counter]
            counter += 1
        final_data.append(single_data)
    mapping_id = "1_iE1D8Pvsq7SQMMjHWhOhidGvkXENiluq01RXvb3n5g"
    doc_template_id = "1g7EvvBPsMi2kXyg0am-iRZ72DJNZNtyUrRwKieXhWn0"
    application_id = "Covid19"
    username = "Admin"
    unique_ids = []
    print(db)
    for data in final_data:
        json_data = pdfData(
            reqd_data=data,
            var_mapping_id=mapping_id,
            doc_template_id=doc_template_id,
            form_id=None,
            form_name= None,
            instance_id=uuid.uuid4(),
            user_name=username,
            application_id=application_id,
            form_submission_date=None)
        db.session.add(json_data)  # Adds new User record to database
        db.session.flush()  # Pushing the object to the database so that it gets assigned a unique id
        unique_ids.append(json_data.unique_id)
        db.session.commit()  # Commits all changes
        status = 'submitted'
    return {"status": status, "uniqueId": unique_ids}

# CHECK STATUS ROUTES
## Custom route for checking status on the basis of username and application id
@app.route("/checkstatus/apiv1/<username>/<applicationId>", methods=['GET'])
def shikshaSathiApp(username, applicationId):
    returnlist = []
    qry = outputTable.query.filter(outputTable.user_name == username,
                                   outputTable.application_id == applicationId).all()  # Query for fetching data
    if not qry:  # If nothing is found in query (Output table)
        queryQueueDb = pdfData.query.filter(pdfData.user_name == username,
                                            pdfData.application_id == applicationId).all()
        if not queryQueueDb:  # If nothing is found in query (Queue management table)
            thisrow = {
                "fileName": None,
                "udise": None,
                "url": None,
                "submissionDate": None,
                "applicationId": None,
                "formId": None,
                "formName": None,
                "status": "Not Found",
                "error": "No data found"
            }
            returnlist.append(thisrow)
        else:  # If data is found in query (Queue management table)
            for row in queryQueueDb:
                thisrow = {
                    "fileName": row.user_name,
                    "udise": row.udise,
                    "url": row.gcs_url,
                    "submissionDate": row.form_submission_date,
                    "applicationId": row.application_id,
                    "formId": row.form_id,
                    "formName": row.form_name,
                    "status": row.current_status,
                    "error": row.error_encountered
                }
                returnlist.append(thisrow)
    else:  # If data is found in query (Output table)
        for row in qry:
            thisrow = {
                "fileName": row.user_name,
                "udise": row.udise,
                "url": row.gcs_url,
                "submissionDate": row.form_submission_date,
                "applicationId": row.application_id,
                "formId": row.form_id,
                "formName": row.form_name,
                "status": "complete",
                "error": None
            }
            returnlist.append(thisrow)

    return jsonify(returnlist)


## Generic route for checking status on the basis of unique id
@app.route("/checkstatus/<uniqueId>", methods=['GET'])  # Generic route for getting the status using uinqueId
def checkStatusUsingUniqueId(uniqueId):
    returnlist = []
    qry = outputTable.query.filter(outputTable.unique_id == uniqueId).all()  # Query for fetching data
    # Query for fetching data
    if not qry:  # If nothing is found in query (Output table)
        queryQueueDb = pdfData.query.filter(pdfData.unique_id == uniqueId).all()
        if not queryQueueDb:  # If nothing is found in query (Queue management table)
            thisrow = {
                "fileName": None,
                "udise": None,
                "url": None,
                "submissionDate": None,
                "applicationId": None,
                "formId": None,
                "formName": None,
                "status": "Not Found",
                "error": "No data found"
            }
            returnlist.append(thisrow)
        else:  # If data is found in query (Queue management table)
            for row in queryQueueDb:
                thisrow = {
                    "fileName": row.user_name,
                    "udise": row.udise,
                    "url": row.gcs_url,
                    "submissionDate": row.form_submission_date,
                    "applicationId": row.application_id,
                    "formId": row.form_id,
                    "formName": row.form_name,
                    "status": row.current_status,
                    "error": row.error_encountered
                }
                returnlist.append(thisrow)
    else:  # If data is found in query (Output table)
        for row in qry:
            thisrow = {
                "fileName": row.user_name,
                "udise": row.udise,
                "url": row.gcs_url,
                "submissionDate": row.form_submission_date,
                "applicationId": row.application_id,
                "formId": row.form_id,
                "formName": row.form_name,
                "status": "complete",
                "error": None
            }
            returnlist.append(thisrow)

    return jsonify(returnlist)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)


# https://script.google.com/a/samagragovernance.in/macros/s/AKfycbz7NPxhAb-n2f-36KepyGxdpxnWzcak1OusVp5IGT3MjI1JC3t7/exec