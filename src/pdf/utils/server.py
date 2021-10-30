"""
Make a endpoint where we continuously receive request from another server
"""

import json
from flask import request
from db.models import PdfData, OutputTable, TempData
from db.app import DB, create_app
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

@app.route("/update", methods=['POST'])
def update_username():
    """
    receive request from another server and save it in queue
    """
    data = json.loads(json.dumps(request.json))
    print(data)

    try:
        temp_qms = TempData.query.filter(TempData.instance_id == data['instance_id']).all()
        pdf_qms = PdfData.query.filter(PdfData.link_id == data['instance_id'],
                                       PdfData.is_update == False).all()
        is_update = False
        is_insert_temp = False
        if pdf_qms:
            for pdf_qm in pdf_qms:
                results = []
                raw_data = pdf_qm.raw_data
                req_data = raw_data['req_data']
                req_data['user_name'] = data['user_name']
                raw_data['USERNAME'] = data['user_name']
                tags = pdf_qm.tags
                tags['USERNAME'] = data['user_name']
                pdf_qm.raw_data = raw_data
                pdf_qm.tags = tags
                pdf_qm.is_update = True
                results.append(pdf_qm)
                DB.session.bulk_save_objects(results)
                DB.session.commit()
                is_update = True
        if temp_qms:
            if is_update:
                for temp_qm in temp_qms:
                    results = []
                    temp_qm.is_update = True
                    results.append(temp_qm)
                    DB.session.bulk_save_objects(results)
                    DB.session.commit()
        else:
            json_data = TempData(
                instance_id=data['instance_id'],
                user_name=data['user_name'],
                form_id=data['form_id']
                )
            DB.session.add(json_data)  # Adds new User record to database
            # Pushing the object to the database so that it gets assigned a unique id
            DB.session.flush()
            DB.session.commit()  # Commits all changes
            is_insert_temp = True
        status = ''
        if pdf_qms:
            status = 'done'
        else:
            status = 'notfound'
        return {'status': status, 'is_insert_temp': is_insert_temp}
    except Exception as ex:
        print(ex)
        return {'status':'error'}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)


# https://script.google.com/a/samagragovernance.in/macros/s/AKfycbz7NPxhAb-n2f-36KepyGxdpxnWzcak1OusVp5IGT3MjI1JC3t7/exec
