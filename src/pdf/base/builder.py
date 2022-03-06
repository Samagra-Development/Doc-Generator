"""
Generate Pdf for all the request
"""
import json
import traceback
import uuid
import os.path
import threading
from time import sleep

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from .interfaces.plugin import Plugin
from .interfaces.shortener import URLShortener
from .interfaces.uploader import Uploader
from ..models import *
import logging


@shared_task
def update_step_choice(id, step):
    doc = Doc.objects.get(pk=id)
    doc.step = step
    doc.save()


@shared_task
def update_status_choice(id, status):
    doc = Doc.objects.get(pk=id)
    doc.status = status
    doc.save()


class Builder:
    def __init__(self, plugin, pdf_data, token):

        # Setup Constants
        self._logger = logging.getLogger()
        self._error = None
        self._data = pdf_data
        self.token = token
        self.config_id = self._data['config_id']
        try:
            self.object = Doc.objects.get(pk=token)
            self.object.data = pdf_data
            self.object.save()
            self.tries = self.object.tries
            update_status_choice.delay(token, 'Processing')
            config = GenericConfig.objects.get(pk=self.config_id)
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
                self.object.status = 'Error'
                self.object.meta = {
                    "message": "Please provide a valid config. Needs to be an instance of GenericConfig."
                }
                self.object.retry = False
                self.object.isActive = False
                self.object.save()
                raise ValueError('Please provide a valid config. Needs to be an instance of GenericConfig.')
            self.tries += 1
            if self.tries > self._max_tries + 1:
                self.object.meta = {
                    "message": "Max Retries Exceeded"
                }
                self.object.retry = False
                self.object.isActive = False
                self.object.save()
            else:
                self.object.tries = self.tries
                self.object.save()
        except ObjectDoesNotExist:
            # update_status_choice.delay(self.token, 'Error')
            traceback.print_exc()
            self.object.status = 'Error'
            self.object.meta = {
                "message": "Wrong Token Id, Object Not Found"
            }
            self.object.retry = False
            self.object.isActive = False
            self.object.save()
            self._logger.error("Wrong Token Id, Object Not Found")
        except Exception as e:
            # update_status_choice.delay(self.token, 'Error')
            traceback.print_exc()
            self._logger.error(f"Exception occurred: {e}", exc_info=True)
            self.object.status = 'Error'
            self.object.meta = {
                "message": "Please provide a valid plugin."
            }
            self.object.retry = False
            self.object.isActive = False
            self.object.save()
            raise ValueError('Please provide a valid plugin.')

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
            if self.tries <= self._max_tries + 1 and self.object.retry is True:
                update_step_choice.delay(self.token, 'Template Processing')
                self._logger.info("Step: Template Processing")
                err_code, err_msg, fetch_template = self._plugin.fetch_template()
                if not err_code:
                    # self._step = Pdf.STEP_CHOICES('Doc Building')
                    update_step_choice.delay(self.token, 'Doc Building')
                    self._logger.info("Step: Doc Building")
                    err_code, err_msg, file_build = self._plugin.build_file(fetch_template)
                    if not err_code and file_build is True:
                        # self._step = Pdf.STEP_CHOICES('Uploading')
                        update_step_choice.delay(self.token, 'Uploading')
                        self._logger.info("Step: Uploading")
                        err_code, err_msg, long_url = self._plugin.upload_file()
                        if err_code is None:
                            # self._step = Pdf.STEP_CHOICES('URL Shortening')
                            self.object.url = long_url['url']
                            self.object.url_meta = long_url['meta']
                            self.object.save()
                            update_step_choice.delay(self.token, 'URL Shortening')
                            self._logger.info("Step: URL Shortening")
                            err_code, err_msg, url = self._plugin.shorten_url(long_url['url'])
                            if err_code is None:
                                print(url)
                                self.object.short_url = url
                                self.object.save()
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
                if error_code is None:
                    update_status_choice.delay(self.token, 'Complete')
                    update_step_choice.delay(self.token, 'Complete')
                else:
                    update_status_choice.delay(self.token, f"{error_code}: {error_msg}")
                    update_step_choice.delay(self.token, 'Complete')
            else:
                data = "Max Retries"
                self._logger.info(data)
        except Exception as e:
            traceback.print_exc()
            error_code = 801
            error_msg = "Unable to process queue"
            update_status_choice.delay(self.token, 'Failed')
            self._logger.error(f"Exception occurred: {e}", exc_info=True)
        finally:
            self.object.isActive = False
            self.object.save()
            return error_code, error_msg, data