---
layout: til
title: Creating a reverse proxy to a multi-site server with Caddy
date: 2024-11-21 11:29:02 +00:00
tags:
  - caddy
summary:
  You need to add Host headers and HTTPS configuration to your `reverse_proxy` block.
---
I was setting up Caddy to run as a reverse proxy in front of the `www.flickr.org` WordPress site, which is currently hosted on WordPress VIP.
Here's the config I needed:

```
reverse_proxy https://192.0.66.95 {
    transport http {
        tls_server_name "go-vip.co"
    }

    header_up Host "www.flickr.org"
}
```

It took a while to work out this config, so I want to write down my debugging steps and some useful links.

## Context

*   At time of writing, our WordPress VIP server runs at `192.0.66.95`
*   Following [my own advice](/2024/netlify-to-caddy/#how-i-did-the-migration), I tested the migration with the alternative domain `www2.flickr.org`

## How I got here

1.  I started with a one-line configuration of the [`reverse_proxy` directive][reverse_proxy]:

    ```
    www2.flickr.org {
        reverse_proxy https://192.0.66.95
    }
    ```

    This fails with an HTTP 502 Bad Gateway error.

    I realised that this is probably because `192.0.66.95` is serving many sites, and it doesn't know it should be serving `www.flickr.org` to the proxy.

2.  I found a section in the [`reverse_proxy` docs][https_header] that suggested adding a `Host` header:

    > Since (most) headers retain their original value when being proxied, it is often necessary to override the Host header with the configured upstream address when proxying to HTTPS, such that the Host header matches the TLS ServerName value:
    >
    > <pre style="padding: 0; margin: 0; margin-bottom: 1em; border: none; background: none"><code>reverse_proxy https://example.com {</code>
<code>    header_up Host {upstream_hostport}</code>
<code>}</code></pre>

    I'm not sure what `{upstream_hostport}` does, so I decided to hard-code the header instead -- I know what it's going to be:

    ```
    www2.flickr.org {
        reverse_proxy https://192.0.66.95 {
            header_up Host "www.flickr.org"
        }
    }
    ```

    This fails with another HTTP 502 Bad Gateway error.

3.  I wasn't sure what was failing this time, so I enabled [debug logs in Caddy][debug]):

    ```
    {
       debug
    }
    ```

    Then I could see all the requests being sent to the upstream proxy, including this one:

    <pre><code>2024/11/21 11:58:25.072	DEBUG	http.handlers.reverse_proxy	upstream roundtrip
{
  "upstream": "192.0.66.95:443",
  "duration": 0.004109724,
  "request": {
        "proto": "HTTP/2.0",
        "method": "GET",
        "host": "www.flickr.org",
        "uri": "/",
        "headers": { … },
        "tls": { … },
        …
  },
  "error": "tls: failed to verify certificate: x509: cannot validate certificate for 192.0.66.95 because it doesn't contain any IP SANs"
}</code></pre><p>That last message is interesting!</p><pre style="white-space: normal;"><code>tls: failed to verify certificate: x509: cannot validate certificate for 192.0.66.95 because it doesn't contain any IP SANs</code></pre><p>I’m not sure what an IP SAN is, but it's a clue!

4.  I tried making an HTTPS request to that IP address using curl:

    ```console
    $ curl -v 'https://192.0.66.95'
    *   Trying 192.0.66.95:443...
    * Connected to 192.0.66.95 (192.0.66.95) port 443
    …
    * SSL connection using TLSv1.3 / AEAD-CHACHA20-POLY1305-SHA256 / [blank] / UNDEF
    * Server certificate:
    *  subject: CN=go-vip.co
    *  start date: Nov 19 09:11:52 2024 GMT
    *  expire date: Feb 17 09:11:51 2025 GMT
    *  subjectAltName does not match ipv4 address 192.0.66.95
    * SSL: no alternative certificate subject name matches target ipv4 address '192.0.66.95'
    * Closing connection
    curl: (60) SSL: no alternative certificate subject name matches target ipv4 address '192.0.66.95'
    More details here: https://curl.se/docs/sslcerts.html

    curl failed to verify the legitimacy of the server and therefore could not
    establish a secure connection to it. To learn more about this situation and
    how to fix it, please visit the web page mentioned above.
    ```

    So now I know that "IP SAN" stands for "IP Subject Alternative Name".

5.  I've lost the link, but I saw somebody suggest looking at the [`http` transport settings for the `reverse_proxy` directive][http_settings].

    This led me to the `tls_server_name` directive, which tells Caddy what the name of the server is -- and presumably the name it should look for on the HTTPS certificate.

    I could see from the `curl` output that the server name is `go.vip.co`, so I added those lines to the config:

    ```
    www2.flickr.org {
        reverse_proxy https://192.0.66.95 {
            header_up Host "www.flickr.org"

            transport http {
                tls_server_name go-vip.co
            }
        }
    }
    ```

[reverse_proxy]: https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
[https_header]: https://caddyserver.com/docs/caddyfile/directives/reverse_proxy#https
[debug]: https://caddyserver.com/docs/caddyfile/options#debug
[http_settings]: https://caddyserver.com/docs/caddyfile/directives/reverse_proxy#the-http-transport
