import os
import raven

import logger

sentry_url = os.getenv('SENTRY_URL')
if sentry_url:
    sentry = raven.Client(sentry_url)
else:
    logger.warning('running without Sentry logging')
