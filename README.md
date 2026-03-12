# Notes Management API

A full‑stack notes application with a Flask backend and React frontend. It supports user registration/login, JWT authentication, role‑based access control (user/admin), notes CRUD, pagination and title search.

---

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy, MySQL, JWT (PyJWT), python-dotenv
- **Frontend**: React, React Router, Axios, Webpack dev server

---

## Folder Structure

```text
backend/
  app.py
  config.py
  requirements.txt
  .env.example
  API_DOCS.md
  supabase_schema.sql
  models/
    user_model.py
    note_model.py
  routes/
    auth_routes.py
    notes_routes.py
  middleware/
    auth_middleware.py
  utils/
    jwt_utils.py

frontend/
  package.json
  webpack.config.js
  public/
    index.html
  src/
    index.js
    App.js
    styles.css
    services/
      api.js
    components/
      Login.js
      Register.js
      Dashboard.js
      CreateNote.js
      EditNote.js
```

---

## Backend Setup

### 1. Create and configure environment

From the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` and set your values:

- `SECRET_KEY` – Flask secret key
- `JWT_SECRET_KEY` – JWT signing secret
- `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` – MySQL connection
- `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` – required if you want `/api/auth/register` to also insert users into your Supabase `public.users` table

### 2. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Create database tables

Make sure your MySQL database (e.g. `notes_db`) exists, then run Python to create tables:

```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
... 
>>> exit()
```

### 4. Run the backend server

```bash
cd backend
python app.py
```

The backend will run on `http://localhost:5000`.

---

## Frontend Setup

From the `frontend/` directory:

```bash
cd frontend
npm install
npm start
```

The frontend will run on `http://localhost:3000` and will call the backend at `http://localhost:5000/api`.

---

## API Overview

Base URL: `http://localhost:5000/api`

### Authentication

- `POST /auth/register` – register a new user
- `POST /auth/login` – login and receive a JWT token

Use the token in the `Authorization` header:

```text
Authorization: Bearer JWT_TOKEN_HERE
```

### Notes

All notes endpoints require a valid JWT:

- `POST /notes` – create a note
- `GET /notes` – list notes (supports `page`, `page_size`, `search` query params)
- `GET /notes/:id` – get a specific note
- `PUT /notes/:id` – update a note
- `DELETE /notes/:id` – delete a note

**Role rules**

- **user**: can create, read, update, delete only their own notes
- **admin**: can view all notes and delete any note

More detailed examples (with curl) are available in `backend/API_DOCS.md`.

---

## Example Requests

### Register

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "email": "alice@example.com",
    "password": "secret123"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "secret123"
  }'
```

### Create Note

```bash
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer JWT_TOKEN_HERE" \
  -d '{
    "title": "My first note",
    "content": "Hello world"
  }'
```

### List Notes (with pagination & search)

```bash
curl "http://localhost:5000/api/notes?page=1&page_size=10&search=first" \
  -H "Authorization: Bearer JWT_TOKEN_HERE"
```

