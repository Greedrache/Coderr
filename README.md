# Coderr Backend

Coderr is a backend for a freelancer developer platform. This Django project provides a REST API
to connect frontend and backend, managing all necessary functionalities for users, projects, and tasks.

---

## Features

- User registration and login
- Create and manage freelancer profiles
- Create, update, and delete projects
- Assign freelancers to projects
- RESTful API structure

---

## Tech Stack

- Python 3.14+
- Django 6.0.3
- Django REST Framework 3.16.1
- SQLite (development) / other DBs as needed

---

## Setup (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/Greedrache/Coderr .
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**cmd:**
```cmd
venv\Scripts\activate
```

**Linux / Mac:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create migrations

```bash
python manage.py makemigrations
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Start the development server

```bash
python manage.py runserver
```

Server runs at: http://127.0.0.1:8000/

---

## Optional

**Create a superuser:**
```bash
python manage.py createsuperuser
```

**Deactivate the virtual environment:**
```bash
deactivate
```

---

## Troubleshooting

- If you have activation issues in PowerShell:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
- If migrations are missing: run `python manage.py migrate`
