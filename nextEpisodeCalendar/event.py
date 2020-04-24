from datetime import datetime, timedelta
from time import gmtime, strftime  # for the timezone

class Event:

    timezone = strftime("%z", gmtime())

    def __init__(self, summary: str, description: str, start: datetime, end: datetime = None, **kwargs):
        self.summary = summary
        self.description = description
        self.start = start
        self.end = end
        if not self.end:
            self.end = self.start + timedelta(hours=1)
        self.options = {}
        self.options.update(kwargs)

    def toCalendarResource(self):
        '''
        Return a dictionary ready to be sent to the calendar api
        '''

        resource = {
            'summary': self.summary,
            'start': {
                'dateTime': self.start.isoformat(),
                'timeZone': Event.timezone
            },
            'end': {
                'dateTime': self.end.isoformat(),
                'timeZone': Event.timezone
            },
            'description': self.description
        }
        resource.update(self.options)
        return resource

    def __str__(self):
        return f'-----{self.summary}-----\n{self.description}\n{self.start.strftime("%B %d, %Y")}'
