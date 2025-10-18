# Product Management API

Backend API lengkap untuk sistem manajemen produk menggunakan FastAPI dengan clean architecture.

## 🚀 Fitur Utama

- **Authentication & Authorization**
  - JWT-based authentication
  - Role-based access control (Admin & User)
  - OAuth2PasswordBearer implementation
  - Secure password hashing dengan bcrypt

- **User Management** (Admin Only)
  - CRUD operations lengkap
  - Pagination, search, filter, dan sorting
  - Status user (aktif/nonaktif)
  - Profile photo support

- **Product Management**
  - CRUD operations dengan business logic
  - Status otomatis (aktif/nonaktif/menipis)
  - Perhitungan harga setelah diskon
  - Multiple images support
  - Stock tracking dengan threshold
  - Advanced filtering dan sorting

- **File Upload**
  - Single & multiple image upload
  - Format support: JPG, PNG, GIF, WEBP, SVG
  - File size validation (max 5MB)
  - Secure file storage dengan unique names
  - Static file serving

- **Database**
  - PostgreSQL dengan async support
  - SQLAlchemy ORM
  - Auto table creation on startup
  - Connection pooling

## 📁 Struktur Folder

```
evaluation-test-api/
├── app/
│   ├── api/
│   │   ├── deps/
│   │   │   └── auth.py          # Authentication dependencies
│   │   └── routes/
│   │       ├── auth.py          # Auth endpoints
│   │       ├── users.py         # User management endpoints
│   │       ├── products.py      # Product management endpoints
│   │       └── upload.py        # File upload endpoints
│   ├── core/
│   │   ├── config.py            # Application settings
│   │   ├── security.py          # JWT & password utilities
│   │   └── file_handler.py      # File upload utilities
│   ├── database/
│   │   ├── base.py              # SQLAlchemy base
│   │   └── session.py           # Database session
│   ├── models/
│   │   ├── user.py              # User ORM model
│   │   └── product.py           # Product ORM model
│   ├── repositories/
│   │   ├── user_repository.py   # User data access
│   │   └── product_repository.py # Product data access
│   ├── schemas/
│   │   ├── common.py            # Common schemas (pagination, etc)
│   │   ├── auth.py              # Auth schemas
│   │   ├── user.py              # User schemas
│   │   ├── product.py           # Product schemas
│   │   └── upload.py            # Upload schemas
│   ├── services/
│   │   ├── auth_service.py      # Auth business logic
│   │   ├── user_service.py      # User business logic
│   │   └── product_service.py   # Product business logic
│   └── main.py                  # Application entry point
├── .env                         # Environment variables (create from .env.example)
├── .env.example                 # Example environment variables
├── .gitignore
├── requirements.txt             # Python dependencies
└── README.md
```

## 🛠️ Teknologi Stack

- **Python 3.10+**
- **FastAPI** - Modern web framework
- **SQLAlchemy 2.0** - ORM dengan async support
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **python-jose** - JWT implementation
- **passlib** - Password hashing
- **uvicorn** - ASGI server

## ⚙️ Setup & Installation

### 1. Prerequisites

- Python 3.10 atau lebih tinggi
- PostgreSQL 13 atau lebih tinggi
- pip atau poetry untuk package management

### 2. Clone & Install Dependencies

```bash
# Clone repository (atau extract zip)
cd evaluation-test-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# MacOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Database

```bash
# Login ke PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE product_management;

# Create user (optional)
CREATE USER product_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE product_management TO product_user;

# Exit
\q
```

### 4. Environment Configuration

```bash
# Copy example env file
cp .env.example .env

# Edit .env dengan text editor favorit
nano .env
```

**Minimal configuration (.env):**

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/product_management

# JWT Settings
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=Product Management API
DEBUG=True
API_V1_PREFIX=/api/v1

# Admin User
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
ADMIN_NAME=Administrator
```

**⚠️ PENTING:** 
- Ganti `SECRET_KEY` dengan key yang aman (gunakan: `openssl rand -hex 32`)
- Ganti password database sesuai setup PostgreSQL Anda
- Ganti default admin password untuk production

### 5. Run Application

```bash
# Development mode (dengan auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Atau menggunakan Python
python -m app.main
```

Server akan berjalan di: **http://localhost:8000**

**Note:** Database tables akan dibuat otomatis saat aplikasi pertama kali dijalankan.

## 📚 API Documentation

### Swagger UI (Interactive)
Buka browser: **http://localhost:8000/docs**

### ReDoc (Alternative)
Buka browser: **http://localhost:8000/redoc**

## 🔐 Authentication

### Cara Mudah: Gunakan Swagger UI

1. Buka **http://localhost:8000/docs**
2. Klik tombol **"Authorize" 🔒** di pojok kanan atas
3. Masukkan kredensial:
   - **username**: `admin@example.com` (gunakan email)
   - **password**: `admin123`
4. Klik **"Authorize"**
5. Sekarang Anda bisa test semua endpoint yang memerlukan authentication!

### Login via API

**Endpoint:** `POST /api/v1/auth/login`

**Request:**
```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin@example.com",
    "nama": "Administrator",
    "role": "admin",
    "status_user": "aktif"
  }
}
```

### Menggunakan Token

Setiap request yang memerlukan authentication, tambahkan header:

```
Authorization: Bearer <access_token>
```

## 🎯 API Endpoints

