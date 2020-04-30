import random, string, json
import os.path,pickle
import uuid
from pdfbase.internal import PDFPlugin
from interface import implements
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.cloud import storage
import requests
from requests.auth import HTTPDigestAuth
from urllib.parse import urlencode
from queuelib import FifoDiskQueue

# implement interface

class GoogleDocsSheetsPlugin(implements(PDFPlugin)):

    def __init__(self):
        #get googledoc-config.json file content and then save this dtaa to class config variable
        with open(os.path.dirname(__file__) + '/googledoc-config.json') as json_file: 
            config = json.load(json_file) 
            self.config = config
    
    def get_token(self):
        creds = None
        SCOPES = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive'
            ]
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.dirname(__file__) + '/token.pickle'):
            with open(os.path.dirname(__file__) + '/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.dirname(__file__)+'/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(os.path.dirname(__file__) + '/token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds
    def getSessionCookie(self):
        error = cookie = None
        r = requests.get(
            self.raw_data['SESSIONCOOKIEBASEURL'],
            auth=HTTPDigestAuth(self.raw_data['ODKUSERNAME'],
                                self.raw_data['ODKPASSWORD']),
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
    
    def get_sheetvalues(self,sheetID, varMapping):
        error = None
        try:
            SPREADSHEET_ID = sheetID
            RANGE_NAME = varMapping
            # call the class get_token method to access google sheet
            creds = self.get_token()
            
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            #get the sheet data
            result = sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME).execute()
            values = result.get('values', [])

            if not values:
                error = "No Mapping details found"
            else:
                mappingValues = values
        except Exception as e:
            error = "Failed to fetch mapping detials"
            mappingValues = None

        return mappingValues, error    

    # this method return all the tags on the basis of which we filter the request    
    def get_tags(self):
        tags = dict()
        tags["SHEETID"] = self.config["SHEETID"]
        tags["SHEETNAME"] = self.config["SHEETNAME"]
        tags["RANGE"] = self.config["RANGE"]
        tags["MAPPINGDETAILS"] = self.config["MAPPINGDETAILS"]
        tags["OPTIONSSHEET"] = self.config["OPTIONSSHEET"]
        tags["DOCTEMPLATEID"] = self.config["DOCTEMPLATEID"]
        tags["APPLICATIONID"] = self.config["APPLICATIONID"]
        return tags        
    #this method fetches the data from google sheet and return it as raw_data and also send tag    
    def fetch_data(self):
        error = None
        tags = None
        try:
            if self.config['RANGE']:
                RANGE_NAME = self.config['SHEETNAME'] + "!" + self.config['RANGE']
            else :
                RANGE_NAME = self.config['SHEETNAME'] 
            #call class method which return sheet data and error if permission is not there    
            getValueMapping = self.get_sheetvalues(self.config['SHEETID'],RANGE_NAME)
            
            mappingError = getValueMapping[1]  # Error in fetching mapping
            mappingValues = getValueMapping[0]  # mapping values list
            if not mappingError:
                raw_data = mappingValues
                # Create a JSON from data.
                column_names = raw_data[0]
                final_data = []
                for data in raw_data[2:]:
                    single_data = dict()
                    counter = 0
                    for col in column_names:
                        single_data[col] = data[counter]
                        counter += 1
                    tags = self.get_tags()
                    all_data = dict()
                    all_data['req_data'] = single_data
                    all_data.update(self.config) # merge tags with sheet each row data
                    #final_data.append(raw_data)
                    raw_data = dict()
                    raw_data['reqd_data'] = all_data
                    raw_data['tags'] = tags
                    q = FifoDiskQueue(os.path.dirname(__file__)+'/../../queuedata')
                    q.push(json.dumps(raw_data).encode('utf-8'))
                    q.close()
                

            else:
                error = "No Mapping details found"
            
        except Exception as e:
            import traceback
            error = "Failed to fetch mapping detials"
            mappingValues = None

        return error

    def fetch_mapping(self,data):
        error = None
        rawData = None
        try:
            getValueMapping = self.get_sheetvalues(data['SHEETID'],data['MAPPINGDETAILS'])
            mappingError = getValueMapping[1]  # Error in fetching mapping
            mappingValues = getValueMapping[0]  # mapping values list
            getOptionsMapping = self.get_sheetvalues(data['SHEETID'],
                                                         data['OPTIONSSHEET'])
            optionsError = getOptionsMapping[1]  # Error in fetching options
            optionsMapping = getOptionsMapping[0]  # options mapping list

            if not mappingError and not optionsError:
               rawData = dict()
               rawData['value_mapping'] = mappingValues
               rawData['options_mapping'] = optionsMapping 
               data.update(rawData)
               rawData = data
               self.raw_data = rawData
            else:
                error = str(mappingError) + str(optionsError) 
                
            
        except Exception as e:
            error = "Failed to fetch mapping detials"
            print(e)

        return rawData, error
    def mapData(self,allData, mappingValues, optionsMapping):
        error = None
        finalData = None
        try:
            mappingValues.pop(0)  # removing the header row of mapping sheet
                    
            finalData = []  # List to hold the final values
            optionsMapping.pop(0)  # removing the header row of options sheet
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
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            error = "Failed to map data"  
        return finalData,error          
                
    def get_config(self):
        return self.config 

    def generateFileDrive(self,url):
        asUrl = url
        error = documentId = fileName = pdfUrl = None
        try:
            #call the app script url
            contents = requests.get(url, timeout=60).json()
            if contents.get("error") != "null":
                error = contents.get('error')
            if error=="undefined":
                error = None
            documentId = contents.get("documentId")
            fileName = contents.get("fileName")
            pdfUrl = contents.get("url")
        except Exception as e:
            import traceback
            error = "Failed to get response from App Script"

        return documentId, fileName, pdfUrl, error

    def build_PDF(self,raw_data,file_name):
        error = None
        fileDownloaded = ''
        fileName=''
        pdfUrl=''
        try:
            data = raw_data['req_data']
            mappingValues = raw_data['value_mapping']
            optionsMapping = raw_data['options_mapping']
            mappedData = self.mapData(data, mappingValues, optionsMapping)
            mappingError = mappedData[1]
            finalData = mappedData[0]
            if not mappingError:
                # URL of google app script
                finalDataStr = json.dumps(finalData)
                payload = {
                    "fileName": file_name,
                    "mylist": finalDataStr,
                    "templateId": raw_data['DOCTEMPLATEID']
                    
                }  # Encoding the url with payload
                if('ODKUSERNAME' in self.raw_data.keys() and self.raw_data['ODKUSERNAME'] and 'ODKPASSWORD' in self.raw_data.keys() and self.raw_data['ODKPASSWORD']):
                    callSessionCookie = self.getSessionCookie()

                    if not callSessionCookie[0]:
                        sessionCookie = callSessionCookie[1]
                    else:
                        error = callSessionCookie[0] 
                    payload['sessionCookie'] =  sessionCookie
                    payload['username'] =  self.raw_data['ODKUSERNAME']
                    payload['password'] =  self.raw_data['ODKPASSWORD']                              
                
                gasUrl = self.config['URL'] + urlencode(payload)

                appScriptResponse = self.generateFileDrive(gasUrl)  # Calling the GAS url and Getting the GAS response
                error = appScriptResponse[3]
                
                if not error:
                    google_doc_name = appScriptResponse[1]
                    pdfUrl = appScriptResponse[2]
                    fileName = appScriptResponse[1] + '.pdf'
                              
                
            else:
                error = mappingError        
                
                
        except Exception as e:
            error = "Failed to generate pdf"
            print(e)
            import traceback
            print(traceback.format_exc())

        return fileName,error,pdfUrl                    
                
    def upload_PDF(self, key,file):
        # Uploads a file to the local server.
        error = ''
        try:
            response = requests.get(file)
            with open(self.config['DIRPATH']+key, 'wb') as f:
                f.write(response.content)
            self.delete_file_drive(file)
        except Exception as e:
            import traceback
            error = "Failed to download file from drive"

        return key,error              
        

    def retrieve_PDF(self, key):
        filedata = ''
        error = None
        file_name = self.config['DIRPATH'] + key+'.pdf'
        try:
            with open(file_name, 'rb') as f:
                filedata = f.read()
        except Exception as e:
            error = 'File not found'
            
        return filedata,error    
        

    def delete_file_drive(self,file):
        # Google drive API to Permanently delete a file, skipping the trash.
        error = done = None
        try:
            creds = None
            creds = self.get_token()
            service = build('drive', 'v3', credentials=creds)
            doc_id = file.split('/')
            file_id = doc_id[5]  # find file id from url here
            service.files().delete(fileId=file_id).execute()
            done = True
        except:
            error = 'Failed to delete file'

        return error, done    