import os
import re

from bs4 import BeautifulSoup
from django.http import JsonResponse


def return_response(final_data, error_code, error_text):
    """
    The function used to give response in all APIs

    Args:
        final_data:
        error_code:
        error_text:

    Returns:
        response

    """
    # Adding the response status code
    if error_code is None:
        status_code = 200
        response = JsonResponse({"data": final_data},
                                safe=False,
                                status=status_code)
    else:
        if error_code == 802:
            return JsonResponse({"error": [{
                "code": error_code,
                "message": error_text
            }]}, status=401)
        else:
            response = JsonResponse(
                {"error": [{
                    "code": error_code,
                    "message": error_text
                }]},
                safe=False,
                status=200)
    return response


def doc_dictionary(key_value):
    data = {
        "1": "Developer",
        "17": "09-02-2022",
        "2": "Software engineer",
        "4": "D.K",
        "6": "R.V Bangalore",
        "7": "09-02-2022",
        "8": "3",
        "9": "Rahul",
        "10": "Math",
        "11": "50",
        "12": "50",
        "13": "Yes",
        "14": "Yes",
        "15": "5",
        "16": "5",
        "17": "5",
        "18": "Yes",
        "19": "Yes",
        "20": "Concept",
        "21": "Teaching way",
        "22": "Practical",
        "23": "Yes",
        "24": "3 hours",
        "25": "100%",
        "26": "100%",
        "27": "Yes",
        "28": "09-02-2022",
        "29": "Math",
        "30": "Rahul",
        "31": "50",
        "32": "50",
        "33": "Yes",
        "34": "Yes",
        "35": "5",
        "36": "5",
        "37": "5",
        "38": "Yes",
        "39": "Yes",
        "40": "Concept",
        "41": "Teaching way",
        "42": "Practical",
        "43": "Yes",
        "44": "3 hours",
        "45": "100%",
        "46": "100%",
        "47": "Yes",
        "48": "09-02-2022",
    }

    for i in data:
        if i == key_value:
            return data[i]

def beautify_html(doc_id):
    html_file = open(f'pdf/drivefiles/{doc_id}.html')
    html_doc = html_file.read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    old_text = soup.find_all(text=re.compile("<<"))

    for i in old_text:
        updated_text = re.findall(r"<<(.*?)>>", i)
        new_text = doc_dictionary(updated_text[0])

        if new_text == None:
            i.replace_with("Not provided")
        else:
            i.replace_with(new_text)

    str_html = soup.prettify()
    html_file.close()
    os.remove(f'pdf/drivefiles/{doc_id}.html')
    return str_html