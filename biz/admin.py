from django.contrib import admin

from .models import Engineer, Client, ClientUser, Issue, IssueLog

admin.site.register(Engineer)
admin.site.register(Client)
admin.site.register(ClientUser)


class InlineIssueLog(admin.TabularInline):
    model = IssueLog
    can_delete = False

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    inlines = [
        InlineIssueLog,
    ]
    fields = ['subject']
