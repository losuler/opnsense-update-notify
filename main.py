#!/usr/bin/env python3

import json
import sys

import requests
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

def parse_res(res):
    if res['status'] == 'ok' and res['update'] > 0:
        message += 'OPNsense Updates Available\n'
        message += f"Packages to download: {response['updates']}\n"
        message += f"Download size:{response['download_size']}\n"

        new_pkgs = response['new_packages']

        if len(new_pkgs) > 0:
            message += 'New:\n'

            if type(new_pkgs) == dict:
                for pkg in new_pkgs:
                    message += f"{new_pkgs[pkg]['name']} {new_pkgs[pkg]['version']}\n"
            else:
                for pkg in new_pkgs:
                    message += f"{pkg['name']} {pkg['version']}\n"

        upg_pkgs = response['upgrade_packages']

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

        reinst_pkgs = response['reinstall_packages']

        if len(reinst_pkgs) > 0:
            message += 'Reinstall:\n'

            if type(reinst_pkgs) == dict:
                for pkg in reinst_pkgs:
                    message += f"{new_pkgs[pkg]['name']} {new_pkgs[pkg]['version']}\n"
            else:
                for pkg in reinst_pkgs:
                    message += f"{pkg['name']} {pkg['version']}\n"

        if response['upgrade_needs_reboot'] == '1':
            message += 'This requires a reboot'

valid_conf('schema.yml', 'config.yml')

with open('config.yml') as f:
    conf = yaml.safe_load(f)

host       = conf['opnsense']['host']
verify     = not conf['opnsense']['self_signed']
api_key    = conf['opnsense']['api_key']
api_secret = conf['opnsense']['api_secret']

url = 'https://' + host + '/api/core/firmware/status'

res = requests.get(url,verify=verify,auth=(api_key, api_secret))

if res.status_code == 200:
    response = json.loads(r.text)
    message = parse_res(res)
else:
    print ('Connection/Authentication issue, response received:')
    print(res.text)
