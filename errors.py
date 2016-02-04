import os
import raven

sentry_url = os.getenv('SENTRY_URL')
if sentry_url:
    sentry = raven.Client(dsn=sentry_url, release=raven.fetch_git_sha(os.path.join(os.path.dirname(__file__), os.pardir)))
