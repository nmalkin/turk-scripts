Mechanical Turk scripts
=======================

This directory contains a mishmash of scripts written, at one point or another,
to make it easier to run and review tasks on Amazon Mechanical Turk.

Prerequisites
-------------
First, you'll want to install the [mturk-python][mturk-python] library.

```sh
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

You will also need an `mturkconfig.json` in the current working directory,
using the [format described here][mturk-python].


[mturk-python]: https://github.com/nmalkin/mturk-python
