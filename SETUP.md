# EduToolsHub — Setup & Contributing Guide

This document describes how to set up, run, test and contribute to EduToolsHub. It focuses on local development (Windows examples provided) and includes cross-platform guidance where applicable.

## Contents
- Prerequisites
- Quick start
- Configuration (env + secrets)
- Database & migrations
- Run (development)
- Tests
# Dependencies & pinning
## Prerequisites

- Supported OS: Windows 10/11, macOS, Linux
- Python: 3.11 or 3.12
- Git installed and configured

Recommended developer tools (optional): pip-tools, pytest.


## Quick start

Clone and prepare your environment:

```powershell
git clone https://github.com/kvdhanush06/EduToolsHub.git
cd EduToolsHub
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
# or: .\.venv\Scripts\activate  # cmd.exe
pip install --upgrade pip
pip install -r requirements.txt
```

If you prefer separating runtime and development packages, create `requirements.in` and use `pip-compile` (see Dependencies section).


## Configuration (env)

Create a `.env` at the repository root to store local settings. Do not commit this file.

Example `.env`:

```text
DEBUG=True
SECRET_KEY=replace-with-a-secure-key
ALLOWED_HOSTS=localhost,127.0.0.1
# DATABASE_URL=sqlite:///db.sqlite3
```

Add `.env` to `.gitignore` if it is not already ignored.


## Database & migrations

This project uses SQLite by default. To apply migrations:

```powershell
python manage.py migrate
```

Create a superuser for local administration:

```powershell
python manage.py createsuperuser
```


## Run (development)

Start the development server:

```powershell
python manage.py runserver
```

Visit http://127.0.0.1:8000 and `/admin/` to log in with the superuser account.


## Tests

Run the Django test suite:

```powershell
python manage.py test
```

Or, with pytest (if configured):

```powershell
pytest -q
```

If tests fail after pulling changes, run `migrate` and re-run tests. Ensure any required environment variables or fixtures are present.


## Dependencies & pinning

For day-to-day development use ranges in `requirements.txt`. For reproducible installs, pin exact versions:

```powershell
pip freeze > requirements-frozen.txt
```

Better: use pip-tools to maintain human-editable inputs and generate a pinned file:

```powershell
pip install pip-tools
pip-compile requirements.in --output-file requirements.txt
pip-sync requirements.txt
```

Use `pip-audit` to check for known vulnerabilities:

```powershell
pip install pip-audit
pip-audit
```


## Production notes

- Use PostgreSQL (or another production RDBMS) instead of SQLite.
- Set `DEBUG=False`, provide a secure `SECRET_KEY`, and set `ALLOWED_HOSTS`.
- Collect static files and serve them via a web server or CDN:

```bash
python manage.py collectstatic
```

- Use Gunicorn/Uvicorn behind a reverse proxy on Linux hosts for production deployments.


## Contributing guidelines

1. Fork the repository, clone your fork and create a branch:

```powershell
git clone https://github.com/kvdhanush06/EduToolsHub.git
cd EduToolsHub
git checkout -b feat/short-description
```

2. Make focused changes with clear commit messages. Prefer small, testable commits.

3. Run tests locally before pushing:

```powershell
pip install -r requirements.txt
python manage.py test
```

4. If your change alters models, add migrations (`makemigrations`) and include them in the PR.

5. Open a pull request against `main`. In your PR include a description of the change, why it is needed and how to test it. Use the checklist below.

PR checklist (suggested):

- [ ] Tests pass locally
- [ ] New behavior covered by tests or documented
- [ ] Migrations included if applicable

Address review feedback, rebase or merge the latest `main` as requested, and keep the PR focused.


## Troubleshooting

- If `pip install` fails on Windows due to build tools, install the required compilers or use pre-built wheels.
- If migrations are inconsistent, and you are on a development database, you may remove `db.sqlite3` and re-run `migrate` to reset state.
- Use `python manage.py runserver --noreload` when diagnosing issues caused by the autoreloader.