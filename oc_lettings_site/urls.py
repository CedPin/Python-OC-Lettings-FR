from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', include('profiles.urls', namespace='profiles')),
    path('', include('lettings.urls', namespace='lettings')),
    path('admin/', admin.site.urls),
]
