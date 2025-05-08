from django.urls import path
from .import views
from .views import *

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('user/login/', login_view, name='user_login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),

    path('teaching_service/', views.teaching_service_view, name='teaching_service'),
    path('nursing_service/', views.nursing_service_view, name='nursing_service'),
    path('volunteering_service/', views.volunteering_service_view, name='volunteering_service'),
    path('provider_dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('provider_teaching_posts/', views.provider_teaching_posts, name='provider_teaching_posts'),
    path('provider_nursing_posts/', views.provider_nursing_posts, name='provider_nursing_posts'),
    path('provider_volunteering_posts/', views.provider_volunteering_posts, name='provider_volunteering_posts'),
    path('provider_my_accepted_posts/', views.my_accepted_posts, name='provider_my_accepted_posts'),
    path('customer_dashboard_my_requests/', views.customer_my_requests, name='customer_my_requests'),







]
