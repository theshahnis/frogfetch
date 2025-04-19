
# 🐸 Frogfetch - A CLI Tool to Manage JFrog Artifactory Instances

A simple and modular command-line tool to interact with [JFrog Artifactory](https://jfrog.com/artifactory/).

At the moment, the CLI supports:

- Authentication via token or username/password
- Connection validation and health checks
- Listing available repositories
- Fetching and updating repositories values
- Deleting repositories

> 🚧 **Coming soon:** Upload/delete artifacts, Create repositories

---

## ⚙️ Configuration

No configuration is required at this stage. All flags (e.g., `--url`, `--token`) are passed via the CLI.
If you require a virtualenv - perform the following command in project root repo:
>python3 -m venv venv

On Linux/Mac use `source venv/bin/activate`

On Windows use `venv\Scripts\activate`

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
| Save values to specific file|`--output <file_name>`| Enter the new filename, better to leave empty for quick loading|
| Apply values to update specific repo| `--file_path <file_path>`| Select a relevant file or keep empty to load the one downloaded from `prepare-edit`|
| Delete repo by force| `--force`|Does not wait for deletion confirmation, less recommanded|

## Commands
| Command                           | Flag            |
|-----------------------------------|-----------------|
| Check credentials and hostname    | `'dry-run'`     |
| List available repos              | `'list-repos'`  |
| Check Artifactory health via ping | `system-health` |
| Pull values of repo before editing| `prepare-edit`  |
| Updates repo values based on file | `apply-edit`    |
| Delete specic repo                | `delete-repo`   |
## Example:
Check credentials and hostname
>python3 frogfetch.py dry-run --url "mydomain.jfrog.io" --token aJGrm31GedYtXzZ...

List available repos:
>python3 frogfetch.py list-repos --url "mydomain.jfrog.io" --token aJGrm31GedYtXzZ...

Check health of Artifactory:
>python3 frogfetch.py system-health --url "mydomain.jfrog.io" --token aJGrm31GedYtXzZ...

Generate a json value file for specific repo before editing it:
>python3 frogfetch.py prepare-edit --url "mydomain.jfrog.io" --token aJGrm31GedYtXzZ... --repo test-repo

Apply changes after editing the json file:
>python3 frogfetch.py prepare-edit --url "mydomain.jfrog.io" --token aJGrm31GedYtXzZ... --repo test-repo

Delete specific repo:
>python3 frogfetch.py delete-repo "mydomain.jfrog.io" --token aJGrm31GedYtXzZ... --repo test-repo