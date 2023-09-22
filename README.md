# jupyter-cli-py
Jupyter Python command-line interface.

Extract informations from Jupyter.


# Usage
```
./jupyter-cli.py --help
options:
  -h, --help            show this help message and exit
  --client CLIENT       Choose the credential (default: exo)
  --version             Version (default: False)
  --info                Information (default: False)
  --users               List users (default: False)
  --user USER           Choose the user (default: None)
  --usermodify          Modify the user (default: False)
  --useradmin {True,False}
                        Add or remove admin for a user (default: None)
  --tokens              List tokens by user (default: False)
  --token TOKEN         Display a user token (default: None)
  --deluser DELUSER     Delete a user (better use --debug) (default: None)
  --groups              List groups and users in the group (default: False)
  --group GROUP         Choose the group (default: None)
  --usergroup {add,del}
                        Add or remove user in a group (better use --debug) (default: None)
  --usernewname USERNEWNAME
                        Change username (default: None)
  --proxy               List proxy (default: False)
  --services            List services (default: False)
  --noheaders           No headers in the output (default: False)
  --debug               Debug information (default: False)
  --verbose             Verbose (default: False)

./jupyter-cli.py --version --debug
./jupyter-cli.py --info --debug

./jupyter-cli.py --users
╭──────────┬────────┬─────────╮
│ username │ kind   │ admin   │
├──────────┼────────┼─────────┤
│ User01   │ user   │ False   │


./jupyter-cli.py --users --user username --debug

./jupyter-cli.py --usermodify --user username --useradmin True --debug
./jupyter-cli.py --usermodify --user username --usernewname newusername --debug
./jupyter-cli.py --usermodify --user username --useradmin False --usernewname newusername --debug

./jupyter-cli.py --deluser username --debug

./jupyter-cli.py --groups --debug
./jupyter-cli.py --groups --group groupname --debug
./jupyter-cli.py --usergroup add --user username --group groupname --debug
./jupyter-cli.py --usergroup del --user username --group groupname --debug

./jupyter-cli.py --services --debug
./jupyter-cli.py --proxy --debug

./jupyter-cli.py --users --user username --tokens --debug
./jupyter-cli.py --users --user username --tokens --token a272 --debug


# History
Still in quick & dirty dev phase!
