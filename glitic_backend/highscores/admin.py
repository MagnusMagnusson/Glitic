from django.contrib import admin
from highscores.models import Simplescore, Simpletable

admin.site.register(Simpletable)
admin.site.register(Simplescore)