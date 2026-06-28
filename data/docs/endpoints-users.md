# TaskFlow API — Users

Users are members of a TaskFlow workspace. The Users API is **read-only** via the public REST API.

**Required scope:** `users:read` for all endpoints in this document.

## List users

```
GET /v1/users
```

### Query parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `role` | string | Filter: `admin`, `member`, or `viewer` |
| `email` | string | Exact email match (case-insensitive) |
| `page` | integer | Page number |
| `per_page` | integer | Items per page (max 100) |

### Example response

```json
{
  "data": [
    {
      "id": "usr_9p4q",
      "email": "alex@example.com",
      "display_name": "Alex Kim",
      "role": "member",
      "created_at": "2025-11-02T12:00:00Z"
    }
  ],
  "meta": { "page": 1, "per_page": 20, "total": 8 }
}
```

## Get a user

```
GET /v1/users/{user_id}
```

Returns user profile fields. Sensitive fields (password hashes, MFA secrets) are **never** returned.

## User roles

| Role | Permissions |
|------|-------------|
| `admin` | Full workspace access; can invite users and manage API keys |
| `member` | Create and edit tasks and projects |
| `viewer` | Read-only access to tasks and projects |

## Invite users

User invitations are **not** available via the REST API. Use the TaskFlow dashboard under **Settings → Team** to send invites.

Attempting `POST /v1/users` returns **405 Method Not Allowed**.

## Deactivate users

Deactivating users is **not** exposed in the public API. Contact workspace admins or use the dashboard.

## Service accounts

Service accounts use IDs prefixed with `svc_` instead of `usr_`. They appear in user listings when `?include_service_accounts=true` is passed.
