from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .plugins.googleDocPlugin.docTokenGen import GoogleDocsSheetsPlugin
import os
from bs4 import BeautifulSoup

# Create your views here.
@api_view(['POST'])
def generatePDF(request):
    if request.method == 'POST':

        docID = request.data['doc_id']


        try:
            drive = GoogleDocsSheetsPlugin.get_token() 
            file = drive.CreateFile({'id': docID})
            file.GetContentFile(f'pdf/drivefiles/{docID}.html', mimetype='text/html')

            fileExist = os.path.exists(f'pdf/drivefiles/{docID}.html')
            if(fileExist == True):
                htmlFile = open(f'pdf/drivefiles/{docID}.html')
                htmlDoc = htmlFile.read()
                soup = BeautifulSoup(htmlDoc, 'html.parser')
                strhtml = soup.prettify()
                data = {
                    "driveDocData": strhtml
                }

                os.remove(f'pdf/drivefiles/{docID}.html')

                return Response(data)
        except:
            return Response("Something went wrong")