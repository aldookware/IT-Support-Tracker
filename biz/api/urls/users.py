from django.conf.urls import url
from biz.api.views import users

urlpatterns = [
    url(r'^$', users.user_list, name='list'),
    url(r'(?P<pk>[\w-]+)/$', users.user_detail, name='detail'),
]