import pytest
import uuid

from django.test.client import Client as test_client
from django.test import TestCase
from mixer.backend.django import mixer
from biz.models import User, Issue, Service, Engineer
from biz.api.views import clients

pytestmark = pytest.mark.django_db


class TestClient(TestCase):
    def setUp(self):
        self.client = mixer.blend('biz.Client', title='test')
        self.user = mixer.blend('biz.User', username='test')
        self.user.set_password('test')
        self.user.save()

    def test_model(self):
        assert self.client.title == 'test', 'Should create a Client instance'
        assert self.client.__str__() == self.client.title, \
            'Client title should match the value of client.__str__() function'

    def test_absolute_url(self):
        # client = test_client()
        # client.login(username=self.user.username, password='test')
        # response = client.get(self.client.get_absolute_url())
        # assert response.status_code == 200, 'Should return a 200 OK is its valid client url'
        assert self.client.get_absolute_url() == '/api/clients/{}/'.format(self.client.pk), \
            'Should return a valid url for a client instance'


class TestUser:
    def test_model(self):
        user = mixer.blend(User, username='test')
        assert user.username == 'test', 'Should create user instance'
        assert user.__str__() == str(user.id), 'Should be abstract class'


class TestIssue(TestCase):
    def setUp(self):
        self.issue = mixer.blend(Issue, subject='Pc wont bootup')
        self.user = mixer.blend('biz.User', username='admin')
        self.user.set_password('test')
        self.user.save()

    def test_model(self):
        assert self.issue.subject == 'Pc wont bootup', 'Should create a Issue instance'
        assert self.issue.__str__() == str(self.issue.id), 'issue__str__() must match str version of ID'

    def test_issue_get_absolute_url(self):
        client = test_client()
        client.login(username='admin', password='test')
        response = client.get(self.issue.get_absolute_url())
        assert response.status_code == 200, \
            'Should return a status code 200 Ok for valid issue instance url'

    def test_issue_log_model(self):
        log = mixer.blend('biz.IssueLog', issue=self.issue)
        assert log.__str__() == str(log.id)
        assert log.issue == self.issue


class TestService:
    def test_model(self):
        key = uuid.uuid4()
        service = mixer.blend(Service, pk=key)
        assert service.pk == key, 'Should create service instance'
        assert service.__str__() == str(service.id), \
            'The service __str__() return value should match the str value the service ID'
        assert isinstance(service, Service), 'Should be an instance of service'


class TestEngineer:
    def test_model(self):
        user = mixer.blend(User, username='test')
        engineer = mixer.blend(Engineer, user=user)
        assert engineer.user == user, 'Should create an Engineer instance'
        assert engineer.__str__() == str(engineer.user.id), \
            'The __str__() should much the str value of the engineer ID'
