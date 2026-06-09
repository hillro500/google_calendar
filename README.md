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

## Setup

Create an app and add yourself as a client:

Google Auth Platform/Clients
https://console.cloud.google.com/auth/

## How to use

Note: 
> Each time a user logs in at a different location, they will need to create a new client. 
An alternative solution would be sharing the credentials.json file that was origninally created.

# Resources

These are some helpful resources used in making this project:

Google Calendar Events API
https://developers.google.com/workspace/calendar/api/v3/reference/events

Google Calendar API Guides
https://developers.google.com/workspace/calendar/api/guides/create-events

Google Auth Platform/Clients
https://console.cloud.google.com/auth/clients?inv=1&invt=Ab0qMA&project=usta-tennis-454822&pli=1

Google's Python Workspace on GitGub 
https://github.com/googleworkspace/python-samples

Markdown (.md) Guide
https://www.markdownguide.org/basic-syntax/
