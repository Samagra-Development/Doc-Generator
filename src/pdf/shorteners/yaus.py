import json
import traceback

import requests
from interface import implements
import logging

from requests import HTTPError

from ..base.interfaces.shortener import URLShortener


class YausShortner(implements(URLShortener)):
    def __init__(self, base_url):
        # Get the logger specified in the file
        self.logger = logging.getLogger()
        # Set url shortner url
        self.base_url = base_url

    def apply(self, long_url, hash_id):
        error_code = error_msg = final_data = None
        try:
            body = json.dumps({
                'url': long_url,
                'userID': f"{hash_id}",
                'project': f"{hash_id}",
                'customHashId': f"{hash_id}"
            })
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(self.base_url, data=body, headers=headers)
            response.raise_for_status()
            resp = response.json()
            if 'shortUrl' in resp:
                final_data = resp
            else:
                raise Exception("short url not generated")
        except HTTPError as http_err:
            traceback.print_exc()
            error_code = response.status_code
            error_msg = http_err
        except Exception as e:
            traceback.print_exc()
            error_code = 809
            error_msg = f"Something went wrong: {e}"
        finally:
            return error_code, error_msg, final_data

    def get_long(self, short_url):
        pass
