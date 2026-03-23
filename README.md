# Fail Safe Reconfiguration (Django App)

## 📌 Description
This project is a Django-based web application for managing servers and performing fail-safe reconfiguration actions.

It provides a simple web interface to:
- View available servers
- Report compromised hosts
- Trigger backend reconfiguration logic

---

## ⚙️ Requirements

- Python 3.10+
- pip
- virtualenv (recommended)

---

## 📦 Installation

### 1. Clone the repository
git clone https://github.com/LefterisTsipis/fale-safe-reconfiguration.git  
cd fale-safe-reconfiguration  

### 2. Create virtual environment
python -m venv venv  

Activate it:

Windows:  
venv\Scripts\activate  

Linux / Mac:  
source venv/bin/activate  

---

### 3. Install dependencies
pip install -r requirements.txt  

---

## 🗄️ Database Setup

Run migrations:  
python manage.py migrate  

(Optional) Load initial data:  
python manage.py init_data  

---

## ▶️ Run the Project

python manage.py runserver  

Open in browser:  
http://127.0.0.1:8000/  
