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
            qms = PdfData.query.filter(PdfData.step != 4,
                                       PdfData.doc_name != '').limit(1).all()
            print(qms)
            if qms:
                try:
                    i = 0
                    results = []
                    for data in qms:
                        obj = GoogleDocsSheetsPlugin()
                        print(data.instance_id)
                        resp = obj.delete_file_drive_google_script(data.instance_id)
                        error = resp[0]
                        success = resp[1]
                        print(error)
                        print(success)
                        if success:
                            data.step = 4
                            results.append(data)
                        i += 1
                    if results:
                        DB.session.bulk_save_objects(results)
                        DB.session.commit()
                        break

                except Exception as ex:
                    logger.error("Exception occurred", exc_info=True)

            else:
                print('not found')
                break
