# Serializers define the API representation.
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault, Serializer

from .models import (
    User, 
    {%- if cookiecutter.documentation.sample_crud.enabled == "True" %}
    UserAddress, 
    Note
    {%- endif %}
)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        )


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

{% if cookiecutter.documentation.sample_crud.enabled == "True" %}
class AddressSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = UserAddress
        fields = [
            "user",
            "building",
            "street_1",
            "street_2",
        ]


class NoteSerializer(ModelSerializer):
    {%- if cookiecutter.authentication.enabled == "True" %}
    user = HiddenField(default=CurrentUserDefault())
    {%- endif %}
    noteId = serializers.IntegerField(source='id', read_only=True)
    createdAt = serializers.DateTimeField(source="created_at" ,read_only=True)

    class Meta:
        model = Note
        fields = [
            "noteId",
            {%- if cookiecutter.authentication.enabled == "True" %}
            "user",
            {%- endif %}
            "content",
            "createdAt",
        ]
{%- endif %}
