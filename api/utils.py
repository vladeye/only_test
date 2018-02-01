import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from rest_framework.exceptions import ValidationError


class BunnyApi:
    def __str__(self):
        """Return a human readable representation of the model instance"""
        return "{}".format(self.name)

    def __init__(self, api_id, api_key):
        self.api_id = api_id
        self.api_key = api_key

    def create_speedy_project(self, readings_data):
        """Creates a Speedy project with the bunny api"""
        payload = {
            'title': readings_data.title,
            'script': readings_data.script,
            'test': readings_data.test
       }
        r = requests.post(
            settings.BUNNY_API_URL + '/projects/addSpeedy',
            data=payload,
            auth=HTTPBasicAuth(self.api_id, self.api_key), verify=False
            )
        if r.status_code == 200 or r.status_code == 201:
            data = r.json()
            return data
        else:
            return {
                'error': {
                    'code': 'bunny-api-error',
                    'message': 'An error occurred while trying to create a speedy project: \n' + r.text,
                }
            }

    def check_for_readings(self, project_id):
        """
        Check if the readings for a particular project
        are available
        """

        r = requests.get(
            settings.BUNNY_API_URL + '/projects/' + str(project_id),
            auth=HTTPBasicAuth(self.api_id, self.api_key), verify=False
            )
        if r.status_code == 200 or r.status_code == 201:
            data = r.json()
            return data
        else:
            return {
                'error': {
                    'code': 'bunny-api-error',
                    'message': 'An error occurred while trying to create a speedy project: \n' + r.text,
                }
            }



class TextAPI:
    def get_wikipedia_basic_info(titles):
        atts = {'prop': 'extracts', 'action': 'query', 'format': 'json',
                'explaintext': True, 'exlimit': '1',
                'titles': titles
                }
        r = requests.get('http://en.wikipedia.org/w/api.php', params=atts)

        if r.status_code == 200:
            data = r.json()
            return data['query']['pages']
        else:
            error = {
                    'code': 'wikipedia-api-error',
                    'message': 'An error occurred while trying to get info with the wikipedia api: \n' + r.text,
                }
            raise ValidationError(error)

        return resp.json()