"""Build the redirect-only site this repository now publishes.

The site moved to https://commit-check.com. This repository is kept as the
historical source — ``docs/`` is still here and still readable — but what it
publishes is a set of redirect stubs, one per URL the old site served, so links
already out in the world land on the page that replaced them.

Why stubs rather than a server redirect: GitHub Pages serves static files and
has no redirect table, so a ``<meta refresh>`` plus a ``rel=canonical`` is the
only mechanism available. The canonical link is what transfers search ranking
to the new URL; the meta refresh and the script are what move a reader.

Deliberately no ``robots: noindex`` on these stubs. It reads like the tidy thing
to do, but it contradicts the canonical: one says "consolidate this page onto
that URL", the other says "drop this page from the index", and a crawler that
honours the second may never act on the first — or carry the noindex across to
the target. A migration wants the canonical to be believed.

Why this runs instead of ``mkdocs build``: once this repository is archived,
Actions stop running and the last deployed artifact is what Pages serves
forever. That artifact needs to be the redirects, so the redirects have to be
deployed *before* the archive switch is flipped, not after.

Run with ``python scripts/build_redirects.py`` — output goes to ``site/``.
"""

from __future__ import annotations

import sys
from pathlib import Path

NEW_SITE = "https://commit-check.com"

#: Every URL the mkdocs site served, taken from its own build output, mapped to
#: the path that replaced it on the new site.
#
# All but one are the same path: the pages, the blog, its archive, author and
# category indexes were carried over unchanged, and the posts kept their
# filenames and ``created`` dates, so the generated slugs match byte for byte.
#
# ``/projects/`` is the exception. It was folded into the Ecosystem section of
# the new landing page, so it redirects to the root rather than to a page that
# does not exist.
SAME_PATH = [
    "/",
    "/getting-started/",
    "/blog/",
    "/blog/2026/06/21/ai-native-json-output-and-a-python-api/",
    "/blog/2026/06/21/from-zero-config-to-org-wide-policy/",
    "/blog/2026/06/21/one-policy-file-for-your-git-history/",
    "/blog/2026/07/06/ai-attribution-governance-enforcing-ai-disclosure-policies-at-the-ci-level/",
    "/blog/archive/2026/",
    "/blog/author/team/",
    "/blog/category/announcements/",
    "/blog/category/updates/",
]

REDIRECTS = {path: path for path in SAME_PATH} | {"/projects/": "/"}

#: The project documentation that came before the mkdocs site: Sphinx pages the
#: ``commit-check/commit-check`` repository published at
#: ``commit-check.github.io/commit-check/<page>.html``. That project site is no
#: longer published, so GitHub Pages serves those paths from *this* site — and
#: without these they fell through to the 404 fallback and landed every reader
#: on the home page. They are still linked from the README of every release up
#: to v2.12 (and so from PyPI), from blog posts and from the Action's docs.
#:
#: The page list is the Sphinx ``docs/`` of v2.12.2, the last release built
#: that way, plus ``cli_args.html``, which sphinx-argparse generated. Each maps
#: to the page that took over its content; ``what-is-new`` was the v2.0.0
#: release notes and ``cli_args`` the command-line reference.
OLD_PROJECT_DOCS = {
    "/commit-check/": "/",  # also serves /commit-check/index.html
    "/commit-check/README.html": "/",
    "/commit-check/cli_args.html": "/configuration/#command-line-arguments",
    "/commit-check/configuration.html": "/configuration/",
    "/commit-check/example.html": "/example/",
    "/commit-check/migration.html": "/migration/",
    "/commit-check/troubleshoot.html": "/troubleshoot/",
    "/commit-check/changelog.html": "/changelog/",
    "/commit-check/what-is-new.html": "/changelog/#v200",
}

# The fragment is carried across by the script: a reader following a deep link
# into a page should keep their place — unless the target already names its
# own section, which a second "#" would break. ``location.replace`` rather than
# ``location.href`` so the stub does not land in the back-button history and
# trap them in a loop between the two sites.
TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moved to commit-check.com</title>
<link rel="canonical" href="{target}">
<meta http-equiv="refresh" content="0; url={target}">
<script>var t = "{target}"; location.replace(t.indexOf("#") < 0 ? t + location.hash : t);</script>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 4rem auto; max-width: 34rem;
         padding: 0 1rem; line-height: 1.6; }}
  a {{ color: #2c9ccd; }}
</style>
</head>
<body>
<h1>This site has moved</h1>
<p>The Commit Check documentation, landing page and blog are now published at
<a href="{target}">{target}</a>.</p>
<p>If you are not redirected automatically, follow the link above.</p>
</body>
</html>
"""


def main() -> int:
    site = Path(__file__).resolve().parent.parent / "site"
    for old, new in (REDIRECTS | OLD_PROJECT_DOCS).items():
        target = NEW_SITE + new
        # "/a/b/" is served from a/b/index.html; "/a/b.html" is the file itself.
        rel = old.strip("/")
        page = site / rel if rel.endswith(".html") else site / rel / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(TEMPLATE.format(target=target), encoding="utf-8")

    # Pages serves this for any path with no file of its own, which covers the
    # URLs this list missed — a stray deep link, a page from an older layout.
    # It points at the new site's root because there is nothing better to guess.
    (site / "404.html").write_text(
        TEMPLATE.format(target=NEW_SITE + "/"), encoding="utf-8"
    )

    # Without this, Pages runs the output through Jekyll, which skips files and
    # directories whose names begin with an underscore.
    (site / ".nojekyll").write_text("", encoding="utf-8")

    print(
        f"wrote {len(REDIRECTS)} site + {len(OLD_PROJECT_DOCS)} project-docs "
        f"redirects + 404 fallback to {site}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
