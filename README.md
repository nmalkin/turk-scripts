Administrative scripts
======================

This directory contains a mishmash of scripts to administer the project's
SurveyGizmo surveys and Mechanical Turk HITs and qualifications.

If you have Docker, you can run them (with the dependencies containerized):

    make
    ./run ./check_balance

Before doing this, you need to have the API keys for the respective services.

For MTurk, you need an `mturkconfig.json` in the [format described
here](https://github.com/nmalkin/mturk-python). For SurveyGizmo, you should have
a `surveygizmo.sh` that `export`s `SURVEYGIZMO_API_KEY` with your API key.
