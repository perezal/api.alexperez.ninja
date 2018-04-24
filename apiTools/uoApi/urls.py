from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'uoApi'
urlpatterns = [
	path('mail_list/', csrf_exempt(views.MailchimpView.as_view()), name='mail_list'),
	path('text_notifications/', csrf_exempt(views.VisitorTextNotificationView.as_view()), name='text_notifications'),
	path('', views.index, name='index'),
]
