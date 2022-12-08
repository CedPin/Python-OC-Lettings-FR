from django.urls import path
from profiles import views

app_name = "profiles"

urlpatterns = [
    path('profiles/', views.index, name='index'),
    path('profiles/<str:username>/', views.profile, name='profile'),
]
