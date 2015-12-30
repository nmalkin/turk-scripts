import os

import mturk

import logger

turk = mturk.MechanicalTurk()

def get_assignments(hit_id, status):
    assert status in {'Submitted', 'Approved', 'Rejected'}

    page = 1
    results_available = True
    while results_available:
        response = turk.request('GetAssignmentsForHIT', {
                'Operation': 'GetAssignmentsForHIT',
                'HITId': hit_id,
                'AssignmentStatus': status,
                #'PageSize': 1, # debug
                'PageNumber': page})

        result = response['GetAssignmentsForHITResponse']['GetAssignmentsForHITResult']
        logger.debug(result)
        num_results = int(result['NumResults'])
        results_available = num_results > 0

        if results_available:
            assignments = result['Assignment']
            if num_results == 1: # assignments is actually just a single object
                yield assignments
            else: # assignments is a list
                for assignment in assignments:
                    yield assignment

        page += 1

def repeat_with_confirmation(operation, iterable):
    """
    Perform `operation` on each item in `iterable`, as long as the user approves
    """
    auto_approve = os.getenv('TURK_AUTO_APPROVE') == '1'
    logger.info('auto approve is %s' % 'on' if auto_approve else 'off')

    for item in iterable:
        if auto_approve:
            operation(item)

        invalid_response = True
        while invalid_response:
            confirmation = input('Approve %s? (y/n/a[pprove all]/s[top]) ' % item)

            invalid_response = False
            if confirmation == 'y':
                operation(item)
            elif confirmation == 'a':
                auto_approve = True
                operation(item)
            elif confirmation == 'n':
                pass
            elif confirmation == 's':
                return
            else:
                invalid_response = True
