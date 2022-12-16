import pytest
from django.urls import reverse
from lettings.models import Letting, Address


@pytest.fixture
def letting_fixture():
    my_address = Address.objects.create(
        number="4",
        street="Rue Cervantes",
        city="Lille",
        state="France",
        zip_code="59000",
        country_iso_code="17",
    )
    return Letting.objects.create(title="My Home", address=my_address)


@pytest.mark.django_db
class TestLetting:

    def test_index(self, client, letting_fixture):
        expected_title = b"<title>Lettings</title>"
        response = client.get(reverse("lettings:index"))
        assert response.status_code == 200
        assert response.context["lettings_list"][0] == letting_fixture
        assert expected_title in response.content

    def test_detail(self, client, letting_fixture):
        expected_title = b"<title>My Home</title>"
        response = client.get(
            reverse("lettings:letting",
                    kwargs={"letting_id": letting_fixture.id})
        )
        assert response.status_code == 200
        assert response.context["title"] == letting_fixture.title
        assert response.context["address"] == letting_fixture.address
        assert expected_title in response.content