### Authentication
- `POST /api/v1/auth/token` - Get OAuth2 token (for Swagger UI)
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/logout` - Logout user

### File Upload
- `POST /api/v1/upload/image` - Upload single image (for user photo)
- `POST /api/v1/upload/images` - Upload multiple images (for product images)

### User Management (Admin Only)
- `POST /api/v1/users` - Create user
- `GET /api/v1/users` - List users (pagination, filter, search, sort)
- `GET /api/v1/users/{id}` - Get user detail
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Product Management
- `POST /api/v1/products` - Create product
- `GET /api/v1/products` - List products (pagination, filter, search, sort)
- `GET /api/v1/products/{id}` - Get product detail
- `PUT /api/v1/products/{id}` - Update product (full)
- `PATCH /api/v1/products/{id}/status` - Update product status only
- `PATCH /api/v1/products/{id}/stock` - Update stock (add/subtract)
- `DELETE /api/v1/products/{id}` - Delete product

## 📝 Contoh Request

### Upload Image

```bash
# Upload single image (for user photo)
curl -X POST "http://localhost:8000/api/v1/upload/image" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.jpg"

# Upload multiple images (for product)
curl -X POST "http://localhost:8000/api/v1/upload/images" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "files=@/path/to/image1.jpg" \
  -F "files=@/path/to/image2.jpg"
```

**Note:** Gunakan URL yang didapat dari response untuk field `photo_profile` (users) atau `gambar` (products).  
**Panduan lengkap:** Lihat [UPLOAD_GUIDE.md](UPLOAD_GUIDE.md)

### Create Product

```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nama_produk": "Laptop ASUS ROG",
    "kategori": "Electronics",
    "deskripsi": "Gaming laptop with RTX 4060",
    "harga_satuan": 15000000,
    "stok_awal": 10,
    "gambar": ["/uploads/abc123.jpg", "/uploads/def456.jpg"],
    "status_produk": "aktif",
    "threshold_stok": 5,
    "diskon": 10.0,
    "rating": 4.5
  }'
```

### List Products with Filters

```bash
curl -X GET "http://localhost:8000/api/v1/products?page=1&limit=10&kategori=Electronics&status=aktif&search=laptop&sort_by=harga_satuan&sort_order=desc" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Stock

```bash
curl -X PATCH "http://localhost:8000/api/v1/products/1/stock" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "adjustment": 5,
    "operation": "subtract"
  }'
```

## 🔄 Business Logic

### Product Status Management

1. **Status Nonaktif:** Produk tidak aktif, tidak cek stok
2. **Status Aktif:** Produk aktif dan tersedia
3. **Status Menipis:** Otomatis muncul jika:
   - Status produk = aktif
   - `threshold_stok` diisi
   - `stok <= threshold_stok`

### Price Calculation

Harga setelah diskon dihitung otomatis:
```python
harga_setelah_diskon = harga_satuan * (1 - diskon / 100)
```

### Stock Operations

- **Add:** Menambah stok
- **Subtract:** Mengurangi stok (validasi: stok tidak boleh negatif)
- Status otomatis recalculate setelah update stok

## 🧪 Testing

### Manual Testing via Swagger UI

1. Buka http://localhost:8000/docs
2. Login menggunakan endpoint `/api/v1/auth/login`
3. Click "Authorize" button
4. Paste token dari response login
5. Test semua endpoints

### Using curl

```bash
# 1. Login
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}' \
  | jq -r '.access_token')

# 2. Get products
curl -X GET "http://localhost:8000/api/v1/products" \
  -H "Authorization: Bearer $TOKEN"
```

## 🗃️ Database Schema

### Users Table
```sql
- id (integer, PK)
- nama (string)
- no_telepon (string)
- email (string, unique)
- password (string, hashed)
- role (enum: admin, user)
- status_user (enum: aktif, nonaktif)
- photo_profile (string, nullable)
- created_at (timestamp)
- updated_at (timestamp)
```

### Products Table
```sql
- id (integer, PK)
- nama_produk (string)
- kategori (string)
- deskripsi (text, nullable)
- harga_satuan (float)
- stok_awal (integer)
- stok (integer)
- gambar (json array)
- status_produk (enum: aktif, nonaktif, menipis)
- threshold_stok (integer, nullable)
- diskon (float, default: 0)
- rating (float, default: 0)
- jumlah_terjual (integer, default: 0)
- created_at (timestamp)
- updated_at (timestamp)
```

## 🚀 Production Deployment

### Environment Variables untuk Production

```env
DEBUG=False
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
SECRET_KEY=<super-secure-key-here>
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### Running with Gunicorn + Uvicorn Workers

```bash
pip install gunicorn

gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Docker (Optional)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t product-api .
docker run -p 8000:8000 --env-file .env product-api
```

## 🐛 Troubleshooting

### Database Connection Error
```
SQLALCHEMY_DATABASE_URI tidak valid
```
**Solusi:** Pastikan PostgreSQL berjalan dan DATABASE_URL di .env sudah benar

### Import Error
```
ModuleNotFoundError: No module named 'app'
```
**Solusi:** Jalankan dari root directory dan pastikan PYTHONPATH sudah benar

### JWT Token Error
```
Could not validate credentials
```
**Solusi:** Token expired atau invalid. Login ulang untuk mendapat token baru

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🤝 Contributing

Silakan buat Pull Request atau Issue jika menemukan bug atau ingin menambah fitur.

## 📄 License

MIT License

## 👤 Author

Product Management API - FastAPI Backend

---

**Default Admin Login:**
- Email: `admin@example.com`
- Password: `admin123`

⚠️ **Jangan lupa ganti password admin untuk production!**
