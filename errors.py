from os import getenv
from raven import Client

sentry_url = getenv('SENTRY_URL')
if sentry_url:
    sentry = Client(sentry_url)
