# 🍽️ Starlight Restaurant — Django Food Ordering Website

Modern restaurant ordering web application built with **Django + PostgreSQL + AJAX**.
Customers can browse menu, filter categories, add items to cart and place orders in real time.

---

## 🌐 Features

* 🧾 Dynamic food menu by categories
* 🛒 Add to cart without page reload (AJAX)
* ➕ Quantity increase/decrease buttons
* 💰 Clean money formatting (5 000 so'm)
* 📦 Checkout & order creation
* 📊 Admin dashboard (Jazzmin UI)
* 🧑‍🍳 Recipes section
* 📱 Responsive modern UI
* 🔔 Toast notifications
* 🧠 Session based cart system

---

## 🛠️ Tech Stack

### Backend

* Python 3.10
* Django 5
* PostgreSQL
* Django Sessions
* Custom template filters

### Frontend

* HTML5
* CSS3 (modular structure)
* Vanilla JavaScript (Fetch API)
* AJAX cart updates

### Admin

* Django Admin
* Jazzmin Dashboard UI


## ⚙️ Installation

### 1️⃣ Clone repository

git clone https://github.com/YOUR_USERNAME/restaurant-website.git
cd restaurant-website

---

### 2️⃣ Create virtual environment

python -m venv venv
venv\Scripts\activate

---

### 3️⃣ Install dependencies

pip install -r requirements.txt

---

### 4️⃣ Configure database (PostgreSQL)

Edit settings.py:

DATABASES = {
"default": {
"ENGINE": "django.db.backends.postgresql",
"NAME": "restaurant",
"USER": "postgres",
"PASSWORD": "your_password",
"HOST": "localhost",
"PORT": "5432",
}
}

---

### 5️⃣ Migrate & run

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Open in browser:
http://127.0.0.1:8000

Admin panel:
http://127.0.0.1:8000/admin

---

## 🧠 How Cart Works

* Cart stored in session
* AJAX requests update quantity
* Floating cart auto refreshes
* No page reload needed

---

## 🚀 Future Improvements

* Online payment (Click / Payme / Stripe)
* Order status tracking
* User accounts
* Delivery map integration
* Multi-language support

---

## 👨‍💻 Author

Your Name
Full-stack Django Developer

GitHub:
https://github.com/YOUR_USERNAME

---

## 📄 License

This project is open-source and free to use for educational purposes.
