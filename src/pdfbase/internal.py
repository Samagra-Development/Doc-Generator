import json
from queuelib import FifoDiskQueue
import os.path,threading
from interface import Interface
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from db.app import db,create_app,get_db
from db.models import pdfData, outputTable
from time import sleep

class PDFPlugin(Interface):

    # **FetchData.process() -> Dict  => Fetches "new" data from the database/server/websocket whatever and provides it in the form of dictionary, one PDF at a time.
    # **FetchMapping.process() -> Dict => Feches mapping and yeilds it in the form of dictionary
    # **BuildPDF.process() -> File => Function to build PDF and return a file
    # **UploadPDF.process(key, File) ->  => Fuction to save PDF
    # **RetrievePDF.process(key) -> File => Function to get the previously saved PDF from the key

    def fetch_data(self):
        pass

    def fetch_mapping(self,data):
        pass

    def build_PDF(self,raw_data,file_name):
        pass

    def upload_PDF(self,key, file):
        pass

    def retrieve_PDF(self, key):
        pass
    

class Config:

    def get_default_config(self):
        config = {"retries": 1, "max_concurrency": 2}
        return config

    def __init__(self, *, config=dict()):

        self.retries = config["retries"]
        self.max_concurrency = config["max_concurrency"]
class PDFBuilder:
    def __init__(self, *, plugin, config):
        try:
            PDFPlugin.verify(type(plugin))
            self._plugin = plugin
            self._config = Config(config=config)
            self._app = get_db()
        except:
            raise ValueError('Please provide a valid plugin. Needs to be an instance of PDFPlugin.')
    def insertOutputTable(self,rec_unique_id, rec_instance_id, rec_doc_url,
                      rec_raw_data, rec_tags, rec_doc_name, rec_pdf_version):
        error = None
        try:
            get_db()
            dataForOutputTable = outputTable(
                unique_id=rec_unique_id,
                instance_id=rec_instance_id,
                doc_url=rec_doc_url,
                raw_data=rec_raw_data,
                tags=rec_tags,
                doc_name=rec_doc_name,
                pdf_version=rec_pdf_version
                )
            db.session.add(dataForOutputTable)  # Adds new request record to database
            db.session.commit()  # Commits all changesgetConnection
            #db.session.flush()
        except:
            error = 'Values not inserted in output table'

        return error
        
    def process_queue(self,qm, i, results):
        error = None
        try:
            config = self._plugin.get_config()
            with self._app.app_context():
                tries = qm.tries
                tries += 1  # Incrementing the tries
                qm.tries = tries
                mapping_data = self._plugin.fetch_mapping(qm.raw_data)
                mappingError = mapping_data[1]

                if not mappingError:
                    qm.raw_data = mapping_data[0]
                    qm.step = 1
                    file_build = self._plugin.build_PDF(qm.raw_data,qm.instance_id)
                    fileName = file_build[0]
                    fileError = file_build[1]
                    
                                                                 
                    if not fileError:
                        qm.step = 2
                        qm.doc_name = file_build[0]
                        qm.doc_url = file_build[2]
                        fileDownloaded = self._plugin.upload_PDF(fileName,qm.doc_url)
                        fileName = fileDownloaded[0]
                        fileError = fileDownloaded[1]
                        if not fileError:
                            qm.step = 3
                            version = qm.pdf_version
                            version += 1
                            qm.pdf_version = version
                            qm.current_status = 'complete'
                            qm.task_completed = True
                            # Now moving the above data to the Output table
                            insertedToOutput = self.insertOutputTable(
                                qm.unique_id, qm.instance_id, qm.doc_url,
                                qm.raw_data, qm.tags,
                                qm.doc_name, qm.pdf_version)

                            if not insertedToOutput:
                                qm.error_encountered = ''
                            else:
                                qm.error_encountered = insertedToOutput
                                qm.task_completed = False
                        else:
                            qm.error_encountered = fileError
                    else:
                        qm.error_encountered = fileError       
                else:
                    qm.error_encountered = mappingError    
            
        except Exception as e:
            error = "Unable to process queue"

        return error,qm        
    def start_queue(self):
        while 1:
            results = []
            qms = pdfData.query.filter(pdfData.tries < self._config.retries, pdfData.task_completed == False).limit(self._config.max_concurrency).all()
            if not qms:
                print("Sleeping for 10 seconds")
                sleep(10)  # If no data is found in database sleep for 10 seconds
                
            else:
                try:
                    i = 0
                    for q in qms:
                        resp = self.process_queue(q, i, results)
                        results.append(resp[1])
                        i += 1
                    db.session.bulk_save_objects(results)
                    db.session.commit()
                    break

                except Exception as e:
                    print(e)
        
                       
        
    def save_pdf_data(self,final_data,tags):
        username = "Admin"
        unique_ids = []
        config = self._plugin.get_config()
        
        json_data = pdfData(
            raw_data=final_data,
            tags = tags,
            instance_id=uuid.uuid4())
        
        db.session.add(json_data)  # Adds new User record to database
        db.session.flush()  # Pushing the object to the database so that it gets assigned a unique id
        unique_ids.append(json_data.unique_id)
        db.session.commit()  # Commits all changes
        status = 'submitted'   
        return {"status": status, "uniqueId": unique_ids}    
    def run(self):
        print("Starting program")
        print("-" * 79)
        with self._app.app_context():
            self.start_queue()
                
        

        print("Program done")
        print()
    def dataDownload(self):
        print("Starting data download")
        print("-" * 79)
        with self._app.app_context():
            while 1:
                q = FifoDiskQueue(os.path.dirname(__file__)+'/../queuedata')
                data = q.pop()
                q.close()
                if not data:
                    print('sleep for 10')
                    sleep(10) 
                    #break
                else:
                    raw_data = json.loads(data.decode('utf-8'))
                    self.save_pdf_data(raw_data['reqd_data'],raw_data['tags'])
                    
    def start(self):
        threads = []
        t1 = threading.Thread(target=self.dataDownload) 
        t2 = threading.Thread(target=self.run)
        t1.start()
        t2.start()
        t1.join()
        t2.join() 
        '''error = self._plugin.fetch_data()
        if error:
            print("Error 5")'''            
        