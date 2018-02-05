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


EXTERNAL_URL_QUESTION = """<?xml version="1.0"?>
<ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
    <ExternalURL>{}</ExternalURL>
    <FrameHeight>1000</FrameHeight>
</ExternalQuestion>
"""


def get_question(url):
    """
    Return a Question string for an External URL HIT pointing to the given URL.
    """
    return EXTERNAL_URL_QUESTION.format(url)


class MTurkScript:
    """
    A class that allows easy access to a MTurk client.
    https://boto3.readthedocs.io/en/latest/reference/services/mturk.html
    """

    def __init__(self):
        parser = self.get_parser()
        self.args = parser.parse_args()
        self.client = self.get_client()

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

    def get_client(self):
        """
        Get the client that connects to the MTurk API. Uses the sandbox if the
        --debug flag was set.
        """
        return get_client(not self.args.production)

    def run(self):
        """
        Run this script
        """
        pass


class QualificationType(object):
    """
    An Enum for QualificationTypeId constants
    https://github.com/nmalkin/mturk-python/blob/master/mturk/mturk.py#L16
    """
    P_SUBMITTED = "00000000000000000000"
    P_ABANDONED = "00000000000000000070"
    P_RETURNED = "000000000000000000E0"
    P_APPROVED = "000000000000000000L0"
    P_REJECTED = "000000000000000000S0"
    N_APPROVED = "00000000000000000040"
    LOCALE = "00000000000000000071"
    ADULT = "00000000000000000060"
    S_MASTERS = "2ARFPLSP75KLA8M8DH1HTEQVJT3SY6"
    MASTERS = "2F1QJWKUDD8XADTFD2Q0G6UTO95ALH"
    S_CATMASTERS = "2F1KVCNHMVHV8E9PBUB2A4J79LU20F"
    CATMASTERS = "2NDP2L92HECWY8NS8H3CK0CP5L9GHO"
    S_PHOTOMASTERS = "2TGBB6BFMFFOM08IBMAFGGESC1UWJX"
    PHOTOMASTERS = "21VZU98JHSTLZ5BPP4A9NOBJEK3DPG"


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
