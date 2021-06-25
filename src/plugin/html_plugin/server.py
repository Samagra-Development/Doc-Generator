"""
Make a endpoint where we continuously receive request from another server
"""

import json
from flask import request
from utils.func import initialize_logger
from db.app import create_app, DB
from db.models import BackupPdfData
from .external import HTMLPlugin
import traceback
import pdfkit

app = create_app()


## Route for saksham samiksha
"""
Following ODK forms are related to this route:
1. Elem mentor visit elem_meo_v1
"""
@app.route("/", methods=['POST'])
def index():
    """
    check server running
    :return:
    """
    return {'status':'OK'}

@app.route("/html-custom", methods=['POST'])
def generate_pdf():
    """
    receive request from another server and save it in queue
    """
    convert_to_pdf()
    # try:
    #     logging = initialize_logger()
    #     # Get the logger specified in the file
    #     logger = logging.getLogger(__name__)
    #     logger.info("Request received")
    #     req_data = json.loads(json.dumps(request.json))
    #     new_req_data = req_data['data'][0]  # Getting the data : [{values}]
    #     instance_id = new_req_data['instanceID']  # Getting the instance id for searching routes

    #     unique_ids = []
    #     json_data = BackupPdfData(
    #         raw_data=req_data,
    #         link_id=instance_id
    #     )
    #     DB.session.add(json_data)  # Adds new User record to database
    #     DB.session.flush()  # Pushing the object to the database so that it gets assigned a unique id
    #     unique_ids.append(json_data.unique_id)
    #     DB.session.commit()  # Commits all changes
    #     obj = HTMLPlugin()
    #     error = obj.fetch_data()
    #     if not error:
    #         status = 'done'
    #     else:
    #         status = error
    #     return {'status':status}
    # except Exception as e:
    #     print(traceback.format_exc())

@app.route("/gdoc-template-to-html", methods=['POST'])
def generate_html_template():
    """
    Converts Google Doc to HTML Template and Stores Template on GCS
    """
    req_data = json.loads(json.dumps(request.json))
    gdoc_url = req_data["form_url"]
    form_id = req_data["formId"]

# https://script.google.com/a/samagragovernance.in/macros/s/AKfycbz7NPxhAb-n2f-36KepyGxdpxnWzcak1OusVp5IGT3MjI1JC3t7/exec

@app.route("/make-pdf", methods=['POST'])
def convert_to_pdf(htmltext=""):
    obj = HTMLPlugin()
    req_data = json.loads(json.dumps(request.json))
    raw_data, error = obj.fetch_data(req_data=req_data)
    print(json.dumps(raw_data, indent=4))
    # raw_data['reqd_data'], raw_data['tags'],raw_data['instance_id']
    obj.build_pdf(raw_data['reqd_data'], raw_data['instance_id'])
   
    if not error:
        # obj.publish_message(raw_data)
        status = 'done'
    else:
        status = error
    # with open('/Users/pritamps/Downloads/af_elem_mon_v1.html') as f:
    #     data = f.read()
        
    #     # pdfkit.from_file(f, 'out.pdf')
    return {"status": status}, 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


