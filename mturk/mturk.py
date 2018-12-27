"""
MTurk utilities
"""

import argparse
import logging

import boto3

ENDPOINT_URL = 'https://mturk-requester{}.us-east-1.amazonaws.com'

LOGGER = logging.getLogger(__name__)


def get_client(sandbox=True):
    """
    Get the client that connects to the MTurk API. Uses the sandbox if the
    --debug flag was set.
    """
    LOGGER.info(f"{'' if sandbox else 'NOT '}using MTurk sandbox")

    url = ENDPOINT_URL.format('-sandbox' if sandbox else '')
    return boto3.client(
        'mturk',
        endpoint_url=url,
        region_name='us-east-1',
    )


class MTurkScript:
    """
    A class that allows easy access to a MTurk client.
    https://boto3.readthedocs.io/en/latest/reference/services/mturk.html
    """

    def __init__(self):
        parser = self.get_parser()
        self.args = parser.parse_args()
        self._client = None

        # Create a logger that can be used within the class
        self.logger = logging.getLogger(type(self).__name__)

    def get_description(self):
        """
        Get the script's description, to be shown as CLI help text
        """
        if hasattr(self, 'DESCRIPTION'):
            return getattr(self, 'DESCRIPTION')
        return self.__doc__

    def get_parser(self):
        """
        Get the parser used for the script's command-line arguments

        Override this method in an MTurkScript to add extra arguments
        """
        parser = argparse.ArgumentParser(description=self.get_description())
        parser.add_argument('--production', action='store_true',
                            help='If set, use the live version of MTurk, instead of the sandbox')
        return parser

    @property
    def client(self):
        """
        Get the client that connects to the MTurk API.
        Initializes it if that hasn't happened yet.
        Uses the sandbox if the --debug flag was set.
        """
        if self._client is None:
            self._client = get_client(not self.args.production)

        return self._client

    def run(self):
        """
        Run this script
        """
        pass


def get_pages(action, response_keyword, **kwargs):
    """
    Helps return paginated MTurk responses

    The action is the MTurk API call to make.
    This function will call it repeatedly, as long a NextToken is returned,
    indicating that there are more pages of responses.

    Within each page, this function will sequentially yield every item under
    the specified keyword in the response.
    """
    response = action(**kwargs)
    if response_keyword not in response:
        logging.error('%s not in response %s', response_keyword, response)

    for item in response[response_keyword]:
        yield item

    while 'NextToken' in response:
        kwargs.update({'NextToken': response['NextToken']})
        response = action(**kwargs)
        for item in response[response_keyword]:
            yield item
