# Personal Portfolio – Backend (Django + Django REST Framework)

This is the backend API for **Bishwajit Karmaker's** portfolio website. It provides RESTful endpoints for managing dynamic content such as Projects, Experience, Education, and Skills. It also includes user authentication (JWT), password reset via email, and contact form submission.

---

## 🛠 Tech Stack

- **Framework**: Django 4.x
- **API**: Django REST Framework (DRF)
- **Auth**: Simple JWT (custom login, password reset, forgot username)
- **Email**: Resend + Zoho Mail
- **Database**: PostgreSQL (Railway)
- **CORS**: Configured for frontend domain
- **Deployment**: Railway (automatic builds)

---

## 📁 Project Structure

portfolio_backend/
├── auth/ # Custom auth views (login, reset, forgot username)
├── projects/ # Project models, serializers, views
├── education/ # Education models, views
├── experience/ # Experience models, views
├── skills/ # Skill models, views
├── contact/ # Contact form handling
├── settings.py # Env, CORS, email config, etc.
├── urls.py # All endpoint routes
└── ...


---

## 🔐 Authentication & Authorization

- JWT token-based auth using **SimpleJWT**
- Custom login view returns access & refresh tokens
- Protected routes (add/edit/delete) only for authenticated users
- Public read-only access to all portfolio content
- Password reset:
  - Generates token/uid and sends email with frontend reset link
  - Uses Resend API + Zoho Mail for delivery
- Forgot Username:
  - Sends the username to user's email without exposing on frontend

---

## 📬 Contact Form

- Route: `POST /api/contact-form/`
- Validates and sends message via Resend to `contact@abdullahstack.com`
- Includes subject, message, and user info
- Stores nothing in the database
- CORS allowed for frontend requests only

---

## 🔗 Endpoints Overview

| Model       | Public Read | Auth Add/Edit/Delete |
|-------------|-------------|------------------------|
| Projects    | ✅          | ✅                    |
| Experience  | ✅          | ✅                    |
| Education   | ✅          | ✅                    |
| Skills      | ✅          | ✅                    |
| Contact     | ✅ (POST)   | ✅ (open for visitors) |
| Auth (JWT)  | ✅          | ✅                    |

---

## 🌍 Deployment

- **Platform**: [Railway](https://railway.app/)
- **Database**: PostgreSQL hosted on Railway
- **CI/CD**: Auto-deploy from GitHub
- **Live API**:  https://web-production-9824e.up.railway.app/api

---

## ⚙️ Environment Variables (`.env`)

```env
SECRET_KEY=your_django_secret
DEBUG=False
ALLOWED_HOSTS=*
DATABASE_URL=your_postgres_url
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.zoho.eu
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=contact@abdullahstack.com
EMAIL_HOST_PASSWORD=your_zoho_app_password
RESEND_API_KEY=your_resend_key
FRONTEND_URL=https://www.abdullahstack.com

🚀 How to Run Locally

# 1. Clone the repo and cd into backend
git clone https://github.com/your-username/portfoliosite-backend.git
cd portfoliosite-backend

# 2. Create virtual environment & install
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Create .env file and apply migrations
touch .env
# (fill it with the vars above)
python manage.py migrate

# 4. Run server
python manage.py runserver

🙌 Credits

    - Authentication via SimpleJWT

    - Email via Resend API + Zoho SMTP

    - Deployed with Railway

    - Maintained and built by Bishwajit Karmaker

Crafted with 🔥 by Bishwajit Karmaker

📃 License

This codebase is for personal and educational purposes only. Do not reuse without permission.