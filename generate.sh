#!/usr/bin/python3

import json
import logging
import os

logger = logging.getLogger(__name__)

try:
  from cookiecutter.main import cookiecutter
except:
  os.system("/usr/bin/python3 -m pip install cookiecutter")
  from cookiecutter.main import cookiecutter

dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, "config.json")
try:
    context = json.load(open(config_path))
    repo_url = context['template']['base_repo']
    tag_name = context['template']['tag_name']
    logger.info("Loaded config from %s", config_path)
    cookiecutter(
        repo_url, no_input=True,
        overwrite_if_exists=True,
        extra_context=context,
        checkout=tag_name
    )
    logger.info("Django Project generated successfully using Cookiecutter")
except Exception as e:
    logger.error(e)
