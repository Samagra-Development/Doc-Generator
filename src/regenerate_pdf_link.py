"""
Cron for regernating file url
"""
import os
import os.path
import calendar
import time
from db.app import DB, create_app
from db.models import PdfData, OutputTable
from utils.func import initialize_logger
from plugin.file_uploader.file_uploader import FileUploader

logging = initialize_logger()
# Get the logger specified in the file
logger = logging.getLogger(__name__)

app = create_app()
if __name__ == '__main__':
    #app.run(debug=True)
    while 1:
        with app.app_context():
            cur_time = calendar.timegm(time.gmtime())
            qms = PdfData.query.filter(PdfData.url_expires < cur_time,
                                       PdfData.long_doc_url != '').limit(1).all()
            if qms:
                try:
                    i = 0
                    results = []
                    for data in qms:
                        raw_data = data.raw_data
                        if all(raw_key in raw_data for raw_key in ("INSTANCEID", "FORMID")) and \
                                raw_data['INSTANCEID'] and raw_data['FORMID']:
                            logger.info(
                                "Regenerate pdf link Start - instance id %s - Form id %s",
                                raw_data['INSTANCEID'], raw_data['FORMID'])

                        doc_url = data.long_doc_url
                        #print(raw_data)
                        doc_id = doc_url.split('/')
                        file_id = doc_id[4]  # find file id from url here
                        file_id = file_id.split('?')
                        file_id = file_id[0]
                        print(file_id)
                        #file_id = '2ffcdec3-d77f-4073-8cc0-d70355769f42.pdf'
                        if ('UPLOADTO' in raw_data and raw_data['UPLOADTO']):
                            upload_to = raw_data['UPLOADTO']

                            if upload_to == 's3':
                                cdn_upload = FileUploader(raw_data['UPLOADTO'],
                                                          raw_data['ACCESSKEY'],
                                                          raw_data['SECRETKEY'])
                            else:
                                base_path = os.path.dirname(os.path.abspath(__file__))
                                cdn_upload = FileUploader(raw_data['UPLOADTO'],
                                                          base_path + '/plugin/google_doc_plugin/' +
                                                          raw_data[
                                                              'GOOGLE_APPLICATION_CREDENTIALS'])
                            resp = cdn_upload.get_object_url(raw_data['BUCKET'], file_id)
                            new_doc_url = resp[0]
                            new_expire_time = resp[1]
                            if new_doc_url:
                                data.long_doc_url = new_doc_url
                                data.url_expires = new_expire_time
                                results.append(data)

                        i += 1
                    if results:
                        DB.session.bulk_save_objects(results)
                        DB.session.commit()
                        if all(raw_key in raw_data for raw_key in ("INSTANCEID", "FORMID")) and \
                                raw_data['INSTANCEID'] and raw_data['FORMID']:
                            logger.info(
                                "Regenerate pdf link Start - instance id %s - Form id %s",
                                raw_data['INSTANCEID'], raw_data['FORMID'])

                        #break
                    #break
                except Exception as ex:
                    ERROR = "Unable to regenerate pdf"
                    logger.error(
                        "Error10 Regenerate pdf link %s ", ERROR)
                    logger.error("Exception occurred", exc_info=True)

            else:
                print('not found')
