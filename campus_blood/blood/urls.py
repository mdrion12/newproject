from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # new homepage
    path('add-donation/', views.add_donation, name='add_donation'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create-profile/', views.create_donor_profile, name='create_donor_profile'),
    path('donors/', views.donor_list, name='donor_list'),
    path('request/<int:donor_id>/', views.request_donor, name='request_donor'),
    path('my-requests/', views.donor_requests, name='donor_requests'),
    path('toggle-availability/', views.toggle_availability, name='toggle_availability'),
    path('respond-request/<int:req_id>/<str:status>/', views.respond_request, name='respond_request'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
