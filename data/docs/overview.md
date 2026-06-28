# TaskFlow API Overview

TaskFlow is a fictional project and task management REST API for portfolio and testing purposes.

## Base URL

All API requests use:

```
https://api.taskflow.io/v1
```

## Versioning

- The current stable version is **v1**.
- Include the version in the URL path (`/v1/...`).
- Breaking changes are announced in release notes at least 30 days before removal.

## Request format

- Send JSON bodies with `Content-Type: application/json`.
- Use UTF-8 encoding for all text fields.
- Timestamps are returned in **ISO 8601 UTC** format (example: `2026-05-20T14:30:00Z`).

## Response format

Successful responses return JSON with a top-level `data` object unless noted otherwise.

Example:

```json
{
  "data": {
    "id": "tsk_8f2a91",
    "title": "Write API docs",
    "status": "open"
  }
}
```

## Pagination

List endpoints accept optional query parameters:

| Parameter | Default | Max | Description |
|-----------|---------|-----|-------------|
| `page` | 1 | — | Page number (1-based) |
| `per_page` | 20 | 100 | Items per page |

Paginated responses include a `meta` object:

```json
{
  "data": [],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 87
  }
}
```

## Idempotency

For `POST` requests that create resources, you may send header:

```
Idempotency-Key: <unique-string>
```

If the same key is reused within 24 hours, TaskFlow returns the original response instead of creating a duplicate.

## Support

- Documentation: https://docs.taskflow.io
- Status page: https://status.taskflow.io
- Contact: api-support@taskflow.io
