from django.test import TestCase
from django.test.client import RequestFactory
from django.http import HttpResponse

from unittest.mock import MagicMock

from .services import NexudusValidator, MailchimpRequest
from .views import VisitorTextNotificationView, MailchimpView

import os

signature = os.getenv('NEXUDUS_TEST_SIGNATURE')

class NexudusValidatorTest(TestCase):

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

        validator = NexudusValidator(post_request)

        self.assertEqual(validator.is_valid(), True)

class VisitorTextNotificationViewTest(TestCase):

    def setUp(self):

        self.factory = RequestFactory()

    def test_post_request(self):

        post_request = self.factory.post(
            '/',
            '{"test": "test json"}',
            'application/json',
            HTTP_HOST='test@api.alexperez.ninja',
            HTTP_X_NEXUDUS_HOOK_SIGNATURE=signature
        )

        response = VisitorTextNotificationView.as_view()(post_request)

        self.assertEqual(response.status_code, 200)

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

