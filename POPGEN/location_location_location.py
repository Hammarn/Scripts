#!/usr/bin/env python
import os

import httplib2
import argparse
import pickle
import os.path
from apiclient import discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools
from geopy.geocoders import Nominatim

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
#SAMPLE_RANGE_NAME = 'Class Data!A2:E'

CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

#def read_from_sheet(column, row):


def get_location(cityname):
        geolocator = Nominatim(user_agent='my-application')
        location = geolocator.geocode(cityname)
        lat = location.latitude
        lng = location.longitude
        return (lat,lng)

def main(ID,subsheet, loc_column, start, stop ):
    ID = ID[0]
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    RANGE = '{shn}!{pc}{sr}:{pc}{er}'.format(shn=subsheet, sr=int(start[0]), pc=loc_column[0], er=int(stop[0]))
    
    
    result = service.spreadsheets().values().get(spreadsheetId = ID, range=RANGE).execute()
    values = result.get('values', [])
    #result = service.spreadsheets().values().update(spreadsheetId=SAMPLESHEET_ID, range=RESULTS_RANGE.format(cell=my_cell), valueInputOption="USER_ENTERED", body=tv).execute()
    for location in values:
        import pdb
        pdb.set_trace()
        get_location(location)
## TODO
## dict for saving output?
## skip empty rows
## write to sheet
## write in a colour that makes it clear it was written by the script



if __name__ == '__main__':
    parser = argparse.ArgumentParser("Read name of a location in a google sheets and return lat. long.")
    parser.add_argument("-l", "--location_column", nargs = 1,
        help="Column in the spreadsheet with the location to be read")
    parser.add_argument("-r", "--row", nargs = 1, default = 1,
        help="which row to start at")
    parser.add_argument("-s", "--stop_row", nargs = 1, default = 1,
        help="which row to stop at")
    parser.add_argument("-o", "--output_column", nargs = 2,
        help="Colums to right to, lattitude followed by longitude")
    parser.add_argument("-id", "--id", nargs = '+', required=True,
        help= "Worksheet ID something like '10mfjefQ3kXRvubtM6yrYRHBGFqw2dg-EPT2DsMpadyGU'")
    parser.add_argument("-sub", "--subsheet_name", default='Sheet1',
        help="Which sheet in the document should be modified")

    args = parser.parse_args()


    main(args.id ,args.subsheet_name ,args.location_column ,args.row ,args.stop_row )
