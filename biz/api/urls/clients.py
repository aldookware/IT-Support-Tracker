from django.conf.urls import url

from ..views.clients import ClientListView, ClientDetailView, ClientCreateViewAPIView, ClientUpdateAPIView

urlpatterns =[
    url(r'^$', ClientListView.as_view(), name='list'),
    url(r'^create/$', ClientCreateViewAPIView.as_view(), name='create'),
    url(r'^(?P<pk>[\w-]+)/$', ClientDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[\w-]+)/update/$', ClientUpdateAPIView.as_view(), name='update'),

]