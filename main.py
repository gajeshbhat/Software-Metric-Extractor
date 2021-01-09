import os
import shutil
from os import walk
from pprint import pprint


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
            {'Project Path': project_dir_path,
             'metric_data': str(project_metric_data).strip()
             }
        )
        output_stream.close()
    return project_metric_list


# Place the projects to analyse in Projects dir
PROJECTS_DIR = "projects"
ANALYSIS_DIR = "Analysis"

projects_to_crawl = get_dirs(PROJECTS_DIR)
project_file_details = get_all_py_files(projects_to_crawl, PROJECTS_DIR)
dirs_to_analyse = copy_analysis_files(project_file_details, ANALYSIS_DIR)
# TODO: Integrate MongoDB and Clean the data and make it available for Analysis
pprint(get_analysis_data(dirs_to_analyse))
