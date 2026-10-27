"""Optional, one-time import of the original menu into an empty database."""

import json
from pathlib import Path

from sqlalchemy import select

from schema import MenuItemRecord
from database import Base, SessionLocal, engine


def init_db():
    Base.metadata.create_all(bind=engine)


def seed_menu() -> int:
    init_db()
    with SessionLocal.begin() as session:
        if session.scalar(select(MenuItemRecord.id).limit(1)) is not None:
            print("Menu already contains data; no rows were changed.")
            return 0
        rows = json.loads(Path(__file__).with_name("seed_menu.json").read_text(encoding="utf-8"))
        # Let PostgreSQL allocate IDs so its sequence remains correct for new rows.
        session.add_all(
            MenuItemRecord(**{key: value for key, value in row.items() if key != "id"})
            for row in rows
        )
    print(f"Imported {len(rows)} menu items.")
    return len(rows)


if __name__ == "__main__":
    seed_menu()
