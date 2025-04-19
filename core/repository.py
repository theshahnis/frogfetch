import click,os,json,requests,sys
from core.base import ArtifactoryManager
from utils.path import get_project_root

class RepositoryManager(ArtifactoryManager):
    def list_repositories(self):
        self.validate_connection()

        endpoint = '/artifactory/api/repositories'
        try:

            response = self.make_request(endpoint)
            if response.status_code == 200:
                repos = response.json()
                click.echo("📦 Repositories:")
                for repo in repos:
                    click.echo(f" - {repo.get('key')} ({repo.get('type')})")
            elif response.status_code == 401:
                raise click.ClickException("🔒 Unauthorized – check your token or credentials.")
            else:
                raise click.ClickException(f"❌ Failed to list repositories: {response.status_code}")
        except Exception as e:
            raise click.ClickException(f"❗ Failed to confirm host - please validate the url: {str(e)}")

    def prepare_edit_repo(self, repo_key: str, output_file: str = None):
        self.validate_connection()

        try:
            endpoint = f'/artifactory/api/repositories/{repo_key}'
            response = self.make_request(endpoint)

            if response.status_code == 200:
                config = response.json()

                # Determine file path
                base_dir = os.path.dirname(os.path.abspath(__file__))
                root_dir = os.path.abspath(os.path.join(base_dir, ".."))
                filename = output_file or f"{repo_key}-values.json"
                file_path = os.path.join(root_dir, filename)

                with open(file_path, 'w') as f:
                    json.dump(config, f, indent=2)

                click.echo(f"📄 Repo config saved to: {file_path}")
                click.echo("✏️ Edit the file and run 'apply-edit-repo' to apply changes.")
            else:
                raise click.ClickException(f"❌ Failed to fetch config for repo '{repo_key}': {response.status_code}")
        except Exception as e:
            click.echo(f"Failed to pull configuration file due to {e}")
    def apply_edit_repo(self, repo_key: str, file_path: str = None):
        self.validate_connection()

        endpoint = f'/artifactory/api/repositories/{repo_key}'

        if not file_path:
            file_path = os.path.join(get_project_root(self), f"{repo_key}-values.json")

        if not os.path.exists(file_path):
            raise click.ClickException(f"❌ File '{file_path}' not found.")

        with open(file_path, 'r') as f:
            updated_config = json.load(f)

        current_config = self.make_request(endpoint).json()

        if updated_config == current_config:
            click.echo("✅ No changes detected. Skipping update.")
            return

        response = requests.post(
            f"https://{self.url}{endpoint}",
            headers=self.headers,
            json=updated_config
        )

        if response.status_code == 200:
            click.echo(f"✅ Repository '{repo_key}' updated successfully.")
        else:
            raise click.ClickException(
                f"❌ Failed to update repo '{repo_key}': {response.status_code} - {response.text}")

    def delete_repository(self, repo_key: str, force: bool = False):
        self.validate_connection()

        endpoint = f"/artifactory/api/repositories/{repo_key}"

        if not force:
            confirm = input(f"⚠️ Are you sure you want to delete repository '{repo_key}'? (yes/[no]): ").strip().lower()
            if confirm != "yes":
                click.echo("❌ Aborted.")
                return

        response = requests.delete(f"https://{self.url}{endpoint}", headers=self.headers)

        if response.status_code == 200:
            click.echo(f"🗑️ Repository '{repo_key}' deleted successfully.")
        elif response.status_code == 404:
            raise click.ClickException(f"🔍 Repository '{repo_key}' not found.")
        elif response.status_code == 401:
            raise click.ClickException("🔒 Unauthorized.")
        else:
            raise click.ClickException(
                f"❌ Failed to delete repository: {response.status_code} - {response.text}")