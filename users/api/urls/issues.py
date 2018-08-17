from django.conf.urls import url
from users.api.views import issues

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', issues.IssueListAPIView.as_view(), name='list'),
    url(r'(?P<pk>[\w-]+)/$', issues.IssueDetailAPIView.as_view(), name='detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)