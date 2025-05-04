from django.urls import path
from .import views
from .views import *

urlpatterns = [
    # Dashboard and Authentication
    path('dashboard/', dashboard_view, name='dashboard'),
    path('user/login/', login_view, name='user_login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),


]
