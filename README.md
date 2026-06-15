# Overview

I created this project because I was in a number of different leagues through USTA, and each one had 10+ matches.
Occassionally I would forget about matches since there were so many to keep track of, and I knew I needed a good
tool to help me do that. I was already very familiar with Google Calendar, began using it and including important 
information such as Home or Away, and location and time. It also allowed me to get reminders on my phone.

Despite this, the process of adding the events including all the relevant information was *very slow*. I turned 
to python to save time. I used the *Google Calendar API* (see links below) as a starting point to interface with 
Google Calendar, and developed my own code that could read in my matches as a *pandas dataframe* from the USTA.com 
website. **Now, I just copy my schedule into a text file, and run my code, and my calendar has all the**
**information I need!**

## Modules

### `google_calendar_helper.py`

This is the backbone of the code that allows for interaction with the user's google calendar.

- `create_events()` 
    - to create calendar events
- `get_creds()` 
    - pulls the users calendar credentials

### `add_usta_league_calendar.py`

This is the part of the code that loads in the tennis schedule, formats it as a dataframe,
and prepares each row as an event to be added to the calendar.

#### Utilities

- `read_csv()`
    - reads in a csv
- `unscramble_csv()`
    - takes a dataframe of a .csv that has been read in from the USTA.com website 
    and formats it appropriately
- `replace_nans()`
    - takes two rows from the .csv dataframe and determines which `np.NaN` columns to replace

#### Google Calendar

- `create_event_df()`
    - takes formatted .csv and prepares a dataframe of events
- `create_events_from_event_df()`
    - uses `event_df` to create events in Google Calendar

#### Main

- `add_schedule_to_calendar()`
    - Main call function

## Pre-requisites

1. Complete the Google API setup steps https://developers.google.com/workspace/calendar/api/quickstart
    - For help, see *Help with Google API Quickstart Guide* section under *Resources and Helpful Links*
2. Get USTA schedule from website: https://tennislink.usta.com/
    1. Login to USTA.com and go to the tennislink website
    2. Navigate to your league and click the **Match Schedule** tab
    3. Copy the schedule, inlcuding the column headers and paste to a text document.
    4. Save the text document in a location you remember and close it.
3. Pull down this google_calendar repo into your workspace.

## How to use

1. Run test.py to ensure connection to Google Calendar is working.
2. Follow the instructions to login to Google Calendar
3. Create a Main.py file that looks something like this:

```python
from add_usta_league_calendar import add_schedule_to_calendar

schedule = r"C:\PATH_TO_SCHEDULE.txt"
my_team = "NAME_OF_TEAM_IN_SCHEDULE"
creds_path = r"PATH_TO_\credentials.json"
calendarId = 'primary' # or None (calendarID of Google Calendar)

if __name__ == "__main__":
    add_schedule_to_calendar(schedule, my_team, creds_path, calendarId)
```
4. Run the code
5. Input your selection in your console of whether you want to add the printed calendar to your Google Calendar

# Resources and Helpful Links

Google Calendar Quickstart
https://developers.google.com/workspace/calendar/api/quickstart/python

Google Calendar Events API
https://developers.google.com/workspace/calendar/api/v3/reference/events

Google Calendar API Guides
https://developers.google.com/workspace/calendar/api/guides/create-events

Google Auth Platform
https://console.cloud.google.com/auth/

Google's Python Workspace on GitGub 
https://github.com/googleworkspace/python-samples

Markdown (.md) Guide
https://www.markdownguide.org/basic-syntax/

## Help with Google API Quickstart Guide

The python quickstart guide will explain the steps to setup a google cloud application and install 
a necessary python environment and packages. Click the link below and follow the instructions:

https://developers.google.com/workspace/calendar/api/quickstart

When Completing the **Prequisites** section:
1. Setup Google Developer Project: https://developers.google.com/workspace/guides/create-project
2. Create an app/project and add yourself as a client to that project

    *NOTE: Login to Google Auth Platform: https://console.cloud.google.com/auth/ to manage projects*

When completing **Set up your environement** section, under **Authorize credentials for a desktop application** 
remember where you save the `credentials.json` file. It will be important later. Also worth noting *a local copy*
*of this file is required to connect to the google app.* Each time a user logs in at a different location, they will 
need to either a copy of the original `credentials.json` or create a new client json.

Complete the **Install the Google client library** section by pip installing the google library and copying and 
pasting the code below into your terminal:

```
python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

*OPTIONAL: Complete **Configure the Sample** section Finish the instructions to verify API is working*
*correctly.*
