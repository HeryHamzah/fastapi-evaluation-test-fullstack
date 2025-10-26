# 📚 API Documentation

## 📋 Table of Contents

- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Error Handling](#error-handling)

---

## 🎯 Overview

Product Management API untuk integrasi aplikasi web & mobile dengan JWT authentication.

**Features:**

- 🔐 JWT Authentication dengan role-based access
- 👥 User Management (Admin only)
- 📦 Product Management dengan filter & sort
- 📤 Upload gambar produk
- 💰 Auto-calculate harga setelah diskon

**Roles:**

- **Admin**: Full access
- **User**: Access products & upload

---

## 🌐 Base URL

```
http://127.0.0.1:8000/api/v1
```

**Default Admin:**

```
Email: admin@example.com
Password: admin123
```

---

## 🔐 Authentication

### Flow

1. Login dengan email & password → dapat `access_token`
2. Include token di header semua request: `Authorization: Bearer <token>`

### Token Expiration

- Access Token: 30 menit
- Refresh Token: 7 hari

---

## 🚀 API Endpoints

## 1. Authentication

### POST /auth/login

Login dan dapatkan access token.

**Request:**

```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

**Response (200):**

```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "admin@example.com",
    "nama": "Administrator",
    "role": "admin"
  }
}
```

**cURL:**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}'
```

---

### POST /auth/logout

Logout user (requires token).

**Headers:** `Authorization: Bearer <token>`

**Response (200):**

```json
{
  "message": "Logout berhasil"
}
```

---

### GET /auth/me

Get current authenticated user.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**

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

---

## 2. User Management (Admin Only)

### POST /users

Create user baru.

**Headers:** `Authorization: Bearer <admin_token>`

**Request:**

```json
{
  "nama": "John Doe",
  "no_telepon": "081234567890",
  "email": "john@example.com",
  "password": "password123",
  "role": "user",
  "status_user": "aktif",
  "photo_profile": "http://127.0.0.1:8000/uploads/photo.jpg"
}
```

**Fields:**

- `nama` (required): Full name
- `no_telepon` (required): Phone (10-20 chars)
- `email` (required): Email (unique)
- `password` (required): Min 6 chars
- `role` (optional): admin/user (default: user)
- `status_user` (optional): aktif/nonaktif (default: aktif)
- `photo_profile` (optional): Photo URL

**Response (201):**

```json
{
  "id": 2,
  "nama": "John Doe",
  "no_telepon": "081234567890",
  "email": "john@example.com",
  "role": "user",
  "status_user": "aktif",
  "photo_profile": "http://127.0.0.1:8000/uploads/photo.jpg",
  "created_at": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T10:00:00"
}
```

---

### GET /users

Get all users dengan pagination.

**Headers:** `Authorization: Bearer <admin_token>`

**Query Params:**

- `page` (default: 1): Page number
- `limit` (default: 10, max: 100): Items per page
- `status`: Filter (aktif/nonaktif)
- `search`: Search by name
- `sort_by` (default: nama): Sort field (nama/email/created_at)
- `sort_order` (default: asc): asc/desc

**Example:**

```
GET /users?page=1&limit=10&status=aktif&search=john&sort_by=nama&sort_order=asc
```

**Response (200):**

