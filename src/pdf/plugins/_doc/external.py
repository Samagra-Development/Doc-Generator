import os
import traceback


from ...plugins._pdf.external import PDFPlugin
from ...uploaders.minio import MinioUploader
from ...utils import build_doc


class DOCXPlugin(PDFPlugin):
    """
        Plugin class which extend from PDFPlugin
    """
    def build_file(self, template_id, token):
        """
        Function to build PDF and return a file (fetch template and build pdf)
        """
        is_successful = False
        template = self.fetch_template(template_id)
        if template is not None:
            is_successful = build_doc(template, token)
        return is_successful

    def upload_file(self, template_id, token):
        """
        Function to save PDF
        """
        error_code = error_msg = final_data = None
        try:
            template = self.build_file(template_id, token)
            print("isSuccessful", template)
            drive_file_loc = f'pdf/drivefiles/{token}.docx"'
            if template is not None:
                if self.uploader == "minio":
                    host = self.user_config["MINIO_HOST"]
                    access_key = self.user_config["MINIO_ACCESS_KEY"]
                    secret_key = self.user_config["MINIO_SECRET_KEY"]
                    bucket_name = self.user_config["MINIO_BUCKET_NAME"]
                    uploader = MinioUploader(host, access_key, secret_key, bucket_name)
                    error_code, error_msg, final_data = uploader.put(f"{token}.docx", f"{token}.docx", None)
                    if error_code is None:
                        if os.path.exists(drive_file_loc):
                            os.remove(drive_file_loc)
                    else:
                        raise Exception("Failed to build the pdf")
                    return error_code, error_msg, final_data
                else:
                    raise Exception("Uploader plugin not supported")
            else:
                raise Exception("Failed to upload the pdf")
        except Exception as e:
            traceback.print_exc()
            error_code = 805
            error_msg = f"Something went wrong: {e}"
        finally:
            return error_code, error_msg, final_data