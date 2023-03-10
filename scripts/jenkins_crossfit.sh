#!/bin/bash -e

pyenv shell 3.10.10

# Create and activate virtualenv
python3 -m venv .venv 2>&1 >> pyprocesses.log
source .venv/bin/activate 2>&1 >> pyprocesses.log

# Install requirements
pip install -r scripts/requirements.txt 2>&1 >> pyprocesses.log

scripts/get_crossfit_spot.py	-u ${USER_BEMADBOX} \
								-p ${PASSWORD_BEMADBOX} \
                                -l INFO

# Configuration in build steps of jenkins 
# pyenv shell 3.10.10