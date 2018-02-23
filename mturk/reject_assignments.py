#!/usr/bin/env python

import abc
import logging

import mturk
import logger

logger.init('info')


class RejectAssignmentsScript(abc.ABC, mturk.MTurkScript):
    """
    Abstract script to remove specified assignments for HIT

    All implementations need to do is implement the FEEDBACK property,
    specifying which manage to send workers when their assignments are being rejected.
    """

    @property
    @abc.abstractmethod
    def FEEDBACK(self):
        ...

    def get_parser(self):
        parser = super().get_parser()
        parser.add_argument('--input-file', '-i',
                            required=True, action='store')
        return parser

    def run(self):
        with open(self.args.input_file) as assignment_file:
            for line in assignment_file:
                assignment_id = line.strip()
                logging.info('rejecting assignment %s', assignment_id)
                self.client.reject_assignment(AssignmentId=assignment_id,
                                              RequesterFeedback=self.FEEDBACK)
