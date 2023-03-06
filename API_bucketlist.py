import requests

import config

api_key = config.API_KEY

api_url = 'https://api.api-ninjas.com/v1/bucketlist'
response = requests.get(api_url, headers={'X-Api-Key': api_key})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)