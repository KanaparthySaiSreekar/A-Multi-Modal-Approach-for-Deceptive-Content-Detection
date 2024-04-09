import time
import requests
import ssl
from urllib.parse import urlparse
import whois
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver


class urlSecurity:
    def __init__(self, link):
        self.url = link
        self.parsed_url = urlparse(self.url)
        self.domain_name = self.parsed_url.netloc
        self.certificate = 'hii'

    def get_sss_certificate(self):
        try:
            #load the server certificate of the domain
            self.certificate = ssl.get_server_certificate((self.domain_name, 443)) #443 for https websites
        except:
            self.certificate = ''

    def check_valid_sss_certificate(self):
        if self.certificate != '':
            try:
                ssl.create_default_context().load_verify_locations(cadata=self.certificate)
            except:
                self.certificate = ''

    def check_is_safe(self):
        check_domain = self.url.split("//")[0]
        print(check_domain)
        if check_domain == 'http:' or 'http://' in self.url:
            self.certificate = ''

    def check_is_domain_safe(self):
        try:
            domain_info = whois.whois(self.domain_name)
            expiration_date = domain_info.expiration_date

            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]

            if expiration_date is not None and expiration_date > datetime.datetime.now():
                print("Domain is registered and not expired")
            else:
                self.certificate = ''

        except:
            self.certificate = ''

    def send_sample_request(self):
        try:
            req = requests.get(self.url, timeout=3)
            if req.status_code != 200:
                try:
                    if req.status_code == 424 and "Access Denied" not in req.text:
                        self.certificate = ''
                except:
                    self.certificate = ''

        except:
            self.certificate = ''


    def run(self):
        self.get_sss_certificate()
        self.check_valid_sss_certificate()
        self.check_is_safe()
        self.check_is_domain_safe()
        self.send_sample_request()

        if self.certificate == '':
            return False
        else:
            return True

