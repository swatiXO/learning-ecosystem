# API contract notes

The source of truth is the live OpenAPI schema at `/docs` (and `/openapi.json`) once the API is running. This file holds notes that don't fit in OpenAPI: auth flow, idempotency semantics, error conventions.

## Idempotency

`POST /events/batch` de-duplicates on client-generated `event_id`. Re-sending the same batch (e.g. after a retry) must be safe.

## Auth (stubbed until Phase 2)

JWT with roles `guardian`, `teacher`, `therapist`, `admin`.
