from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .services import NexudusAuthenticator, MailchimpRequest, TwilioRequest, NexudusMemberDataRequest

import os
import json
import logging

class VisitorTextNotificationView(View):

	logger = logging.getLogger('uoApi.visitorTextNotificationView')
	response = HttpResponse()

	def send_twilio_request(self, member_name, visitor_name, member_phone):
		twilio_request = TwilioRequest(member_name, visitor_name, member_phone)
		twilio_request.send_request()

	def send_member_phone_request(self, member_id):
		data_request = NexudusMemberDataRequest(member_id)
		response = data_request.send_request()
		member_phone = response['MobilePhone']
		if member_phone is None:
			self.response = HttpResponse(status=400, reason='Member has no listed mobile number')
			return
		return response['MobilePhone']

	def post(self, request):

		authenticator = NexudusAuthenticator(request)
		self.response = HttpResponse(status=authenticator.response_code)
		if authenticator.is_valid():
			request_body_str = request.body.decode('utf-8')
			request_body_loaded = json.loads(request_body_str)
			for request in request_body_loaded:
				member_name = request['CoworkerFullName']
				visitor_name = request['FullName']
				member_id = request['CoworkerId']
				member_phone = self.send_member_phone_request(member_id)
				if self.response.status_code == 200:
					self.send_twilio_request(member_name, visitor_name, member_phone)

		return self.response

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
