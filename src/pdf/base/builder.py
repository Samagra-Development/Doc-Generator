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

steps = [
    'Not Started',
    'Template Processing',
    'Doc Building',
    'Uploading',
    'URL Shortening',
    'Completed',
]

statuses = [
    'Queued',
    'Processing',
    'Complete',
    'Failed',
    'Error',
]


@shared_task
def update_step_choice(id, step, idx):
    if idx > steps.index(step):
        print(f"older step: {step}")
    else:
        print(f"step: {step}")
        doc = Doc.objects.get(pk=id)
        doc.step = step
        doc.save()
        print("saved step")


@shared_task
def update_status_choice(id, status, idx):
    if status not in ['Failed', 'Error']:
        if idx > statuses.index(status):
            print(f"older status: {status}")
        else:
            print(f"status: {status}")
            doc = Doc.objects.get(pk=id)
            doc.status = status
            doc.save()
            print("saved status")
    else:
        print(f"status: {status}")
        doc = Doc.objects.get(pk=id)
        doc.status = status
        doc.save()
        print("saved status")


class Builder:
    def __init__(self, plugin, pdf_data, token):

        # Setup Constants
        self._logger = logging.getLogger()
        self._error = None
        self._data = pdf_data
        self.token = token
        self.config_id = self._data['config_id']
        self.step = 0
        self.status = 0
        try:
            self.object = Doc.objects.get(pk=token)
            self.object.data = pdf_data
            self.object.save()
            self.tries = self.object.tries
            self.status += 1
            update_status_choice.delay(token, 'Processing', self.status)
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
                self.step += 1
                update_step_choice.delay(self.token, 'Template Processing', self.step)
                self._logger.info("Step: Template Processing")
                err_code, err_msg, fetch_template = self._plugin.fetch_template()
                if not err_code:
                    # self._step = Pdf.STEP_CHOICES('Doc Building')
                    self.step += 1
                    update_step_choice.delay(self.token, 'Doc Building', self.step)
                    self._logger.info("Step: Doc Building")
                    err_code, err_msg, file_build = self._plugin.build_file(fetch_template)
                    if not err_code and file_build is True:
                        # self._step = Pdf.STEP_CHOICES('Uploading')
                        self.step += 1
                        update_step_choice.delay(self.token, 'Uploading', self.step)
                        self._logger.info("Step: Uploading")
                        err_code, err_msg, long_url = self._plugin.upload_file()
                        if err_code is None:
                            # self._step = Pdf.STEP_CHOICES('URL Shortening')
                            self.object.url = long_url['url']
                            self.object.url_meta = long_url['meta']
                            self.object.save()
                            self.step += 1
                            update_step_choice.delay(self.token, 'URL Shortening', self.step)
                            self._logger.info("Step: URL Shortening")
                            err_code, err_msg, url = self._plugin.shorten_url(long_url['url'])
                            if err_code is None:
                                print(url)
                                self.object.short_url = url
                                self.object.save()
                                data = url
                            else:
                                self._logger.info("Failed to shorten the url")
                                error_code = err_code
                                error_msg = err_msg
                        else:
                            self._logger.info("Failed to upload the file")
                            error_code = err_code
                            error_msg = err_msg
                    else:
                        self._logger.info("Failed to build the file")
                        error_code = err_code
                        error_msg = err_msg
                self._logger.info("Request Receive Pdf generation End")
                if error_code is None:
                    self.step += 1
                    self.status += 1
                    self.object.status("Complete")
                    self.object.step("Completed")
                    self.object.retry = False
                else:
                    self.status += 1
                    update_status_choice.delay(self.token, f"{error_code}: {error_msg}", self.status)
            else:
                data = "Max Retries"
                self._logger.info(data)
        except Exception as e:
            traceback.print_exc()
            error_code = 801
            error_msg = "Unable to process queue"
            self.status += 1
            update_status_choice.delay(self.token, 'Failed', self.status)
            self._logger.error(f"Exception occurred: {e}", exc_info=True)
        finally:
            self.object.isActive = False
            self.object.save()
            return error_code, error_msg, data
