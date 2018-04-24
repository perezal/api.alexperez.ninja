from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('arrivals/<int:stop_id>/', views.arrivals, name='arrivals'),
	path('lines/', views.lines, name='lines'),
	path('lines/<int:line_id>/', views.lines, name='lines'),
	path('stops/<str:longitude>/<str:latitude>/', views.stops, name='stops'),
]
