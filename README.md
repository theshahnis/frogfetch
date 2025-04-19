
# 🐸 Frogfetch - A CLI Tool to Manage JFrog Artifactory Instances

A simple and modular command-line tool to interact with [JFrog Artifactory](https://jfrog.com/artifactory/).

At the moment, the CLI supports:

- Authentication via token or username/password
- Connection validation and health checks
- Listing available repositories

> 🚧 **Coming soon:** Upload/delete artifacts, create/delete repositories

---

## ⚙️ Configuration

No configuration is required at this stage. All flags (e.g., `--url`, `--token`) are passed via the CLI.

If you'd like to configure defaults in the future, support for `.env` or config files will be added.

---

## 📦 Installation

Install dependencies with:

```bash
pip install -r requirements.txt
```

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