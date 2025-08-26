from datetime import datetime
from typing import List, Optional, Union
import json, os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Index, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

# ---------------- DB setup ----------------
DB_URL = "sqlite:///./cars.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)

    # identity/display
    vin = Column(String, unique=True, nullable=True, index=True)
    make = Column(String, index=True)
    model = Column(String, index=True)
    trim = Column(String, nullable=True)
    year = Column(Integer, index=True)
    title = Column(String, nullable=True)

    # numbers
    mileage = Column(Integer, nullable=True)
    price = Column(Float, index=True)
    currency = Column(String, nullable=True)

    # location
    city = Column(String, nullable=True)
    state = Column(String, index=True)

    # attributes
    seller_type = Column(String, nullable=True)
    exterior_color = Column(String, nullable=True)
    interior_color = Column(String, nullable=True)
    transmission = Column(String, nullable=True)
    drivetrain = Column(String, nullable=True)
    fuel_type = Column(String, nullable=True)
    body_type = Column(String, nullable=True)

    # timestamps
    posted_at = Column(DateTime, default=datetime.utcnow)

    # source/meta
    source = Column(String, nullable=True)
    url = Column(String, nullable=True)
    auction_status = Column(String, nullable=True)
    end_time = Column(String, nullable=True)
    time_left = Column(String, nullable=True)
    number_of_views = Column(Integer, nullable=True)
    number_of_bids = Column(Integer, nullable=True)

    # long text
    description = Column(Text, nullable=True)
    highlights = Column(Text, nullable=True)
    equipment = Column(Text, nullable=True)
    modifications = Column(Text, nullable=True)
    known_flaws = Column(Text, nullable=True)
    service_history = Column(Text, nullable=True)
    ownership_history = Column(Text, nullable=True)
    seller_notes = Column(Text, nullable=True)
    other_items = Column(Text, nullable=True)

    # media/tech
    engine = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    images_json = Column(Text, nullable=True)

    # location/seller extra
    location_address = Column(String, nullable=True)
    location_url = Column(String, nullable=True)
    seller_name = Column(String, nullable=True)
    seller_url = Column(String, nullable=True)

Index("ix_cars_search", Car.make, Car.model, Car.year, Car.price, Car.state)
Base.metadata.create_all(bind=engine)

# ---------------- App & config ----------------
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="VINFREAK API", version="0.6.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Pydantic models ----------------
class CarIn(BaseModel):
    vin: Optional[str] = None
    make: str
    model: str
    trim: Optional[str] = None
    year: int
    mileage: Optional[int] = Field(default=None, ge=0)
    price: float = Field(ge=0)
    currency: Optional[str] = None

    city: Optional[str] = None
    state: Optional[str] = None
    seller_type: Optional[str] = None
    exterior_color: Optional[str] = None
    interior_color: Optional[str] = None
    transmission: Optional[str] = None
    drivetrain: Optional[str] = None
    fuel_type: Optional[str] = None
    body_type: Optional[str] = None
    posted_at: Optional[datetime] = None

    source: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    auction_status: Optional[str] = None
    end_time: Optional[str] = None
    time_left: Optional[str] = None
    number_of_views: Optional[int] = None
    number_of_bids: Optional[int] = None

    description: Optional[str] = None
    highlights: Optional[str] = None
    equipment: Optional[str] = None
    modifications: Optional[str] = None
    known_flaws: Optional[str] = None
    service_history: Optional[str] = None
    ownership_history: Optional[str] = None
    seller_notes: Optional[str] = None
    other_items: Optional[str] = None

    engine: Optional[str] = None
    image_url: Optional[str] = None
    images: Optional[List[str]] = None

    location_address: Optional[str] = None
    location_url: Optional[str] = None
    seller_name: Optional[str] = None
    seller_url: Optional[str] = None

class CarOut(CarIn):
    id: int
    class Config:
        from_attributes = True

