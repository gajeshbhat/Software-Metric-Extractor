import os
import click
from dotenv import load_dotenv
from core.fetch_repos import fetch_github_repositories
from core.analyze_metrics import process_projects
from core.db import get_session, Repository, Project, Directory, File, Metric

# Load .env automatically
load_dotenv()

@click.group()
def cli():
    """📊 Software Metrics Extractor CLI

    A research-oriented tool to collect and analyze software metrics from open-source GitHub repositories.
    """
    pass

@cli.command("fetch")
@click.option('--limit', default=100, show_default=True, help='Number of repositories to fetch')
@click.option('--language', default='Python', show_default=True, help='Programming language to filter by')
def fetch_repos(limit, language):
    """🌐 Fetch trending GitHub repositories and clone them."""
    os.environ['REPO_LIMIT'] = str(limit)
    os.environ['REPO_LANGUAGE'] = language
    fetch_github_repositories()
    click.echo("✅ Repository fetching complete.")

@cli.command("analyze")
@click.option('--projects-dir', default='projects', show_default=True, help='Directory containing cloned projects')
def analyze_projects(projects_dir):
    """🔍 Analyze cloned projects and store metrics in the database."""
    os.environ['PROJECTS_DIR'] = projects_dir
    process_projects()
    click.echo("✅ Metric analysis and storage complete.")

@cli.command("reset-db")
@click.confirmation_option(prompt='⚠️ Are you sure you want to delete ALL data in the database?')
def reset_db():
    """🧨 Wipe all metric data from the database."""
    session = get_session()
    for model in [Metric, File, Directory, Project, Repository]:
        session.query(model).delete()
    session.commit()
    session.close()
    click.echo("🧹 All database records have been cleared.")

if __name__ == '__main__':
    cli()
