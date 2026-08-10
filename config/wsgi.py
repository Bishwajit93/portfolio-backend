"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable called ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

# Emergency owner recovery.
# This does nothing unless ADMIN_RECOVERY_ENABLED=true in Railway.
try:
    from config.admin_recovery import run_admin_recovery

    run_admin_recovery()
except Exception as exc:
    # Never prevent the website from starting because of the emergency helper.
    print(f"ADMIN RECOVERY: skipped because of error: {exc}")
