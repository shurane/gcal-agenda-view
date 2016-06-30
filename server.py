import json

import flask
import uuid
import httplib2

from apiclient import discovery
from oauth2client import client


app = flask.Flask(__name__)


@app.route('/')
def index():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        calendar_service = discovery.build('calendar', 'v3', http_auth)


        try:
            page_token = None
            while True:
                events = calendar_service.events().list(calendarId="afjfh167jal8h60e2lgnolitcc@group.calendar.google.com").execute()
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


    return "{}"


@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
      'client_secrets.json',
      scope='https://www.googleapis.com/auth/calendar.readonly',
      redirect_uri=flask.url_for('oauth2callback', _external=True))
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
    app.secret_key = str(uuid.uuid4())
    app.debug = True
    app.run()


# I somehow cobbled this together from these sources:
# Also the Google API docs are trash.
# https://developers.google.com/api-client-library/python/auth/web-app#example
# https://developers.google.com/google-apps/calendar/v3/reference/events/list#parameters
# https://github.com/google/google-api-python-client/blob/master/samples/calendar_api/calendar_sample.py
