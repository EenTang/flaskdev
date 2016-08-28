from flask import Blueprint

main = Blueprint('main', __name__)


from . import views, errors
from ..models import Permission


# inject Permission to templates, but i don't know how it work
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
