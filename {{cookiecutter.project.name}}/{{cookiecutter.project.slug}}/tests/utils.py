import os
import json
from rest_framework.test import APIClient

dir_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(dir_path, "data")


def get_authenticated_client(user_data):
    client = APIClient()
    response = client.post('/auth/login/', data=user_data, format='json')
    token = response.data.get('key')
    client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    return client
