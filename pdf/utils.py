import os

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


def beautify_html(doc_id):
    html_file = open(f'pdf/drivefiles/{doc_id}.html')
    html_doc = html_file.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    str_html = soup.prettify()
    html_file.close()
    os.remove(f'pdf/drivefiles/{doc_id}.html')
    return str_html