class PaginatedCars(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[CarOut]

# ---------------- Helpers ----------------
def to_dict(obj: Car) -> dict:
    d = {
        "id": obj.id,
        "vin": obj.vin,
        "make": obj.make,
        "model": obj.model,
        "trim": obj.trim,
        "year": obj.year,
        "mileage": obj.mileage,
        "price": obj.price,
        "currency": obj.currency,
        "city": obj.city,
        "state": obj.state,
        "seller_type": obj.seller_type,
        "exterior_color": obj.exterior_color,
        "interior_color": obj.interior_color,
        "transmission": obj.transmission,
        "drivetrain": obj.drivetrain,
        "fuel_type": obj.fuel_type,
        "body_type": obj.body_type,
        "posted_at": obj.posted_at.isoformat() if obj.posted_at else None,
        "source": obj.source,
        "url": obj.url,
        "title": obj.title,
        "auction_status": obj.auction_status,
        "end_time": obj.end_time,
        "time_left": obj.time_left,
        "number_of_views": obj.number_of_views,
        "number_of_bids": obj.number_of_bids,
        "description": obj.description,
        "highlights": obj.highlights,
        "equipment": obj.equipment,
        "modifications": obj.modifications,
        "known_flaws": obj.known_flaws,
        "service_history": obj.service_history,
        "ownership_history": obj.ownership_history,
        "seller_notes": obj.seller_notes,
        "other_items": obj.other_items,
        "engine": obj.engine,
        "image_url": obj.image_url,
        "images": [],
        "location_address": obj.location_address,
        "location_url": obj.location_url,
        "seller_name": obj.seller_name,
        "seller_url": obj.seller_url,
    }
    try:
        if obj.images_json:
            imgs = json.loads(obj.images_json)
            if isinstance(imgs, list):
                d["images"] = [str(u) for u in imgs if str(u).strip()]
    except Exception:
        pass
    if not d["images"] and obj.image_url:
        d["images"] = [obj.image_url]
    return d

def parse_int(q: Optional[Union[str, int, float]]) -> Optional[int]:
    if q is None: return None
    if isinstance(q, int): return q
    try:
        s = str(q).strip()
        if s == "": return None
        return int(float(s))
    except Exception:
        return None

def parse_float(q: Optional[Union[str, int, float]]) -> Optional[float]:
    if q is None: return None
    if isinstance(q, (int, float)): return float(q)
    try:
        s = str(q).strip().replace(",", "")
        if s == "": return None
        return float(s)
    except Exception:
        return None

# ---------------- Routes ----------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/cars", response_model=CarOut)
def create_car(car: CarIn):
    db = SessionLocal()
    try:
        obj = Car(**car.model_dump(exclude={"images"}))
        if car.images:
            obj.images_json = json.dumps(car.images)
            if not obj.image_url:
                obj.image_url = car.images[0]
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return CarOut.model_validate(to_dict(obj))
    finally:
        db.close()

@app.post("/cars/bulk", response_model=dict)
def bulk_insert(cars: List[CarIn]):
    db = SessionLocal()
    inserted = 0
    skipped = 0
    try:
        for c in cars:
            try:
                obj = Car(**c.model_dump(exclude={"images"}))
                if c.images:
                    obj.images_json = json.dumps(c.images)
                    if not obj.image_url:
                        obj.image_url = c.images[0]
                db.add(obj)
                db.commit()
                inserted += 1
            except IntegrityError:
                db.rollback()
                skipped += 1
        return {"inserted": inserted, "skipped": skipped}
    finally:
        db.close()

@app.get("/cars/{car_id}", response_model=CarOut)
def get_car(car_id: int):
    db = SessionLocal()
    try:
        obj = db.get(Car, car_id)
        if not obj:
            raise HTTPException(404, "Car not found")
        return CarOut.model_validate(to_dict(obj))
    finally:
        db.close()

@app.get("/cars/by_vin/{vin}", response_model=CarOut)
def get_car_by_vin(vin: str):
    db = SessionLocal()
    try:
        obj = db.query(Car).filter(Car.vin == vin).first()
        if not obj:
            raise HTTPException(404, "Car not found")
        return CarOut.model_validate(to_dict(obj))
    finally:
        db.close()

@app.get("/cars", response_model=PaginatedCars)
def list_cars(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),

    make: Optional[str] = None, model: Optional[str] = None, trim: Optional[str] = None,
    city: Optional[str] = None, state: Optional[str] = None, seller_type: Optional[str] = None,
    exterior_color: Optional[str] = None, interior_color: Optional[str] = None,
    transmission: Optional[str] = None, drivetrain: Optional[str] = None,
    fuel_type: Optional[str] = None, body_type: Optional[str] = None,
    engine: Optional[str] = None, auction_status: Optional[str] = None, title: Optional[str] = None,

    year_from: Optional[str] = None, year_to: Optional[str] = None,
    price_min: Optional[str] = None, price_max: Optional[str] = None,
    mileage_min: Optional[str] = None, mileage_max: Optional[str] = None,

    search: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
):
    db = SessionLocal()
    try:
        q = db.query(Car)

        def like(col, val):
            nonlocal q
            if val:
                q = q.filter(col.ilike(f"%{val}%"))

        like(Car.make, make); like(Car.model, model); like(Car.trim, trim)
        like(Car.city, city); like(Car.state, state); like(Car.seller_type, seller_type)
        like(Car.exterior_color, exterior_color); like(Car.interior_color, interior_color)
        like(Car.transmission, transmission); like(Car.drivetrain, drivetrain)
        like(Car.fuel_type, fuel_type); like(Car.body_type, body_type)
        like(Car.engine, engine); like(Car.auction_status, auction_status); like(Car.title, title)

        yf = parse_int(year_from); yt = parse_int(year_to)
        pmin = parse_float(price_min); pmax = parse_float(price_max)
        mmin = parse_int(mileage_min); mmax = parse_int(mileage_max)

        if yf is not None: q = q.filter(Car.year >= yf)
        if yt is not None: q = q.filter(Car.year <= yt)
        if pmin is not None: q = q.filter(Car.price >= pmin)
        if pmax is not None: q = q.filter(Car.price <= pmax)
        if mmin is not None: q = q.filter(Car.mileage >= mmin)
        if mmax is not None: q = q.filter(Car.mileage <= mmax)

        if search:
            s = f"%{search}%"
            q = q.filter(
                (Car.make.ilike(s)) | (Car.model.ilike(s)) | (Car.trim.ilike(s)) |
                (Car.city.ilike(s)) | (Car.state.ilike(s)) | (Car.title.ilike(s))
            )

        if sort:
            if sort == "price_asc": q = q.order_by(Car.price.asc())
            elif sort == "price_desc": q = q.order_by(Car.price.desc())
            elif sort == "year_desc": q = q.order_by(Car.year.desc())
            elif sort == "year_asc": q = q.order_by(Car.year.asc())
            elif sort == "mileage_asc": q = q.order_by(Car.mileage.asc())
            elif sort == "mileage_desc": q = q.order_by(Car.mileage.desc())

        total = q.count()
        rows = q.offset((page - 1) * page_size).limit(page_size).all()
        items = [CarOut.model_validate(to_dict(r)) for r in rows]
        return PaginatedCars(total=total, page=page, page_size=page_size, items=items)
    finally:
        db.close()

# ---------------- Admin (/admin) ----------------
from starlette.middleware.sessions import SessionMiddleware
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend

# session middleware for admin login
app.add_middleware(SessionMiddleware, secret_key=os.environ.get("ADMIN_SECRET", "dev-secret-change-me"))

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

class CarAdmin(ModelView, model=Car):
    name = "Car"
    name_plural = "Cars"
    icon = "fa-solid fa-car"
    column_list = [Car.id, Car.year, Car.make, Car.model, Car.trim, Car.price, Car.mileage, Car.state, Car.auction_status, Car.vin]
    column_searchable_list = [Car.vin, Car.make, Car.model, Car.trim, Car.city, Car.state, Car.title]
    # NOTE: No column_filters/default_sort/formatters to avoid 500s. We'll add later.

admin = Admin(app, engine, authentication_backend=AdminAuth(secret_key=os.environ.get("ADMIN_SECRET", "dev-secret-change-me")))
admin.add_view(CarAdmin)
