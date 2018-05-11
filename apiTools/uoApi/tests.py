from django.test import TestCase
from django.test.client import RequestFactory
from django.http import HttpResponse

from unittest.mock import MagicMock

from .services import NexudusAuthenticator, NexudusMemberDataRequest, MailchimpRequest
from .views import VisitorTextNotificationView, MailchimpView

import os

signature = os.getenv('NEXUDUS_TEST_SIGNATURE')

class NexudusAuthenticatorTest(TestCase):

    def setUp(self):

        self.factory = RequestFactory()

    def test_is_valid(self):

        post_request = self.factory.post(
            '/',
            '{"test": "test json"}',
            'application/json',
            HTTP_HOST='test@api.alexperez.ninja',
            HTTP_X_NEXUDUS_HOOK_SIGNATURE=signature
        )

        authenticator = NexudusAuthenticator(post_request)

        self.assertEqual(authenticator.is_valid(), True)

class VisitorTextNotificationViewTest(TestCase):

    def setUp(self):
        VisitorTextNotificationView.send_twilio_request = MagicMock()
        VisitorTextNotificationView.send_member_phone_request = MagicMock(return_value="1")
        self.factory = RequestFactory()
        self.view = VisitorTextNotificationView()

    def test_post_request(self):

        visitor_data = os.getenv('NEXUDUS_VISITOR_NOTIFICATION_DATA')
        visitor_signature = os.getenv('NEXUDUS_VISITOR_NOTIFICATION_SIGNATURE')

        post_request = self.factory.post(
            '/',
            visitor_data,
            'application/json',
            HTTP_HOST='test@api.alexperez.ninja',
            HTTP_X_NEXUDUS_HOOK_SIGNATURE=visitor_signature
        )

        response = VisitorTextNotificationView.as_view()(post_request)

        self.assertEqual(response.status_code, 200)
        self.view.send_member_phone_request.assert_called_with(440488283)
        self.view.send_twilio_request.assert_called_with("Alex Perez", "Fake Visitor", "1")

    def test_bad_authentication(self):

        post_request = self.factory.post(
            '/',
            {"test": "bad_athentication_test"},
            'application/json',
            HTTP_HOST='test@api.alexperez.ninja',
            HTTP_X_NEXUDUS_HOOK_SIGNATURE='BADSIGNATURE1234'
        )

        response = VisitorTextNotificationView.as_view()(post_request)

        self.assertEqual(response.status_code, 403)

    def test_no_authentication(self):

        post_request = self.factory.post(
            '/',
            {"test": "no_athentication_test"},
            'application/json',
            HTTP_HOST='test@api.alexperez.ninja',
        )

        response = VisitorTextNotificationView.as_view()(post_request)

        self.assertEqual(response.status_code, 401)

class MailchimpViewTest(TestCase):
    def setUp(self):
        MailchimpView.send_mailchimp_request = MagicMock()
        self.mailchimp = MailchimpView()

        self.factory = RequestFactory()
        self.request_ok = self.factory.post(
            '/',
            '{"test": "test json"}',
            'application/json',
            HTTP_HOST='test@api.alexperez.ninja',
            HTTP_X_NEXUDUS_HOOK_SIGNATURE=signature
        )
        self.request_bad_auth = self.factory.post(
            '/',
            {"test": "bad_athentication_test"},
            'application/json',
            HTTP_HOST='test@api.alexperez.ninja',
            HTTP_X_NEXUDUS_HOOK_SIGNATURE='BADSIGNATURE1234'
        )
        self.request_no_auth = self.factory.post(
            '/',
            {"test": "no_athentication_test"},
            'application/json',
            HTTP_HOST='test@api.alexperez.ninja',
        )

    def test_post_request(self):

        response = MailchimpView.as_view()(self.request_ok)

        self.assertEqual(response.status_code, 200)
        self.mailchimp.send_mailchimp_request.assert_called_once()

    def test_mailchimp_request_is_called(self):

        post_request = self.request_ok

        response = MailchimpView.as_view()(post_request)

        self.mailchimp.send_mailchimp_request.assert_called_once()

    def test_bad_authentication(self):

        post_request = self.request_bad_auth

        response = MailchimpView.as_view()(post_request)

        self.assertEqual(response.status_code, 403)
        self.mailchimp.send_mailchimp_request.assert_not_called()

    def test_no_authentication(self):

        post_request = self.request_no_auth

        response = MailchimpView.as_view()(post_request)

        self.assertEqual(response.status_code, 401)
        self.mailchimp.send_mailchimp_request.assert_not_called()

# class NexudusMemberDataRequestTest(TestCase):
#     def setUp(self):
#         pass
#
#     def test_request(self):
#         request = NexudusMemberDataRequest(440488283)
#         print(request.send_request())

class MailchimpRequestTest(TestCase):
    # for the Mailchimp service, not the View (see above)
    def setUp(self):
        self.data_ok = [{
            "Email": "fakeemail@uwxdsctsed.com",
            "Name": "Fake Username"
        }]

    def test_data_formatting(self):
        mailchimp_data = MailchimpRequest().format_mailchimp_data(self.data_ok)

        correctly_formatted_data = '{"status": "subscribed", "email_address": "fakeemail@uwxdsctsed.com", "merge_fields": {"FNAME": "Fake", "LNAME": "Username"}}'

        self.assertEqual(mailchimp_data, correctly_formatted_data)

