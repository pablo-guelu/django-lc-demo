# Django demo for Laravel Cloud

Minimal Django 5.2 app to test deployments on Laravel Cloud.

Pages:
- `/` shows Python and Django versions, whether `DATABASE_URL` is set, and a database write test. A green box means static files are served.
- `/health/` returns `{"status": "ok"}`.
- `/admin/` is the Django admin.

Laravel Cloud settings:
- Build command: `python manage.py collectstatic --noinput`
- Start command: `gunicorn clouddemo.wsgi --bind [::]:$PORT`
- Deploy command: `python manage.py migrate --noinput`
- Environment variable: `DJANGO_SECRET_KEY`

Run locally:
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
