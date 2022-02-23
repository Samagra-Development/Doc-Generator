import os
import re
import traceback
import requests
import aspose.words as aw

from bs4 import BeautifulSoup
from django.http import JsonResponse
import pdfkit
from minio import Minio
from requests import HTTPError

from .models import Pdf


def get_sample_data():
    sample_data = {
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
    return sample_data


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


def format_html(html_str, data):
    # html_file = open(f'pdf/drivefiles/{doc_id}.html')
    # html_doc = html_file.read()
    soup = BeautifulSoup(html_str, 'html.parser')
    old_text = soup.find_all(text=re.compile("<<"))

    for i in old_text:
        updated_text = re.findall(r"<<(.*?)>>", i)
        new_text = data[updated_text[0]]

        if new_text is None:
            i.replace_with("Not provided")
        else:
            i.replace_with(new_text)

    str_html = soup.prettify()
    # html_file.close()
    # os.remove(f'pdf/drivefiles/{doc_id}.html')
    return str_html


def build_pdf(html_str, file_name):
    is_successful = error = None
    drive_file_loc = f'pdf/drivefiles/{file_name}.pdf'
    try:
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdfkit.from_string(html_str, drive_file_loc, configuration=config)
        is_successful = True
    except Exception as e:
        traceback.print_exc()
        error = f"Failed to generate doc: {e}"
    return is_successful, error


def build_doc(html_str, file_name):
    drive_file_loc = f'pdf/drivefiles/{file_name}.docx'
    try:
        doc = aw.Document()
        builder = aw.DocumentBuilder(doc);
        builder.insert_html(html_str)
        doc.save(drive_file_loc)
        return True
    except:
        traceback.print_exc()
        return False


def send_get_request(url, params=None, headers=None):
    try:
        request = requests.get(url, params=params, headers=headers)
        request.raise_for_status()
        return request.json()
    except HTTPError as http_err:
        return JsonResponse(
            {"error": [{
                "code": request.status_code,
                "message": http_err
            }]},
            safe=False,
            status=200)
    except ValueError:
        traceback.print_exc()
        return request.content
    except Exception as err:
        return JsonResponse(
            {"error": [{
                "code": 804,
                "message": f"Something went wrong!: {e}"
            }]},
            safe=False,
            status=200)


def send_post_request(url, params=None, data=None, json=None, headers=None):
    try:
        request = requests.post(url, params=params, json=json, data=data, headers=headers)
        request.raise_for_status()
        return request.json()
    except HTTPError as http_err:
        return JsonResponse(
            {"error": [{
                "code": request.status_code,
                "message": http_err
            }]},
            safe=False,
            status=200)
    except ValueError:
        traceback.print_exc()
        return request.content
    except Exception as e:
        return JsonResponse(
            {"error": [{
                "code": 804,
                "message": f"Something went wrong!: {e}"
            }]},
            safe=False,
            status=200)


def publish_to_url(pdf_id, url, headers=None):
    pdf = Pdf.objects.get(pk=pdf_id)
    response = send_post_request(url, data=pdf, headers=headers)
    return response
