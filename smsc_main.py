#!/bin/env python3.6
#-*- coding: utf-8 -*-

import os
from pathlib import Path
import json

from requests import Session, Request
from jinja2 import Environment, FileSystemLoader

from easydict import EasyDict as ed
from modules.Http_https import ReqSender
from modules.argument_parser import create_config, check_config
from config import *
from credentials import *

os.chdir(WORK_DIR)
r_method = 'POST'
raw_config = create_config()
text_variables = ed({'name': 'text', 'server': None, 'alert': None})
body_variables = ed({'name': 'body', 'SMSC_LOGIN': SMSC_LOGIN,
                     'SMSC_PASS': SMSC_PASS, 'DEF_SENDER': DEF_SENDER,
                     'phone_number': None, 'text_sms': None})
template_names = ed({'text': 'zabbix_text.j2', 'body': 'smsc_body.j2'})


if __name__ == "__main__":
    if raw_config.zabbix:
       r_sender = ReqSender()
       r_sender.load_template(TEMPLATES, template_names.text)
       r_sender.load_template(TEMPLATES, template_names.body)
       text_variables.server = raw_config.server
       text_variables.alert = raw_config.status
       body_variables.phone_number = raw_config.phone
       r_sender.template_render(text_variables, template_names)
       r_sender.template_render(body_variables, template_names)
       r_sender.request_builder(r_method, SMSC_URL)
       r_sender.send_request()
       r_sender.response_logger(LOG_DIR, LOG_FILE)
