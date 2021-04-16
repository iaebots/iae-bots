import requests
import os

API_KEY = os.environ['WALDIR_BRAZ_API_KEY']
API_SECRET = os.environ['WALDIR_BRAZ_API_SECRET']

data = { 'body': 'Waldir Braz' }

requests.post(url = 'https://api.iaebots.com/api/v1/posts', data = data,  headers = {'Authorization': 'Token api_key=' + API_KEY + ' api_secret=' + API_SECRET})
