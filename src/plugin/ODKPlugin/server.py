import random, string, json
from flask import Flask, request
from flask import jsonify
from .app import create_app
from queuelib import FifoDiskQueue
import uuid
app = create_app()
from .external import ODKSheetsPlugin


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

@app.route("/saksham-custom", methods=['POST'])
def getPdfForSaksham():

    obj = ODKSheetsPlugin()
    error = obj.fetch_data()
    if not error:
        status = 'done'
    else:
        status = error    
    return {'status':status}
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)


# https://script.google.com/a/samagragovernance.in/macros/s/AKfycbz7NPxhAb-n2f-36KepyGxdpxnWzcak1OusVp5IGT3MjI1JC3t7/exec