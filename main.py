from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from schema import MenuItemRecord
from database import Base, SessionLocal, engine
from models import MenuItem, MenuResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        engine.dispose()


app = FastAPI(
    title="MenuFlow — Restaurant Menu REST API",
    description="Restaurant menu REST API built with FastAPI, SQLAlchemy, and PostgreSQL.",
    version="0.1.0",
    lifespan=lifespan,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DatabaseSession = Annotated[Session, Depends(get_db)]


@app.get("/")
def root():
    return {"message": "Welcome to the Chai Point API!"}


@app.get("/menu", response_model=MenuResponse)
def get_menu(
    db: DatabaseSession,
    category: str | None = Query(None, description="Filter by chai, snacks or combos"),
):
    statement = select(MenuItemRecord).order_by(MenuItemRecord.id)
    if category:
        statement = statement.where(MenuItemRecord.category == category.lower())
    items = db.scalars(statement).all()
    if category and not items:
        raise HTTPException(status_code=404, detail=f"No item found in category: {category}")
    return MenuResponse(count=len(items), items=items)


@app.get("/menu/{item_id}", response_model=MenuItem)
def get_item(item_id: int, db: DatabaseSession):
    item = db.get(MenuItemRecord, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Menu item with id {item_id} not found")
    return item
