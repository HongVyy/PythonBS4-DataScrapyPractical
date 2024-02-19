import requests
import json

urls = [
    "https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year=2015",
    "https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year=2014",
    "https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year=2013",
    "https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year=2012",
    "https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year=2011",
    "https://www.scrapethissite.com/pages/ajax-javascript/?ajax=true&year=2010"
]

with open('output.json', 'a') as json_file:
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        for item in data:
            json.dump(item, json_file)
            json_file.write('\n')
print("Data has been written to output.json file.")
