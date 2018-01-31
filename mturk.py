import argparse
import json

import boto3

ENDPOINT_URL = 'https://mturk-requester{}.us-east-1.amazonaws.com'


def get_client(sandbox=True):
    """
    Get the client that connects to the MTurk API. Uses the sandbox if the
    --debug flag was set.
    """
    url = ENDPOINT_URL.format('-sandbox' if sandbox else '')
    return boto3.client(
        'mturk',
        endpoint_url=url,
        region_name='us-east-1',
    )


def get_worker_ids(filename):
    """
    Get the worker_ids contained in the given JSON file.
    """
    worker_ids = []
    with open(filename, 'r') as f:
        worker_ids = [
            row['worker_id']
            for row in json.load(f)
        ]
    return worker_ids


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


class MTurkScript(object):
    """
    A class that allows easy access to a MTurk client.
    https://boto3.readthedocs.io/en/latest/reference/services/mturk.html
    """
    DESCRIPTION = 'An MTurk script'

    def __init__(self):
        parser = self.get_parser()
        self.args = parser.parse_args()
        self.client = self.get_client()

    def get_parser(self):
        parser = argparse.ArgumentParser(description=self.DESCRIPTION)
        parser.add_argument('-d', '--debug', action='store_true',
                            help='If set, use the sandbox API')
        return parser

    def get_client(self):
        """
        Get the client that connects to the MTurk API. Uses the sandbox if the
        --debug flag was set.
        """
        return get_client(self.args.debug)

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
