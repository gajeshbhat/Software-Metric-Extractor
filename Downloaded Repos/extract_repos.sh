# cheating knowing we currently have 9 pages
#Source : https://stackoverflow.com/questions/56335204/is-there-a-way-to-bulk-batch-download-all-repos-from-github-based-on-a-search-re
for i in {1..9}
do
    curl "https://api.github.com/search/repositories?q=machine learning+language:python%23&per_page=100&page=$i" \
     | jq -r '.items[].ssh_url' >> urls.txt
done

cat urls.txt | xargs -P8 -L1 git clone