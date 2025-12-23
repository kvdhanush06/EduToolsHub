Setup and deployment notes
=========================

This document explains how to set up the project for local development and basic production guidance.

Local development (Windows)

1. Create and activate a virtual environment

   PowerShell:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   CMD:
   ```cmd
   python -m venv venv
   venv\Scripts\activate.bat
   ```

2. Install requirements

   ```powershell
   pip install -r requirements.txt
   ```

3. Database migrations

   ```powershell
   python manage.py migrate
   ```

4. Create an admin user (optional)

   ```powershell
   python manage.py createsuperuser
   ```

5. Run the development server

   ```powershell
   python manage.py runserver
   ```

6. Access the app

   Open your browser at: http://127.0.0.1:8000

Environment variables and production notes

- SECRET_KEY and DEBUG: For production, remove hard-coded secrets from `settings.py` and supply them via environment variables.
- ALLOWED_HOSTS: Set appropriate hostnames.
- Static files: run `python manage.py collectstatic` and serve via a web server (Nginx/Apache) or a CDN.
- Database: use PostgreSQL or MySQL for production; update `DATABASES` in `edutoolshub/settings.py` accordingly.

Optional: Docker

You can containerize the app using a simple Python/Django Dockerfile and a separate production-grade database container (Postgres). If you want, I can add Dockerfiles and a docker-compose manifest.

Troubleshooting

- If migrations fail, check `dashboard/migrations/` and the current database state; removing `db.sqlite3` and re-running `migrate` on a development machine is a quick reset.
- If static files are missing, ensure `STATIC_URL`/`STATIC_ROOT` are configured and `collectstatic` was run for production.
