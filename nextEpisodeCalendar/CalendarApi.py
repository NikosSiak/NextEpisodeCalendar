import pickle
import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from nextEpisodeCalendar.event import Event


class API:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar.events']
        PRIVATE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
        TOKEN_FILE_PATH = os.path.join(PRIVATE_DIR, 'token.pickle')
        CLIENT_SECRET_FILE_PATH = os.path.join(PRIVATE_DIR, 'client_secret.json')

        creds = None
        if os.path.exists(TOKEN_FILE_PATH):
            with open(TOKEN_FILE_PATH, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE_PATH, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)
        
    def addEvents(self, events: list):
        '''
        Adds a list of Events to the primary calendar of user.
        
        Parameters:
            events (list): A list of Event objects.
        '''
        existing_events = self.service.events().list(calendarId='primary').execute()['items']

        for event in events:
            if not next((item for item in existing_events
                if item['summary'] == event.summary and item['description'] == event.description), None):
            
                self.service.events().insert(calendarId='primary', body=event.toCalendarResource()).execute()
