import os, re
import datetime as dt
import pandas as pd
import numpy as np
from pytz import timezone

import google_calendar_helper as gch

#%% Utilities

def read_csv(filepath) -> pd.DataFrame:
    filepath = os.path.join(filepath)
    return pd.read_csv(filepath, sep='\t')

def unscramble_csv(df:pd.DataFrame):
    entries = []
    corrected_series = pd.Series(index=df.columns).astype(str)

    for idx, row in df.iterrows():
        len_row = len(row[~row.isna()])
        if len_row == 1:
            len_corrected = len(corrected_series[~corrected_series.isna()])
            if len_corrected == 2:
                corrected_series = replace_nans(corrected_series, row, split_row=True)
            elif len_corrected > 2 and len_corrected < 8:
                _print_debug_info(row, corrected_series)
            else:
                if not corrected_series.isna().all():
                    entries.append(corrected_series)
                    corrected_series = pd.Series(index=df.columns).astype(str)
                corrected_series['Match ID'] = row['Match ID']
        elif len_row  == 3:
                if len(corrected_series[~corrected_series.isna()]) == 1:
                    corrected_series = replace_nans(corrected_series, row, split_row=False)
                else:
                    corrected_series = replace_nans(corrected_series, row, split_row=True)
        elif len_row == 5:
            if len(corrected_series[~corrected_series.isna()]) == 4:
                    corrected_series = replace_nans(corrected_series, row, split_row=True)
            else:
                corrected_series = replace_nans(corrected_series, row, split_row=False)
        elif len_row == 7:
            corrected_series = replace_nans(corrected_series, row, split_row=False)
        else:
            _print_debug_info(row, corrected_series)
    
    df = pd.DataFrame(columns=df.columns)
    for entry in entries:
        to_merge = pd.DataFrame([entry.values], columns=entry.index)
        df = pd.concat([df, to_merge], ignore_index=True)

    return df

def replace_nans(row_with_nans:pd.Series, replacement_row:pd.Series, split_row:bool=False) -> pd.Series:
    pd.testing.assert_index_equal(row_with_nans.index, replacement_row.index)
    columns = row_with_nans.index
    combined = pd.Series(index=columns).astype(str)

    non_na_1 = len(row_with_nans[~row_with_nans.isna()])
    non_na_2 = len(replacement_row[~replacement_row.isna()])

    # Make Map of Columns
    col_map = {}
    i = 0
    for col in list(columns):
        col_map[i] = col
        i += 1

    if split_row:
        for i in range(non_na_1 - 1):
            combined[col_map[i]] = row_with_nans[col_map[i]]

        split1 = row_with_nans[col_map[non_na_1 - 1]]
        split2 = replacement_row[col_map[0]]

        # if characters are mismatching no space between them
        if re.match(r'\w\W|\W\w', split1[-1] + split2[0]):
            combined[col_map[non_na_1 - 1]] = split1 + split2
        else:
            combined[col_map[non_na_1 - 1]] = split1 + ' ' + split2
        for i in range(non_na_1, non_na_1 + non_na_2 - 1): #subtract out the duplicate column on split
            combined[col_map[i]] = replacement_row[col_map[i - non_na_1 + 1]]
    else:
        for i in range(non_na_1):
            combined[col_map[i]] = row_with_nans[col_map[i]]
        for i in range(non_na_1, non_na_1 + non_na_2):
            combined[col_map[i]] = replacement_row[col_map[i - non_na_1]]
    
    return pd.Series(combined)

def _print_debug_info(row:pd.Series, corrected_series:pd.Series) -> Exception:
    print('Lenght of row: ', len(row[~row.isna()]))
    print('Length so far: ', len(corrected_series[~corrected_series.isna()]))
    print('Row so far: \n', corrected_series)
    print('Broken row: \n', row)
    return Exception("Weird split here, you're gonna have to do some coding.")

#%% Calendar Functions

def create_event_df(df:pd.DataFrame, my_team) -> pd.DataFrame:
    event_df = pd.DataFrame()

    b = df['Schedule Time'].str.contains('R') # skip matches that have been rescheduled.

    event_df['Start'] = pd.to_datetime(df['Schedule Date'][~b] + ' ' + df['Schedule Time'][~b], format ='%m/%d/%Y %I:%M %p').apply(lambda x: timezone('America/Chicago').localize(x)) # type: ignore
    event_df['End'] = event_df['Start'].apply(lambda x: x + dt.timedelta(hours=2))
    event_df['Location'] = df['Facility/Match Site'][~b]
    for idx, row in df[~b].iterrows():
        if my_team == row['Home Team']:
            event_df.at[idx, 'Summary'] = row['Captain/Phone.1'].split(' ')[1] + ' @ ' + row['Captain/Phone'].split(' ')[1] + ' HOME' # type: ignore
            event_df.at[idx,'Description'] = row['Home Team'] + ' HOME match, bring balls.' # type: ignore
        else:
            event_df.at[idx, 'Summary'] = row['Captain/Phone.1'].split(' ')[1] + ' @ ' + row['Captain/Phone'].split(' ')[1] + ' AWAY' # type: ignore
            event_df.at[idx,'Description'] = row['Visiting Team'] + ' AWAY match' # type: ignore
    return event_df
    # if you only want matches that haven't happened yet.
    # return event_df[event_df['Start'] > dt.datetime.now(tz=timezone('America/Chicago'))]

def create_events_from_event_df(event_df, creds_path='credentials.json', calendarId='primary'):
    creds = gch.get_creds(creds_path)

    reminder_overrides = [{'method': 'popup', 'minutes': 24 * 60},
                          {'method': 'popup', 'minutes': 2 * 60}]

    for idx, row in event_df.iterrows():
        gch.create_event(creds,
                         row['Summary'],
                         row['Start'],
                         row['End'],
                         location=row['Location'],
                         description=row['Description'],
                         reminder_overrides=reminder_overrides,
                         calendarId=calendarId
                         )

#%% Main

def add_schedule_to_calendar(filepath, my_team, creds_path, calendarId):
    df = read_csv(filepath)
    scrambled = False
    # if text file has not already been formatted, format text file.
    if df['Facility/Match Site'].isna().any():
        df = unscramble_csv(df)
        scrambled = True
    event_df = create_event_df(df, my_team)
    print('Event DataFrame:')
    print(event_df)
    print()
    add = input('Do you want to add events to calender? Y/N: ')
    if add.lower().strip() == 'y' or add.lower().strip() == 'yes':
        create_events_from_event_df(event_df, creds_path=creds_path)
        if scrambled:
            df.to_csv(filepath, index=False, sep='\t')
    elif add.lower().strip() == 'n' or add.lower().strip() == 'no':
        return
    else:
        print('unrecognized input')