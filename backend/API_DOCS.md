# Notes Management API – Backend Documentation

Base URL: `http://localhost:5000/api`

---

## Authentication

### Register

**Endpoint**

- `POST /auth/register`

**Request body (JSON)**

```json
{
  "name": "Alice",
  "email": "alice@example.com",
  "password": "secret123"
}
```

**Example curl**

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "email": "alice@example.com",
    "password": "secret123"
  }'
```

**Responses**

- `201 Created` – user registered
- `400 Bad Request` – validation errors or email already exists
- `500 Internal Server Error` – could not write user to Supabase (if enabled)

---

### Login

**Endpoint**

- `POST /auth/login`

**Request body (JSON)**

```json
{
  "email": "alice@example.com",
  "password": "secret123"
}
```

**Example curl**

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "secret123"
  }'
```

**Successful response (200)**

```json
{
  "message": "Login successful",
  "token": "JWT_TOKEN_HERE",
  "user": {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "role": "user"
  }
}
```

Use this token in the `Authorization` header:

```text
Authorization: Bearer JWT_TOKEN_HERE
```

---

## Notes

All Notes endpoints require a valid JWT token in the `Authorization` header.

### Create Note

**Endpoint**

- `POST /notes`

**Request body**

```json
{
  "title": "My First Note",
  "content": "This is the content"
}
```

**Example curl**

```bash
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer JWT_TOKEN_HERE" \
  -d '{
    "title": "My First Note",
    "content": "This is the content"
  }'
```

**Responses**

- `201 Created` – note created
- `400 Bad Request` – missing title/content
- `401 Unauthorized` – invalid/missing token

---

### List Notes (with pagination & search)

**Endpoint**

- `GET /notes`

**Query params**

- `page` (optional, default `1`)
- `page_size` (optional, default from config, max from config)
- `search` (optional, search by title, case-insensitive)

**Example curl**

```bash
curl "http://localhost:5000/api/notes?page=1&page_size=10&search=first" \
  -H "Authorization: Bearer JWT_TOKEN_HERE"
```

**Successful response (200)**

```json
{
  "notes": [
    {
      "id": 1,
      "title": "My First Note",
      "content": "This is the content",
      "user_id": 1
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total": 1
  }
}
```

Normal users see only their own notes. Admins can see all notes.

---

### Get Single Note

**Endpoint**

- `GET /notes/:id`

**Example curl**

```bash
curl http://localhost:5000/api/notes/1 \
  -H "Authorization: Bearer JWT_TOKEN_HERE"
```

**Responses**

- `200 OK` – returns note
- `403 Forbidden` – user not allowed to access this note
- `404 Not Found` – note not found

---

### Update Note

**Endpoint**

- `PUT /notes/:id`

**Request body**

```json
{
  "title": "Updated Title",
  "content": "Updated content"
}
```

**Example curl**

```bash
curl -X PUT http://localhost:5000/api/notes/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer JWT_TOKEN_HERE" \
  -d '{
    "title": "Updated Title",
    "content": "Updated content"
  }'
```

**Responses**

- `200 OK` – note updated
- `400 Bad Request` – invalid input
- `403 Forbidden` – cannot update someone else’s note (unless admin)
- `404 Not Found` – note not found

---

### Delete Note

**Endpoint**

- `DELETE /notes/:id`

**Example curl**

```bash
curl -X DELETE http://localhost:5000/api/notes/1 \
  -H "Authorization: Bearer JWT_TOKEN_HERE"
```

**Responses**

- `200 OK` – note deleted
- `403 Forbidden` – cannot delete someone else’s note (unless admin)
- `404 Not Found` – note not found

