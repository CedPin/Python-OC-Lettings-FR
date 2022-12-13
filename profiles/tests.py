import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile


@pytest.fixture
def profile_fixture():
    user = User.objects.create(username="CedPi")
    return Profile.objects.create(user=user, favorite_city="Lille")


@pytest.mark.django_db
class TestProfile:

    def test_index(self, client, profile_fixture):
        expected_title = b"<title>Profiles</title>"
        response = client.get(reverse("profiles:index"))
        assert response.status_code == 200
        assert response.context["profiles_list"][0] == profile_fixture
        assert expected_title in response.content

    def test_detail(self, client, profile_fixture):
        expected_title = b"<title>CedPi</title>"
        response = client.get(
            reverse("profiles:profile",
                    kwargs={"username": profile_fixture.user.username})
        )
        assert response.status_code == 200
        assert response.context["profile"] == profile_fixture
        assert expected_title in response.content
