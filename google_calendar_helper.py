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

def get_10_calendar_events():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = get_creds('credentials.json')

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = dt.datetime.now(tz=dt.timezone.utc).isoformat() #had to remove code to make this work
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")

#%% Utilities

def get_creds(filepath_to_credentials:str) -> Credentials:
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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

def create_event(creds:Credentials,
                 summary:str, 
                 start:dt.datetime, 
                 end:dt.datetime, 
                 location:str='', 
                 description:str='', 
                 recurrance:str='', 
                 timezone='America/Chicago',
                 attendees:list[dict]=[], 
                 reminder_overrides:list[dict]=[],
                 calendarId:str='primary'):
  # Refer to the Python quickstart on how to setup the environment:
  # https://developers.google.com/workspace/calendar/quickstart/python
  # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
  # stored credentials.

  # EXAMPLE:
  # event = {
  #   'summary': 'Google I/O 2015',
  #   'location': '800 Howard St., San Francisco, CA 94103',
  #   'description': 'A chance to hear more about Google\'s developer products.',
  #   'start': {
  #     'dateTime': '2015-05-28T09:00:00-07:00',
  #     'timeZone': 'America/Chicago',
  #   },
  #   'end': {
  #     'dateTime': '2015-05-28T17:00:00-07:00',
  #     'timeZone': 'America/Chicago',
  #   },
  #   'recurrence': [
  #     'RRULE:FREQ=DAILY;COUNT=2'
  #   ],
  #   'attendees': [
  #     {'email': 'lpage@example.com'},
  #     {'email': 'sbrin@example.com'},
  #   ],
  #   'reminders': {
  #     'useDefault': False,
  #     'overrides': [
  #       {'method': 'email', 'minutes': 24 * 60},
  #       {'method': 'popup', 'minutes': 10},
  #     ],
  #   },
  # }
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

#%% Main

def main():
  get_10_calendar_events()

if __name__ == "__main__":
  main()
