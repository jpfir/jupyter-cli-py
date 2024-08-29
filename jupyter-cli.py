#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#############################################################################
# pip3 install tabulate --user
#
# https://url.ext/jupyter/hub/token
# https://jupyterhub.readthedocs.io/en/stable/reference/rest-api.html#/jupyterhub-rest-api
#############################################################################
import requests
import json
import argparse
import sys
import os.path
from http.client import HTTPConnection  # Debug mode
from configparser import ConfigParser
from tabulate import tabulate

#############################################################################
# Function to make HTTP requests to JupyterHub API
def make_request(method='GET', resource='', auth='', headers={}, params='', data=''):
    url = api_url + resource
    headers.update({'accept': 'application/json'})

    if args.verbose or args.debug:
        print(url)
        if args.debug:
            HTTPConnection.debuglevel = 1

    try:
        response = requests.request(method, url, auth=auth, headers=headers, params=params, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        sys.exit(1)

    if args.verbose or args.debug:
        print(f'Status code: {response.status_code}')
        if args.debug and response.status_code != 204:
            print(json.dumps(response.json(), sort_keys=True, indent=2, separators=(',', ': ')))

    if response.status_code != 204:
        return response.json()
    return response

#############################################################################
# Argument parser setup
parser = argparse.ArgumentParser(description='JupyterHub CLI Utility',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--client', default='exo', help='Choose the credential')
parser.add_argument('--version', action='store_true', help='Version')
parser.add_argument('--info', action='store_true', help='Information')
parser.add_argument('--users', action='store_true', help='List users')
parser.add_argument('--user', help='Choose the user')
parser.add_argument('--usermodify', action='store_true', help='Modify the user')
parser.add_argument('--useradmin', choices=['True', 'False'], help='Add or remove admin for a user')
parser.add_argument('--tokens', action='store_true', help='List tokens by user')
parser.add_argument('--token', help='Display a user token')
parser.add_argument('--deluser', help='Delete a user (better use --debug)')
parser.add_argument('--groups', action='store_true', help='List groups and users in the group')
parser.add_argument('--group', help='Choose the group')
parser.add_argument('--usergroup', choices=['add', 'del'], help='Add or remove user in a group (better use --debug)')
parser.add_argument('--usernewname', help='Change username')
parser.add_argument('--proxy', action='store_true', help='List proxy')
parser.add_argument('--services', action='store_true', help='List services')
parser.add_argument('--noheaders', action='store_true', help='No headers in the output')
parser.add_argument('--debug', action='store_true', help='Debug information')
parser.add_argument('--verbose', action='store_true', help='Verbose')
args = parser.parse_args()

#############################################################################
# Load configuration
config_file = './config.conf'
if not os.path.isfile(config_file):
    sys.exit(f"""❌ Configuration file '{config_file}' not found!
Please create the file with the following structure:

[jupyter]
api_key_exo = <your_api_key>
api_url_exo = <your_jupyterhub_url>

You can replace 'exo' with the client name you use with the --client option.
""")

config = ConfigParser(interpolation=None)
config.read(config_file, encoding='utf-8')
api_key = config.get('jupyter', f'api_key_{args.client}')
api_url = f"https://{config.get('jupyter', f'api_url_{args.client}')}/jupyter/hub/api/"

#############################################################################
# Functions for different operations
def show_version():
    return make_request(resource='', headers={'Authorization': f'token {api_key}'})

def show_info():
    return make_request(resource='info', headers={'Authorization': f'token {api_key}'})

def list_users():
    if args.user:
        if args.tokens:
            if args.token:
                return make_request(resource=f'users/{args.user}/tokens/{args.token}', headers={'Authorization': f'token {api_key}'})
            return make_request(resource=f'users/{args.user}/tokens', headers={'Authorization': f'token {api_key}'})
        return make_request(resource=f'users/{args.user}', headers={'Authorization': f'token {api_key}'})
    else:
        users = make_request(resource='users', headers={'Authorization': f'token {api_key}'})
        table = [[user['name'], user['kind'], user['admin']] for user in users]
        tablefmt = 'plain' if args.noheaders else 'rounded_outline'
        headers = None if args.noheaders else ['username', 'kind', 'admin']
        print(tabulate(sorted(table), headers=headers, tablefmt=tablefmt))

def delete_user():
    return make_request(method='DELETE', resource=f'users/{args.deluser}', headers={'Authorization': f'token {api_key}', 'Content-Type': 'application/json'})

def list_groups():
    resource = 'groups'
    if args.group:
        resource += f'/{args.group}'
    return make_request(resource=resource, headers={'Authorization': f'token {api_key}'})

def modify_usergroup():
    if not args.group or not args.user:
        print('You have to choose a group and a user')
        sys.exit(1)
    method = 'DELETE' if args.usergroup == 'del' else 'POST'
    data = json.dumps({'users': [args.user]})
    return make_request(method=method, resource=f'groups/{args.group}/users', headers={'Authorization': f'token {api_key}', 'Content-Type': 'application/json'}, data=data)

def modify_user():
    if not args.user:
        print('You have to choose a user')
        sys.exit(1)
    if not args.useradmin and not args.usernewname:
        print('Choose useradmin and/or newusername to change!')
        sys.exit(1)
    data = {}
    if args.useradmin:
        data['admin'] = args.useradmin == 'True'
    if args.usernewname:
        data['name'] = args.usernewname
    return make_request(method='PATCH', resource=f'users/{args.user}', headers={'Authorization': f'token {api_key}', 'Content-Type': 'application/json'}, data=json.dumps(data))

def list_services():
    return make_request(resource='services', headers={'Authorization': f'token {api_key}'})

def list_proxy():
    return make_request(resource='proxy', headers={'Authorization': f'token {api_key}'})

#############################################################################
# Main logic to handle operations
# Avoided match to be compatible with older py3 versions
if args.version:
    show_version()
elif args.info:
    show_info()
elif args.users:
    list_users()
elif args.deluser:
    delete_user()
elif args.groups:
    list_groups()
elif args.usergroup:
    modify_usergroup()
elif args.usermodify:
    modify_user()
elif args.services:
    list_services()
elif args.proxy:
    list_proxy()

#############################################################################
