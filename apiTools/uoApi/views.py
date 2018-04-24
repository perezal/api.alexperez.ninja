from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .services import NexudusValidator, MailchimpRequest

import os
import json
import logging

class VisitorTextNotificationView(View):

	logger = logging.getLogger('uoApi.views')

	def post(self, request):

		validator = NexudusValidator(request)

		if validator.is_valid():
			request_body_str = request.body.decode('utf-8')
			corrected_json = request_body_str.replace("'", '"') # Nexudus uses single quotes
			request_body_loaded = json.loads(corrected_json)

			# Text notification code goes here

		return HttpResponse(status=validator.response_code)

	def get(self, request):

		return HttpResponse("<html><body><h1>Established!</h1></body></html>")

class MailchimpView(View):

	def send_mailchimp_request(self, data):

		MailchimpRequest().send_request(data)

	def post(self, request):

		validator = NexudusValidator(request)

		if validator.is_valid():
			request_body_str = request.body.decode('utf-8')
			corrected_json = request_body_str.replace("'", '"') # Nexudus uses single quotes
			request_body_loaded = json.loads(corrected_json)

			self.send_mailchimp_request(request_body_loaded)

		return HttpResponse(status=validator.response_code)

	def get(self, request):
		html = "<html><body><h1 style='font-size:75px;'>Tests or log review could go here!</h1></body></html>"
		return HttpResponse(html)


def index(request):
	return render(request, 'uoApi/index.html')
