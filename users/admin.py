from django.contrib import admin

from users.models import User
from .models import *


admin.site.register(User)
admin.site.register(TeachingRequest)
admin.site.register(NursingService)
admin.site.register(VolunteeringService)
admin.site.register(ContactMessage)



