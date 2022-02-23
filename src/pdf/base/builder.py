"""
Generate Pdf for all the request
"""
import json
import traceback
import uuid
import os.path
import threading
from time import sleep
from .interfaces.plugin import Plugin
from .interfaces.shortener import URLShortener
from .interfaces.uploader import Uploader
from ..models import *
import logging


class Builder:
    def __init__(self, plugin, config_id, pdf_data, token):

        # Setup Constants
        self._logger = logging.getLogger()
        self._error = None
        # self._step = Pdf.STEP_CHOICES('Not Started')
        # self._status = Pdf.Q_STATUS_CHOICES('Queued')
        self._data = pdf_data
        try:
            self.object = Pdf.objects.get(pk=token)
            config = GenericConfig.objects.get(pk=config_id)
            self._logger = logging.getLogger()
            Plugin.verify(type(plugin))
            self._plugin = plugin
            if isinstance(config, GenericConfig):
                self._config = config
                self._uploader = config.get_uploader()
                self._shortener = config.get_shortener()
                self._max_tries = config.retries
            else:
                self._logger.error("Config is not an instance of GenericConfig")
                raise ValueError('Please provide a valid config. Needs to be an instance of GenericConfig.')
        except:
            self._logger.error("Exception occurred", exc_info=True)
            raise ValueError('Please provide a valid plugin. Needs to be an instance of PDFPlugin.')

    def _persist(self):
        try:
            # TODO: Insert PDF
            print("Dummy")
        except Exception as ex:
            self._error = 'Values not inserted in output table'
            self._logger.error("Error %s", self._error)
            self._logger.error("Exception occurred", exc_info=True)
        return 1

    def _process(self):
        """
        function for generating pdf
        """
        self._logger.info("Request Receive Pdf generation Start")
        error_code = error_msg = data = None
        try:
            # tries = self._data.tries
            # tries += 1  # Incrementing the tries
            # self._data.tries = tries
            # self._step = Pdf.STEP_CHOICES('Data Fetching')
            # self._step = Pdf.STEP_CHOICES('Template Processing')
            self._logger.info("Step: Template Processing")
            err_code, err_msg, fetch_template = self._plugin.fetch_template()
            if not err_code:
                # self._step = Pdf.STEP_CHOICES('Doc Building')
                self._logger.info("Step: Doc Building")
                err_code, err_msg, file_build = self._plugin.build_file(fetch_template)
                if not err_code and file_build is True:
                    # self._step = Pdf.STEP_CHOICES('Uploading')
                    self._logger.info("Step: Uploading")
                    err_code, err_msg, long_url = self._plugin.upload_file()
                    if err_code is None:
                        # self._step = Pdf.STEP_CHOICES('URL Shortening')
                        self._logger.info("Step: URL Shortening")
                        err_code, err_msg, url = self._plugin.shorten_url(long_url)
                        if err_code is None:
                            print(url)
                            data = url
                        else:
                            print("Failed to shorten the url")
                            error_code = err_code
                            error_msg = err_msg
                    else:
                        print("Failed to upload the file")
                        error_code = err_code
                        error_msg = err_msg
                else:
                    print("Failed to build the file")
                    error_code = err_code
                    error_msg = err_msg
            self._logger.info("Request Receive Pdf generation End")
            return error_code, error_msg, data
        except Exception as e:
            traceback.print_exc()
            error_code = 801
            error_msg = "Unable to process queue"
            self._logger.error(f"Exception occurred: {e}", exc_info=True)
            return error_code, error_msg, data