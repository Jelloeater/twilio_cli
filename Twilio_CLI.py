# Download the helper library from https://www.twilio.com/docs/python/install
from requests.utils import quote
from twilio.rest import Client
import settings

import argparse
import logging

__author__ = 'jesse'

class helpers():
    @staticmethod
    def build_say_url(speech_input:str):
        url_begin="http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSay%3E"
        message_url = speech_input.replace(" ", "+")
        url_end= "%3C%2FSay%3E%3C%2FResponse%3E"
        return  url_begin + message_url + url_end

    @staticmethod
    def send_call(phone_in:str,message_in:str):
        client = Client(settings.account_sid, settings.auth_token)
        url = helpers.build_say_url(message_in)
        call = client.calls.create(url=url, to='+'+phone_in, from_='+'+settings.from_phone_number)
        logging.debug(call.sid)


def main():
    LOG_FILENAME = 'error.log'
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug",
                        action="store_true",
                        help="Debug Mode Logging")

    parser.add_argument("-p",
                        required=True,
                        help="Phone Number to call (ex 19008675309)")

    parser.add_argument("-m",
                        required=True,
                        help="Message to speak")

    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] --- %(message)s "
                                   "(%(filename)s:%(lineno)s)",
                            level=logging.DEBUG)
        logging.debug('Debug Mode Enabled')
    else:
        logging.basicConfig(filename=LOG_FILENAME,
                            format="[%(asctime)s] [%(levelname)8s] --- %(message)s "
                                   "(%(filename)s:%(lineno)s)",
                            level=logging.WARNING)

    helpers.send_call(phone_in=args.p,message_in=args.m)
   
if __name__ == "__main__":
    main()