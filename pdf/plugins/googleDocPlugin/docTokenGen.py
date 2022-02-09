from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleDocsSheetsPlugin():

    def get_token(self):
        """ To do authentication """

        gauth = GoogleAuth()
        gauth.CommandLineAuth()
        drive = GoogleDrive(gauth)

        return drive
