# TaskFlow API — Errors

TaskFlow uses conventional HTTP status codes and a consistent JSON error body.

## Error response format

```json
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "Too many requests. Retry after 30 seconds.",
    "doc_url": "https://docs.taskflow.io/errors/rate_limit_exceeded"
  }
}
```

Optional field `details` may contain validation errors as an array of objects with `field` and `message`.

## HTTP status codes

| Status | When it occurs |
|--------|----------------|
| 400 | Invalid JSON, missing required field, invalid parameter value |
| 401 | Missing or invalid authentication |
| 403 | Authenticated but not allowed (wrong scope or role) |
| 404 | Resource not found |
| 405 | HTTP method not supported for endpoint |
| 409 | Conflict (duplicate idempotency misuse or state conflict) |
| 422 | Semantic validation failed (e.g., due date in the past when not allowed) |
| 429 | Rate limit exceeded |
| 500 | Unexpected server error |
| 503 | Service temporarily unavailable |

## Common error codes

| Code | HTTP | Description |
|------|------|-------------|
| `invalid_api_key` | 401 | API key missing, invalid, or revoked |
| `insufficient_scope` | 403 | API key lacks required scope |
| `resource_not_found` | 404 | Project, task, or user ID does not exist |
| `validation_error` | 400 | One or more request fields failed validation |
| `rate_limit_exceeded` | 429 | Account exceeded allowed request rate |
| `project_archived` | 409 | Cannot create tasks in an archived project |
| `method_not_allowed` | 405 | Endpoint does not support this HTTP method |

## Validation example

Request:

```json
POST /v1/tasks
{ "title": "", "project_id": "prj_7k2m" }
```

Response **400**:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed",
    "details": [
      { "field": "title", "message": "title must be between 1 and 200 characters" }
    ]
  }
}
```

## Retry guidance

- **429**: Honor the `Retry-After` response header (seconds). Do not retry immediately in a tight loop.
- **500 / 503**: Retry with exponential backoff (start at 1s, max 32s, up to 5 attempts).
- **400 / 401 / 403 / 404**: Do not retry without fixing the request.

## Request ID

Every error response includes header:

```
X-Request-Id: req_01h2xyz...
```

Include this ID when contacting api-support@taskflow.io.
