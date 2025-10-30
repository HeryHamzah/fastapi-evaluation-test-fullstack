# API Usage Examples

Contoh lengkap penggunaan semua endpoint API.

## 🔐 Authentication

### Login via Swagger UI (Recommended for Testing)

1. **Buka Swagger UI**: http://localhost:8000/docs
2. **Klik tombol "Authorize" 🔒** di pojok kanan atas
3. **Masukkan kredensial:**
   - **username**: `admin@example.com` (masukkan email di field username)
   - **password**: `admin123`
4. **Klik "Authorize"**
5. Sekarang semua endpoint yang memerlukan auth sudah bisa diakses!

**Note:** Field "username" di Authorize dialog sebenarnya menerima **email**.

### Login via API (JSON)

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123"
  }'
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

### OAuth2 Token Endpoint (for Swagger UI)

Endpoint ini digunakan otomatis oleh Swagger UI saat Anda klik tombol "Authorize".

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=admin@example.com&password=admin123'
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Logout

```bash
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Current User

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**

```json
{
  "id": 1,
  "nama": "Administrator",
  "no_telepon": "0000000000",
  "email": "admin@example.com",
  "role": "admin",
  "status_user": "aktif",
  "photo_profile": null,
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

## 📤 File Upload

### Upload Single Image

Upload satu gambar untuk user photo profile:

```bash
curl -X POST "http://localhost:8000/api/v1/upload/image" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/profile.jpg"
```

**Response:**

```json
{
  "filename": "profile.jpg",
  "url": "/uploads/abc123def456.jpg",
  "size": 102400
}
```

### Upload Multiple Images

Upload beberapa gambar sekaligus untuk product images:

```bash
curl -X POST "http://localhost:8000/api/v1/upload/images" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "files=@/path/to/image1.jpg" \
  -F "files=@/path/to/image2.jpg" \
  -F "files=@/path/to/image3.jpg"
```

**Response:**

```json
{
  "files": [
    {
      "filename": "image1.jpg",
      "url": "/uploads/abc123.jpg",
      "size": 204800
    },
    {
      "filename": "image2.jpg",
      "url": "/uploads/def456.jpg",
      "size": 153600
    },
    {
      "filename": "image3.jpg",
      "url": "/uploads/ghi789.jpg",
      "size": 184320
    }
  ],
  "count": 3
}
```

**Workflow:**

1. Upload image(s) dulu
2. Dapatkan URL dari response
3. Gunakan URL tersebut di field `photo_profile` (users) atau `gambar` (products)

**Supported formats:** JPG, JPEG, PNG, GIF, WEBP, SVG  
**Max size:** 5MB per file  
**Max files:** 10 files per request

**📖 Panduan lengkap:** Lihat [UPLOAD_GUIDE.md](UPLOAD_GUIDE.md)

## 👥 User Management (Admin Only)

### Create User

```bash
curl -X POST "http://localhost:8000/api/v1/users" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "John Doe",
    "no_telepon": "081234567890",
    "email": "john@example.com",
    "password": "password123",
    "role": "user",
    "status_user": "aktif",
    "photo_profile": "/uploads/abc123.jpg"
  }'
```

### List Users with Filters

```bash
# Basic list
curl -X GET "http://localhost:8000/api/v1/users?page=1&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# With filters
curl -X GET "http://localhost:8000/api/v1/users?page=1&limit=10&status=aktif&search=john&sort_by=nama&sort_order=asc" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "nama": "John Doe",
      "email": "john@example.com",
      "no_telepon": "081234567890",
      "role": "user",
      "status_user": "aktif",
      "photo_profile": "https://example.com/photo.jpg",
      "created_at": "2024-01-01T10:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

### Get User by ID

```bash
curl -X GET "http://localhost:8000/api/v1/users/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update User

```bash
curl -X PUT "http://localhost:8000/api/v1/users/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nama": "John Updated",
    "status_user": "nonaktif"
  }'
```

### Delete User

```bash
curl -X DELETE "http://localhost:8000/api/v1/users/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📦 Product Management

### Create Product

```bash
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nama_produk": "Laptop ASUS ROG Strix",
    "kategori": "Electronics",
    "deskripsi": "Gaming laptop with RTX 4060, 16GB RAM, 512GB SSD",
    "harga_satuan": 15000000,
    "stok_awal": 10,
    "gambar": [
      "/uploads/abc123.jpg",
      "/uploads/def456.jpg"
    ],
    "status_produk": "aktif",
    "threshold_stok": 5,
    "diskon": 10.0,
    "rating": 4.5,
    "jumlah_terjual": 0
  }'
