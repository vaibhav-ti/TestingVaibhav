import logging
{%- if cookiecutter.authentication.social.devconnect.enabled == 'True' %}
import requests
{%- endif %}

from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

{%- if cookiecutter.authentication.social.devconnect.enabled == 'True' %}
from rest_framework.authtoken.models import Token

from {{cookiecutter.project.slug}}.settings import DEVCONNECT_ISSUER_URL, DEVCONNECT_CLIENT_ID, DEVCONNECT_CLIENT_SECRET, REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI
{%- endif %}

from .models import (
    User,
    {%- if cookiecutter.documentation.sample_crud.enabled == "True" %}
    UserAddress,
    Note
    {%- endif %}
)
from .serializers import (
    UserSerializer,
    PasswordSerializer,
    {%- if cookiecutter.documentation.sample_crud.enabled == "True" %}
    AddressSerializer,
    NoteSerializer
    {%- endif %}
)
from .permissions import IsOwnerOrAdmin

logger = logging.getLogger(__name__)


class HealthCheck(APIView):
    """
        API View to return the Health of the service
    """
    def get(self, request):
        return Response(status=status.HTTP_200_OK)


# ViewSets define the view behavior.
class UserViewSet(ModelViewSet):
    """
        A viewset for viewing and editing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')
        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)

{% if cookiecutter.documentation.sample_crud.enabled == "True" %}
class AddressViewSet(ModelViewSet):
    """
        Views for viewing and editing user address instances.
    """
    queryset = UserAddress.objects.all()
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = AddressSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            logger.info("Authenticated User: ", self.request.user)
            queryset = UserAddress.objects.all()
            if not self.request.user.is_superuser:
                queryset = queryset.filter(user=self.request.user)
            return queryset
        return []


class NoteViewSet(ModelViewSet):
    serializer_class = NoteSerializer
    {%- if cookiecutter.authentication.enabled == "True" %}
    permission_classes = [IsAuthenticated]
    {%- endif %}

    def get_queryset(self):
        {%- if cookiecutter.authentication.enabled == "True" %}
        queryset = Note.objects.filter(user=self.request.user)
        {% else %}
        queryset = Note.objects.all()
        {%- endif -%}
        return queryset


class SampleViewSet(ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
{% endif %}


{% if cookiecutter.authentication.social.devconnect.enabled == 'True' %}
class DevConnectAuthView(APIView):
    """
    Authenticates user with DevConnect and returns a token
    """

    def post(self, request):
        url = DEVCONNECT_ISSUER_URL.rstrip("/") + "/protocol/openid-connect/token/"
        code = request.data.get('code')
        if code is None:
            return Response("Code Not Found", status=status.HTTP_400_BAD_REQUEST)
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        post_data = {
            'client_id': DEVCONNECT_CLIENT_ID,
            'client_secret': DEVCONNECT_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI
        }
        response = requests.post(url, data=post_data, headers=header)

        if (response.status_code == 200):
            body = response.json()
            logger.info(f"Auth Response Fetched")
            id_token = body['access_token']
            url = DEVCONNECT_ISSUER_URL.rstrip("/") + "/protocol/openid-connect/userinfo/"
            header = {
                'Authorization': 'Bearer ' + id_token
            }
            response = requests.get(url, headers=header)

            if response.status_code == 200:
                details = response.json()
                logger.info(f"User Info {details}")
                user, _ = User.objects.get_or_create(
                    username=details['preferred_username'],
                    defaults={
                        'email': details['email'],
                        'first_name': details['given_name'],
                        'last_name': details['family_name']
                    }
                )
                token, _ = Token.objects.get_or_create(user=user)
                # return TokenSerializer
                return Response({"token": str(token)}, status=status.HTTP_200_OK)
            else:
                logger.error(f"Unable to fetch User Info from DevConnect")
                return Response(status=response.status_code)
        logger.error(f"Unable to fetch Credentials using the provided Code")
        return Response(status=response.status_code)
{% endif %}
