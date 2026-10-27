# MenuFlow API

MenuFlow is a lightweight FastAPI service for serving restaurant menu data from PostgreSQL. It exposes a simple read-only API for browsing menu items by category or item ID, with SQLAlchemy handling database access and Pydantic models shaping the API responses.

## Overview

This project is designed for a restaurant menu catalog and is intentionally simple and easy to run locally. The API reads from a PostgreSQL table named `menu_items`, and the application automatically creates the table if it does not already exist.

### Key capabilities

- Browse all menu items
- Filter menu items by category
- Fetch a single item by ID
- Return clean JSON responses through FastAPI
- Use PostgreSQL as the persistent data source
- Keep the API read-only from the application layer

## Tech stack

- Python 3.x
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- psycopg
- Pydantic
- dotenv

## Project structure

```text
.
├── .env.example            # Example environment configuration
├── .gitignore              # Git exclusions
├── database.py             # PostgreSQL connection and session setup
├── main.py                 # FastAPI app and route definitions
├── models.py               # Pydantic response models
├── requirements.txt        # Python dependencies
├── schema.py               # SQLAlchemy model for menu_items
├── README.md               # Project documentation
├── scripts/                # Optional utilities and helper scripts
└── .venv/                  # Local virtual environment (not tracked in Git)
```

## Application flow

`FastAPI endpoint -> SQLAlchemy query -> PostgreSQL -> JSON response`

This keeps the API logic thin while letting the database handle persisted menu data.

## Local setup (PowerShell)

### 1. Clone the repository and create a virtual environment

```powershell
git clone https://github.com/Aditya-kr-007/menuflow-api.git
cd menuflow-api
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 2. Start PostgreSQL and create a database

If you are using PostgreSQL locally, create a database such as `restaurant_menu`:

```powershell
& 'C:\Program Files\PostgreSQL\18\bin\psql.exe' -U postgres -c 'CREATE DATABASE restaurant_menu;'
```

If you prefer a GUI tool, you can also create the database using pgAdmin.

### 3. Configure environment variables

Copy the example environment file and update the database URL:

```powershell
Copy-Item .env.example .env
```

Then set the value in `.env`:

```dotenv
DATABASE_URL="postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/restaurant_menu"
```

Notes:

- Replace `YOUR_PASSWORD` with your local PostgreSQL password.
- If your username or password contains special characters, percent-encode them (for example, `@` becomes `%40`).
- The database should already exist before the app starts.
- The app creates missing tables automatically on startup.

### 4. Run the API

```powershell
python -m uvicorn main:app --reload
```

The application will start in development mode and expose the API at:

- http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

## API endpoints

### Root endpoint

```http
GET /
```

Returns a simple welcome message.

### Get all menu items

```http
GET /menu
```

Optional query parameter:

```http
GET /menu?category=chai
```

### Get a single menu item

```http
GET /menu/{item_id}
```

Example:

```http
GET /menu/1
```

## Example response

```json
{
  "status": "success",
  "count": 2,
  "items": [
    {
      "id": 1,
      "name": "Masala Chai",
      "category": "chai",
      "price": 35.0,
      "description": "Aromatic tea with milk and spices.",
      "available": true
    }
  ]
}
```

## Behavior and conventions

- `GET /menu` returns all items in order by ID.
- `GET /menu?category=...` filters by category and returns 404 if no items match.
- `GET /menu/{item_id}` returns 404 if the ID does not exist.
- An empty table returns an empty menu list.
- The API is currently read-only from the application perspective; menu data is managed directly in PostgreSQL or via SQL tools.

## Notes for development

- Startup creates missing tables with `Base.metadata.create_all()`.
- This project does not implement schema migrations; for future table changes, use a migration tool or manual SQL updates.
- The app follows the standard SQLAlchemy session pattern for database access.

## Optional utilities

This project includes optional helper scripts documented in [scripts/README.md](scripts/README.md). Those scripts are not required for the running API itself.

## License

This project is intended for local development and learning use. Add a license file if you plan to publish or share it more broadly.
