"""
Cron for deleting file from google drive
"""
from db.app import DB, create_app
from db.models import PdfData
from utils.func import initialize_logger
from plugin.google_doc_plugin.external import GoogleDocsSheetsPlugin

logging = initialize_logger()
# Get the logger specified in the file
logger = logging.getLogger(__name__)

app = create_app()
if __name__ == '__main__':
    #app.run(debug=True)
    while 1:
        with app.app_context():
            qms = PdfData.query.filter(PdfData.step != 5,
                                       PdfData.long_doc_url != '').limit(1).all()
            print(qms)
            if qms:
                try:
                    i = 0
                    results = []
                    for data in qms:
                        obj = GoogleDocsSheetsPlugin()
                        raw_data = data.raw_data
                        if all(raw_key in raw_data for raw_key in ("INSTANCEID", "FORMID")) and \
                        raw_data['INSTANCEID'] and raw_data['FORMID']:
                            logger.info("Step7 Delete from drive Start "
                                        "- instance id %s - Form id %s",
                                        raw_data['INSTANCEID'], raw_data['FORMID'])
                        doc_url = data.doc_url
                        # print(raw_data)
                        doc_id = doc_url.split('/')
                        file_id = doc_id[5]  # find file id from url here
                        resp = obj.delete_file_drive_google_script(file_id)
                        error = resp[0]
                        success = resp[1]
                        print(error)
                        print(success)
                        if success:
                            data.step = 5
                            results.append(data)
                        i += 1
                    if results:
                        DB.session.bulk_save_objects(results)
                        DB.session.commit()
                        if all(raw_key in raw_data for raw_key in ("INSTANCEID", "FORMID")) and \
                        raw_data['INSTANCEID'] and raw_data['FORMID']:
                            logger.info("Step7 Delete from drive End - instance id %s - Form id %s",
                                        raw_data['INSTANCEID'], raw_data['FORMID'])
                        #break

                except Exception as ex:
                    ERROR = 'Unable to delete file from drive'
                    logger.error(
                        "Error9 Delete from drive %s ", ERROR)
                    logger.error("Exception occurred", exc_info=True)

            else:
                print('not found')
                break
