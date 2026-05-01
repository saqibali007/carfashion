# CarFashion — Django E-Commerce Setup Guide

## 📁 Project Structure
```
carfashion/
├── carfashion/         ← Django project settings
│   ├── settings.py
│   └── urls.py
├── store/              ← Main app
│   ├── models.py       ← Database models
│   ├── views.py        ← All page logic
│   ├── forms.py        ← Forms
│   ├── admin.py        ← Admin panel config
│   ├── email_utils.py  ← Gmail email functions
│   ├── urls.py         ← URL routes
│   └── templates/store/ ← HTML templates
├── templates/
│   └── base.html       ← Base layout
├── static/store/
│   ├── css/main.css    ← All styles
│   └── js/main.js
├── requirements.txt
└── manage.py
```

---

## 🚀 Setup Instructions

### Step 1: Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create admin superuser
```bash
python manage.py createsuperuser
# Enter username, email, and password when prompted
```

### Step 4: Load sample products
```bash
python manage.py seed_data
```

### Step 5: Run the development server
```bash
python manage.py runserver
```

Now visit: **http://localhost:8000**

Admin panel: **http://localhost:8000/admin/**

---

## 📧 Gmail Email Setup (IMPORTANT)

For order receipt emails, you need to configure Gmail SMTP:

1. Go to your Google Account → Security
2. Enable **2-Step Verification**
3. Go to **App Passwords** → Select app: Mail → Generate
4. Copy the 16-character app password

Edit `carfashion/settings.py`:
```python
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_16_char_app_password'
DEFAULT_FROM_EMAIL = 'CarFashion <your_email@gmail.com>'
```

For testing without email (prints to console):
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## ✅ Features

### Customer Features
- ✅ Register / Login / Logout
- ✅ Browse products by category
- ✅ Search and filter products
- ✅ Product detail with reviews
- ✅ Shopping cart
- ✅ Checkout with shipping address
- ✅ Order placement and history
- ✅ Order receipt to Gmail
- ✅ Home service booking
- ✅ Service booking confirmation email
- ✅ Profile management

### Admin Features (at /admin)
- ✅ Add/Edit/Delete products
- ✅ Update stock in bulk (list_editable)
- ✅ Stock status indicators (Green/Orange/Red)
- ✅ Manage orders and update status
- ✅ View and manage home service bookings
- ✅ Customer management
- ✅ Review moderation

### Products Seeded
- 6 Categories: Lighting, DRLs, Body Kits, Interior, Performance, Wraps
- 18 Products including LED bulbs, DRLs, body kits, seat covers, etc.

---

## 🎨 Theme
Dark automotive theme with red/gold accents — inspired by premium car culture.
Font: Rajdhani (headings) + Inter (body)
