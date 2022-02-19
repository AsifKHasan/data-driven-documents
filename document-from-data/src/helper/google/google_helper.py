#!/usr/bin/env python3
'''
    helper routines for google
'''

import gspread

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from google.auth.transport.urllib3 import AuthorizedHttp

''' from a connector spec returns a google service client connection
'''
def connector_client(google_data_connector_spec):
    # get credentials for service-account
    credentials = service_account.Credentials.from_service_account_file(google_data_connector_spec['credential-json'])
    scoped_credentials = credentials.with_scopes(
                                                [
                                                    "https://spreadsheets.google.com/feeds",
                                                    'https://www.googleapis.com/auth/spreadsheets',
                                                    "https://www.googleapis.com/auth/drive.file",
                                                    "https://www.googleapis.com/auth/drive"
                                                ]
                                            )

    # using gspread for proxying the gsheet API's
    client = gspread.authorize(scoped_credentials)

    # authed_session = AuthorizedSession(credentials)
    # response = authed_session.get('https://www.googleapis.com/storage/v1/b')

    # authed_http = AuthorizedHttp(credentials)
    # response = authed_http.request('GET', 'https://www.googleapis.com/storage/v1/b')

    return client

def gsheet_data(client, gsheet_data_source_spec):
    # get the worksheet where the data is
    gsheet = client.open(title=gsheet_data_source_spec['sheet'])
    ws = gsheet.worksheet(title=gsheet_data_source_spec['worksheet'])

    # get values in the specified range
    values = ws.get_values(gsheet_data_source_spec['data-range'])

    return values
