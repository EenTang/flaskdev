from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*agrs, **kwagrs):
            if not current_user.can(permission):
                abort(403)
            return f(*agrs, **kwagrs)
        return decorated_function
    return decorator


def adminstrator_required(f):
    return permission_required(Permission.ADMINSTER)(f)


