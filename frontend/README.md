# CodPanel Frontend

Vite + Vue 3 + TypeScript scaffold for the new CodPanel frontend.

Environment

- Copy frontend/.env.example to frontend/.env.local and adjust if needed.
- The dev server will proxy /api to the backend specified in VITE_BACKEND (defaults to http://localhost:8000).

Run locally

cd frontend
npm install
npm run dev

Notes

- Authentication uses HttpOnly session cookies managed by the backend. The frontend will call /auth/login which should set the cookie; frontend never stores tokens in localStorage/sessionStorage.
- Axios is configured with withCredentials: true and includes a global 401 handler that redirects to /login.
