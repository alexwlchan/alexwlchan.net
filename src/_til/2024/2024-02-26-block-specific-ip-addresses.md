---
layout: til
date: 2024-02-26 10:15:24 +00:00
title: How to restrict a page to specific IP addresses
tags:
  - nginx
---
I had a login page which I wanted to restrict to an approved list of IP addresses, primarily to reduce spam.
You still had to login with a username/password if your IP address was approved, but it was harder for spambots to hammer the login form.

This is how you can use nginx to restrict a page to a fixed set of users:

```nginx
location /wp-login.php {
    allow 1.2.3.4;
    allow 5.6.7.8;
    deny all;

    # forward to real login page, e.g. with a `proxy_pass`
}
```

If somebody doesn't have an approved IP address, they'll get a generic HTTP 403 Forbidden error page.

It may be helpful to customise the error page, to give instructions to legitimate users about how to get themselves unblocked.
This is how you can create a custom error page:

```nginx
location /wp-login.php {
    allow 1.2.3.4;
    allow 5.6.7.8;
    deny all;

    error_page 403 /wp_login_blocked.html;

    # forward to real login page, e.g. with a `proxy_pass`
}

location = /wp_login_blocked.html {
    allow all;
    default_type text/plain;
    return 200 "<html>
      <head>
        <title>403 Forbidden</title>
      </head>
      <body>
        <h1>403 Forbidden</h1>
        <p>
          Your IP address is $remote_addr.
          You aren't allowed to log in!
        </p>
      </body>
      </html>
      ";
}
```

