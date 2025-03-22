# 📊 Software Metric Extractor

> **A research-oriented tool to extract static code metrics from trending open-source Python repositories.**  
Ideal for academic studies, benchmarking, or enriching datasets for training machine learning models.

---

## 🌟 Overview

**Software Metric Extractor** automates the pipeline of:

1. **Fetching trending Python repositories** from GitHub.
2. **Cloning and storing** them locally.
3. **Extracting static code metrics** using [Radon](https://radon.readthedocs.io/en/latest/) (e.g., Cyclomatic Complexity, Maintainability Index).
4. **Storing metrics into a MySQL database** using SQLAlchemy.

This tool is perfect for researchers and developers studying software quality, complexity, and maintainability patterns in open-source projects.

---

## 🧾 Project Structure

```
.
├── cli/
│   └── main.py               # CLI entry point
├── core/
│   ├── analyze_metrics.py    # Radon-based metrics extraction
│   ├── db.py                 # DB models & session manager
│   ├── fetch_repos.py        # GitHub scraping logic
├── docker-compose.yml        # MySQL container setup
├── projects/                 # Local clones of repositories
├── requirements.txt          # Python dependencies
├── run.py                    # CLI launcher
└── .env                      # Environment variables
```

---

## 🛠️ Prerequisites

- **Python 3.11+**
- **Docker & Docker Compose**
- A valid **GitHub Personal Access Token**

---

## ⚙️ Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/software-metric-extractor.git
cd software-metric-extractor
```

---

### 2. Create a `.env` file

```ini
# .env

# GitHub API Token (for higher rate limits)
GITHUB_TOKEN=ghp_...

# MySQL Database URL (used by SQLAlchemy)
DATABASE_URL=mysql+pymysql://metrics_user:metrics_password@localhost/software_metrics
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=software_metrics
MYSQL_USER=metrics_user
MYSQL_PASSWORD=your_database_password

# Optional defaults
REPO_LIMIT=100
REPO_LANGUAGE=Python
```

---

### 3. Start MySQL with Docker

```bash
docker-compose up -d
```

This will spin up a MySQL 8.0 container with a database named `software_metrics`.

---

### 4. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 5. Run the CLI

```bash
python run.py --help
```

### CLI Commands:

#### 🔍 Fetch repositories
```bash
python run.py fetch-repos --limit 50 --language Python
```

#### 📈 Analyze and compute metrics
```bash
python run.py analyze
```

#### 🧹 Reset database
```bash
python run.py reset-db
```

---

## 📦 Metrics Extracted

Each file and project is analyzed for:

- Cyclomatic Complexity
- Maintainability Index
- Lines of Code (LOC)
- Number of Functions
- Comment Lines

---

## 🧪 Use Case: ML Research

This project was originally designed for a **research study** exploring the relationship between code structure and performance in large language models. The resulting dataset can be used for:

- **Code complexity prediction**
- **Model training for software quality estimations**
- **Empirical software engineering research**

---

## 🧰 Tech Stack

- Python 🐍
- SQLAlchemy ORM
- MySQL 8
- Docker 🐳
- Radon (code analysis)
- GitHub API & GitPython
- Selenium (for trending repo scraping)

---

## 📜 License
MIT License © 2025  
Crafted with ❤️ for software engineering research.