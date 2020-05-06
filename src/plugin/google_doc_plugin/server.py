"""
Receive Request from external application and save in queue
"""
from .app import create_app
from .external import GoogleDocsSheetsPlugin

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

@app.route("/covid-custom", methods=['POST'])
def get_pdf_covid19():
    """
    define route which save request in queue
    """
    obj = GoogleDocsSheetsPlugin()
    error = obj.fetch_data()
    print('in googledoc')
    if not error:
        status = 'done'
    else:
        status = error
    return {'status':status}

    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
# https://script.google.com/a/samagragovernance.in/macros/s/AKfycbz7NPxhAb-n2f-36KepyGxdpxnWzcak1OusVp5IGT3MjI1JC3t7/exec
