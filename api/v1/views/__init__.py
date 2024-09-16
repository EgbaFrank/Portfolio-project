"""
Views module
"""
from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


from api.v1.views.index import *
from api.v1.views.shops import *
from api.v1.views.users import *
from api.v1.views.orders import *
from api.v1.views.places import *
from api.v1.views.products import *
from api.v1.views.shop_lists import *
from api.v1.views.categories import *
from api.v1.views.link_products import *