```json
{
  "items": [
    {
      "id": 1,
      "nama": "Administrator",
      "email": "admin@example.com",
      "no_telepon": "0000000000",
      "role": "admin",
      "status_user": "aktif",
      "photo_profile": null
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

---

### GET /users/{user_id}

Get user by ID.

**Headers:** `Authorization: Bearer <admin_token>`

**Response (200):** Same as create response

---

### PUT /users/{user_id}

Update user (all fields optional).

**Headers:** `Authorization: Bearer <admin_token>`

**Request:**

```json
{
  "nama": "John Updated",
  "status_user": "nonaktif"
}
```

**Response (200):** Updated user object

---

### DELETE /users/{user_id}

Delete user.

**Headers:** `Authorization: Bearer <admin_token>`

**Response (200):**

```json
{
  "message": "User berhasil dihapus"
}
```

---

## 3. Product Management

### POST /products

Create produk baru.

**Headers:** `Authorization: Bearer <token>`

**Request:**

```json
{
  "nama_produk": "Laptop ASUS ROG",
  "kategori": "Electronics",
  "deskripsi": "Gaming laptop with RTX 4060",
  "harga_satuan": 15000000.0,
  "stok_awal": 10,
  "gambar": [
    "http://127.0.0.1:8000/uploads/laptop-1.jpg",
    "http://127.0.0.1:8000/uploads/laptop-2.jpg"
  ],
  "status_produk": "aktif",
  "threshold_stok": 5,
  "diskon": 10.0,
  "rating": 4.5,
  "jumlah_terjual": 0
}
```

**Fields:**

- `nama_produk` (required): Product name
- `kategori` (required): Category
- `deskripsi` (optional): Description
- `harga_satuan` (required): Price (> 0)
- `stok_awal` (required): Initial stock (>= 0)
- `gambar` (optional): Array of image URLs
- `status_produk` (optional): aktif/nonaktif/menipis (default: aktif)
- `threshold_stok` (optional): Min stock alert
- `diskon` (optional): Discount % 0-100 (default: 0)
- `rating` (optional): Rating 0-5 (default: 0)
- `jumlah_terjual` (optional): Units sold (default: 0)

**Response (201):**

```json
{
  "id": 1,
  "nama_produk": "Laptop ASUS ROG",
  "kategori": "Electronics",
  "deskripsi": "Gaming laptop with RTX 4060",
  "harga_satuan": 15000000.0,
  "stok_awal": 10,
  "stok": 10,
  "gambar": ["http://127.0.0.1:8000/uploads/laptop-1.jpg"],
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

**Notes:**

- `harga_setelah_diskon` auto-calculated: `harga_satuan * (1 - diskon/100)`
- Status auto "menipis" if `stok <= threshold_stok`
- Upload images first via `/upload/images` endpoint

---

### GET /products

Get all products dengan pagination.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**

- `page` (default: 1): Page number
- `limit` (default: 10, max: 100): Items per page
- `kategori`: Filter by category
- `status`: Filter (aktif/nonaktif/menipis)
- `search`: Search by product name
- `sort_by` (default: nama_produk): nama_produk/harga_satuan/stok/kategori
- `sort_order` (default: asc): asc/desc

**Example:**

```
GET /products?page=1&limit=20&kategori=Electronics&status=aktif&search=laptop&sort_by=harga_satuan&sort_order=desc
```

**Response (200):**

```json
{
  "items": [
    {
      "id": 1,
      "nama_produk": "Laptop ASUS ROG",
      "kategori": "Electronics",
      "deskripsi": "Gaming laptop with RTX 4060, 16GB RAM, 512GB SSD",
      "harga_satuan": 15000000.0,
      "stok": 10,
      "status_produk": "aktif",
      "diskon": 10.0,
      "rating": 4.5,
      "jumlah_terjual": 0,
      "harga_setelah_diskon": 13500000.0,
      "gambar": ["http://127.0.0.1:8000/uploads/laptop-1.jpg"]
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10,
  "pages": 1
}
```

---

### GET /products/{product_id}

Get product by ID.

**Headers:** `Authorization: Bearer <token>`

**Response (200):** Full product object

---

### PUT /products/{product_id}

Update product (all fields optional).

**Headers:** `Authorization: Bearer <token>`

**Request:**

```json
{
  "nama_produk": "Laptop ASUS ROG Updated",
  "harga_satuan": 16000000.0,
  "diskon": 15.0
}
```

**Response (200):** Updated product object

---

### PATCH /products/{product_id}/status

Update status only.

**Headers:** `Authorization: Bearer <token>`

**Request:**

```json
{
  "status_produk": "nonaktif"
}
```

**Response (200):** Updated product object

---

### PATCH /products/{product_id}/stock

Update stock (add/subtract).

**Headers:** `Authorization: Bearer <token>`

**Request:**

```json
{
  "adjustment": 5,
  "operation": "add"
}
```

**Operations:**

- `add`: Tambah stock
- `subtract`: Kurangi stock (validate cukup)

**Response (200):** Updated product object

---

### DELETE /products/{product_id}

Delete product.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**

```json
{
  "message": "Produk berhasil dihapus"
}
```

---

## 4. File Upload

### POST /upload/image

Upload single image.

**Headers:**

- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Form Data:**

- `file`: Image file

**Supported:** JPG, JPEG, PNG, GIF, WEBP, SVG (Max: 5MB)

**Response (201):**

```json
{
  "filename": "laptop.jpg",
  "url": "http://127.0.0.1:8000/uploads/laptop_1234567890.jpg",
  "size": 245678
}
```

**cURL:**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/upload/image" \
  -H "Authorization: Bearer <token>" \
  -F "file=@/path/to/image.jpg"
```

---

### POST /upload/images

Upload multiple images (max 10).

**Headers:**

- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Form Data:**

- `files`: Multiple image files

**Response (201):**

```json
{
  "files": [
    {
      "filename": "product-1.jpg",
      "url": "http://127.0.0.1:8000/uploads/product-1_1234567890.jpg",
      "size": 245678
    },
    {
      "filename": "product-2.jpg",
      "url": "http://127.0.0.1:8000/uploads/product-2_1234567891.jpg",
      "size": 198765
    }
  ],
  "count": 2
}
```

**cURL:**

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/upload/images" \
  -H "Authorization: Bearer <token>" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg"
```

---

## 📦 Data Models

### User

```typescript
{
  id: number;
  nama: string;
  no_telepon: string;
  email: string;
  role: "admin" | "user";
  status_user: "aktif" | "nonaktif";
  photo_profile: string | null;
  created_at: datetime;
  updated_at: datetime;
}
```

### Product

```typescript
{
  id: number
  nama_produk: string
  kategori: string
  deskripsi: string | null
  harga_satuan: number
  stok_awal: number
  stok: number
  gambar: string[]
  status_produk: "aktif" | "nonaktif" | "menipis"
  threshold_stok: number | null
  diskon: number
  rating: number
  jumlah_terjual: number
  harga_setelah_diskon: number  // calculated
  created_at: datetime
  updated_at: datetime
}
```

---

## ❌ Error Handling

### Status Codes

- `200` OK
- `201` Created
- `400` Bad Request
- `401` Unauthorized (invalid/missing token)
- `403` Forbidden (insufficient permissions)
- `404` Not Found
- `422` Validation Error
- `500` Server Error

### Error Response

```json
{
  "detail": "Error message"
}
```

### Validation Error

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## 💡 Best Practices

### 1. Upload Flow

```
1. Upload image → GET url
2. Use url in product/user creation
```

### 2. Authentication

```
1. Login once → store access_token
2. Include token in all requests
3. Handle 401 → re-login
```

### 3. Pagination

```
Start with limit=10, increase if needed
Use search & filters to reduce data
```

### 4. Error Handling

```typescript
try {
  const response = await api.request();
  return response.data;
} catch (error) {
  if (error.status === 401) {
    // Re-authenticate
  } else if (error.status === 422) {
    // Show validation errors
  }
}
```

---

## 💻 Client Implementation Examples

### Flutter/Dart

```dart
class ApiService {
  final String baseUrl = 'http://127.0.0.1:8000/api/v1';
  String? accessToken;

  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      accessToken = data['access_token'];
      return data;
    }
    throw Exception('Login failed');
  }

  Future<List<Product>> getProducts({int page = 1, int limit = 10}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/products?page=$page&limit=$limit'),
      headers: {'Authorization': 'Bearer $accessToken'},
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return (data['items'] as List)
          .map((item) => Product.fromJson(item))
          .toList();
    }
    throw Exception('Failed to load products');
  }
}
```

### React Native/TypeScript

```typescript
class ApiService {
  private baseUrl = "http://127.0.0.1:8000/api/v1";
  private accessToken: string | null = null;

  async login(email: string, password: string) {
    const response = await fetch(`${this.baseUrl}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    this.accessToken = data.access_token;
    return data;
  }

  async getProducts(page = 1, limit = 10) {
    const response = await fetch(
      `${this.baseUrl}/products?page=${page}&limit=${limit}`,
      {
        headers: { Authorization: `Bearer ${this.accessToken}` },
      }
    );

    return await response.json();
  }
}
```

---

## 🔗 Additional Resources

- **Interactive API Docs:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **Health Check:** http://127.0.0.1:8000/health

---

**Created:** January 2024  
**Version:** 1.0.0  
**Base URL:** http://127.0.0.1:8000/api/v1
