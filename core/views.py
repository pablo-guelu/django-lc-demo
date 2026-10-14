import logging
import os
import platform

import django
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

from .models import Visit

logger = logging.getLogger(__name__)


def _db_status():
    try:
        Visit.objects.create()
        return {"ok": True, "engine": connection.vendor, "visits": Visit.objects.count()}
    except Exception as exc:  # show the error on the page, this is a test app
        logger.exception("Database check failed")
        return {"ok": False, "engine": connection.vendor, "error": str(exc)}


def home(request):
    context = {
        "python": platform.python_version(),
        "django": django.get_version(),
        "db": _db_status(),
        "has_database_url": "DATABASE_URL" in os.environ,
    }
    logger.info("Home page served")
    return render(request, "core/home.html", context)


def health(request):
    return JsonResponse({"status": "ok"})
