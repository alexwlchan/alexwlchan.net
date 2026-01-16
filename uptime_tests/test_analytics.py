"""
Test my tracking pixel and analytics dashboard at analytics.alexwlchan.net.
"""

import httpx


def test_analytics_homepage() -> None:
    """
    The analytics app is running.
    """
    resp = httpx.get("https://analytics.alexwlchan.net/")

    assert resp.status_code == 200


def test_dashboard_is_protected() -> None:
    """
    If you try to load the dashboard as a public user, you can't see it.
    """
    resp = httpx.get("https://analytics.alexwlchan.net/dashboard/")

    assert resp.status_code == 302
    assert resp.headers["location"] == "/?next=%2Fdashboard%2F"
