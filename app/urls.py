"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers

# from users.api.views import EngineerViewSet, ClientViewSet, UserViewSet

router = routers.DefaultRouter()
# router.register(r'engineers', EngineerViewSet)
# router.register(r'clients', ClientViewSet)
# router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/users/', include('users.api.urls.users', namespace='user-api')),
    url(r'^api/issues/', include('users.api.urls.issues', namespace='issue-api')),
    url(r'^api/clients/', include('users.api.urls.clients', namespace='issue-api')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
