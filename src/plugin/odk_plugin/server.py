"""
Make a endpoint where we continuously receive request from another server
"""

import json
from flask import request
from utils.func import initialize_logger
from db.app import create_app, DB
from db.models import BackupPdfData
from .external import ODKSheetsPlugin


app = create_app()


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
@app.route("/", methods=['POST'])
def index():
    """
    check server running
    :return:
    """
    return {'status':'OK'}

@app.route("/saksham-custom", methods=['POST'])
def get_pdf_for_saksham():
    """
    receive request from another server and save it in queue
    """
    logging = initialize_logger()
    # Get the logger specified in the file
    logger = logging.getLogger(__name__)
    logger.info("Request received")
    req_data = json.loads(json.dumps(request.json))
    new_req_data = req_data['data'][0]  # Getting the data : [{values}]
    instance_id = new_req_data['instanceID']  # Getting the instance id for searching routes

    unique_ids = []
    json_data = BackupPdfData(
        raw_data=req_data,
        link_id=instance_id
    )
    DB.session.add(json_data)  # Adds new User record to database
    DB.session.flush()  # Pushing the object to the database so that it gets assigned a unique id
    unique_ids.append(json_data.unique_id)
    DB.session.commit()  # Commits all changes
    obj = ODKSheetsPlugin()
    error = obj.fetch_data()
    if not error:
        status = 'done'
    else:
        status = error
    return {'status':status}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


# https://script.google.com/a/samagragovernance.in/macros/s/AKfycbz7NPxhAb-n2f-36KepyGxdpxnWzcak1OusVp5IGT3MjI1JC3t7/exec
