# Flask User, Project, and Task API

This project is a RESTful API built using **Flask**, **SQLAlchemy**, and **PostgreSQL** to manage users, projects, and tasks.

---

## ✅ Requirements

- Python 3.9+
- PostgreSQL
- `pipenv` or `virtualenv` (recommended)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

> 💡 If using `pipenv`, you can instead run:
> ```bash
> pipenv shell
> ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🛠️ Database Setup

### 4. Create PostgreSQL Database

```bash
createdb flask_db
```

If needed, modify the default database connection string in `config.py`:

```python
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/flask_db'
```

### 5. Initialize the Database

```bash
flask shell
```

Inside the shell:

```python
from database import db
from app import app

with app.app_context():
    db.create_all()
    exit()
```

### 6. Seed the Database

```bash
python seed.py
```

---

## 🚀 Running the Application

```bash
flask run
```

---

## 📡 API Endpoints

| Method | Endpoint             | Description                |
|--------|----------------------|----------------------------|
| GET    | `/users`             | Get all users              | (supports page and per_page)
| POST   | `/users`             | Create a new user          |
| GET    | `/users/<id>`        | Get a single user          |
| PUT    | `/users/<id>`        | Update user details        |
| DELETE | `/users/<id>`        | Delete a user              |
| GET    | `/projects`          | Get all projects           |
| POST   | `/projects`          | Create a new project       | (supports page and per_page)
| GET    | `/projects/<id>`     | Get a single project       |
| PUT    | `/projects/<id>`     | Update project             |
| DELETE | `/projects/<id>`     | Delete a project           |
| GET    | `/tasks`             | Get all tasks              | (supports page and per_page)
| POST   | `/tasks`             | Create a new task          |
| GET    | `/tasks/<id>`        | Get a single task          |
| PUT    | `/tasks/<id>`        | Update a task              |
| DELETE | `/tasks/<id>`        | Delete a task              |

---

## 📦 Project Structure (example)

```
my-project/
│
├── app.py
├── config.py
├── database.py
├── seed.py
├── requirements.txt
├── models/
│   ├── user.py
│   ├── project.py
│   └── task.py
├── routes/
│   ├── user_routes.py
│   ├── project_routes.py
│   └── task_routes.py
└── README.md
```

---

🧰 Postman Collection
To make testing easier, a Postman collection is provided covering all API endpoints with example requests and payloads.

How to use:
Download the collection JSON file: flask_api_postman_collection.json

Open Postman and import the JSON file via File > Import.

The collection will appear in your workspace with all endpoints organized.

You can run requests directly, modify parameters (like page and per_page for pagination), and test the API easily.

---

## 🧚‍♂️ Testing

You can use tools like [Postman](https://www.postman.com/) or `curl` to test the endpoints.

---

## 📌 Notes

- Ensure PostgreSQL is running before initializing or seeding the database.
- Update `.env` or `config.py` for custom configurations like DB credentials or port settings.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).