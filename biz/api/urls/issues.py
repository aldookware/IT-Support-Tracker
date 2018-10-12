from django.conf.urls import url
from biz.api.views import issues


urlpatterns = [
    url(r'^$', issues.IssueListAPIView.as_view(), name='list'),
    url(r'create/$', issues.IssueCreateAPIView.as_view(), name='create'),
    url(r'(?P<pk>[\w-]+)/$', issues.IssueDetailAPIView.as_view(), name='detail'),
]
