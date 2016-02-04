import os
import raven

sentry_url = os.getenv('SENTRY_URL')
if sentry_url:
    sentry = raven.Client(sentry_url)
