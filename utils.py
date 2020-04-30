from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.cloud import storage
import os
import pickle, os.path

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive'
]


def fetch_data():
    error = None
    try:
        SAMPLE_SPREADSHEET_ID = "1_iE1D8Pvsq7SQMMjHWhOhidGvkXENiluq01RXvb3n5g"
        SHEET_NAME = "PDF generator excel"
        RANGE = "C1:AM37"
        SAMPLE_RANGE_NAME = SHEET_NAME + "!" + RANGE
        creds = None

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('instance/token.pickle'):
            print("Here 1")
            with open('instance/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        print(creds)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            print("Here 0")
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'instance/credentials2.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('instance/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            error = "No Mapping details found"
        else:
            mappingValues = values
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        error = "Failed to fetch mapping detials"
        mappingValues = None

    return mappingValues, error