import json

import pytest
from django.test import TestCase
from django.test import RequestFactory
from django.test.client import Client as c
from django.utils import timezone

from mixer.backend.django import mixer

from biz.api.views.issues import IssueListAPIView

pytestmark = pytest.mark.django_db


class IssueListView(TestCase):
    def setUp(self):
        self.issue = mixer.blend('biz.Issue', subject='test issue')
        self.user = mixer.blend('biz.User', is_engineer=True, username='tes')
        self.user.set_password('test')
        self.user.save()

        self.client = mixer.blend('biz.Client', title='CiF')

        self.request = c()
        self.request.login(username=self.user.username, password='test')
        self.content_type = 'application/json'

    def test_issue_list_view_access(self):
        req = RequestFactory().get('api/issues/')
        req.user = self.user
        response = IssueListAPIView.as_view()(req)
        assert response.status_code == 200, 'Should be callable by authorised biz only'

    def test_issue_create(self):
        self.user = mixer.blend('biz.User', is_superuser=True, username='test')
        self.request.login(username=self.user.username, password='test')

        # we define test data
        data = json.dumps({
            'subject': 'Qickbooks Issue',
            'client': str(self.client.pk),
            'created_by': str(self.user),
            'issue_description': "Quickbooks has not been working for two weeks now, ",
            'expected_date': str(timezone.now().date())
        })

        res = self.request.post('/api/issues/create/', data=data, content_type=self.content_type)
        assert res.status_code == 201, 'Should post an Instance of the Issue in to the database'

    def test_issue_update(self):
        data = json.dumps({
            'issue_description': 'remember to email dave',
            'created_by': str(self.user.pk),
            'client': str(self.client.pk), })

        res = self.request.put(
            self.issue.get_absolute_url(),
            data=data,
            content_type=self.content_type)
        assert res.status_code == 200, 'Should update issue record'


class LandingView:
    def test_annoymous(self):
        client = c()
        response = client.get('/')
        assert response.status_code == 200, 'Main API landing page should be callable'
