# 📤 Upload Image Guide

Panduan lengkap untuk upload gambar di Product Management API.

## 🎯 Overview

API menyediakan endpoint terpisah untuk upload file. Workflow-nya:

1. **Upload file** → Dapat URL
2. **Gunakan URL** di field `gambar` (products) atau `photo_profile` (users)

## 📋 Spesifikasi

- **Format support**: JPG, JPEG, PNG, GIF, WEBP, SVG
- **Max size**: 5MB per file
- **Max files**: 10 files per request (untuk multiple upload)
- **Authentication**: Required (Bearer token)

## 🚀 Cara Upload via Swagger UI

### A. Upload Single Image (untuk User Photo Profile)

1. **Login dulu** via Authorize button
2. Buka endpoint `POST /api/v1/upload/image`
3. Click **"Try it out"**
4. Click **"Choose File"** dan pilih gambar
5. Click **"Execute"**
6. **Copy URL** dari response:
   ```json
   {
     "filename": "profile.jpg",
     "url": "/uploads/abc123.jpg",  ← Copy this
     "size": 102400
   }
   ```
7. **Gunakan URL** saat create/update user di field `photo_profile`

### B. Upload Multiple Images (untuk Product Images)

1. Buka endpoint `POST /api/v1/upload/images`
2. Click **"Try it out"**
3. Click **"Add string item"** untuk setiap file
4. Click **"Choose File"** untuk setiap slot
5. Click **"Execute"**
6. **Copy semua URL** dari response:
   ```json
   {
     "files": [
       {"url": "/uploads/img1.jpg"},
       {"url": "/uploads/img2.jpg"}
     ],
     "count": 2
   }
   ```
7. **Gunakan array URL** saat create/update product:
   ```json
   {
     "gambar": [
       "/uploads/img1.jpg",
       "/uploads/img2.jpg"
     ]
   }
   ```

## 💻 Cara Upload via Code

### 1. Upload Single Image (Python)

```python
import requests

# Login dulu
login_response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={
        "email": "admin@example.com",
        "password": "admin123"
    }
)
token = login_response.json()["access_token"]

# Upload image
with open("profile.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/upload/image",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": f}
    )

image_url = response.json()["url"]
print(f"Image uploaded: {image_url}")

# Gunakan URL untuk create/update user
user_data = {
    "nama": "John Doe",
    "email": "john@example.com",
    "photo_profile": image_url  # ← Use uploaded URL
}
```

### 2. Upload Multiple Images (Python)

```python
import requests

# Upload multiple images
files = [
    ("files", open("image1.jpg", "rb")),
    ("files", open("image2.jpg", "rb")),
    ("files", open("image3.jpg", "rb"))
]

response = requests.post(
    "http://localhost:8000/api/v1/upload/images",
    headers={"Authorization": f"Bearer {token}"},
    files=files
)

# Extract URLs
image_urls = [file["url"] for file in response.json()["files"]]
print(f"Uploaded {len(image_urls)} images")

# Gunakan URLs untuk create product
product_data = {
    "nama_produk": "Laptop Gaming",
    "kategori": "Electronics",
    "harga_satuan": 15000000,
    "stok": 10,
    "gambar": image_urls  # ← Use uploaded URLs
}
```

### 3. Upload via JavaScript/Fetch

```javascript
// Upload single image
async function uploadImage(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/api/v1/upload/image', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  
  const data = await response.json();
  return data.url;
}

// Usage
const fileInput = document.querySelector('input[type="file"]');
const imageUrl = await uploadImage(fileInput.files[0]);

// Create user with uploaded image
await fetch('http://localhost:8000/api/v1/users', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    nama: 'John Doe',
    email: 'john@example.com',
    photo_profile: imageUrl
  })
});
```

### 4. Upload via cURL

```bash
# Upload single image
curl -X POST "http://localhost:8000/api/v1/upload/image" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@/path/to/image.jpg"

# Upload multiple images
curl -X POST "http://localhost:8000/api/v1/upload/images" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "files=@/path/to/image1.jpg" \
  -F "files=@/path/to/image2.jpg" \
  -F "files=@/path/to/image3.jpg"
```

## 📝 Contoh Lengkap: Create Product dengan Images

```bash
# 1. Login
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}' \
  | jq -r '.access_token')

# 2. Upload images
IMAGES=$(curl -X POST "http://localhost:8000/api/v1/upload/images" \
  -H "Authorization: Bearer $TOKEN" \
  -F "files=@laptop1.jpg" \
  -F "files=@laptop2.jpg" \
  | jq -c '[.files[].url]')

# 3. Create product dengan images
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"nama_produk\": \"Laptop Gaming ASUS ROG\",
    \"kategori\": \"Electronics\",
    \"deskripsi\": \"Laptop gaming high-end\",
    \"harga_satuan\": 25000000,
    \"stok\": 5,
    \"gambar\": $IMAGES
  }"
```

## 🗂️ File Storage

- **Lokasi**: `/uploads/` directory
- **Format nama**: `{uuid}.{extension}` (e.g., `abc123def456.jpg`)
- **Akses**: http://localhost:8000/uploads/abc123def456.jpg

## ⚠️ Error Handling

### File Too Large
```json
{
  "detail": "Ukuran file terlalu besar. Maksimal 5MB"
}
```

### Invalid Format
```json
{
  "detail": "Format file tidak didukung. Gunakan: .jpg, .jpeg, .png, .gif, .webp, .svg"
}
```

### Too Many Files
```json
{
  "detail": "Maksimal 10 file per upload"
}
```

### Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

## 🔐 Security Notes

- ✅ File type validation (only images)
- ✅ File size limit (5MB)
- ✅ Unique filename (UUID-based)
- ✅ Authentication required
- ✅ CORS enabled

## 💡 Best Practices

1. **Compress images** sebelum upload untuk performa lebih baik
2. **Validate file size** di client-side sebelum upload
3. **Show preview** sebelum submit form
4. **Handle upload errors** dengan graceful degradation
5. **Store URLs** di database, bukan binary files

## 🎨 Frontend Integration Tips

### React Example

```jsx
import { useState } from 'react';

function ProductForm() {
  const [images, setImages] = useState([]);
  const [uploading, setUploading] = useState(false);

  const handleImageUpload = async (files) => {
    setUploading(true);
    const formData = new FormData();
    
    Array.from(files).forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('/api/v1/upload/images', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });
      
      const data = await response.json();
      const urls = data.files.map(f => f.url);
      setImages(urls);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        multiple
        accept="image/*"
        onChange={(e) => handleImageUpload(e.target.files)}
        disabled={uploading}
      />
      
      {uploading && <p>Uploading...</p>}
      
      <div className="preview">
        {images.map((url, i) => (
          <img key={i} src={url} alt={`Preview ${i}`} />
        ))}
      </div>
    </div>
  );
}
```

## 📚 Related Endpoints

- **Create Product**: `POST /api/v1/products` - Use uploaded image URLs
- **Update Product**: `PUT /api/v1/products/{id}` - Update image URLs
- **Create User**: `POST /api/v1/users` - Use uploaded photo URL
- **Update User**: `PUT /api/v1/users/{id}` - Update photo URL
