import abc
import logging

from .mturk import MTurkScript

EXTERNAL_URL_QUESTION = """<?xml version="1.0"?>
<ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
    <ExternalURL>{}</ExternalURL>
    <FrameHeight>600</FrameHeight>
</ExternalQuestion>
"""


def get_question(url):
    """
    Return a Question string for an External URL HIT pointing to the given URL.
    """
    return EXTERNAL_URL_QUESTION.format(url)


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


class CreateHit(abc.ABC, MTurkScript):
    """
    Abstract script for HIT creation

    Includes common code for handling qualifications,
    however the actual HIT creation, with the HIT's real details,
    must be done in a subclass
    """

    MINIMUM_PERCENTAGE_APPROVED = 95

    def get_parser(self):
        parser = super().get_parser()
        parser.add_argument('--exclude-qualification', action='append',
                            help='Qualification ID of qualification that excludes participation in this HIT')
        parser.add_argument('--include-qualification', action='append',
                            help='Qualification ID of qualification that is necessary participation in this HIT')
        parser.add_argument('--hit-type', '-t',
                            help='The HITTypeId to use. If specified, the HIT will be created using the CreateHITWithHITType operation.')
        return parser

    def get_qualifications(self):
        qualifications = [
            {
                'QualificationTypeId': QualificationType.LOCALE,
                'Comparator': 'EqualTo',
                'LocaleValues': [{
                    'Country': 'US',
                }],
                'RequiredToPreview': True,
            },
            {
                'QualificationTypeId': QualificationType.P_APPROVED,
                'Comparator': 'GreaterThan',
                'IntegerValues': [self.MINIMUM_PERCENTAGE_APPROVED],
                'RequiredToPreview': True,
            },
        ]

        exclude = self.args.exclude_qualification
        if exclude is not None:
            for qualification_id in exclude:
                logging.debug(
                    'excluding workers with qualification %s', qualification_id)
                qualifications.append({
                    'QualificationTypeId': qualification_id,
                    'Comparator': 'DoesNotExist',
                    'RequiredToPreview': True,
                })

        include = self.args.include_qualification
        if include is not None:
            for qualification_id in include:
                logging.debug(
                    'allowing workers with qualification %s', qualification_id)
                qualifications.append({
                    'QualificationTypeId': qualification_id,
                    'Comparator': 'Exists',
                    'RequiredToPreview': True,
                })

        return qualifications

    def create_hit(self, **kwargs):
        if self.args.hit_type:
            self.logger.info(
                'creating HIT using HITTypeId %s. Title, Description, Reward, and Keywords from calling script will be ignored.', self.args.hit_type)
            new_args = {arg: kwargs[arg] for arg in [
                'LifetimeInSeconds', 'MaxAssignments', 'Question']}
            new_args.update(HITTypeId=self.args.hit_type)
            response = self.client.create_hit_with_hit_type(**new_args)
        else:
            response = self.client.create_hit(**kwargs)
        return response

    @abc.abstractmethod
    def run(self):
        ...
