# TaskFlow API — Projects

Projects group tasks under a shared goal or team.

**Required scope:** `projects:read` for GET, `projects:write` for POST/PATCH/DELETE.

## List projects

```
GET /v1/projects
```

### Query parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter: `active`, `archived`, or `all` (default `active`) |
| `page` | integer | Page number |
| `per_page` | integer | Items per page (max 100) |

### Example response

```json
{
  "data": [
    {
      "id": "prj_7k2m",
      "name": "Website Redesign",
      "status": "active",
      "task_count": 12,
      "created_at": "2026-01-10T09:00:00Z"
    }
  ],
  "meta": { "page": 1, "per_page": 20, "total": 3 }
}
```

## Get a project

```
GET /v1/projects/{project_id}
```

Returns a single project object including `description` and `owner_id`.

## Create a project

```
POST /v1/projects
```

### Request body

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | yes | string | 1–120 characters |
| `description` | no | string | Up to 2000 characters |
| `owner_id` | no | string | User ID; defaults to authenticated user |

### Example request

```json
{
  "name": "Q3 Marketing Launch",
  "description": "Campaign assets and landing pages"
}
```

## Update a project

```
PATCH /v1/projects/{project_id}
```

Updatable fields: `name`, `description`, `status` (`active` or `archived`).

## Archive a project

```
DELETE /v1/projects/{project_id}
```

This is a **soft delete**. The project `status` becomes `archived`; tasks remain but cannot be assigned to new work without unarchiving.

## Deprecated endpoint

```
GET /v1/project-list
```

**Deprecated** as of 2026-03-01. Use `GET /v1/projects` instead. This endpoint will be removed on **2026-09-01**.
