# core/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import MasterUser

class MasterUserBackend(BaseBackend):
    """
    Authenticate against the master_user table.
    On successful login, create/update a mirror Django User (only to support admin/site).
    master_user remains the source of truth — passwords checked against master_user.password.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            mu = MasterUser.objects.get(username=username)
        except MasterUser.DoesNotExist:
            return None
        if not mu.is_active:
            return None

        # Try Django compatible password check first:
        try:
            if check_password(password, mu.password):
                # sync to django auth user
                user, created = User.objects.get_or_create(username=mu.username)
                # update staff/superuser flags based on role
                user.is_staff = (mu.role == 'admin')
                user.is_superuser = (mu.role == 'admin')
                # do not set password here (we use master_user as source of truth)
                user.save()
                return user
        except Exception:
            # check_password may fail if mu.password is in an unknown format.
            # fallback: (temporary) raw compare - ONLY if mu.password stored in cleartext (NOT RECOMMENDED)
            if password == mu.password:
                user, _ = User.objects.get_or_create(username=mu.username)
                user.is_staff = (mu.role == 'admin')
                user.is_superuser = (mu.role == 'admin')
                user.save()
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
