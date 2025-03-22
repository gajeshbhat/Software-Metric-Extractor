import os
import requests
import subprocess
import re
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from core.db import get_session, Repository

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# GitHub API Search Query for **100 Most Trending Repositories**
SEARCH_QUERY = "language:python stars:>500 fork:false sort:stars"

# GitHub API URL Template
GITHUB_API_URL = "https://api.github.com/search/repositories?q={query}&per_page=50&page={page}"

# Cloning directory
CLONE_DIR = "projects"

# Ensure the directory exists
os.makedirs(CLONE_DIR, exist_ok=True)


def is_mostly_english(text):
    """Returns True if at least 80% of characters are ASCII (English-like)."""
    if not text:
        return True
    total_chars = len(text)
    english_chars = sum(1 for char in text if re.match(r'[A-Za-z0-9\s.,!?]', char))
    return (english_chars / total_chars) > 0.8


def clone_repository(repo_url, repo_name):
    """Clones the repository into the projects directory."""
    repo_path = os.path.join(CLONE_DIR, repo_name)
    
    if os.path.exists(repo_path):
        print(f"⚠️ Skipping {repo_name}, already cloned.")
        return repo_path
    
    try:
        print(f"🔄 Cloning {repo_name} into {repo_path}...")
        subprocess.run(["git", "clone", "--depth=1", repo_url, repo_path], check=True)
        print(f"✅ Successfully cloned {repo_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error cloning {repo_name}: {e}")
        return None
    
    return repo_path


def fetch_github_repositories():
    """Fetch repositories using GitHub API, store metadata in MySQL, and clone them."""
    session = get_session()
    
    for page in range(1, 3):  # Fetch 2 pages (50 repos per page = 100 total)
        print(f"📡 Fetching page {page} from GitHub API...")

        response = requests.get(GITHUB_API_URL.format(query=SEARCH_QUERY, page=page), headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ GitHub API error: {response.status_code} - {response.json()}")
            break

        repositories = response.json().get("items", [])
        for repo in repositories:
            # Skip non-English descriptions
            if not is_mostly_english(repo.get("description", "")):
                print(f"❌ Skipping non-English repository: {repo['full_name']}")
                continue

            # Avoid duplicates
            if session.query(Repository).filter_by(github_id=repo["id"]).first():
                print(f"⚠️ Skipping duplicate: {repo['full_name']}")
                continue

            # Clone the repository
            cloned_path = clone_repository(repo["clone_url"], repo["name"])
            if not cloned_path:
                continue  # Skip if cloning failed

            # Insert repository metadata into MySQL
            new_repo = Repository(
                github_id=repo["id"],
                name=repo["name"],
                full_name=repo["full_name"],
                clone_url=repo["clone_url"],
                stars=repo["stargazers_count"],
                forks=repo["forks_count"],
                language=repo["language"],
                description=repo["description"],
                is_fork=repo["fork"],
                created_at=repo["created_at"],
                updated_at=repo["updated_at"]
            )

            session.add(new_repo)
            print(f"✅ Stored {repo['full_name']} in database")

        session.commit()

if __name__ == "__main__":
    fetch_github_repositories()
