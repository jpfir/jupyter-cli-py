# Jupyter CLI (jupyter-cli-py)

Jupyter Python command-line interface for managing and extracting information
from a JupyterHub instance.

## Features
- **User Management**: List, modify, and delete users.
- **Group Management**: Add or remove users from groups.
- **Token Management**: List and manage user tokens.
- **Service & Proxy Management**: View services and proxy information.
- **Debugging**: Verbose and debug options to troubleshoot API interactions.

## Prerequisites
Before using this CLI tool, ensure you have the necessary dependencies installed:

```bash
pip3 install requests tabulate --user
```

## Configuration
This CLI tool requires a configuration file (`config.conf`) to function. The
configuration file should contain API keys and URLs for your JupyterHub instance.
Below is an example structure:

```ini
[jupyter]
api_key_exo = <your_api_key>
api_url_exo = <your_jupyterhub_url>
```

Replace `<your_api_key>` and `<your_jupyterhub_url>` with the actual API key and
URL for your JupyterHub instance. The `exo` part can be replaced with any client
name you prefer.

## Usage

```bash
./jupyter-cli.py --help
```

### Command-Line Options
Here's a breakdown of the available options:

- `--client CLIENT`: Choose the credential (default: `exo`)
- `--version`: Show the current version of the CLI tool
- `--info`: Display general information about the JupyterHub instance
- `--users`: List all users
- `--user USER`: Specify a user for further actions
- `--usermodify`: Modify a user's attributes
- `--useradmin {True,False}`: Add or remove admin privileges for a user
- `--tokens`: List tokens associated with a user
- `--token TOKEN`: Display a specific token for a user
- `--deluser DELUSER`: Delete a user (recommended to use with `--debug`)
- `--groups`: List all groups and the users within them
- `--group GROUP`: Specify a group for further actions
- `--usergroup {add,del}`: Add or remove a user from a group (recommended to use with `--debug`)
- `--usernewname USERNEWNAME`: Change a user's username
- `--proxy`: List proxy information
- `--services`: List services
- `--noheaders`: Omit headers in the output
- `--debug`: Enable debug information for API requests
- `--verbose`: Enable verbose output

### Examples

#### General Information

```bash
./jupyter-cli.py --version --debug
./jupyter-cli.py --info --debug
```

#### User Management

```bash
./jupyter-cli.py --users
./jupyter-cli.py --users --user username --debug
./jupyter-cli.py --usermodify --user username --useradmin True --debug
./jupyter-cli.py --usermodify --user username --usernewname newusername --debug
./jupyter-cli.py --usermodify --user username --useradmin False --usernewname newusername --debug
./jupyter-cli.py --deluser username --debug
```

#### Group Management

```bash
./jupyter-cli.py --groups --debug
./jupyter-cli.py --groups --group groupname --debug
./jupyter-cli.py --usergroup add --user username --group groupname --debug
./jupyter-cli.py --usergroup del --user username --group groupname --debug
```

#### Token Management

```bash
./jupyter-cli.py --users --user username --tokens --debug
./jupyter-cli.py --users --user username --tokens --token a272 --debug
```

#### Service & Proxy Management

```bash
./jupyter-cli.py --services --debug
./jupyter-cli.py --proxy --debug
```

## Development Status

**Note**: This tool is still in the "quick & dirty" development phase.
Contributions and improvements are welcome!
