#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Send cleaned up versions of a web page to a Kindle.

http://alexwlchan.net/2016/06/reading-web-pages-on-my-kindle/

Requires Python 3.
"""

import inspect

import contextlib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import re
import tempfile
import smtplib
import sys

import requests

try:  # Pythonista on iOS
    import appex
    import keychain as keyring
except ImportError:
    import keyring


#: API key for the Instaparser API
API_KEY = 'abcdef123456'

#: Email address for sending documents to your Kindle.
KINDLE_ADDR = 'send.to.kindle.address@kindle.com'

#: Username/password for the FastMail SMTP client
USERNAME = keyring.get_password('fastmail', 'username')
PASSWORD = keyring.get_password('fastmail', 'password')


def get_html_from_url(url):
    """Scrapes a URL for HTML; returns the saved HTML file."""
    req = requests.get('https://www.instaparser.com/api/1/article',
                       params={'api_key': API_KEY, 'url': url})

    if req.status_code != requests.codes.ok:
        raise RuntimeError("Unexpected error from the Instaparser API: %s"%
                           req.status_code)

    title = re.sub(u'[–—/:;,.]', '-', req.json()['title'])
    text = req.json()['html'].encode('ascii', 'xmlcharrefreplace')

    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, '%s.html' % title.replace('"', '\''))

    with open(path, 'wb') as outfile:
        outfile.write(b"<html><body>%s</body></html>" % text)

    return path


class FastMailSMTP(smtplib.SMTP_SSL):
    """A wrapper for handling SMTP connections to FastMail."""

    def __init__(self, username, password):
        super().__init__('mail.messagingengine.com', port=465)
        self.login(username, password)

    def send_message(self, *,
                     from_addr,
                     to_addrs,
                     msg,
                     subject,
                     attachments=None):
        msg_root = MIMEMultipart()
        msg_root['Subject'] = subject
        msg_root['From'] = from_addr
        msg_root['To'] = ', '.join(to_addrs)

        msg_alternative = MIMEMultipart('alternative')
        msg_root.attach(msg_alternative)
        msg_alternative.attach(MIMEText(msg))

        if attachments:
            for attachment in attachments:
                prt = MIMEBase('application', "octet-stream")
                prt.set_payload(open(attachment, "rb").read())
                encoders.encode_base64(prt)
                prt.add_header(
                    'Content-Disposition', 'attachment; filename="%s"'
                    % attachment.replace('"', ''))
                msg_root.attach(prt)

        self.sendmail(from_addr, to_addrs, msg_root.as_string())


def send_html_page_to_kindle(url, html_file):
    """Sends an email with the HTML file attached to your Kindle address."""
    with FastMailSMTP(USERNAME, PASSWORD) as server:
        server.send_message(from_addr="alex@alexwlchan.net",
                            to_addrs=[KINDLE_ADDR],
                            msg="",
                            subject="[autogen] Kindle email for %s" % url",
                            attachments=[html_file])


def main():
    try:
        url = appex.get_url()
    except NameError:
        url = sys.argv[1]

    html_file = get_html_from_url(url)
    send_html_page_to_kindle(url, html_file)

    try:
        appex.finish()
    except NameError:
        sys.exit(0)


if __name__ == '__main__':
    main()
