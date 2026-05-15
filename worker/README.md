# EOSDFW Contact Form Worker

Cloudflare Worker that receives contact form submissions from https://eosdfw.com/contact.html and emails them to **ray.myers@eosworldwide.com** via MailChannels (free for Cloudflare Workers).

## One-time setup

```bash
npm install -g wrangler
wrangler login
cd worker/
wrangler deploy
```

Wrangler will print the Worker URL, e.g.
`https://eosdfw-contact-form.<your-subdomain>.workers.dev`

## Wire it to the site

Update `templates/pages/contact.html`:

```html
<form action="https://eosdfw-contact-form.<your-subdomain>.workers.dev"
      method="POST">
```

Rebuild and push:

```bash
python3 build.py
git add -A && git commit -m "Wire contact form to Cloudflare Worker"
git push origin main
```

## MailChannels DKIM (recommended)

Without DKIM, MailChannels may reject outbound mail from `eosdfw.com`. Add these to the Cloudflare DNS for eosdfw.com:

| Type | Name                       | Value                                              |
|------|----------------------------|----------------------------------------------------|
| TXT  | `_mailchannels`            | `v=mc1 cfid=<your-account-id>.workers.dev`         |
| TXT  | `eosdfw._domainkey`        | `v=DKIM1; k=rsa; p=<generated-public-key>`         |

Generate the DKIM keypair: https://mailchannels.zendesk.com/hc/en-us/articles/7122849237389

## Spam protection (optional)

Add Cloudflare Turnstile to the form, then set the secret:

```bash
wrangler secret put TURNSTILE_SECRET
```

The worker auto-detects the secret and validates the `cf-turnstile-response` field on every submission.
