import requests
import json

url = "https://api.nytimes.com/svc/archive/v1/{}/{}.json?api-key={api_key}"

dates = [("1918", "10"), ("2020", "10")]

#titles within time periods
for year, month in dates:
  response = requests.get(url.format(year, month))
  content = json.loads(response.text)

  #write to file
  titles = [item["headline"]["main"] for item in content["response"]["docs"]]
  with open("titles_{}.txt".format(year), "w") as f:
    f.write("\n".join(titles))
