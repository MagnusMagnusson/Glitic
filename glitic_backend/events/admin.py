from django.contrib import admin
from events.models import Event, Eventcounter, Eventregister, Eventnote

admin.site.register(Event)
admin.site.register(Eventregister)

class EventNodeinline(admin.TabularInline):
    model = Eventnote

class EventCounterAdmin(admin.ModelAdmin):
    inlines = [
        EventNodeinline,
    ]


admin.site.register(Eventcounter, EventCounterAdmin)