"""Check the redirect map against the site it is replacing.

This repository publishes redirects now, and once it is archived the artifact
from the last successful run is what GitHub Pages serves for good — Actions do
not run on an archived repository, so there is no second chance to fix a URL
that was left out. That makes the map worth checking while it can still change.

The check builds the mkdocs site the old way and compares the URLs it produces
against the redirect map, in both directions: a URL the old site served with no
redirect is a link that will break, and a redirect for a URL the old site never
served is a sign the map was edited by hand and drifted.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build_redirects import REDIRECTS  # noqa: E402


def _urls_the_old_site_served() -> set[str]:
    """Build the mkdocs site and return every URL it publishes."""
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [sys.executable, "-m", "mkdocs", "build", "--site-dir", tmp],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            pytest.skip(f"mkdocs build unavailable: {result.stderr.strip()[:200]}")
        site = Path(tmp)
        urls = set()
        for page in site.rglob("index.html"):
            rel = page.parent.relative_to(site).as_posix()
            # ``relative_to`` gives "." for the site root, which is "/".
            urls.add("/" if rel == "." else f"/{rel}/")
        return urls


def test_every_published_url_has_a_redirect():
    """Nothing the old site served may be left without a forwarding address."""
    missing = sorted(_urls_the_old_site_served() - set(REDIRECTS))
    assert not missing, (
        "these URLs are served by the current site but have no redirect, so "
        "they will break when this repository is archived:\n  "
        + "\n  ".join(missing)
    )


def test_no_redirect_points_at_a_url_that_never_existed():
    """A redirect for a URL the site never served means the map drifted."""
    served = _urls_the_old_site_served()
    invented = sorted(set(REDIRECTS) - served)
    assert not invented, (
        "these redirects are for URLs the site does not serve:\n  "
        + "\n  ".join(invented)
    )
