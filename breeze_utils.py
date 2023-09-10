import os
import datetime
from utils import get_birthdays
import requests
import json

api_key = os.environ.get('BREEZE_API_KEY')
SUBDOMAIN = os.environ.get('SUBDOMAIN')


def list_tags():
    url = f'https://{SUBDOMAIN}.breezechms.com/api/tags/list_tags'
    return make_request(url)

def get_people_by_tag(tagname=""):
    tags = list_tags()
    filtered_tags = [tag for tag in tags if tagname in tag['name']]
    tagid = ""
    if len(filtered_tags) > 0:
        tagid = filtered_tags[0]['id']
        people = get_people(
                   details = 1,
                   filter_params = {
                    'tag_contains': f'y_{tagid}'
                    })
        return [{'last_name':person['last_name'],'first_name':person['first_name'],'birthdate':person['details']['details']['birthdate']} for person in people]
                 
    return "no matching tags found"
   
def get_person(id):
    """
     get person
    """
    url = f'https://{SUBDOMAIN}.breezechms.com/api/people/{id}'
    return make_request(url)

def get_people(details=0,filter_params={}):
    """
     get people.
     people can be filtered by tag
    """
    filter_json = json.dumps(filter_params)
    # Construct the API URL
    url = f'https://{SUBDOMAIN}.breezechms.com/api/people/?details={details}'
    if filter_params:
        url = f'https://{SUBDOMAIN}.breezechms.com/api/people/?details={details}&filter_json={filter_json}'
    return make_request(url)

def make_request(url):
    # Set up the request headers with your API key
    headers = {
        'Content-Type': 'application/json',
          'Api-Key': api_key
    }

    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        return response.json()
    else:
        return f"Request failed with status code {response.status_code}"



