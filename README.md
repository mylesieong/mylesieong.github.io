# Sai vs. Reality — mylesieong.github.io

The parent domain for everything I ship. One brand carrying an unrelated and
growing set of products, so no single launch has to build its own audience from
zero.

Two jobs, in this order:

1. **Product distribution** — each product's landing page, plus the SEO pages
   that capture search intent for it.
2. **Personal brand** — the reason a stranger trusts the products.

Job 2 serves job 1. Personal-brand content never pushes the products below the
fold on the homepage.

The site is English-only. Two of the product sites ship their own translations;
that is deliberate and scoped to those sites.

## Layout

| Path | What it is |
| --- | --- |
| `build.py` | Renders every hub page. **Run it after any content change.** |
| `gen_og.py` | Renders the per-page OG images and the normalised product icons. |
| `serve.py` | Local preview: `python3 serve.py` then <http://localhost:8123>. |
| `assets/css/site.css` | The whole design system. One accent, light and dark. |
| `assets/og/` | Generated. One OG image per page — never a shared default. |
| `assets/icons/` | Generated. Product icons flattened onto a contrast-checked plate. |
| `products/` | Product sites. Most are submodules — see below. |
| `_content/` | Hand-written page bodies that `build.py` pulls in. |
| `sitemap.xml` | Generated sitemap **index**, pointing at every sitemap on the domain. |

Generated files are committed, the same way the Flexi and Bible Project sites
already work. GitHub Pages serves what is in the repo; there is no CI build.

## Adding a product

1. Append a dict to `PRODUCTS` in `build.py`:

   ```python
   dict(slug="my-thing", name="My Thing", status="building", owner="hub",
        path="/products/my-thing/",
        icon="/assets/icons/my-thing.png",
        line="One sentence saying what it actually is."),
   ```

   `status` is one of `live`, `beta`, `building`, `killed`. `owner` is
   `submodule` if the product has its own repository, `hub` if its page lives
   here. Order in the list is the order on the page.

2. If it has an icon, add it to `ICON_SRC` in `gen_og.py` and add a card to
   `CARDS` so it gets its own OG image, then run `python3 gen_og.py`.

3. Run `python3 build.py`. The product now appears on the homepage, in
   `/products/`, and in the sitemap.

That is the whole job for a product whose page lives here. If it gets its own
site, mount it as a submodule (below) and `build.py` will link to it without
touching it.

### Killing a product

Change its `status` to `"killed"` and add an entry to `POSTMORTEMS` in
`build.py` with the four fields: what you believed, what you built, what the
evidence said, what you would do differently. Anything left as `None` renders
as "Not yet written" rather than being quietly omitted.

**A killed product keeps its URL.** It is never deleted and never redirected —
it gains a status banner and the post-mortem. That rule has no exceptions.

## Adding a build-log post

Append a dict to the **front** of `BUILD_LOG` in `build.py` (newest first):

```python
dict(slug="what-broke-this-week",
     path="/build-log/what-broke-this-week/",
     date="2026-09-04",
     title="What broke this week",
     blurb="One line for the index and the homepage.",
     desc="One sentence for the meta description and the social card.",
     og="/assets/og/build-log-what-broke.png",
     body="""      <p>The post, as HTML.</p>"""),
```

Then add a matching card to `CARDS` in `gen_og.py`, run `python3 gen_og.py` and
`python3 build.py`. The newest post appears on the homepage automatically.

The ask is always the same: what I'm building, what broke, and what the numbers
actually said. Numbers are evidence about a decision, not a scoreboard.

## Product sites are submodules

Each shipped product's site lives in its own repository and is mounted here, so
the product page and the hub release independently.

| Path | Repository |
| --- | --- |
| `products/pool-billiards-self-trainer/` | `PoolBilliardsSelfTrainerWebsite` |
| `products/runout-rank/` | `RunoutRankWebsite` |
| `products/flexi/` | `FlexiWebsite` |
| `products/bible-project/` | `BibleReaderWebsite` |
| `products/tacet/` | `TacetWebsite` |
| `products/snooker-self-trainer/` | `SnookerSelfTrainerWebsite` |

Clone with `git clone --recurse-submodules`, or run `git submodule update --init`
in an existing checkout.

Each of those sites is served from a sub-path, never the origin root, and each
keeps a `privacy-policy.html` at the top of its mount because that exact URL is
printed in the App Store and Google Play listings.

To move a product site forward, commit **in its own repository** on `main` —
never on a detached HEAD — then update the pointer here:

```bash
git submodule update --remote products/<name>
git commit -am "Update the <name> site"
```

`build.py` never writes inside `products/*` for a submodule-owned product.

## Sitemaps and robots

Only the `robots.txt` at the origin root is honoured by crawlers, so
`/robots.txt` lists every sitemap on the domain, including the ones inside each
submodule. `/sitemap.xml` is a sitemap **index** pointing at `/sitemap-pages.xml`
(the hub's own pages) plus each product's own sitemap. A product site keeping
its own `sitemap.xml` is correct and expected; add it to `PRODUCT_SITEMAPS` in
`build.py` when you mount a new one.

Search Console verification lives at `googlef3c32cf8dc998f2f.html`. Do not
delete it.

## Analytics

Google Analytics 4 is emitted into every hub page by `build.py`; the
measurement ID is the `GA_ID` constant near the top. One property covers the
whole domain, so no cross-domain setup is needed.

**The submodule-owned product sites are not tracked**, by choice. They are
served from this origin at sub-paths, but their HTML comes from their own
repositories, so covering them means either a one-line loader committed into
each product repo or moving this site to a CI build. Neither is worth doing
until the hub numbers prove useful. Clicks from a hub page into `/products/*`
therefore look like exits.

Build an untagged copy with `GA_ID= python3 build.py`.
