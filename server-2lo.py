import json
from httplib2 import Http

from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import client
from apiclient import discovery

import flask
from flask import render_template
from flask.ext.cache import Cache # TODO deprecated?
import uuid

app = flask.Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

# reference: https://developers.google.com/identity/protocols/OAuth2ServiceAccount

scopes = ['https://www.googleapis.com/auth/calendar.readonly']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gcal-agenda-view-4deaf3bca396.json', scopes=scopes)
http_auth = credentials.authorize(Http())
calendar_service = discovery.build('calendar', 'v3', http_auth)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
@cache.cached(timeout=60)
def events():
    print('am I cached? no')
    all_events = []

    try:
        page_token = None
        while True:
            events = calendar_service.events().list(calendarId="afjfh167jal8h60e2lgnolitcc@group.calendar.google.com", pageToken=page_token).execute()
            all_events.extend(events['items'])
            # print(json.dumps(events, indent=2))
            # for calendar_list_entry in calendar_list['items']:
                # print(calendar_list_entry['summary'])
            page_token = events.get('nextPageToken')
            if not page_token:
                break
                page_token = None

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')
    return flask.jsonify(all_events)


if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())
    app.debug = True
    app.run()
