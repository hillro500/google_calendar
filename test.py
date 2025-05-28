import google_calendar_helper as gch

def get_10_calendar_events():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = gch.get_creds('credentials.json')

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
    
  print("Program completed successfully.")

#%% Main

def main():
  get_10_calendar_events()

if __name__ == "__main__":
  print("Testing Google Calendar Helper")
  print("====================================")
  main()
