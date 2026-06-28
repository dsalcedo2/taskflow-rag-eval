# TaskFlow API — Tasks

Tasks represent individual units of work. Every task belongs to exactly one project.

**Required scope:** `tasks:read` for GET, `tasks:write` for POST/PATCH/DELETE.

## List tasks

```
GET /v1/tasks
```

### Query parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `project_id` | string | Filter by project (recommended) |
| `status` | string | `open`, `in_progress`, `done`, or `cancelled` |
| `assignee_id` | string | Filter by assigned user |
| `due_before` | string | ISO 8601 date; tasks due on or before this date |
| `page` | integer | Page number |
| `per_page` | integer | Items per page (max 100) |

### Example

```
GET /v1/tasks?project_id=prj_7k2m&status=open&per_page=50
```

## Get a task

```
GET /v1/tasks/{task_id}
```

Returns full task object including `description`, `priority`, `assignee_id`, `due_at`, and `labels`.

## Create a task

```
POST /v1/tasks
```

### Request body

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `title` | yes | string | 1–200 characters |
| `project_id` | yes | string | Parent project ID |
| `description` | no | string | Up to 5000 characters |
| `priority` | no | string | `low`, `medium`, `high` (default `medium`) |
| `assignee_id` | no | string | User to assign |
| `due_at` | no | string | ISO 8601 UTC datetime |

### Example request

```json
{
  "title": "Draft API authentication guide",
  "project_id": "prj_7k2m",
  "priority": "high",
  "due_at": "2026-05-25T17:00:00Z"
}
```

## Update a task

```
PATCH /v1/tasks/{task_id}
```

Updatable fields: `title`, `description`, `status`, `priority`, `assignee_id`, `due_at`, `labels`.

Valid `status` values: `open`, `in_progress`, `done`, `cancelled`.

## Delete a task

```
DELETE /v1/tasks/{task_id}
```

Permanently deletes the task. This action **cannot be undone**.

## Task priorities

| Value | Description |
|-------|-------------|
| `low` | No urgency |
| `medium` | Default priority |
| `high` | Urgent; surfaced first in dashboard views |

## Webhook trigger

Creating or updating a task may emit `task.created` or `task.updated` events if webhooks are configured (see rate-limits and webhooks policy in operations docs).
