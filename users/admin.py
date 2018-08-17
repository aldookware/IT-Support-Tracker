from django.contrib import admin

from .models import Engineer, Client, ClientUser

admin.site.register(Engineer)
admin.site.register(Client)
admin.site.register(ClientUser)