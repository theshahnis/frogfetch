
## CLI tool to manage Artifactory instances

A simple CLI tool to get information from Artifactory.
At the moment it only checks for the url and user auth.
Todo:
 - add system-health command

## Configuration

na
```
na
```

## Installation

Run the following commands to install any dependencies:
>pip install -r requirements.txt
> 
## Usage


| Usage              | Flag                            | Explanation                                                  |
|--------------------|---------------------------------|--------------------------------------------------------------|
| Auth with password | `'--user <user> --pass <pass>'` | Use username and password to authenticate to the artifcatory |
| Auth with Token    | `'--token <token>'`             | Use Reference Token to authenticate to the artifactory       |
| Artifactory URL    | `--url <artifactory_url>`       | Enter the relevant artifactory server url                    |

## Commands
| Command                           | Flag            |
|-----------------------------------|-----------------|
| Check credentials and hostname    | `'dry-run'`     |
| List available repos              | `'list-repos'`  |
| Check Artifactory health via ping | `system-health` |


## Example:
Check credentials and hostname
>python3 frogfetch.py dry-run --url "mydomain.jfrog.io" --token "aJGrm31GedYtXzZ..."

List available repos:
>python3 frogfetch.py list-repos --url "mydomain.jfrog.io" --token "aJGrm31GedYtXzZ..."

Check health of Artifactory:
>python3 frogfetch.py system-health --url "mydomain.jfrog.io" --token "aJGrm31GedYtXzZ..."