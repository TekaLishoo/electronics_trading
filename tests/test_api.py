import pytest
from django.urls import reverse


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


def test_request_inactive_user(api_client):
    """
    Check API request of an inactive user.
    """

    url = reverse("product-list")
    response = api_client.get(url)
    assert response.status_code == 403


def test_update_request(api_client):
    """
    Check update API request of an inactive user.
    """

    url = reverse("networkobject-detail", kwargs={"pk": 2})
    response = api_client.post(url, data={"type": 2})
    assert response.status_code == 403
