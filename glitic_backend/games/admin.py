from django.contrib import admin
from clientkeys.models import Clientkey
from games.models import Game


class ClientkeyInline(admin.TabularInline):
    model = Clientkey
    extra = 0
    readonly_fields=["key","name","revoked","expired"]
    fields = ["key", "name","revoked","expired"]

class GameAdmin(admin.ModelAdmin):
    inlines = [
        ClientkeyInline,
    ]

admin.site.register(Game, GameAdmin)