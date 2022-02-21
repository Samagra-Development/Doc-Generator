# json.loads(req.json()['body'])
import json
import os

import requests

from ...plugins._pdf.external import PDFPlugin


class PDFMakePlugin(PDFPlugin):
    """
        Plugin class which extend from PDFPlugin
    """
    def fetch_template(self, template_id):
        """
        Fetches template and returns it in the form of string
        """
        data = json.dumps({
            "id": template_id,
            "data": self._data
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(os.getenv('PROCESS_TEMPLATE_URL'), data=data, headers=headers)
        if response.status_code == 201:
            template_string = json.loads(response.json()['processed']) if "processed" in response.json() else None
            return template_string
        else:
            return None