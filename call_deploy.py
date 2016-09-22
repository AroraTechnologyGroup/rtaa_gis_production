import requests
req = requests.get("https://gisapps.aroraengineers.com:8006/git-pull/rtaa-staging")
print(req.content)