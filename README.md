Mechanical Turk scripts
=======================

This directory contains a mishmash of scripts written
to make it easier to run and review tasks on Amazon Mechanical Turk.

Prerequisites
-------------
You'll need to [set up your AWS credentials](https://boto3.readthedocs.io/en/latest/guide/configuration.html).


Installation
-------------
```
pip install git+https://github.com/nmalkin/turk-scripts.git
```

Usage
-----
The following scripts are available:

- approve_assignments
- assign_qualification
- check_balance
- create_additional_assignments
- create_qualification
- delete_qualification
- get_column_from_csv
- intersect
- list_hit_assignments
- list_qualification_types
- list_workers_with_qualification_type
- really_delete_hit
- remove_qualification
- print_hit_workers
- print_submitted_assignments
- subtract

Please see each of those files for detailed usage instructions.
