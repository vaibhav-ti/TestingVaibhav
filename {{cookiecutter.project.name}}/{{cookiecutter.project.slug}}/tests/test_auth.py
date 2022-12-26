import os
import json
import pytest

from .utils import get_authenticated_client

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
data_path = os.path.join(dir_path, "data")

user_data = json.load(open(os.path.join(data_path, 'sample.user.json')))

CONTENT_TYPE = 'application/json'


@pytest.mark.django_db
class TestUsers:
    pytestmark = pytest.mark.django_db

    def test_signup(self, client, db):
        response = client.post('/auth/registration/', data=user_data, content_type=CONTENT_TYPE)
        assert response.status_code == 201
        assert "key" in response.data

    def test_login(self, client, signup):
        response = client.post('/auth/login/', data=user_data, content_type=CONTENT_TYPE)
        assert response.status_code == 200
        assert 'key' in response.data

    def test_login_fail(self, client):
        response = client.post('/auth/login/', data=user_data, content_type=CONTENT_TYPE)
        assert response.status_code == 400

    def test_logout(self, client, django_user_model, signup):
        client = get_authenticated_client(user_data)
        response = client.post('/auth/logout/', content_type=CONTENT_TYPE)
        assert response.status_code == 200
