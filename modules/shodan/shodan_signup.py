import re
from hashlib import md5
from typing import Dict

from getmailnow.mailboxes import WebhookSite
from html_form_to_dict import html_form_to_dict
from requests import Session

from lib.commons.melman_logging import get_logger

SHODAN_REGISTER_URL = "https://account.shodan.io/register"
SHODAN_CSRF_TOKEN = "csrf_token"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/120.0.0.0 Safari/537.36"
ACTIVATION_REGEX = re.compile("https://account.shodan.io/activate/[0-9a-z]+")

logger = get_logger("ShodanSignup")

class ShodanSignup:
    _mail: WebhookSite

    def __init__(self) -> None:
        self._mail = WebhookSite()
        self._session = Session()
        self._session.headers.update({
            "User-Agent": USER_AGENT
        })

    def register_new_account(self) -> Session:
        # Request new account
        logger.info("Registering new Shodan account")
        self._session.post(SHODAN_REGISTER_URL, data=self.generate_register_params())

        # Get activation link
        activation_link = self._mail.wait_for_code(ACTIVATION_REGEX)

        # Activate!
        logger.info("Activating new account")
        self._session.get(activation_link.group())

        return self._session

    def get_csrf_token(self) -> None:
        response = self._session.get(SHODAN_REGISTER_URL)
        form = html_form_to_dict(response.text)

        return form[SHODAN_CSRF_TOKEN]

    def generate_register_params(self) -> Dict[str, str]:
        return {
            "username": self.get_username(),
            "password": self.get_password(),
            "password_confirm": self.get_password(),
            "email": self._mail.get_email(),
            "csrf_token": self.get_csrf_token()
        }

    def get_username(self) -> str:
        return self.get_password()[::-1]

    def get_password(self) -> str:
        return md5(self._mail.get_email().encode()).hexdigest()
