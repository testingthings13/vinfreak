import os
from typing import Dict, Type
from starlette.middleware.sessions import SessionMiddleware
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from markupsafe import Markup

class AdminAuth(AuthenticationBackend):
    async def login(self, request):
        form = await request.form()
        u = form.get("username")
        p = form.get("password")
        if u == os.environ.get("ADMIN_USER", "admin") and p == os.environ.get("ADMIN_PASS", "admin"):
            request.session.update({"token": "ok"})
            return True
        return False

    async def logout(self, request):
        request.session.clear()

    async def authenticate(self, request):
        return request.session.get("token") == "ok"

def init_admin(app, engine, models: Dict[str, Type]):
    """
    Mount SQLAdmin at /admin using provided SQLAlchemy models.
    Usage in app.py: init_admin(app, engine, {"Car": Car})
    """
    Car = models["Car"]

    # Ensure session middleware (needed for admin login)
    app.add_middleware(SessionMiddleware, secret_key=os.environ.get("ADMIN_SECRET", "dev-secret-change-me"))

    # Build a ModelView dynamically so we don't import from app.py
    class CarAdmin(ModelView, model=Car):
        name = "Car"
        name_plural = "Cars"
        icon = "fa-solid fa-car"

        # Columns in the table view
        column_list = [
            Car.id, Car.year, Car.make, Car.model, Car.trim, Car.price, Car.mileage,
            Car.state, Car.transmission, Car.drivetrain, Car.auction_status, Car.vin, Car.image_url
        ]

        # Search & filters
        column_searchable_list = [Car.vin, Car.make, Car.model, Car.trim, Car.city, Car.state, Car.title]
        column_filters = [
            Car.make, Car.model, Car.year, Car.state, Car.seller_type,
            Car.transmission, Car.drivetrain, Car.body_type, Car.auction_status
        ]

        # Default sort (posted_at desc)
        column_default_sort = [(Car.posted_at, True)]

        # Make image and URLs clickable/visible in list & detail
        column_formatters = {
            Car.image_url: lambda m, a: Markup(f'<img src="{getattr(m, a) or ""}" style="height:48px;border-radius:6px" onerror="this.style.display=`none`">') if getattr(m, a) else "",
            Car.url:       lambda m, a: Markup(f'<a href="{getattr(m, a)}" target="_blank">source</a>') if getattr(m, a) else "",
        }
        column_formatters_detail = column_formatters

        # If you want to hide internal fields from the form, list them here:
        # form_excluded_columns = [Car.images_json]

    admin = Admin(app, engine, authentication_backend=AdminAuth(secret_key=os.environ.get("ADMIN_SECRET", "dev-secret-change-me")))
    admin.add_view(CarAdmin)
    return admin
