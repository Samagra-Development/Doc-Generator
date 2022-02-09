import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .plugins.googleDocPlugin.docTokenGen import GoogleDocsSheetsPlugin
import os
import pdfkit


# Create your views here.
from .utils import return_response, beautify_html


@api_view(['POST'])
def generate_pdf(request):
    final_data = []
    error_text = error_code = None
    if request.method == 'POST':
        doc_id = request.data['doc_id']
        try:
            drive = GoogleDocsSheetsPlugin()
            token = drive.get_token()
            file = token.CreateFile({'id': doc_id})
            file.GetContentFile(f'pdf/drivefiles/{doc_id}.html', mimetype='text/html')
            # print(file.GetContentString())

            drive_file_loc = f'pdf/drivefiles/{doc_id}'

            if os.path.exists(drive_file_loc + '.html'):
                str_html = beautify_html(doc_id)


                # PDF generation starts                
                pdfkit.from_string(str_html, drive_file_loc + '.pdf')
            # if os.path.exists(drive_file_loc + '.pdf'):
            #     os.remove(drive_file_loc + '.pdf')
                # PDF generation ends

                return HttpResponse(str_html)
            else:
                raise ObjectDoesNotExist()
        except ObjectDoesNotExist:
            error_code = 804
            error_text = "File not found"
        except Exception as e:
            traceback.print_exc()
            error_code = 804
            error_text = f"Something went wrong!: {e}"

    response = return_response(final_data, error_code, error_text)
    return response
