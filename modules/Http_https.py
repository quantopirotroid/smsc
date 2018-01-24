import os
#import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

import requests
from requests import Request, Session
from jinja2 import Environment, FileSystemLoader
from easydict import EasyDict as ed


class ReqSender():
    ''''''
    def __init__(self):
        self.__templates = {}
        self.__text = None
        self.__personal = None
        self.__body = None
        self.__request = None
        self.__response = None
    def request_builder(self, req_type, url, post_body=None):
        if self.__body and not post_body:
            post_body = self.__body
            req = Request(req_type, url, data=post_body)
            prepared = req.prepare()
            self.__request = prepared
            return prepared
        elif post_body:
            req = Request(req_type, url, data=post_body)
            prepared = req.prepare()
            self.__request = prepared
            return prepared
    def load_template(self, td, template):
        loader = FileSystemLoader(td)
        env = Environment(loader=loader)
        loaded_template = env.get_template(template)
        self.__templates[template] = loaded_template
        return template
    def response_logger(self, log_dir, file_name):
        os.chdir(log_dir)
        current_time = datetime.now().strftime('%Y-%m-%d-%m:%S')
        xml_string = self.__response.content.decode('utf-8')
        xml_root = ET.fromstring(xml_string)
        if self.__response.status_code == 200:
            logged_text = ('{}, '
                           'INFO: Status_code:{}, '
                           'SMS_ID:{}\n').format(
                                               current_time,
                                               self.__response.status_code,
                                               xml_root[0][0].get('sms_id')
                                               )
        else:
            logged_text = 'ERROR:\n{}'.format(xml_string+'\n')
        with open(file_name, 'a') as log:
            log.write(logged_text)
    def template_render(self, variables_dict, t_names_dict):
        if variables_dict.name == 'text':
            text = self.__templates[t_names_dict.text].render(variables_dict)
            self.__text = text
        if variables_dict.name == 'body' and self.__text:
            variables_dict.text_sms = self.__text
            body = self.__templates[t_names_dict.body].render(variables_dict)
            self.__body = body.encode('utf-8')
    def send_request(self):
        if self.__request:
            session = Session()
            self.__response = session.send(self.__request)



if __name__ == '__main__':
    print('Do not use me separately!')
