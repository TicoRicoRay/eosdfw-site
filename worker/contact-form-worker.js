/**
 * EOSDFW.com Contact Form Worker
 *
 * Receives POST submissions from https://eosdfw.com/contact.html
 * and emails them to ray.myers@eosworldwide.com via MailChannels
 * (free outbound mail relay available to Cloudflare Workers).
 *
 * Deployment:
 *   1. wrangler init (or paste into a Worker in the Cloudflare dashboard)
 *   2. Add custom domain route: form.eosdfw.com/* (or workers.dev URL)
 *   3. (Optional) Set TURNSTILE_SECRET as a secret to enable Cloudflare Turnstile spam filtering
 *   4. Update DKIM TXT record in DNS so MailChannels accepts mail from eosdfw.com
 *
 * Update the FORM_ACTION in contact.html to this Worker's URL.
 */

const TO_EMAIL = "ray.myers@eosworldwide.com";
const TO_NAME = "Ray Myers";
const FROM_EMAIL = "no-reply@eosdfw.com";
const FROM_NAME = "EOSDFW Contact Form";
const ALLOWED_ORIGINS = [
  "https://eosdfw.com",
  "https://www.eosdfw.com",
];

const CORS_HEADERS = (origin) => ({
  "Access-Control-Allow-Origin": ALLOWED_ORIGINS.includes(origin) ? origin : "https://eosdfw.com",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
  "Vary": "Origin",
});

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS(origin) });
    }

    if (request.method !== "POST") {
      return new Response("Method not allowed", { status: 405, headers: CORS_HEADERS(origin) });
    }

    // Parse form-encoded or JSON payloads
    const contentType = request.headers.get("content-type") || "";
    let data;
    try {
      if (contentType.includes("application/json")) {
        data = await request.json();
      } else {
        const form = await request.formData();
        data = Object.fromEntries(form.entries());
      }
    } catch (e) {
      return jsonError("Invalid payload", 400, origin);
    }

    // Honeypot — silently accept and discard bots
    if (data.website || data._gotcha) {
      return Response.redirect("https://eosdfw.com/thanks.html", 303);
    }

    // Required fields
    if (!data.name || !data.email || !data.message) {
      return jsonError("Name, email, and message are required.", 400, origin);
    }

    // Basic email shape check
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(data.email))) {
      return jsonError("That email address doesn't look right.", 400, origin);
    }

    // Optional: verify Turnstile token if secret is configured
    if (env.TURNSTILE_SECRET && data["cf-turnstile-response"]) {
      const ok = await verifyTurnstile(env.TURNSTILE_SECRET, data["cf-turnstile-response"], request.headers.get("CF-Connecting-IP"));
      if (!ok) return jsonError("Spam check failed. Please try again.", 400, origin);
    }

    const subject = `New EOSDFW.com inquiry from ${data.name}`;
    const plain =
      `New inquiry from EOSDFW.com\n\n` +
      `Name:    ${data.name}\n` +
      `Email:   ${data.email}\n` +
      `Company: ${data.company || "(not provided)"}\n` +
      `Team:    ${data.team_size || "(not provided)"}\n\n` +
      `Message:\n${data.message}\n`;

    const mailRes = await fetch("https://api.mailchannels.net/tx/v1/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        personalizations: [{ to: [{ email: TO_EMAIL, name: TO_NAME }] }],
        from: { email: FROM_EMAIL, name: FROM_NAME },
        reply_to: { email: data.email, name: data.name },
        subject,
        content: [{ type: "text/plain", value: plain }],
      }),
    });

    if (!mailRes.ok) {
      const body = await mailRes.text();
      console.error("MailChannels error", mailRes.status, body);
      return jsonError("Couldn't send your message right now. Please email ray.myers@eosworldwide.com directly.", 502, origin);
    }

    // If form is submitted from a normal <form>, follow with a redirect.
    const accepts = request.headers.get("accept") || "";
    if (!accepts.includes("application/json")) {
      return Response.redirect("https://eosdfw.com/thanks.html", 303);
    }

    return new Response(JSON.stringify({ ok: true }), {
      status: 200,
      headers: { "Content-Type": "application/json", ...CORS_HEADERS(origin) },
    });
  },
};

function jsonError(message, status, origin) {
  return new Response(JSON.stringify({ ok: false, error: message }), {
    status,
    headers: { "Content-Type": "application/json", ...CORS_HEADERS(origin) },
  });
}

async function verifyTurnstile(secret, token, ip) {
  const body = new FormData();
  body.append("secret", secret);
  body.append("response", token);
  if (ip) body.append("remoteip", ip);
  const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    body,
  });
  if (!res.ok) return false;
  const json = await res.json();
  return !!json.success;
}
