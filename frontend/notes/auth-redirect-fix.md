# Auth redirect loop fix

This file records the recent fix for the authentication redirect loop.

Summary

- Added redirect sanitization and loop prevention in the Auth store.
  - File: frontend/src/app/stores/auth.ts
  - Implemented sanitizeRedirect(raw?: string | null) to allow only single pathnames, strip queries/hashes and reject redirects to `/login`.
  - Updated login(), logout(), and handleUnauthenticated() to use the sanitizer and avoid nested redirect params.
- Ensured the Vite dev server proxies `/api/v1` requests to the backend so login requests reach `/api/v1/auth/login`.
  - File: frontend/vite.config.ts
- Improved Axios error handling so UI receives readable error strings and no `alert()` popups occur.
  - File: frontend/src/services/api/axios.ts
- Removed alert() usage in the UI and replaced with inline error messaging and loading indicators.
  - Files: frontend/src/features/auth/LoginView.vue, frontend/src/features/dashboard/DashboardView.vue

Validation performed

- Code updated and pushed to branch `feature/new-frontend`.
- Manual review confirms the auth store sanitizes redirect values and prevents nested redirect querystrings.

How to verify locally

1. Ensure backend is running on http://localhost:8000
2. In the frontend directory, ensure .env.local contains:

```
VITE_API_BASE=/api/v1
VITE_BACKEND=http://localhost:8000
```

3. Start frontend dev server (restart if already running):

```
npm install
npm run dev
```

4. Confirm behavior:
- Navigate to /dashboard when unauthenticated → should redirect to `/login?redirect=/dashboard` (single-level).
- Login with admin/admin → should redirect to /dashboard without nested redirect parameters.
- Trigger unauthenticated handler while on `/login?redirect=/dashboard` → URL should remain `/login?redirect=/dashboard` (no nesting).

