import os
import json
import shutil
from os import walk
from pprint import pprint
from metric_db import get_session, get_overall_obj, get_each_file_obj, ProjectMetric


def get_all_py_files(dir_list, root_dir):
    py_file_list = list()
    for dir in dir_list:
        current_dir_path = root_dir + "/" + dir
        current_project_details = {
            'name': str(dir),
            'path': str(current_dir_path),
            'python_files': []
        }
        for (dir_path, dir_name, file_names) in walk(current_dir_path):
            for file in file_names:
                if str(file).endswith(".py"):
                    current_project_details['python_files'].append(
                        {'file_name': file,
                         'file_path': dir_path + os.sep + file,
                         }
                    )
        current_project_details['Total files'] = len(current_project_details['python_files'])
        py_file_list.append(current_project_details)
    return py_file_list


# print(only_python)
def get_dirs(root_dir):
    dir_list = next(os.walk(root_dir))[1]
    return dir_list


def copy_analysis_files(project_details, current_directory):
    analysis_dirs = []

    for project in project_details:

        new_dir_name = project['name'] + str('_analysis')
        new_dir_path = current_directory + os.sep + new_dir_name
        analysis_dirs.append(new_dir_path)

        if not os.path.exists(new_dir_path):
            os.makedirs(new_dir_path)

        for py_file in project['python_files']:
            shutil.copy(py_file['file_path'], new_dir_path)
    return analysis_dirs


def get_analysis_data(projects_dirs):
    project_metric_list = list()
    for project_dir_path in projects_dirs:
        output_stream = os.popen("multimetric " + str(project_dir_path + "/*.py"))
        project_metric_data = output_stream.read()
        project_metric_list.append(
            {'project_name': str(project_dir_path).split('/')[1],
             'Project Path': project_dir_path,
             'metric_data': str(project_metric_data).strip()
             }
        )
        output_stream.close()
    return project_metric_list


def insert_metric_db(each_project_metric, project_name):
    db_session = get_session()
    overall_metric_obj = get_overall_obj(each_project_metric['overall_metrics'], project_name)

    db_session.add(overall_metric_obj)
    db_session.commit()

    project_saved_inst = db_session.query(ProjectMetric).filter_by(project_name=str(project_name)).first()

    for file_metric in each_project_metric['file_metrics_list']:
        each_file_obj = get_each_file_obj(file_metric,project_saved_inst)
        db_session.add(each_file_obj)

    db_session.commit()
    db_session.close()


def create_project_metric(project_metric_json):
    for x in project_metric_json:
        json_metric = json.loads(x["metric_data"])
        project_files_metric = json_metric["files"]

        overall_metrics = json_metric["overall"]
        mean_metric = json_metric['stats']['mean']
        sd_metric = json_metric['stats']['sd']

        file_metric_list = list()
        for key, value in project_files_metric.items():
            if value != {}:
                file_metric_list.append(value)
        current_project_metric = {
            'overall_metrics': overall_metrics,
            'overall_mean': mean_metric,
            'overall_sd': sd_metric,
            'file_metrics_list': file_metric_list
        }
        insert_metric_db(current_project_metric, x['project_name'])


# Place the projects to analyse in Projects dir
PROJECTS_DIR = "projects"
ANALYSIS_DIR = "Analysis"

# Insert table into database
projects_to_crawl = get_dirs(PROJECTS_DIR)
project_file_details = get_all_py_files(projects_to_crawl, PROJECTS_DIR)
dirs_to_analyse = copy_analysis_files(project_file_details, ANALYSIS_DIR)
analysis_data = get_analysis_data(dirs_to_analyse)
# pprint(analysis_data)

# TODO: Update the type or convert the json types to float in database object instantiation
# Creates project metric
create_project_metric(analysis_data)
