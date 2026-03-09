---
layout: note
date: 2024-02-26 10:15:24 +00:00
title: How to restrict a page to specific IP addresses
topic: Computers and code
hidden_topics:
  - nginx
---
I had a login page which I wanted to restrict to an approved list of IP addresses, primarily to reduce spam.
You still had to login with a username/password if your IP address was approved, but it was harder for spambots to hammer the login form.

This is how you can use nginx to restrict a page to a fixed set of users:

<pre class="lng-nginx"><code>location <span class="n">/wp-login.php</span> <span class="p">{</span>
    allow 1.2.3.4;
    allow 5.6.7.8;
    deny all;

    <span class="c"># forward to real login page, e.g. with a `proxy_pass`</span>
<span class="p">}</span></code></pre>

If somebody doesn't have an approved IP address, they'll get a generic HTTP 403 Forbidden error page.

It may be helpful to customise the error page, to give instructions to legitimate users about how to get themselves unblocked.
This is how you can create a custom error page:

<pre class="lng-nginx"><code>location <span class="n">/wp-login.php</span> <span class="p">{</span>
    allow 1.2.3.4;
    allow 5.6.7.8;
    deny all;

    error_page 403 /wp_login_blocked.html;

    <span class="c"># forward to real login page, e.g. with a `proxy_pass`</span>
<span class="p">}</span>

location = <span class="n">/wp_login_blocked.html</span> <span class="p">{</span>
    allow all;
    default_type text/plain;
    return 200 <span class="s">"&lt;html&gt;
      &lt;head&gt;
        &lt;title&gt;403 Forbidden&lt;/title&gt;
      &lt;/head&gt;
      &lt;body&gt;
        &lt;h1&gt;403 Forbidden&lt;/h1&gt;
        &lt;p&gt;
          Your IP address is $remote_addr.
          You aren't allowed to log in!
        &lt;/p&gt;
      &lt;/body&gt;
      &lt;/html&gt;
      "</span>;
<span class="p">}</span></code></pre>

