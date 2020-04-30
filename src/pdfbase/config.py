##########################################################
#                                                        #
#           Project Fixed valiables declared             #
#                                                        #
##########################################################
import os
## VARIABLE - SERVER DEPENDENT
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/root/template-to-pdf/instance/gcs-creds.json'  # On server
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/var/www/html/samagra/pdf-from-googledocs/src/GoogleDocPlugin/gcs-creds.json'  # On Laptop

### Shiksha Saathi
#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:docker@139.59.45.41:5432/postgres'  # Database credentials for creating conection for shiksha saathi PDF builder
#BUCKET = "shiksha-saathi"  # GCS bucket for shiksha saathi PDFs
#URL = "https://script.google.com/macros/s/AKfycby9y5_9_RhA-gai_x6ppzdWrluX16zxp_mY9jPBmwnwbyRHA17E/exec?"  # URL of google app script for shiksha saathi

### Saksham Samiksha
#SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:docker@139.59.45.41:5432/postgres'  # Database credentials for creating conection for saksham samiksha PDF builder
SQLALCHEMY_DATABASE_URI = 'postgresql://auriga:auriga123@localhost:5432/auriga'  # Database credentials for creating conection for saksham samiksha PDF builder
BUCKET = "covid19_samagra"  # GCS bucket for saksham samiksha PDFs
# URL = "https://script.google.com/a/samagragovernance.in/macros/s/AKfycbz7NPxhAb-n2f-36KepyGxdpxnWzcak1OusVp5IGT3MjI1JC3t7/exec?"  # URL of google app script for saksham samiksha
URL = "https://script.google.com/macros/s/AKfycbw1Et6M-NEQ9nnPw5OqSt5kCCFg5orR1dsIZ0gRJB8YJTZj864/exec?"
## CONSTANT - SERVER INDEPENDENT
SECRET_KEY = 'p9Bv<3Eid9dQW#$&sdER25wSF2w4fs$i01'  # Secret API key
SQLALCHEMY_TRACK_MODIFICATIONS = False
FLASK_CONFIG = 'production'  # Flask config (also present in app/__init__.py)
DIRPATH = "uploadFiles/"  # Directory for downloading the pdf's from drive
GOOGLECLOUDBASEURL = 'https://storage.googleapis.com/' + BUCKET + '/'  # GCS pdf base url
SESSIONCOOKIEBASEURL = 'http://aggregate.cttsamagra.xyz:8080/Aggregate.html#submissions/filter///'  # Base url for getting session cookie
MAPPINGDETAILS = 'mappingDetails'  # name of mapping details sheet
OPTIONSSHEET = 'optionsSheet'  # name of options mapping sheet
ODKUSERNAME = 'samagra'  # Username of ODK aggregate (data streaming server)
ODKPASSWORD = 'impact@scale'  # Password of ODK aggregate server
