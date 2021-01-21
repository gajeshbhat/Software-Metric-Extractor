import requests
import json
from pprint import pprint

REPO_FORMAT = "https://api.github.com/search/repositories?q=machine%20learninglanguage:python%23&per_page=100&page="


def get_test_json():
    with open('test.json') as f:
        data = json.load(f)
        return data["items"]


def get_repo_json(url):
    current_repo_source = requests.get(url).json()
    return current_repo_source["items"]


def get_all_repo_url(number_of_pages):
    repo_ssh_url_list = []
    for repo_num in range(1, number_of_pages + 1):
        current_repo_format = REPO_FORMAT + str(repo_num)
        repo_json_resp = get_test_json() #get_repo_json(current_repo_format)
        # TODO Page or wrong resp handling
        for repos in repo_json_resp:
            repo_ssh_url_list.append(repos['git_url'])
    return repo_ssh_url_list


# Write to file

url_file = open("../urllist.txt", "w")

ssh_url_list = get_all_repo_url(1)  # 1*100 per page = 100 Repos

for url in ssh_url_list:
    url_file.write(url + str("\n"))
url_file.close()

# Test
# pprint(get_all_repo_url(1))
