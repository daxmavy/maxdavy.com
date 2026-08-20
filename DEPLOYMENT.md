# Deployment

The site is a Hugo build served by **GitHub Pages** at **https://maxdavy.com**,
with DNS and TLS fronted by **Cloudflare**.

```
git push origin main
      │
      ▼
GitHub Actions (.github/workflows/deploy.yml)
  hugo --minify  →  ./public  →  actions/deploy-pages
      │
      ▼
GitHub Pages  ──(claims maxdavy.com via static/CNAME)──▶  https://maxdavy.com
      ▲
      └── Cloudflare DNS: apex A/AAAA → GitHub Pages anycast IPs
                          www CNAME  → daxmavy.github.io
```

## Everyday deploys

Nothing manual. Push to `main` and the workflow rebuilds and publishes:

```bash
git add -A && git commit -m "Update content" && git push
```

Watch it with `gh run watch` or on the repository's **Actions** tab.

## Local preview

```bash
hugo server -D
# http://localhost:1313
```

## The pieces, and where they are configured

| Piece | Where | Notes |
|---|---|---|
| Custom domain | `static/CNAME` | Contains `maxdavy.com`. Deleting it un-claims the domain. |
| Base URL | `hugo.toml` | `baseURL = 'https://maxdavy.com/'` |
| Build & deploy | `.github/workflows/deploy.yml` | Pages source must be set to **GitHub Actions**, not "Deploy from a branch". |
| DNS | Cloudflare | See below. |

### DNS

Managed with the `maxdavy-site` skill's helper (the Cloudflare token lives only
at `~/.config/maxdavy/cloudflare-token`):

```bash
~/.claude/skills/maxdavy-site/scripts/maxdavy.sh dns list
```

The apex points at GitHub's Pages anycast addresses:

```
185.199.108.153   185.199.109.153   185.199.110.153   185.199.111.153
2606:50c0:8000::153   2606:50c0:8001::153   2606:50c0:8002::153   2606:50c0:8003::153
```

These records are **DNS-only** (grey cloud), not proxied. GitHub terminates TLS
itself and provisions the certificate for `maxdavy.com`; putting Cloudflare's
proxy in front interferes with that certificate's issuance and renewal. If you
ever do want the orange cloud, issue the certificate first and set the zone's
SSL/TLS mode to **Full (strict)**.

## The old address

`daxmavy.github.io` now serves a redirect stub — a short "moved" message and then
a bounce to maxdavy.com, path preserved. Its source is the
`daxmavy/daxmavy.github.io` repository.

## Newsletter

The subscribe form posts to Buttondown (`layouts/partials/newsletter.html`). It
appears at the foot of blog posts only; it is no longer on the homepage.

## Troubleshooting

**Actions run is green but the site is stale** — hard-refresh; Pages caches at the
edge for a few minutes.

**`maxdavy.com` serves a certificate error right after setup** — GitHub needs the
DNS records to resolve to it before it can issue the certificate. Wait, then in
the repository's Settings → Pages re-save the custom domain and tick *Enforce
HTTPS*.

**A curl from Max's laptop shows a self-signed certificate** — that is Cloudflare
WARP/Gateway TLS-inspecting, not a site fault. Check in a browser, or use
`curl -k`.
