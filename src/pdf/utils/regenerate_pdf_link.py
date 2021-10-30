"""
Cron for regernating file url
"""
import os
import os.path
import calendar
import time
from db.app import DB, create_app
from db.models import PdfData, OutputTable
from utils.func import initialize_logger, info_log, print_log
from plugin.file_uploader.file_uploader import FileUploader
from plugin.odk_plugin.external import ODKSheetsPlugin


logging = initialize_logger()
# Get the logger specified in the file
logger = logging.getLogger(__name__)

app = create_app()
if __name__ == '__main__':
    #app.run(debug=True)

    with app.app_context():
        cur_time = calendar.timegm(time.gmtime())
        qms = PdfData.query.filter(PdfData.url_expires < cur_time,
                                   PdfData.long_doc_url != '').all()
        if qms:
            try:
                i = 0
                results = []
                data = dict()
                for data in qms:
                    raw_data = data.raw_data
                    LOG_MSG = "Step15 Regenerate pdf link Start"
                    info_log(logger.info,
                             LOG_MSG,
                             data.raw_data)
                    print_log(LOG_MSG, data.raw_data)
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
                            LOG_MSG = "Step15.1 Short Url generation Start"
                            info_log(logger.info, LOG_MSG,
                                     data.raw_data)
                            print_log(LOG_MSG, data.raw_data)
                            obj = ODKSheetsPlugin()
                            obj.set_raw_data(data.raw_data)
                            short_url_resp = obj.shorten_url(data.long_doc_url)
                            short_url = short_url_resp[0]
                            error = short_url_resp[1]
                            if error:
                                data.error_encountered = error
                            else:
                                data.doc_name = short_url
                                data.step = 4
                                output_qms = OutputTable.query.filter(
                                    OutputTable.instance_id == data.instance_id).all()
                                output_results = []
                                if output_qms:
                                    LOG_MSG = "Step15.2 Short Url generation Save " \
                                              "in output table Start"
                                    info_log(logger.info, LOG_MSG,
                                             data.raw_data)
                                    print_log(LOG_MSG, data.raw_data)
                                    for output_data in output_qms:
                                        output_data.doc_name = data.doc_name
                                        output_results.append(output_data)
                                    if output_results:
                                        DB.session.bulk_save_objects(output_results)
                                        DB.session.commit()
                                        LOG_MSG = "Step15.2 Short Url generation Save " \
                                                  "in output table End"
                                        info_log(logger.info,
                                                 LOG_MSG,
                                                 data.raw_data)
                                        print_log(LOG_MSG, data.raw_data)
                                else:
                                    LOG_MSG = "Error15 Not found in output table " \
                                              "on link regenration"
                                    info_log(logger.error, LOG_MSG,
                                             data.raw_data)
                                    print_log(LOG_MSG, data.raw_data)
                            results.append(data)
                            LOG_MSG = "Step15.1 Short Url generation End"
                            info_log(logger.info, LOG_MSG,
                                     data.raw_data)
                            print_log(LOG_MSG, data.raw_data)
                    i += 1
                    if i%10 == 0:
                        if results:
                            DB.session.bulk_save_objects(results)
                            DB.session.commit()
                            LOG_MSG = "Step15 Regenerate pdf link End"
                            info_log(logger.info,
                                     LOG_MSG,
                                     data.raw_data)
                            print_log(LOG_MSG, data.raw_data)

                        results = []
                if results:
                    DB.session.bulk_save_objects(results)
                    DB.session.commit()
                    LOG_MSG = "Step15 Regenerate pdf link End"
                    info_log(logger.info,
                             LOG_MSG,
                             data.raw_data)
                    print_log(LOG_MSG, data.raw_data)
                    #break
                #break
            except Exception as ex:
                ERROR = "Unable to regenerate pdf"
                logger.error(
                    "Error10 Regenerate pdf link %s ", ERROR)
                print("Error10 Regenerate pdf link %s ", ERROR)
                logger.error("Exception occurred", exc_info=True)

        else:
            LOG_MSG = "Not found in regenerate pdf link"
            print_log(LOG_MSG, '')
            #print('not found')
