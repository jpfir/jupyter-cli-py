#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#############################################################################
#############################################################################
#############################################################################
# pip3 install tabulate --user
#
# https://url.ext/jupyter/hub/token
# https://jupyterhub.readthedocs.io/en/stable/reference/rest-api.html#/jupyterhub-rest-api
#############################################################################
import requests
import json
import argparse
import sys, os.path
from http.client import HTTPConnection  # Debug mode
from configparser import ConfigParser
from tabulate import tabulate
#############################################################################
def request( method='GET', resource='', params='', headers={} ):
  url=api_url+resource
  headers.update({'accept': 'application/json'})
  if (args.verbose) or (args.debug):
    print(url)
    if (args.debug):
      # print statements from `http.client.HTTPConnection` to console/stdout
      HTTPConnection.debuglevel=1
  response=requests.request(
    method,
    api_url+resource,
    headers=headers,
    json=params,
  )
  if (args.verbose) or (args.debug):
    print('Status code: '+str(response.status_code))
  if (args.debug) and not response.status_code == 204 :
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=2, separators=(',', ': ')))
  if not response.status_code == 204:
    return(response.json())
  else:
    return(response)
#############################################################################
#############################################################################
parser = argparse.ArgumentParser(description='https://github.com/osgpcq/jupyter-cli-py',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--client',               default='exo',       help='Choose the credential')
parser.add_argument('--version',              action='store_true', help='Version')
parser.add_argument('--info',                 action='store_true', help='Information')
parser.add_argument('--users',                action='store_true', help='List users')
parser.add_argument('--user',                 action='store',      help='Choose the user')
parser.add_argument('--usermodify',           action='store_true', help='Modify the user')
parser.add_argument('--useradmin',            action='store',      help='Add or remove admin for a user', choices=['True', 'False'])
parser.add_argument('--tokens',               action='store_true', help='List tokens by user')
parser.add_argument('--token',                action='store',      help='Display a user token')
parser.add_argument('--deluser',              action='store',      help='Delete a user (better use --debug)')
parser.add_argument('--groups',               action='store_true', help='List groups and users in the group')
parser.add_argument('--group',                action='store',      help='Choose the group')
parser.add_argument('--usergroup',            action='store',      help='Add or remove user in a group (better use --debug)', choices=['add', 'del'])
parser.add_argument('--usernewname',          action='store',      help='Change username')
parser.add_argument('--proxy',                action='store_true', help='List proxy')
parser.add_argument('--services',             action='store_true', help='List services')
parser.add_argument('--noheaders',            action='store_true', help='No headers in the output')
parser.add_argument('--debug',                action='store_true', help='Debug information')
#parser.add_argument('--verbose',              action='store_true', default=True, help='Verbose')
parser.add_argument('--verbose',              action='store_true', default=False, help='Verbose')
args = parser.parse_args()

config_file='./config.conf'
if os.path.isfile(config_file):
  parser = ConfigParser(interpolation=None)
  parser.read(config_file, encoding='utf-8')
  api_key = parser.get('jupyter', 'api_key_'+args.client)
  api_url = 'https://'+parser.get('jupyter', 'api_url_'+args.client)+'/jupyter/hub/api/'
else:
  sys.exit('Configuration file not found!')

if (args.version):
  version=request( resource='', headers={ 'Authorization': 'token '+api_key } )
if (args.info):
  info=request( resource='info', headers={ 'Authorization': 'token '+api_key } )
if (args.users):
  if (args.user):
    if (args.tokens):
      if (args.token):
        token=request( resource='users/'+args.user+'/tokens/'+args.token, headers={ 'Authorization': 'token '+api_key } )
      else:
        tokens=request( resource='users/'+args.user+'/tokens', headers={ 'Authorization': 'token '+api_key } )
    else:
      user=request( resource='users/'+args.user, headers={ 'Authorization': 'token '+api_key } )
  else:
    users=request( resource='users', headers={ 'Authorization': 'token '+api_key } )
    table = []
    for user in users:
      table.append([
        user['name'],
        user['kind'],
        user['admin'],
      ]),
    if args.noheaders:
      print(tabulate(sorted(table), tablefmt='plain'))
    else:
      print(tabulate(sorted(table), tablefmt='rounded_outline', headers=['username','kind','admin']))
if (args.deluser):
  users=request( method='DELETE', resource='users/'+args.deluser, headers={ 'Authorization': 'token '+api_key, 'Content-Type': 'application/json' } )
if (args.groups):
  resource='groups'
  if (args.group):
    resource=resource+'/'+args.group
  groups=request( resource=resource, headers={ 'Authorization': 'token '+api_key } )
if (args.usergroup):
  if not (args.group) or not (args.user):
    print('You have to choose a group and a user')
    quit()
  userlist= [ args.user ]
  if args.usergroup == 'del':
    method='DELETE'
  else:
    method='POST'
  if (args.debug):
    print(userlist)
    print(method)
  groups=request( method=method, resource='groups/'+args.group+'/users', params={ 'users': userlist }, headers={ 'Authorization': 'token '+api_key, 'Content-Type': 'application/json' } )
if (args.usermodify):
  if not (args.user):
    print('You have to choose a user')
    quit()
  if not (args.useradmin) and not (args.usernewname):
    print('Choose useradmin and/or nweusername to change!')
  else:
    params={}
    if (args.debug):
      print(args.user)
      print(args.useradmin)
      print(args.usernewname)
    if args.useradmin == "True":
      params.__setitem__("admin", True)
    else:
      params.__setitem__("admin", False)
    if args.usernewname:
      params.__setitem__("name", args.usernewname)
    if (args.debug):
      print(params)
    groups=request( method='PATCH', resource='users/'+args.user, params=params, headers={ 'Authorization': 'token '+api_key, 'Content-Type': 'application/json' } )
if (args.services):
  services=request( resource='services', headers={ 'Authorization': 'token '+api_key } )
if (args.proxy):
  services=request( resource='proxy', headers={ 'Authorization': 'token '+api_key } )
#############################################################################
#############################################################################
#############################################################################
