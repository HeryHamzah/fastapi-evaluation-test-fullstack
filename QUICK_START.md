# Quick Start Guide

Panduan cepat untuk menjalankan Product Management API.

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Git (optional)

## 🚀 4 Langkah Setup

### 1️⃣ Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Install packages
pip install -r requirements.txt
```

### 2️⃣ Setup Database

```bash
# Login ke PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE product_management;
\q
```

### 3️⃣ Configure Environment

```bash
# Copy and edit .env
cp .env.example .env
```

Edit `.env` minimal:
```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/product_management
SECRET_KEY=your-secret-key-here
```

💡 **Generate SECRET_KEY:**
```bash
openssl rand -hex 32
```

### 4️⃣ Start Server

```bash
uvicorn app.main:app --reload
```

**Note:** Tables akan dibuat otomatis saat aplikasi pertama kali dijalankan.

✅ **API Running:** http://localhost:8000

## 🎯 Test API

### 1. Open Swagger UI
http://localhost:8000/docs

### 2. Login
- Click **POST /api/v1/auth/login**
- Try it out
- Use credentials:
  ```json
  {
    "email": "admin@example.com",
    "password": "admin123"
  }
  ```
- Copy the `access_token`

### 3. Authorize
- Click **Authorize** button (🔒)
- Enter: `Bearer <your_token>`
- Click Authorize

### 4. Test Endpoints
Try creating a product:
```json
{
  "nama_produk": "Test Product",
  "kategori": "Electronics",
  "harga_satuan": 100000,
  "stok_awal": 10,
  "status_produk": "aktif"
}
```

## 📱 Quick API Reference

### Authentication
```bash
POST /api/v1/auth/login
POST /api/v1/auth/logout
```

### Users (Admin Only)
```bash
GET    /api/v1/users
POST   /api/v1/users
GET    /api/v1/users/{id}
PUT    /api/v1/users/{id}
DELETE /api/v1/users/{id}
```

### Products
```bash
GET    /api/v1/products
POST   /api/v1/products
GET    /api/v1/products/{id}
PUT    /api/v1/products/{id}
PATCH  /api/v1/products/{id}/status
PATCH  /api/v1/products/{id}/stock
DELETE /api/v1/products/{id}
```

## 🔥 Common Commands

```bash
# Run server
uvicorn app.main:app --reload

# Run on different port
uvicorn app.main:app --reload --port 8080

# Run in production mode (without reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## ⚠️ Troubleshooting

### Port already in use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Database connection error
- Check PostgreSQL is running: `pg_isready`
- Verify DATABASE_URL in .env
- Test connection: `psql -U postgres -d product_management`

### Module not found
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Tables not created
```bash
# Pastikan DATABASE_URL benar, lalu restart aplikasi
# Tables akan dibuat otomatis saat startup
```

## 📖 Next Steps

- Read full [README.md](README.md)
- Explore API at http://localhost:8000/docs
- Review code structure in `app/` directory

## 🆘 Need Help?

Common issues:
1. ✅ Virtual environment activated?
2. ✅ PostgreSQL running?
3. ✅ .env file exists with correct values?
4. ✅ Using correct Python version (3.10+)?

---

**Happy Coding! 🚀**
