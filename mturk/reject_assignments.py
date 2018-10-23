#!/usr/bin/env python

import abc
import logging

import mturk
import mturk.logger as logger

logger.init('info')


class RejectAssignmentsScript(abc.ABC, mturk.MTurkScript):
    """
    Abstract script to reject specified assignments for HIT

    All implementations need to do is implement the FEEDBACK property,
    specifying which message to send workers when their assignments are being rejected.

    For example:

    class MyRejectionScript(RejectAssignmentsScript):
        self.FEEDBACK = 'Sorry…'
    
    Then run this script, providing as an argument the name of a file with 
    the assignmentIds to be rejected, one per line.
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
