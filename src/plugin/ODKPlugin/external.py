import random, string, json
from flask import request
import os.path,pickle
import uuid
from plugin.GoogleDocPlugin.external import GoogleDocsSheetsPlugin
import requests
from queuelib import FifoDiskQueue

# implement interface

class ODKSheetsPlugin(GoogleDocsSheetsPlugin):

    def __init__(self):
        #get googledoc-config.json file content and then save this dtaa to class config variable
        with open(os.path.dirname(__file__) + '/config.json') as json_file: 
            config = json.load(json_file) 
            self.config = config
    

    # this method return all the tags on the basis of which we filter the request    
    def get_tags(self):

        tags = dict()
        tags["SHEETID"] = self.config["SHEETID"]
        tags["MAPPINGDETAILS"] = self.config["MAPPINGDETAILS"]
        tags["OPTIONSSHEET"] = self.config["OPTIONSSHEET"]
        tags["DOCTEMPLATEID"] = self.config["DOCTEMPLATEID"]
        tags["APPLICATIONID"] = self.config["APPLICATIONID"]
        if self.raw_data:
            tags["FORMID"] = self.raw_data["FORMID"]
            tags["USERNAME"] = self.raw_data["USERNAME"]
            tags["FORMSUBMISSIONDATE"] = self.raw_data["FORMSUBMISSIONDATE"]
            tags["INSTANCEID"] = self.raw_data["INSTANCEID"]
        return tags        
    #this method fetches the data from google sheet and return it as raw_data and also send tag    
    def fetch_data(self):
        error = None
        tags = None
        try:
            reqData = json.loads(json.dumps(request.json))  # Converting unicodes to str and then str to dict.
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
            all_data = dict()
            all_data['req_data'] = myDict
            all_data['FORMID'] = formId
            all_data['INSTANCEID'] = instanceId
            all_data['USERNAME'] = userName
            all_data['FORMSUBMISSIONDATE'] = formSubmissionDate
            self.raw_data = all_data
            tags = self.get_tags()
            all_data.update(self.config)
            raw_data = dict()
            raw_data['reqd_data'] = all_data
            raw_data['tags'] = tags
            
            q = FifoDiskQueue(os.path.dirname(__file__)+'/../../queuedata')
            q.push(json.dumps(raw_data).encode('utf-8'))
            q.close()
            
        except Exception as e:
            import traceback
            error = "Failed to fetch mapping detials"
            

        return error 
