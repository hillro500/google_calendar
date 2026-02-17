"""
Code taken and adapted from https://developers.google.com/workspace/calendar/api/guides/create-events.

This module is meant to be used as a helper module that can imported and used to create events to a google
calendar specified by the user.
"""

import datetime as dt
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dateutil import parser

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

#%%
def create_event(creds:Credentials,
                 summary:str, 
                 start:dt.datetime, 
                 end:dt.datetime, 
                 location:str='', 
                 description:str='', 
                 recurrance:str='', 
                 timezone:str='America/Chicago',
                 attendees:list[dict]=[], 
                 reminder_overrides:list[dict]=[],
                 calendarId:str='primary') -> None:
  '''
  Creates an event in Google Calendar.

  Refer to the Python quickstart on how to setup the environment:
  https://developers.google.com/workspace/calendar/quickstart/python
  Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
  stored credentials.

  Parameters
  ----------
  creds : Credentials
      required credentials to make edits to Google Calender. Typically from
      get_creds function
  summary : str
      Event description
  start : dt.datetime
      start datetime of event
  end : dt.datetime
      end datetime of event
  location : str, optional
      Address or name of location of event.
      The default is ''.
  description : str, optional
      Additional details about the event.
      The default is ''.
  recurrance : str, optional
      Frequency of recurrance of event.
      The default is ''.
  timezone : str, optional
      Timezone recognized by Coogle Calender API.
      The default is 'America/Chicago'.
  attendees : list[dict], optional
      List containing dictionary of attendees recognized by Google Calendar 
      API.
      The default is [].
  reminder_overrides : list[dict], optional
      List containing dictionary of Google API recongnized overrides.
      The default is [].
  calendarId : str, optional
      A Google Calendar calendarID.
      The default is 'primary'.

  Returns
  -------
  None.
  
  Example
  -------

  event = {
    'summary': 'Google I/O 2015',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
      'dateTime': '2015-05-28T09:00:00-07:00',
      'timeZone': 'America/Chicago',
    },
    'end': {
      'dateTime': '2015-05-28T17:00:00-07:00',
      'timeZone': 'America/Chicago',
    },
    'recurrence': [
      'RRULE:FREQ=DAILY;COUNT=2'
    ],
    'attendees': [
      {'email': 'lpage@example.com'},
      {'email': 'sbrin@example.com'},
    ],
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
      ],
    },
  }
  
  '''
  try:
    service = build("calendar", "v3", credentials=creds)

    start_formatted = start.isoformat()
    end_formatted = end.isoformat()

    reminders = {}
    if reminder_overrides:
      reminders['useDefault'] = False
      reminders['overrides'] = reminder_overrides
    else:
      reminders['useDefault'] = True

    event = {
      'summary': summary,
      'location': location,
      'description': description,
      'start': {
        'dateTime': start_formatted,
        'timeZone': timezone,
      },
      'end': {
        'dateTime': end_formatted,
        'timeZone': timezone,
      },
      'recurrence': 
        recurrance
      ,
      'attendees': 
        attendees
      ,
      'reminders':
        reminders
      ,
    }

    event = service.events().insert(calendarId=calendarId, body=event).execute()
    print('Event created: ',(event.get('htmlLink')))

  except HttpError as error:
    print(f"An error occurred: {error}")

#%% Utilities

def get_creds(filepath_to_credentials:str) -> Credentials:
  '''
  Accesses user credentials and caches them in token.json.
  
  Parameters
  ----------
  filepath_to_credentials : str
      A system filepath to credentials.json file. If no credentials.json
      exists, will create a credentials.json at this location.
  
  Returns
  -------
  Credentials
      Credentials from google.oauth2.credentials
  
  '''
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  else:
    creds = None
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          filepath_to_credentials, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds # type: ignore