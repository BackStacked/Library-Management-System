# 📚 Library Management System API

This is a **FastAPI-based Library Management System** with user authentication, role-based access (Admin/User), and book borrowing functionality.

---

## 🔑 Authentication

### Signup (Register User/Admin)

**POST** `/users/signup`

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "mypassword",
  "admin_secret": "supersecretadminkey" // optional → only if registering as admin
}
```

➡️ Returns created user details (without password).

### Login

**POST** `/users/login`

- Uses `form-data` with fields:

  - `username` → user email
  - `password` → user password

➡️ Returns JWT token:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

---

## 👤 Users

### List Users (Admin Only)

**GET** `/users/`

- Requires Bearer Token.
- Only `admin` role can access.

### Promote User to Admin

**PUT** `/users/promote/{user_id}`

- Requires Bearer Token.
- Admin only.
- Promotes a user to `admin` role.

---

## 📖 Books

### Add Book (Admin Only)

**POST** `/books/`

```json
{
  "title": "Book Title",
  "author": "Author Name",
  "isbn": "123456"
}
```

➡️ Returns created book details.

### List Books

**GET** `/books/?skip=0&limit=10`
➡️ Returns paginated list of books.

### Get Book by ID

**GET** `/books/{book_id}`
➡️ Returns book details.

### Update Book (Admin Only)

**PUT** `/books/{book_id}`

```json
{
  "title": "New Title",
  "author": "New Author",
  "isbn": "654321"
}
```

➡️ Updates and returns book.

### Delete Book (Admin Only)

**DELETE** `/books/{book_id}`
➡️ Deletes book and returns confirmation.

---

## 📕 Borrow / Return

### Borrow a Book

**POST** `/borrow/borrow/{book_id}`

- Requires Bearer Token.
- Marks a book as borrowed by the current user.

### Return a Book

**POST** `/borrow/return/{book_id}`

- Requires Bearer Token.
- Marks a book as returned.

---

## ⚙️ Roles & Access Control

- **Admin** → Can manage books & users.
- **User** → Can borrow/return books, view books.

---

## ⚡ Environment Setup

This project requires environment variables.
Copy the example file and rename it:

```bash
cp .env.example .env
```

Then, update `.env` with your values (e.g., database URL, JWT secret, etc.).

## ▶️ Running the Project

```bash
uvicorn app.main:app --reload
```

API docs available at:

- Swagger UI → `http://127.0.0.1:8000/docs`
- ReDoc → `http://127.0.0.1:8000/redoc`

---

## 🧪 Testing the Project

This project includes **pytest-based tests**.

Run all tests:

```bash
pytest -v
```

If pytest command is not recognized, try:

```bash
python -m pytest -v
```

# or

```bash
python3 -m pytest -v
```

Run only user tests:

```bash
pytest app/tests/test_users.py -v
```

Run with live logs:

```bash
pytest -s
```

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.  
Copyright © 2025 **Backstacked**
