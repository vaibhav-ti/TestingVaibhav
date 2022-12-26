#!/bin/bash
python -m pip install --upgrade pip
pip install -r requirements.txt
export PYTHONPATH='.'
export DEBUG=true
pylint --load-plugins pylint_django,pylint_django.checkers.migrations --django-settings-module={{cookiecutter.project.slug}}.settings --fail-under=6 ./*