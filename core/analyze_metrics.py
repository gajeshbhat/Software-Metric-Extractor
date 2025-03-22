import os
import json
import subprocess
from core.db import get_session, Project, Directory, File, Metric, Repository

PROJECTS_DIR = "projects"

def run_radon_analysis(target_path):
    """Runs Radon commands to extract metrics and returns JSON results."""
    commands = {
        "complexity": ["radon", "cc", "-j", target_path],
        "maintainability": ["radon", "mi", "-j", target_path],
        "raw_metrics": ["radon", "raw", "-j", target_path],
    }
    
    results = {}
    for metric, command in commands.items():
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode == 0:
            try:
                output = process.stdout.strip()
                results[metric] = json.loads(output) if output else {}
            except json.JSONDecodeError:
                print(f"❌ Error decoding JSON for {metric}: {process.stdout}")
                results[metric] = {}
        else:
            print(f"❌ Error running Radon for {metric}: {process.stderr}")
            results[metric] = {}

    return results

def get_cyclomatic_complexity(file_path, complexity_data):
    """Extracts cyclomatic complexity for a given file."""
    if isinstance(complexity_data, dict) and file_path in complexity_data:
        file_complexity_data = complexity_data[file_path]
        if isinstance(file_complexity_data, list) and file_complexity_data:
            return file_complexity_data[0].get("complexity", 0)
    return 0  # Default value

def save_metrics_to_db(project_name, project_path, analysis_data):
    """Stores project, directory, file, and metric data into MySQL."""
    session = get_session()
    repository = session.query(Repository).filter_by(name=project_name).first()
    if not repository:
        print(f"❌ Repository {project_name} not found in DB. Skipping.")
        return

    project_entry = session.query(Project).filter_by(repository_id=repository.id).first()
    file_metrics = [
        {"complexity": get_cyclomatic_complexity(file_path, analysis_data.get("complexity", {})),
         "lines_of_code": file_data.get("loc", 0)}
        for file_path, file_data in analysis_data.get("raw_metrics", {}).items()
    ]

    if file_metrics:
        project_metrics = {
            "total_files": len(file_metrics),
            "total_lines_of_code": sum(f["lines_of_code"] for f in file_metrics),
            "avg_cyclomatic_complexity": sum(f["complexity"] for f in file_metrics) / len(file_metrics)
        }
        
        if project_entry:
            print(f"🔄 Updating existing project: {project_name}")
            project_entry.total_files = project_metrics["total_files"]
            project_entry.total_lines_of_code = project_metrics["total_lines_of_code"]
            project_entry.avg_cyclomatic_complexity = project_metrics["avg_cyclomatic_complexity"]
        else:
            print(f"➕ Creating new project: {project_name}")
            project_entry = Project(
                repository_id=repository.id,
                path=project_path,
                **project_metrics
            )
            session.add(project_entry)
        session.commit()

    dir_cache = {}
    for file_path, raw_data in analysis_data.get("raw_metrics", {}).items():
        dir_path = os.path.dirname(file_path)
        if dir_path not in dir_cache:
            directory_entry = session.query(Directory).filter_by(path=dir_path, project=project_entry).first()
            if not directory_entry:
                directory_entry = Directory(path=dir_path, project=project_entry)
                session.add(directory_entry)
                session.commit()
            dir_cache[dir_path] = directory_entry

        file_entry = session.query(File).filter_by(path=file_path, directory=dir_cache[dir_path]).first()
        if file_entry:
            print(f"🔄 Updating file metrics for {file_path}")
            file_entry.lines_of_code = raw_data.get("loc", 0)
            file_entry.cyclomatic_complexity = get_cyclomatic_complexity(file_path, analysis_data.get("complexity", {}))
        else:
            file_entry = File(
                directory=dir_cache[dir_path],
                name=os.path.basename(file_path),
                path=file_path,
                lines_of_code=raw_data.get("loc", 0),
                cyclomatic_complexity=get_cyclomatic_complexity(file_path, analysis_data.get("complexity", {}))
            )
            session.add(file_entry)
        session.commit()

        session.query(Metric).filter_by(file_id=file_entry.id).delete()
        session.commit()

        metric_entries = [
            Metric(file=file_entry, metric_name="cyclomatic_complexity", metric_value=file_entry.cyclomatic_complexity),
            Metric(file=file_entry, metric_name="maintainability_index", metric_value=analysis_data.get("maintainability", {}).get(file_path, {}).get("mi", 0)),
            Metric(file=file_entry, metric_name="lines_of_code", metric_value=raw_data.get("loc", 0)),
            Metric(file=file_entry, metric_name="comment_lines", metric_value=raw_data.get("comment", 0)),
            Metric(file=file_entry, metric_name="functions", metric_value=raw_data.get("functions", 0))
        ]
        session.add_all(metric_entries)
        session.commit()

    session.close()
    print(f"✅ Finished processing {project_name}.")

def process_projects():
    """Scans all projects and extracts metrics using Radon."""
    projects_to_analyze = os.listdir(PROJECTS_DIR)
    
    for project_name in projects_to_analyze:
        project_path = os.path.join(PROJECTS_DIR, project_name)
        if os.path.isdir(project_path):
            print(f"🚀 Analyzing: {project_name}...")
            analysis_data = run_radon_analysis(project_path)
            save_metrics_to_db(project_name, project_path, analysis_data)
    
    print("✅ Analysis completed!")