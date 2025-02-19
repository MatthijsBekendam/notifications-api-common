from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

import pytest
from zgw_consumers.constants import APITypes
from zgw_consumers.service import Service

from notifications_api_common.models import NotificationsConfig
from testapp import urls  # noqa


def dummy_get_response(request):
    raise NotImplementedError()


@pytest.fixture()
def request_with_middleware(rf):
    request = rf.get("/")
    SessionMiddleware(get_response=dummy_get_response).process_request(request)
    MessageMiddleware(get_response=dummy_get_response).process_request(request)
    return request


@pytest.fixture()
def notifications_config():
    service = Service.objects.create(
        api_root="http://some-api-root/api/v1/", api_type=APITypes.nrc
    )
    config = NotificationsConfig.get_solo()
    config.notifications_api_service = service
    config.save()
    return config
