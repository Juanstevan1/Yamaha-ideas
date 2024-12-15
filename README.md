# Yamaha Ideas 🚀

Yamaha Ideas is a Django-based project designed to manage ideas, users, and notifications efficiently. This project is built with modern tools and practices to ensure scalability and maintainability.

---

## 📋 Table of Contents

1. [Project Description](#-project-description)
2. [Features](#-features)
3. [Technologies Used](#-technologies-used)
4. [Prerequisites](#-prerequisites)
5. [Installation Guide](#-installation-guide)
6. [Usage](#-usage)
7. [Technical Documentation](#-technical-documentation)
8. [Authors](#-authors)

---

## 📖 Project Description

Yamaha Ideas is a platform where users can:
- Share and manage ideas collaboratively.
- Receive notifications for updates or actions.
- Manage users and roles through an intuitive interface.

This project leverages Django for backend development, PostgreSQL for database management, and Bootstrap for responsive design.

---

## ✨ Features

- **Idea Management**: Create, update, and delete ideas with ease.
- **User Notifications**: Automatic notifications for relevant actions.
- **Scalable Architecture**: Designed for both local and production environments.

---

## 🛠 Technologies Used

| Technology    | Description                  |
|---------------|------------------------------|
| Django        | Web framework for the backend. |
| PostgreSQL    | Database management system.  |
| Bootstrap     | Frontend styling and design. |
| pgAdmin       | PostgreSQL database management tool. |
| AWS RDS       | Managed PostgreSQL database service in the cloud.|

---

## ✅ Prerequisites

Before starting, ensure you have the following installed:

- **Python** (version 3.10 or higher)
- **PostgreSQL** (version 14 or higher)
- **Git** (latest version)
- **pip** (Python package manager)
- (Optional) **Docker** (if deploying with containers)

---

## 📦 Installation Guide

### 1️⃣ Clone the repository
```bash
https://github.com/Juanstevan1/Yamaha-ideas.git
cd yamaha-ideas
```

### 2️⃣ Create a virtual environment
```bash
python -m venv env
# For Linux/MacOS
source env/bin/activate
# For Windows
env\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure the database
Update the `DATABASES` section in `settings.py` with your PostgreSQL credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5️⃣ Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create a superuser
```bash
python manage.py createsuperuser
```

### 7️⃣ Run the server
```bash
python manage.py runserver
```

---

## 🚀 Usage

1. Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000).
2. Access the admin panel at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) using the superuser credentials.
3. Start creating and managing ideas, users, and notifications.

---

## 🗂 Technical Documentation

### Directory Structure

- **/yamaha_ideas**: Main project folder containing settings and configurations.
- **/apps**: Contains all Django apps (`ideas`, `users`, etc.).
- **/templates**: HTML templates for the frontend.
- **/static**: Static files (CSS, JS, images).

---

## 👩‍💻 Authors

- **Melissa Guerra Pastrana** - [GitHub Profile](https://github.com/your-profile)
- **Sanny Valery Agualimpia Renteria** - [GitHub Profile](https://github.com/sanvalar)
- **Gonzalo Isaza** - [GitHub Profile](https://github.com/chaloisaza)
- **Luis Gabriel Pacheco** - [GitHub Profile](https://github.com/collaborator-profile)
- **Juan Esteban Garcia Galvis** - [GitHub Profile](https://github.com/Juanstevan1)

---

