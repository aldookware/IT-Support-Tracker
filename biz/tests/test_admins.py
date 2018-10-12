import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib import admin
from django.test import TestCase
from django.test.client import Client
from biz import admin as ad

from mixer.backend.django import mixer


class TestIssueAdmin(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.issue = mixer.blend('biz.Issue', subject='I cant not connect to the server')
        self.client = Client()

    def test_issue_modeladmin(self):
        issue_admin = ad.IssueAdmin(self.issue, self.site)
        self.assertEqual(str(issue_admin), 'biz.IssueAdmin'), 'Should check for existance of  Issue admin'

    def test_inline_fieldsets(self):
        issue_admin = ad.IssueAdmin(self.issue, self)
        request = self.client.get('/')
        self.assertEqual(list(issue_admin.get_fields(request)), ['subject'])
        # issue_log = mixer.blend('biz.IssueLog', issue=self.issue)
        #
        # issue_log_inline = ad.InlineIssueLog(issue_log, self.site)
        # form = issue_log_inline.get_formset(None).form
        # self.assertEqual(form._meta.fields, ['issue', 'notes'])
