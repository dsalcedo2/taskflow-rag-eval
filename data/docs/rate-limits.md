# TaskFlow API — Rate Limits and Webhooks

## Rate limits

Rate limits protect API stability. Limits apply **per API key** unless noted otherwise.

| Plan | Requests per minute | Burst |
|------|---------------------|-------|
| Sandbox (`tf_test_sk_`) | 60 | 10 |
| Starter | 120 | 20 |
| Pro | 600 | 50 |
| Enterprise | Custom | Custom |

When you exceed the limit, the API returns **429 Too Many Requests** with error code `rate_limit_exceeded`.

### Rate limit headers

Every response includes:

```
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1716215400
```

`X-RateLimit-Reset` is a Unix timestamp (seconds) when the window resets.

### Retry-After

429 responses include:

```
Retry-After: 30
```

Wait at least that many seconds before retrying.

## Webhooks overview

Webhooks notify your server when events occur in TaskFlow.

- Configure webhook URLs in the dashboard under **Developers → Webhooks**.
- TaskFlow sends **HTTPS POST** requests with a JSON body.
- Webhook signing secret is shown once at creation; verify signatures using header `X-TaskFlow-Signature`.

## Supported webhook events

| Event | Fired when |
|-------|------------|
| `task.created` | A new task is created |
| `task.updated` | A task field changes |
| `task.deleted` | A task is permanently deleted |
| `project.archived` | A project is archived |

## Webhook delivery policy

- TaskFlow retries failed deliveries up to **5 times** over 24 hours.
- A delivery is considered failed if your endpoint returns a non-2xx status or times out after **10 seconds**.
- Webhook payloads include `event`, `created_at`, and `data` objects.

## Webhook rate limits

Outbound webhook deliveries are limited to **300 events per minute** per workspace. If exceeded, events are queued for up to 6 hours.

## Not available via API

The following are **dashboard-only** and not documented as REST endpoints:

- Creating or deleting webhook subscriptions
- Rotating webhook signing secrets
- Exporting workspace billing invoices

If asked about billing exports or invoice APIs, refer users to the dashboard billing section.
