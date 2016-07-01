
An agenda view for Google Calendars that I would enjoy a little better. For starters, it would look nicer on mobile. The default agenda view is
not bad, but there are a few things I'd like to change.

Example for the default view: http://bit.ly/ehtesh-music

Looked at the Calendar API and came across this [useful API call][1]:

    GET
    https://www.googleapis.com/calendar/v3/calendars/afjfh167jal8h60e2lgnolitcc%40group.calendar.google.com/events?timeMax=2016-07-05T10%3A00%3A00Z&timeMin=2016-06-28T10%3A00%3A00Z&key={YOUR_API_KEY}

To get started:

    # activate your virtualenv
    pip install -r requirements.txt
    python server-2lo.py
    # point browser to http://localhost:5000/


----

[1]: https://developers.google.com/google-apps/calendar/v3/reference/events/list
