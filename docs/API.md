# API v1

This document describes the mocked API v1 endpoints available for development.

All endpoints are available under the /api/v1 prefix. The backend sets an HttpOnly cookie named `session` for authenticated requests.

Authentication

- POST /api/v1/auth/login
  - Request JSON: { "username": "string", "password": "string" }
  - Response: 200 OK
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com"
    }
  - Notes: Only credentials `admin` / `admin` are accepted. On success the server sets an HttpOnly cookie `session=mock-session` (SameSite=Lax).

- GET /api/v1/auth/me
  - Requires cookie `session=mock-session`.
  - Response: 200 OK with user object (same shape as login response).
  - 401 if not authenticated.

- POST /api/v1/auth/logout
  - Clears the `session` cookie.
  - Response: { "success": true }

Dashboard

- GET /api/v1/dashboard/overview
  - Response: 200 OK
  {
    "totalServers": number,
    "onlineServers": number,
    "offlineServers": number,
    "connectedPlayers": number,
    "cpuUsagePercent": number,
    "memoryUsagePercent": number
  }

- GET /api/v1/dashboard/activity
  - Response: 200 OK
  [ { "id": number, "type": "info|warning|error", "message": string, "created_at": string (ISO) }, ... ]

- GET /api/v1/dashboard/quick-actions
  - Response: 200 OK
  [ { "id": number, "name": string, "description": string }, ... ]

- GET /api/v1/dashboard/logs
  - Response: 200 OK
  [ { "id": number, "level": "info|warning|error", "message": string, "timestamp": string (ISO) }, ... ]

Servers

- GET /api/v1/servers?q=&status=
  - Query params:
    - q: optional search string (matches name, ip, game)
    - status: optional filter (running|stopped|starting|stopping|crashed)
  - Response: 200 OK
  [
    {
      "id": number,
      "name": string,
      "ip": string,
      "game": string,
      "map": string,
      "players": number,
      "cpu": number,
      "ram": number,
      "status": string
    },
    ...
  ]

- GET /api/v1/servers/{id}
  - Response: 200 OK (single server object as above) or 404 if not found.

- POST /api/v1/servers/{id}/power
  - Body: { "action": "start|stop|restart|kill" }
  - Response: 200 OK { "result": "ok" } or 400 for unknown action.

- GET /api/v1/servers/{id}/overview
  - Response: 200 OK
  { "game": string, "map": string, "players": number, "uptime": string }

- GET /api/v1/servers/{id}/console
  - Response: 200 OK
  [ "line1", "line2", ... ]

- GET /api/v1/servers/{id}/files
  - Response: 200 OK
  [ { "name": string, "size": number }, ... ]

- GET /api/v1/servers/{id}/config
  - Response: 200 OK
  { ... arbitrary configuration JSON ... }

- GET /api/v1/servers/{id}/backups
  - Response: 200 OK
  [ { "name": string, "created_at": string (ISO) }, ... ]

- GET /api/v1/servers/{id}/metrics
  - Response: 200 OK
  { "cpu_percent": number, "memory_percent": number }

Notes

- The current implementation is mocked for development and returns static data.
- Authentication uses an HttpOnly cookie named `session` with value `mock-session` on successful authentication. Cookies use SameSite=Lax and Secure=False for local development.
