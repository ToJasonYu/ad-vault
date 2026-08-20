# dashboard-react

Advertiser-facing dashboard: sign up or log in, create campaigns, and see impressions,
clicks, and spend per campaign. Talks to `backoffice-rails`'s JSON API with plain `fetch` —
no state-management library, the app is small enough not to need one.

## Setup

Requires `backoffice-rails` running (see `backoffice-rails/README.md`).

```
npm install
npm run dev
```

Opens on `http://localhost:5173`. Override the API's location with a `VITE_API_BASE_URL` env
var (defaults to `http://127.0.0.1:3000`).

## Structure

- `src/api.ts` — the only place that talks to the Rails API; every request attaches the
  advertiser's Bearer token (stored in `localStorage` after login/signup)
- `src/components/AuthForm.tsx` — combined login/signup form
- `src/components/CampaignList.tsx`, `CampaignForm.tsx` — campaign table and creation form
