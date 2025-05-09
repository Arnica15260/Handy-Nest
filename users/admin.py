from django.contrib import admin

from users.models import User
from .models import *


admin.site.register(User)
admin.site.register(TeachingRequest)
admin.site.register(NursingService)
admin.site.register(VolunteeringService)
admin.site.register(ContactMessage)

@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'completed_services', 'last_certificate_milestone')
    search_fields = ('user__username',)
    list_filter = ('completed_services',)

