# FormSeal

FormSeal is a **server-blind, browser-native encrypted form poster**.

Form submissions are encrypted **in the browser** using X25519 sealed boxes before being sent to any POST endpoint. The backend receives and stores **opaque ciphertext only**. Decryption is operator-controlled and happens offline.

FormSeal is **not a hosted service, dashboard, or SaaS product.**  
It is a drop-in client-side utility.

---

## Security guarantee

> **If the POST endpoint is fully compromised, seized, or maliciously operated, previously submitted form data remains confidential.**

This guarantee holds because:

- Encryption happens client-side, in the browser
- The backend stores ciphertext only
- Decryption keys never exist in the backend environment

A backend compromise yields no recoverable plaintext.

---

## Threat model

FormSeal is designed for environments where:

- The hosting provider or backend may be compromised
- The backend must be treated as hostile
- Data seizure is a realistic concern
- Retroactive disclosure must be prevented

FormSeal prioritizes **backward confidentiality** — protecting already-submitted data — over convenience or real-time administration.

---

## How it works

On submit, FormSeal:

1. Collects field values from your form by `name` attribute
2. Validates them against your schema rules
3. Seals the payload with `crypto_box_seal` (Curve25519 + XSalsa20-Poly1305)
4. POSTs `{ ciphertext: "<base64url>" }` to your configured endpoint

Your endpoint stores the ciphertext. Only the holder of the private key can decrypt it.

---

## Installation

**npx (recommended):**

```bash
npx @formseal/client
```

Scaffolds `./formseal/` into your project. Nothing else is left behind.

**Manual:**

Download `formseal_client-vX.Y.Z.zip` from the [latest release](https://github.com/grayguava/formseal-client/releases/latest), extract, and drop the `formseal/` folder into your project.

Verify integrity with the SHA256 hashes in the release notes.

---

## Setup

### 1. Configure

Edit `formseal/config/formseal.config.js`:

- Set `endpoint` to your POST API URL
- Set `recipientPublicKey` to your base64url public key
- Adjust `submitStates` and `onSuccess` / `onError` behaviour

Edit `formseal/config/fields.schema.js`:

- Set `formSelector`, `submitSelector`, `statusSelector`
- Define your fields with validation rules

### 2. Wire up your HTML

```html
<!-- Your form — write it however you want -->
<form id="contact-form" novalidate>

  <!-- Honeypot (required, hide off-screen with CSS) -->
  <input type="text" name="_hp" tabindex="-1" autocomplete="off"
    style="position:absolute;left:-9999px;opacity:0;height:0;">

  <!-- Fields — [name] must match fields.schema.js -->
  <input type="text"  name="name">
  <span data-fs-error="name"></span>

  <input type="email" name="email">
  <span data-fs-error="email"></span>

  <textarea name="message"></textarea>
  <span data-fs-error="message"></span>

  <button type="submit" id="contact-submit">Send message</button>
</form>

<!-- FormSeal writes status messages here -->
<div id="contact-status"></div>

<!-- Optional: callbacks -->
<script>
  window.formsealCallbacks = {
    onSuccess: function(response) { },
    onError:   function(error)    { },
  };
</script>

<!-- Single script tag -->
<script src="/formseal/globals.js"></script>
```

See [`sample/index.html`](./sample/index.html) for a complete working example.

---

## CSS hooks

FormSeal sets these attributes. Style them however you want:

|Selector|When|
|---|---|
|`[data-fs-error="name"]`|Populated with validation error|
|`[aria-invalid="true"]`|Set on invalid inputs|
|`[data-fs-status="success"]`|Set on status element on success|
|`[data-fs-status="error"]`|Set on status element on error|

---

## Payload format

```json
{
  "_fs": {
    "version": "fs.v2.1",
    "origin": "contact-form",
    "id": "<uuid>",
    "submitted_at": "<iso8601>",
    "client_tz": "<tz>"
  },
  "data": {
    "name": "...",
    "email": "...",
    "message": "..."
  }
}
```

The entire object is JSON-serialised and sealed with `crypto_box_seal`.  
Your endpoint receives `{ ciphertext: "<base64url>" }`.

---

## Backend compromise impact

If the POST endpoint or storage layer is compromised, an attacker can:

- Access encrypted submission blobs
- Observe submission timing and size
- Modify backend code affecting future submissions

They **cannot**:

- Decrypt existing submissions without the private key
- Recover plaintext from stored ciphertext
- Retroactively compromise already-encrypted data

---

## What FormSeal does not do

- No admin dashboard or inbox UI
- No server-side decryption
- No hosted service
- No bundler or build step required
- No npm dependencies

These omissions are intentional.

---

## Administrative tooling

Decryption, export, and operator workflows are out of scope for this repository.

Operator tooling is maintained separately:

**FormSeal Sync** — https://github.com/grayguava/formseal-sync

---

## License

MIT