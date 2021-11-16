from django.contrib import admin
from clientkeys.models import Clientkey, ClientKeyPermission

class ClientKeyAdmin(admin.ModelAdmin):
    readonly_fields = ["key"]


admin.site.register(ClientKeyPermission)
admin.site.register(Clientkey, ClientKeyAdmin)