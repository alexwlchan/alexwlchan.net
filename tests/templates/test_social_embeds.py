"""
Tests for `mosaic.templates.social_embeds`.
"""

import json
from pathlib import Path

from jinja2 import Environment
import minify_html
import pytest

from mosaic import templates as t


with open("social_embeds/data.json") as in_file:
    SOCIAL_EMBEDS = json.load(in_file)


@pytest.fixture
def env(out_dir: Path) -> Environment:
    """
    Creates a basic instance of the Jinja2 environment.
    """
    return t.get_jinja_environment(src_dir=Path("src"), out_dir=out_dir)


class TestSocialExtension:
    """
    Tests for SocialExtension.
    """

    def test_render_youtube(self, env: Environment) -> None:
        """
        Test the basic usage of the {% youtube %} tag.
        """
        md = '{% youtube "https://www.youtube.com/watch?v=Ej2EJVMkTKw" %}'

        html = env.from_string(md).render().strip()
        assert minify_html.minify(html) == (
            "<iframe allow=\"accelerometer 'none'; ambient-light-sensor 'none'; "
            "autoplay 'none'; battery 'none'; bluetooth 'none'; "
            "browsing-topics 'none'; camera 'none'; ch-ua 'none'; "
            "display-capture 'none'; domain-agent 'none'; "
            "document-domain 'none'; encrypted-media 'none'; "
            "execution-while-not-rendered 'none'; "
            "execution-while-out-of-viewport 'none'; gamepad 'none'; "
            "geolocation 'none'; gyroscope 'none'; hid 'none'; "
            "identity-credentials-get 'none'; idle-detection 'none'; "
            "keyboard-map 'none'; local-fonts 'none'; magnetometer 'none'; "
            "microphone 'none'; midi 'none'; navigation-override 'none'; "
            "otp-credentials 'none'; payment 'none'; picture-in-picture 'none'; "
            "publickey-credentials-create 'none'; publickey-credentials-get 'none'; "
            "screen-wake-lock 'none'; serial 'none'; speaker-selection 'none'; "
            "sync-xhr 'none'; usb 'none'; web-share 'none'; "
            "window-management 'none'; xr-spatial-tracking 'none'\" "
            'csp="sandbox allow-scripts allow-same-origin;" '
            'sandbox="allow-scripts allow-same-origin" '
            'style="aspect-ratio: 560 / 315; width: 100%; max-width: 560px;" '
            'title="Using privilege to improve inclusion" allowfullscreen '
            "class=youtube credentialless frameborder=0 "
            "id=youtube_Ej2EJVMkTKw loading=lazy "
            "src=https://www.youtube-nocookie.com/embed/Ej2EJVMkTKw></iframe>"
        )

    def test_twitter_includes_media(self, env: Environment) -> None:
        """
        Twitter embeds with media include the pictures.
        """
        md = '{% tweet "https://twitter.com/iamkimiam/status/848188958567800832" %}'
        html = env.from_string(md).render().strip()

        assert "C8VfWJyXkAIWboG_1x.jpg" in html

    @pytest.mark.parametrize("url", SOCIAL_EMBEDS.keys())
    def test_all_social_embeds(self, env: Environment, url: str) -> None:
        """
        Test all the existing social embeds.
        """
        if url.startswith("https://bsky.app"):
            md = f'{{% bluesky "{url}" %}}'
        elif url.startswith("https://twitter.com"):
            md = f'{{% tweet "{url}" %}}'
        elif url.startswith("https://www.youtube.com"):
            md = f'{{% youtube "{url}" %}}'
        else:
            md = f'{{% mastodon "{url}" %}}'

        env.from_string(md).render()
