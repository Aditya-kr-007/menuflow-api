# MenuFlow — Restaurant Menu REST API

FastAPI serves menu records stored in PostgreSQL through SQLAlchemy 2.0.

## Application structure

| File | Purpose |
| --- | --- |
| `main.py` | FastAPI endpoints that query the database |
| `database.py` | PostgreSQL connection and SQLAlchemy sessions |
| `schema.py` | SQLAlchemy definition of the `menu_items` table |
| `models.py` | Pydantic API response models |
| `.env.example` | Database connection template; copy to `.env` |

Request flow: FastAPI endpoint → SQLAlchemy query → PostgreSQL → JSON response.
Menu records are stored in PostgreSQL and can be managed through pgAdmin or SQL.

## Local setup (PowerShell)

1. Install dependencies:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

2. Start PostgreSQL and create a database using pgAdmin or psql:

   ```powershell
   & 'C:\Program Files\PostgreSQL\18\bin\psql.exe' -U postgres -c 'CREATE DATABASE restaurant_menu;'
   ```

3. Copy `.env.example` to `.env` and set your database connection:

   ```powershell
   Copy-Item .env.example .env
   ```

   ```dotenv
   DATABASE_URL="postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/restaurant_menu"
   ```

   Percent-encode special characters in the username/password (for example, `@`
   becomes `%40`). The `+psycopg` selects the installed PostgreSQL driver.
   Set the database name to match your PostgreSQL database. `.env` is ignored by Git
   so local credentials are not uploaded.
   The database must already exist; the application creates missing tables at startup.

4. Start the API:

   ```powershell
   python -m uvicorn main:app --reload
   ```

Open http://127.0.0.1:8000/docs. The existing routes remain available:
`GET /`, `GET /menu`, `GET /menu?category=chai`, and `GET /menu/{item_id}`.
An empty table returns an empty menu; unknown categories and IDs return 404.
Manage records in PostgreSQL with pgAdmin or SQL; the API remains read only.

Optional setup utilities are documented separately in [scripts/README.md](scripts/README.md).
They are not used by the running API.

Startup uses `Base.metadata.create_all()` to create missing tables. It does not
migrate existing columns; use schema migrations for future table changes.

Connection/session handling follows the
[SQLAlchemy session documentation](https://docs.sqlalchemy.org/en/20/orm/session_basics.html).

