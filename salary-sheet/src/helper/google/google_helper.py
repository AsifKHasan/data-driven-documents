#!/usr/bin/env python3

import pygsheets

import httplib2

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GoogleHelper(object):

    def authorize(self, service_account_file):
        self._context = {}

        try:
            _G = pygsheets.authorize(service_account_file=service_account_file)
            credentials = ServiceAccountCredentials.from_json_keyfile_name(service_account_file, scopes=['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets'])
            credentials.authorize(httplib2.Http())
            gauth = GoogleAuth()
            gauth.credentials = credentials

            self._context['_G'] = _G
            self._context['service'] = discovery.build('sheets', 'v4', credentials=credentials)
            self._context['drive'] = GoogleDrive(gauth)
        except Exception as e:
            return False

        return True

    def open_gsheet(self, gsheet_name):
        if self._context and '_G' in self._context and self._context['_G']:
            return self._context['_G'].open(gsheet_name)
        else:
            return None
