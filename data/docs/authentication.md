# TaskFlow API Authentication

All TaskFlow API requests must be authenticated unless explicitly marked as public (none of the v1 resource endpoints are public).

## API keys (recommended for server-to-server)

Send your secret API key in the `Authorization` header using the Bearer scheme:

```
Authorization: Bearer tf_live_sk_xxxxxxxxxxxxxxxx
```

- Keys starting with `tf_live_sk_` are **production** keys.
- Keys starting with `tf_test_sk_` are **sandbox** keys (no billing, data may be reset weekly).
- Never expose secret keys in client-side code or public repositories.

## Scoped keys

When creating an API key in the TaskFlow dashboard, you may restrict scopes:

| Scope | Allows |
|-------|--------|
| `tasks:read` | List and get tasks |
| `tasks:write` | Create, update, delete tasks |
| `projects:read` | List and get projects |
| `projects:write` | Create, update, archive projects |
| `users:read` | List and get users in your workspace |

A request missing the required scope returns **403 Forbidden** with error code `insufficient_scope`.

## Workspace header (optional)

For accounts with multiple workspaces, pass:

```
X-TaskFlow-Workspace: ws_abc123
```

If omitted, the API uses your default workspace.

## Token expiration

- API keys do **not** expire unless revoked in the dashboard.
- Short-lived **session tokens** (`tf_sess_...`) expire after **1 hour** and are intended for internal tools only. Do not use session tokens in production integrations.

## Authentication errors

| HTTP status | Error code | Meaning |
|-------------|------------|---------|
| 401 | `invalid_api_key` | Key missing, malformed, or revoked |
| 401 | `expired_session` | Session token expired |
| 403 | `insufficient_scope` | Key lacks required scope |

## Example authenticated request

```bash
curl -X GET "https://api.taskflow.io/v1/tasks" \
  -H "Authorization: Bearer tf_test_sk_demo123" \
  -H "Content-Type: application/json"
```
