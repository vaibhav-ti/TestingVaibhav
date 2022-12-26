from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    UserViewSet,
    HealthCheck,
    {% if cookiecutter.documentation.sample_crud.enabled == "True" %}
    AddressViewSet,
    NoteViewSet
    {% endif %}
)

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r'users', UserViewSet, basename="user-detail")
{% if cookiecutter.documentation.sample_crud.enabled == "True" %}
router.register(r'user-addresses', AddressViewSet, basename="user-address-detail")
router.register(r'notes', NoteViewSet, basename="note-detail")
{% endif %}
urlpatterns = [
    path('healthcheck/', HealthCheck.as_view())
]
