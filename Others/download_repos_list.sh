# cheating knowing we currently have 9 pages
#NOTE : Install jq (command line json parsers before you run this code. Or Prase using python itself.)
# TODO: Create a python service to download the files from github given the parameters
#Source : https://stackoverflow.com/questions/56335204/is-there-a-way-to-bulk-batch-download-all-repos-from-github-based-on-a-search-re
cat urllist.txt | xargs -P8 -L1 git clone