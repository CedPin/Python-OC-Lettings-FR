from django.urls import reverse


class TestLettingSite:

    def test_index(self, client):
        expected_title = b"<title>Holiday Homes</title>"
        response = client.get(reverse("index"))
        assert response.status_code == 200
        assert expected_title in response.content
