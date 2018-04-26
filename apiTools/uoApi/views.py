from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .services import NexudusAuthenticator, MailchimpRequest

import os
import json
import logging

class VisitorTextNotificationView(View):

	logger = logging.getLogger('uoApi.visitorTextNotificationView')

	def post(self, request):

		authenticator = NexudusAuthenticator(request)

		if authenticator.is_valid():
			request_body_str = request.body.decode('utf-8')
			request_body_loaded = json.loads(request_body_str)

			self.logger.info(request_body_str)

			# Text notification code goes here

		return HttpResponse(status=authenticator.response_code)

	def get(self, request):

		return HttpResponse("<html><body><h1>Established!</h1></body></html>")

class MailchimpView(View):

	def send_mailchimp_request(self, data):

		MailchimpRequest().send_request(data)

	def post(self, request):

		authenticator = NexudusAuthenticator(request)

		if authenticator.is_valid():
			request_body_str = request.body.decode('utf-8')
			request_body_loaded = json.loads(request_body_str)

			self.send_mailchimp_request(request_body_loaded)

		return HttpResponse(status=authenticator.response_code)

	def get(self, request):
		html = "<html><body><h1 style='font-size:75px;'>Tests or log review could go here!</h1></body></html>"
		return HttpResponse(html)


def index(request):
	return render(request, 'uoApi/index.html')
