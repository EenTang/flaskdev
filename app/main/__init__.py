# -*- coding: utf-8 -*-
from flask import Blueprint

## 此处要加参数 static_folder, 在图片上传时会用到静态 static 路径
main = Blueprint('main', __name__, static_folder='', template_folder='templates', static_url_path='')


from . import views, errors
from ..models import Permission


# inject Permission to templates, but i don't know how it work
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
