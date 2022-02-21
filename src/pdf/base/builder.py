"""
Generate Pdf for all the request
"""
import json
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
    def __init__(self, plugin, config, pdf_data):

        # Setup Constants
        self._error = None
        self._step = Pdf.STEP_CHOICES('Not Started')
        self._status = Pdf.Q_STATUS_CHOICES('Queued')
        self._data = pdf_data
        try:
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
        self._logger.info("Step2 Request Receive Pdf generation Start", self._data.raw_data)
        error = None
        try:
            tries = self._data.tries
            tries += 1  # Incrementing the tries
            self._data.tries = tries
            self._step = Pdf.STEP_CHOICES('Data Fetching')
            fetch_data = self._plugin.fetch_data(self._data.raw_data)
            fetch_error = fetch_data[1]

            if not fetch_error:
                self._data.raw_data = fetch_data[0] if fetch_data is not None else self._data

                self._step = Pdf.STEP_CHOICES('Template Processing')
                file_build = self._plugin.build_pdf(self._data.raw_data, self._data.instance_id)
                file_name = file_build[0]
                file_error = file_build[1]
                if not file_error:
                    self._data.step = 2
                    self._data.doc_name = file_build[0]
                    self._data.doc_url = file_build[2]
                    file_downloaded = self._uploader.upload_pdf(file_name, self._data.doc_url)
                    upload_file_url = file_downloaded[0]
                    file_error = file_downloaded[1]
                    if not file_error:
                        self._step = Pdf.STEP_CHOICES('Template Processing')
                        version = self._data.pdf_version
                        version += 1
                        self._data.pdf_version = version
                        self._data.current_status = 'complete'
                        self._data.task_completed = True
                        self._data.long_doc_url = upload_file_url
                        self._data.url_expires = file_downloaded[2]
                        short_url_resp = self._shortener.put(self._data.long_doc_url, self._data.doc_url)
                        short_url = short_url_resp[0]
                        error = short_url_resp[1]
                        if error:
                            self._data.error_encountered = error
                            self._data.task_completed = False
                        else:
                            self._data.doc_name = short_url
                            self._data.step = 4
                            # Now moving the above data to the Output table
                            inserted_to_output = self._persist()
                            if not inserted_to_output:
                                self._data.error_encountered = ''
                            else:
                                self._data.error_encountered = inserted_to_output
                                self._data.task_completed = False

                    else:
                        self._data.error_encountered = file_error
                else:
                    self._data.error_encountered = file_error
            else:
                self._data.error_encountered = mapping_error
            self._logger.info("Step2 Request Receive Pdf generation End", self._data.raw_data)

        except Exception as ex:
            error = "Unable to process queue"
            self._logger.error("Error 8 " + error, self._data.raw_data)
            self._logger.error("Exception occurred", exc_info=True)
        return error, self._data