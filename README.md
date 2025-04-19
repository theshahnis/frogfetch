
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



## Example:
Check credentials and hostname
>python3 frogfetch.py dry-run --url "mydomain.jfrog.io" --token "aJGrm31GedYtXzZ..."