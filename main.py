#!/usr/bin/env python3

import json
import sys

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import yaml
import yamale

def valid_conf(schema_file, config_file):
    schema_yamale = yamale.make_schema(schema_file)
    config_yamale = yamale.make_data(config_file)

    try:
        yamale.validate(schema_yamale, config_yamale)
    except ValueError as e:
        for r in e.results:
            for err in r.errors:
                print(f"[ERROR] {err}")
        sys.exit(1)

def parse_res(resp):
    if int(resp['updates']) > 0:
        message = 'OPNsense Updates Available\n'
        message += f"Packages to download: {resp['updates']}\n"
        message += f"Download size:{resp['download_size']}\n"

        new_pkgs = resp['new_packages']

        if len(new_pkgs) > 0:
            message += 'New:\n'

            if type(new_pkgs) == dict:
                for pkg in new_pkgs:
                    message += f"{new_pkgs[pkg]['name']} {new_pkgs[pkg]['version']}\n"
            else:
                for pkg in new_pkgs:
                    message += f"{pkg['name']} {pkg['version']}\n"

        upg_pkgs = resp['upgrade_packages']

        if len(upg_pkgs) > 0:
            message += 'Upgrade:\n'

            if type(upg_pkgs) == dict:
                for pkg in upg_pkgs:
                    message += f"{new_pkgs[pkg]['name']} from {new_pkgs[pkg]['current_version']}" + \
                        f"to {new_pkgs[pkg]['new_version']}\n"
            else:
                for pkg in upg_pkgs:
                    message += f"{pkg['name']} from {pkg['current_version']}" + \
                        f"to {pkg['new_version']}\n"

        reinst_pkgs = resp['reinstall_packages']

        if len(reinst_pkgs) > 0:
            message += 'Reinstall:\n'

            if type(reinst_pkgs) == dict:
                for pkg in reinst_pkgs:
                    message += f"{new_pkgs[pkg]['name']} {new_pkgs[pkg]['version']}\n"
            else:
                for pkg in reinst_pkgs:
                    message += f"{pkg['name']} {pkg['version']}\n"

        if resp['upgrade_needs_reboot'] == '1':
            message += 'This requires a reboot\n'

    if resp['upgrade_major_version'] != '':
        try:
            message
        except NameError:
            message = 'OPNsense Major Upgrade Available\n'
        else:
            message += 'OPNsense Major Upgrade Available\n'
        message += f"{resp['upgrade_major_version']} from {resp['product_version']}"

    return message

def send_telegram(msg, chatid, token):
    url = f'https://api.telegram.org/bot{token}/sendMessage?text={msg}&chat_id={chatid}'
    r = requests.get(url)
    return r

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

valid_conf('schema.yml', 'config.yml')

with open('config.yml') as f:
    conf = yaml.safe_load(f)

host       = conf['opnsense']['host']
# verify is false if self signed
verify     = not conf['opnsense']['self_signed']
api_key    = conf['opnsense']['api_key']
api_secret = conf['opnsense']['api_secret']

t_chatid = conf['telegram']['chatid']
t_token = conf['telegram']['token']

url = 'https://' + host + '/api/core/firmware/status'

r = requests.get(url,verify=verify,auth=(api_key, api_secret))

if r.status_code == 200:
    res = json.loads(r.text)
    message = parse_res(res)

    if message != None:
        send_telegram(message, t_chatid, t_token)
    else:
        print('[INFO] There is nothing to update.')

else:
    print(f'[ERROR] {res.text}')
