---
category: Python
date: 2016-05-10 12:41:00 +0000
layout: post
summary: A quick python-smtplib wrapper for sending emails through FastMail.
tags: python
title: A Python smtplib wrapper for FastMail
---

Sometimes I want to send email from a Python script on my Mac.
Up to now, my approach has been to shell out to `osascript`, and use AppleScript to invoke Mail.app to compose and send the message.
This is sub-optimal on several levels:

*   It relies on Mail.app having up-to-date email config;
*   The compose window of Mail.app briefly pops into view, stealing focus from my main task;
*   Having a Python script shell out to run AppleScript is an ugly hack.

Plus it was a bit buggy and unreliable.
Not a great solution.

My needs are fairly basic: I just want to be able to send a message from my email address, with a bit of body text and a subject, and optionally an attachment or two.
And I'm only sending messages from one email provider, [FastMail][fastmail].

Since the Python standard library includes [smtplib][smtplib], I decided to give that a try.

After a bit of mucking around, I came up with this wrapper:

```python
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

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
```

lines 7&ndash;12 create a subclass of [smtplib.SMTP_SSL][smtp_ssl], and uses the supplied credentials to log into FastMail.
Annoyingly, this subclassing is broken on Python 2, because SMTP_SSL is an old-style class, and so [super() doesn't work][super].
I only use Python 3 these days, so that's okay for me, but you'll need to change that if you want a backport.

For getting my username/password into the script, I use the [keyring module][keyring].
It gets them from the system keychain, which feels pretty secure.
My email credentials are important &ndash; I don't just want to store them in an environment variable or a hard-coded string.

lines 14&ndash;19 defines a convenience wrapper for sending a message.
The `*` in the arguments list denotes the [end of positional arguments][pep3102] &ndash; all the remaining arguments have to be called as keyword arguments.
This is a new feature in Python 3, and I really like it, especially for functions with lots of arguments.
It helps enforce clarity in the calling code.

In lines 20&ndash;23, I'm setting up a MIME message with my email headers.
I deliberately use a multi-part MIME message so that I can add attachments later, if I want.

Then I add the body text.
With MIME, you can send multiple versions of the body: a plain text and an HTML version, and the recipient's client can choose which to display.
In practice, I almost always use plaintext email, so that's all I've implemented.
If you want HTML, [see Stack Overflow][mimehtml].

Then lines 29&ndash;37 add the attachments &ndash; if there are any.
Note that I use None as the default value for the attachments argument, not an empty list &ndash; this is to avoid any gotchas around [mutable default arguments][mutable].

Finally, on line 39, I call the sendmail method from the SMTP class, which actually dispatches the message into the aether.

The nice thing about subclassing the standard SMTP class is that I can use my wrapper class as a drop-in replacement.
Like so:

    :::python
    with FastMailSMTP(user, pw) as server:
        server.send_message(from_addr='hello@example.org',
                            to_addrs=['jane@doe.net', 'john@smith.org'],
                            msg='Hello world from Python!',
                            subject='Sent from smtplib',
                            attachments=['myfile.txt'])

I think this is a cleaner interface to email.
Mucking about with MIME messages and SMTP is a necessary evil, but I don't always care about those details.
If I'm writing a script where email support is an orthogonal feature, it's nice to have them abstracted away.

[mimehtml]: http://stackoverflow.com/a/920928/1558022
[smtplib]: https://docs.python.org/3.5/library/smtplib.html
[fastmail]: https://www.fastmail.com/
[super]: https://docs.python.org/2/library/functions.html?highlight=super#super
[smtp_ssl]: https://docs.python.org/3.5/library/smtplib.html#smtplib.SMTP_SSL
[keyring]: https://pypi.python.org/pypi/keyring
[pep3102]: https://www.python.org/dev/peps/pep-3102/
[mutable]: http://docs.python-guide.org/en/latest/writing/gotchas/#mutable-default-arguments