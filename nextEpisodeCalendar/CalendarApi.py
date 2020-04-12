import pickle
import os.path
from datetime import datetime

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

from nextEpisodeCalendar.event import Event


class API:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
        TOKEN_FILE_PATH = os.path.join(DATA_DIR, 'token.pickle')
        CLIENT_SECRET_FILE_PATH = os.path.join(DATA_DIR, 'client_secret.json')
        CALENDAR_ID_FILE_PATH = os.path.join(DATA_DIR, 'calendarID.pickle')

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

        if os.path.exists(CALENDAR_ID_FILE_PATH):
            with open(CALENDAR_ID_FILE_PATH, 'rb') as f:
                self.calendarID = pickle.load(f)
        else:
            self.calendarID = self.createCalendar()
            with open(CALENDAR_ID_FILE_PATH, 'wb') as f:
                pickle.dump(self.calendarID, f)

    def createCalendar(self):
        calendar = {'summary': 'episodes'}
        created_calendar = self.service.calendars().insert(body=calendar).execute()
        return created_calendar['id']

        
    def addEvents(self, events: list):
        '''
        Adds a list of Events to the primary calendar of user.
        
        Parameters:
            events (list): A list of Event objects.
        '''
        existing_events = self.service.events().list(calendarId=self.calendarID).execute()['items']

        for event in events:
            if not next((item for item in existing_events
                if item['summary'] == event.summary and item['description'] == event.description), None):
            
                self.service.events().insert(calendarId=self.calendarID, body=event.toCalendarResource()).execute()

    def getEvents(self) -> list:
        '''
        Returns a list of Event objects sorted by date.
        '''
        events = self.service.events().list(calendarId=self.calendarID).execute()['items']
        events = [Event(event['summary'], 
                        event['description'], 
                        datetime.strptime(event['start']['dateTime'], '%Y-%m-%dT%H:%M:%S%z')
                    ) 
                for event in events]

        return sorted(events, key=lambda event: event.start)
