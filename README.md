# Data Nexa

A data-profiling product prototype with a React interface and a FastAPI AI-insight engine. The intended product helps users move from a dataset to a profile, quality issues, and recommendations.

**Status:** partial implementation. The full upload → profile → saved insight flow is not connected.

## What exists

| Area | Current source |
| --- | --- |
| Frontend | React/JavaScript pages, stores, upload components, and API clients |
| AI engine | Groq orchestration, prompt building, anonymization helpers, parsing, categorization, and cache logic |
| API | Health endpoint and insight router |
| Authentication/upload/workspaces | Planned frontend contracts; corresponding complete backend workflows are missing |
| Reports/remediation | Some screens and actions use static or mock content |

The frontend is JavaScript/JSX, not TypeScript. A folder named `tests` exists in the backend, but it currently contains only a package marker.

## Source map

- [backend/app/main.py](backend/app/main.py): registered routes.
- [backend/app/api/v1/insights.py](backend/app/api/v1/insights.py): insight endpoints and placeholders.
- [backend/app/core/ai_engine](backend/app/core/ai_engine): implemented AI modules.
- [frontend/src](frontend/src): interface and client contracts.
- [.kiro/specs](.kiro/specs): design requirements and planned tasks; these are not proof of completed features.

## Local development

Use Python 3.11+ and a Node.js version compatible with the checked-in Vite dependencies.

From `backend/`, create and activate a virtual environment, then install `requirements.txt`. Copy `.env.example` to a local `.env` and supply fresh `SECRET_KEY` and `GROQ_API_KEY` values.

The default database URL uses `aiosqlite`, which is missing from the requirements file. Install that driver for a SQLite experiment, or configure a PostgreSQL database with the declared async driver. These paths need runtime validation.

```bash
# From backend/
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

For the interface:

```bash
# From frontend/
npm ci
npm run dev
```

Copy `frontend/.env.example` to `frontend/.env`; its API setting is `VITE_API_URL=http://localhost:8000/api/v1`. Set backend `ALLOWED_ORIGINS` to the actual frontend origin printed by Vite. The existing default origins may differ.

After successful backend startup, inspect `http://localhost:8000/docs` and `/health`. A healthy process does not prove the planned upload/auth routes work.

## Development checks

The frontend declares `npm run build` and `npm run lint`. It has no `npm run test` script. There is a backend Dockerfile, but no checked-in frontend Dockerfile or implemented backend test suite in this revision.

## Data handling and limitations

The design uses an external AI provider. It cannot promise that all data stays inside a VPC. Anonymization helpers need validation before any sensitive dataset is used.

Workspace authorization, persistence, cache identity, supported file formats, and request limits need completion. Treat advertised multi-tenancy and authentication as goals until the end-to-end flow is implemented and tested.

The existing README identifies this project as proprietary. This documentation change does not grant a new license. See [project status](docs/PROJECT_STATUS.md).

## Validation

This documentation was checked against repository files on 13 October 2026. Builds, application runs, and test suites were not executed during this documentation pass. Commands below describe the intended local workflow, not a verified deployment.
