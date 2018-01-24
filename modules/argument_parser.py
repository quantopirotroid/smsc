import re
from validators import email as mail_check
import sys
import argparse


def create_config():
    ''''''
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', default=None)
    parser.add_argument('-m', '--mail', default=None)
    parser.add_argument('-p', '--phone', default=None)
    parser.add_argument('-S', '--server', default=None)
    parser.add_argument('-s', '--status', default=None)
    parser.add_argument('-z', '--zabbix',
                        action='store_const',
                        const=True, default=None)
    parser.add_argument('-b', '--bad_flag',
                        action='store_const',
                        const=True, default=None)
    parser.add_argument('-i', '--interact',
                        action='store_const',
                        const=True, default=None)
    raw_config = parser.parse_args(sys.argv[1:])
    return raw_config 


def check_config(raw_config):
    ''''''
    phone_regex = re.compile(r'^\+79[0-9]{9}$|^89[0-9]{9}$')
    if raw_config.interact:
        raw_config.name = input('Имя пользователя: ')
        while not re.findall(phone_regex, str(raw_config.phone)):
            raw_config.phone = input('Номер телефона в формате'
                                     '+79XXXXXXXXX или 89XXXXXXXXX: ')
        while not mail_check(raw_config.mail):
            raw_config.mail = input('Адрес электронной почты: ')
    elif not (raw_config.name and raw_config.phone and raw_config.mail):
        print('RTMF!!!')
        raise SystemExit(1) 
    else:
        config = raw_config
        return config


if __name__ == '__main__':
     print('Do not use me separately!')

