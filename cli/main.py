import click
from cli.system_commands import system_health, dry_run
from cli.repo_commands import list_repos,prepare_edit,apply_edit,delete_repo
from utils import get_logger

logger = get_logger("frogfetch")

@click.group()
def cli():
    """Frogfetch - A CLI tool to interact with Artifactory"""
    pass

# Register all subcommands here
cli.add_command(system_health)
cli.add_command(dry_run)
cli.add_command(list_repos)
cli.add_command(prepare_edit)
cli.add_command(apply_edit)
cli.add_command(delete_repo)