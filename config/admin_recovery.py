import os
from django.contrib.auth import get_user_model


def run_admin_recovery() -> None:
    """
    One-shot emergency admin recovery controlled by Railway environment variables.

    Required:
      ADMIN_RECOVERY_ENABLED=true
      ADMIN_RECOVERY_USERNAME=<username>
      ADMIN_RECOVERY_PASSWORD=<new password>

    Optional:
      ADMIN_RECOVERY_EMAIL=<email>

    After successful login, set ADMIN_RECOVERY_ENABLED=false.
    """
    enabled = os.getenv("ADMIN_RECOVERY_ENABLED", "false").strip().lower()
    if enabled not in {"1", "true", "yes", "on"}:
        return

    username = os.getenv("ADMIN_RECOVERY_USERNAME", "").strip()
    password = os.getenv("ADMIN_RECOVERY_PASSWORD", "").strip()
    email = os.getenv("ADMIN_RECOVERY_EMAIL", "").strip()

    if not username or not password:
        print("ADMIN RECOVERY: username/password missing; skipped.")
        return

    User = get_user_model()

    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": email},
    )

    if email:
        user.email = email

    user.set_password(password)
    user.is_active = True
    user.is_staff = True
    user.is_superuser = True
    user.save(
        update_fields=[
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "email",
        ]
    )

    action = "created" if created else "recovered"
    print(f"ADMIN RECOVERY: account '{username}' successfully {action}.")
