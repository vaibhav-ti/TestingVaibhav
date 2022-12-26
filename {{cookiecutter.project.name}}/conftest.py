import os
import json
import pytest
from rest_framework.test import APIClient

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "{{cookiecutter.project.slug}}/tests/data")

user_data = json.load(open(os.path.join(data_path, 'sample.user.json')))

CONTENT_TYPE = 'application/json'


def get_authenticated_client():
    client = APIClient()
    response = client.post('/auth/login/', data=user_data, format='json', content_type=CONTENT_TYPE)
    token = response.data.get('key')
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    return client


@pytest.fixture()
def signup(client, db):
    client.post('/auth/registration/', data=user_data, content_type=CONTENT_TYPE)