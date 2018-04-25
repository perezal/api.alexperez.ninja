from hashlib import sha256
import hmac
import requests
import json
import os
import logging

class NexudusAuthenticator():
    def __init__(self, request):
        self.__NEXUDUS_KEY = os.getenv('NEXUDUS_WEBHOOK_PASS')
        self.logger = logging.getLogger('uoApi.views')
        self.request = request

        self.response_code = self.__authenticate_request()

    def is_valid(self):
        if self.response_code == 200:
            return True
        else:
            return False

    def __create_hash(self, body, key):
        dig = hmac.new(
            key,
            msg=body,
            digestmod=sha256
        )
        calculated_hmac = dig.hexdigest().upper()
        return calculated_hmac

    def __verify_webhook(self, signature, body, key):
        calculated_hmac = self.__create_hash(body, key)
        return (calculated_hmac == signature)

    def __authenticate_request(self):
        body = self.request.body
        body_str = body.decode('utf-8')

        try:
        	signature = self.request.META['HTTP_X_NEXUDUS_HOOK_SIGNATURE']
        except:
        	self.logger.info('No Signature')
        	self.logger.info(self.request.META['HTTP_HOST'])
        	self.logger.info(body_str)
        	return 401 # 401 Unauthorized / No Authentication

        if (self.__verify_webhook(signature, body, str.encode(self.__NEXUDUS_KEY))):
        	self.logger.info('Nexudus Authentication Successful')
        	self.logger.info(body_str)
        	return 200
        else:
        	self.logger.info('Nexudus Authentication Unsuccessful')
        	self.logger.info(body_str)
        	return 403 # 403 Forbidden

class MailchimpRequest():

    def __init__(self):
        # The contents of username do not matter, but must exist
        self.username = os.getenv('MAILCHIMP_USER')
        self.password = os.getenv('MAILCHIMP_PASS')
        self.api_url = os.getenv('MAILCHIMP_API_URL')

    def send_request(self, data):
        mailchimp_data = self.format_mailchimp_data(data)
        requests.post(self.api_url, data=mailchimp_data, auth=(self.username, self.password))

    # method needs refactor
    def format_mailchimp_data(self, data):

        for item in data:
            output = {"status": "subscribed"}
            if ('Email' in item):
                output['email_address'] = item['Email']
            else:
                output['email_address'] = ""

            last_name = ""
            first_name = ""
            if ('Name' in item):
                name_array = item['Name'].split()
                if len(name_array) == 1:
                    first_name = name_array[0]
                elif len(name_array) > 1:
                    last_name = " ".join(name_array[1:])
                    first_name = name_array[0]
            output['merge_fields'] = {'FNAME': first_name, 'LNAME': last_name}

            output = json.dumps(output)
            return output