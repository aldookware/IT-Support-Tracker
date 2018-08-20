import pytest
import uuid
from mixer.backend.django import mixer
from users.models import Client, User, Issue, Service, Engineer

pytestmark = pytest.mark.django_db


class TestClient:
    def test_model(self):
        client = mixer.blend(Client, title='test')
        assert client.title == 'test', 'Should client instance'

    def test_absolute_url(self):
        client = mixer.blend(Client)
        # assertIs(client.get_absolute_url())
        pass


class TestUser:
    def test_model(self):
        user = mixer.blend(User, username='test')
        assert user.username == 'test', 'Should create user instance'


class TestIssue:
    def test_model(self):
        issue = mixer.blend(Issue, subject='Pc wont bootup')
        assert issue.subject == 'Pc wont bootup', 'Should create a Issue instance'


class TestService:
    def test_model(self):
        key = uuid.uuid4()
        service = mixer.blend(Service, pk=key)
        assert service.pk == key, 'Should create service instance '


class TestEngineer:
    def test_model(self):
        user = mixer.blend(User, username='aldo')
        engineer = mixer.blend(Engineer, user=user)
        assert engineer.user == user, 'Should create an Engineer instance '


