"""
Cron for deleting file from google drive
"""
from db.app import DB, create_app
from db.models import PdfData
from utils.func import initialize_logger, info_log, print_log
from plugin.google_doc_plugin.external import GoogleDocsSheetsPlugin


logging = initialize_logger()
# Get the logger specified in the file
logger = logging.getLogger(__name__)

app = create_app()
if __name__ == '__main__':
    #app.run(debug=True)

    with app.app_context():
        qms = PdfData.query.filter(PdfData.step != 5,
                                   PdfData.long_doc_url != '', PdfData.is_delete == True).all()
        print(qms)
        if qms:
            try:
                i = 0
                results = []
                data = dict()
                for data in qms:
                    obj = GoogleDocsSheetsPlugin()
                    raw_data = data.raw_data
                    LOG_MSG = "Step7 Delete from drive Start"
                    info_log(logger.info,
                             LOG_MSG,
                             data.raw_data)
                    print_log(LOG_MSG, data.raw_data)
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
                    else:
                        LOG_MSG = "Error in deleting file from drive "
                        print_log(LOG_MSG, data.raw_data)
                        LOG_MSG = error
                        print_log(LOG_MSG, data.raw_data)
                    if i % 10 == 0:
                        if results:
                            DB.session.bulk_save_objects(results)
                            DB.session.commit()
                            LOG_MSG = "Step7 Delete from drive End"
                            info_log(logger.info,
                                     LOG_MSG,
                                     data.raw_data)
                            print_log(LOG_MSG, data.raw_data)

                        results = []
                    i += 1
                    #break
                if results:
                    DB.session.bulk_save_objects(results)
                    DB.session.commit()
                    LOG_MSG = "Step7 Delete from drive End"
                    info_log(logger.info,
                             LOG_MSG,
                             data.raw_data)
                    print_log(LOG_MSG, data.raw_data)

            except Exception as ex:
                ERROR = 'Unable to delete file from drive'
                logger.error(
                    "Error9 Delete from drive %s ", ERROR)
                print("Error9 Delete from drive %s ", ERROR)
                logger.error("Exception occurred", exc_info=True)

        else:
            print('not found in delete file from drive')
