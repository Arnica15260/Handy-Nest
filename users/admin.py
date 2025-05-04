from django.contrib import admin

from users.models import User
from .models import *


admin.site.register(User)