```

**Response:**

```json
{
  "id": 1,
  "nama_produk": "Laptop ASUS ROG Strix",
  "kategori": "Electronics",
  "deskripsi": "Gaming laptop with RTX 4060, 16GB RAM, 512GB SSD",
  "harga_satuan": 15000000.0,
  "stok_awal": 10,
  "stok": 10,
  "gambar": [
    "https://example.com/laptop1.jpg",
    "https://example.com/laptop2.jpg"
  ],
  "status_produk": "aktif",
  "threshold_stok": 5,
  "diskon": 10.0,
  "rating": 4.5,
  "jumlah_terjual": 0,
  "harga_setelah_diskon": 13500000.0,
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

### List Products with Filters

```bash
# Basic list
curl -X GET "http://localhost:8000/api/v1/products?page=1&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Filter by category
curl -X GET "http://localhost:8000/api/v1/products?kategori=Electronics" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Filter by status
curl -X GET "http://localhost:8000/api/v1/products?status=aktif" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Search by name
curl -X GET "http://localhost:8000/api/v1/products?search=laptop" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Combined filters with sorting
curl -X GET "http://localhost:8000/api/v1/products?page=1&limit=10&kategori=Electronics&status=aktif&search=laptop&sort_by=harga_satuan&sort_order=desc" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response:**

```json
{
  "items": [
    {
      "id": 1,
      "nama_produk": "Laptop ASUS ROG Strix",
      "kategori": "Electronics",
      "deskripsi": "Gaming laptop with RTX 4060, 16GB RAM, 512GB SSD",
      "harga_satuan": 15000000.0,
      "stok": 10,
      "status_produk": "aktif",
      "diskon": 10.0,
      "rating": 4.5,
      "jumlah_terjual": 0,
      "harga_setelah_diskon": 13500000.0,
      "gambar": ["https://example.com/laptop1.jpg"]
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

### Get Product by ID

```bash
curl -X GET "http://localhost:8000/api/v1/products/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Product (Full Update)

```bash
curl -X PUT "http://localhost:8000/api/v1/products/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nama_produk": "Laptop ASUS ROG Strix Updated",
    "harga_satuan": 14000000,
    "diskon": 15.0
  }'
```

### Update Product Status Only

```bash
# Set to nonaktif
curl -X PATCH "http://localhost:8000/api/v1/products/1/status" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status_produk": "nonaktif"
  }'

# Set to aktif
curl -X PATCH "http://localhost:8000/api/v1/products/1/status" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status_produk": "aktif"
  }'
```

### Update Product Stock

```bash
# Add stock
curl -X PATCH "http://localhost:8000/api/v1/products/1/stock" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "adjustment": 5,
    "operation": "add"
  }'

# Subtract stock
curl -X PATCH "http://localhost:8000/api/v1/products/1/stock" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "adjustment": 3,
    "operation": "subtract"
  }'
```

### Delete Product

```bash
curl -X DELETE "http://localhost:8000/api/v1/products/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🐍 Python Examples

### Using requests library

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "admin@example.com",
        "password": "admin123"
    }
)
data = response.json()
token = data["access_token"]

# Headers with token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Create product
product_data = {
    "nama_produk": "Test Product",
    "kategori": "Electronics",
    "harga_satuan": 100000,
    "stok_awal": 10,
    "status_produk": "aktif"
}

response = requests.post(
    f"{BASE_URL}/products",
    json=product_data,
    headers=headers
)
print(response.json())

# List products
response = requests.get(
    f"{BASE_URL}/products?page=1&limit=10",
    headers=headers
)
print(response.json())

# Update stock
response = requests.patch(
    f"{BASE_URL}/products/1/stock",
    json={"adjustment": 5, "operation": "add"},
    headers=headers
)
print(response.json())
```

## 📱 JavaScript/TypeScript Examples

### Using fetch API

```javascript
const BASE_URL = "http://localhost:8000/api/v1";

// Login
async function login() {
  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: "admin@example.com",
      password: "admin123",
    }),
  });

  const data = await response.json();
  return data.access_token;
}

// Get products
async function getProducts(token) {
  const response = await fetch(`${BASE_URL}/products?page=1&limit=10`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return await response.json();
}

// Create product
async function createProduct(token, productData) {
  const response = await fetch(`${BASE_URL}/products`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(productData),
  });

  return await response.json();
}

// Usage
const token = await login();
const products = await getProducts(token);
console.log(products);
```

## 🔄 Complete Workflow Example

### Bash Script

```bash
#!/bin/bash

API="http://localhost:8000/api/v1"

# 1. Login
echo "🔐 Logging in..."
TOKEN=$(curl -s -X POST "$API/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}' \
  | jq -r '.access_token')

echo "✅ Token received: ${TOKEN:0:20}..."

# 2. Create product
echo "📦 Creating product..."
PRODUCT=$(curl -s -X POST "$API/products" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nama_produk": "Test Product",
    "kategori": "Electronics",
    "harga_satuan": 100000,
    "stok_awal": 10,
    "status_produk": "aktif",
    "threshold_stok": 5
  }')

PRODUCT_ID=$(echo $PRODUCT | jq -r '.id')
echo "✅ Product created with ID: $PRODUCT_ID"

# 3. Get product details
echo "🔍 Getting product details..."
curl -s -X GET "$API/products/$PRODUCT_ID" \
  -H "Authorization: Bearer $TOKEN" | jq

# 4. Update stock
echo "📊 Updating stock..."
curl -s -X PATCH "$API/products/$PRODUCT_ID/stock" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"adjustment": 5, "operation": "subtract"}' | jq

# 5. List products
echo "📋 Listing products..."
curl -s -X GET "$API/products?page=1&limit=5" \
  -H "Authorization: Bearer $TOKEN" | jq

echo "✨ Done!"
```

## 📊 Query Parameters Reference

### User List

- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)
- `status`: Filter by status (`aktif` or `nonaktif`)
- `search`: Search by name
- `sort_by`: Sort field (`nama`, `email`, `created_at`)
- `sort_order`: Sort order (`asc` or `desc`)

### Product List

- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)
- `kategori`: Filter by category
- `status`: Filter by status (`aktif`, `nonaktif`, or `menipis`)
- `search`: Search by product name
- `sort_by`: Sort field (`updated_at`, `nama_produk`, `harga_satuan`, `stok`, `kategori`) — default: `updated_at`
- `sort_order`: Sort order (`asc` or `desc`) — default: `desc`

**Default behavior:** Tanpa parameter `sort_by/sort_order`, daftar produk diurutkan berdasarkan `updated_at desc` (terbaru dulu).

---

**💡 Tip:** Gunakan `jq` untuk format JSON yang lebih readable di terminal!

```bash
# Install jq
# Mac: brew install jq
# Ubuntu: sudo apt install jq
```
