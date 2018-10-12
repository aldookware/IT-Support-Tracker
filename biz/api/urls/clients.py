from django.conf.urls import url, include

from ..views.clients import ClientViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', ClientViewSet)

urlpatterns =[
    url(r'^', include(router.urls)),
]