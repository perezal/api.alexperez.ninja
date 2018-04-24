from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('uo/', include('uoApi.urls')),
    path('trimet/', include('trimetApi.urls')),
]
