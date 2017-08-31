import requests
import sys

def get_data(tel_number):
    post_url = "https://www.kody.su/api/v2/search.json"
    params = {'q': tel_number, 'key': 'test'}
    p = requests.post(post_url, params=params).json()
    try:
        operator = p['numbers'][0]['operator']
    except(LookupError):
        operator = 'Non-Mobile'
    finally:
        region = p['numbers'][0]['region']
    return print(operator, region)

if len(sys.argv) > 1:
    get_data(sys.argv)
