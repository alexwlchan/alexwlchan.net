I use [Caddy](https://caddyserver.com/) as my web server.

To deploy new Caddy config:

1.  SSH on to my web server, and `cd` to the checkout of this repo:

    ```console
    $ ssh alexwlchan@alexwlchan.net
    $ cd ~/repos/alexwlchan.net
    ```

2.  Pull the config that you want, e.g. `git pull origin main`

3.  Switch to this folder and reload Caddy:

    ```console
    $ cd caddy
    $ sudo caddy reload
    ```
