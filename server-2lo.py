import json
from httplib2 import Http

from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery

scopes = ['https://www.googleapis.com/auth/calendar.readonly']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gcal-agenda-view-4deaf3bca396.json', scopes=scopes)
http_auth = credentials.authorize(Http())
calendar_service = discovery.build('calendar', 'v3', http_auth)


all_events = []

try:
    page_token = None
    while True:
        events = calendar_service.events().list(calendarId="afjfh167jal8h60e2lgnolitcc@group.calendar.google.com", pageToken=page_token).execute()
        print(json.dumps(events, indent=2))
        # for calendar_list_entry in calendar_list['items']:
            # print(calendar_list_entry['summary'])
        page_token = events.get('nextPageToken')
        if not page_token:
            break
            page_token = None

except client.AccessTokenRefreshError:
    print('The credentials have been revoked or expired, please re-run'
          'the application to re-authorize.')
