# Qwen Image Edit API - Complete Developer Guide

## 🚀 Quick Start

**Live API URL:** `https://qwen-image-edit-api.onrender.com`

### 1. Health Check
```bash
curl https://qwen-image-edit-api.onrender.com/api/health
```

**Response:**
```json
{
  "message": "Qwen Image Edit API is running",
  "status": "ok"
}
```

---

## 📋 API Overview

This is a Flask-based REST API for image editing and analysis. Upload images via POST requests with optional prompts to get editing suggestions and image analysis.

**Base URL:** `https://qwen-image-edit-api.onrender.com`

**Supported Image Formats:** JPEG, PNG, BMP, GIF, WebP

---

## 🔌 API Endpoints

### 1. Health Check Endpoint

**Endpoint:** `GET /api/health`

**Description:** Verify API is running and accessible.

**Example:**
```bash
curl https://qwen-image-edit-api.onrender.com/api/health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "message": "Qwen Image Edit API is running"
}
```

---

### 2. Edit Image Endpoint

**Endpoint:** `POST /api/edit-image`

**Description:** Upload an image and get editing suggestions with optional prompt.

**Parameters:**
- `image` (file, **required**): Image file to edit
- `prompt` (string, optional): Editing instruction (default: "Enhance this image")

**Example with cURL:**
```bash
curl -X POST https://qwen-image-edit-api.onrender.com/api/edit-image \
  -F "image=@photo.jpg" \
  -F "prompt=Make the image brighter and add more contrast"
```

**Example with Python (requests):**
```python
import requests

url = "https://qwen-image-edit-api.onrender.com/api/edit-image"

with open('photo.jpg', 'rb') as f:
    files = {'image': f}
    data = {'prompt': 'Enhance colors and brightness'}
    response = requests.post(url, files=files, data=data)
    
print(response.json())
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Image editing completed",
  "image_size": "640x640",
  "prompt_used": "Make the image brighter",
  "notes": "Basic image enhancement applied"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "No image provided"
}
```

---

### 3. Upload & Analyze Endpoint

**Endpoint:** `POST /api/upload-and-analyze`

**Description:** Upload an image with a detailed prompt for comprehensive analysis.

**Parameters:**
- `image` (file, **required**): Image file to analyze
- `prompt` (string, **required**): Detailed editing/analysis instruction

**Example with cURL:**
```bash
curl -X POST https://qwen-image-edit-api.onrender.com/api/upload-and-analyze \
  -F "image=@photo.jpg" \
  -F "prompt=Remove background and add a gradient background"
```

**Example with Python (requests):**
```python
import requests

url = "https://qwen-image-edit-api.onrender.com/api/upload-and-analyze"

with open('photo.jpg', 'rb') as f:
    files = {'image': f}
    data = {'prompt': 'Analyze the image and suggest improvements'}
    response = requests.post(url, files=files, data=data)
    
print(response.json())
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "image_format": "JPEG",
  "image_size": "1280x1280",
  "prompt_received": "Remove background and add gradient",
  "message": "Image uploaded and analyzed successfully"
}
```

---

## 📦 Integration Examples

### JavaScript/Node.js Integration

```javascript
// Using fetch API
const editImage = async (imageFile, prompt) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('prompt', prompt);
  
  const response = await fetch(
    'https://qwen-image-edit-api.onrender.com/api/edit-image',
    {
      method: 'POST',
      body: formData
    }
  );
  
  const result = await response.json();
  console.log(result);
  return result;
};

// Usage
const input = document.querySelector('input[type="file"]');
const prompt = 'Enhance brightness and contrast';
await editImage(input.files[0], prompt);
```

### React Example

```jsx
import React, { useState } from 'react';

function ImageEditor() {
  const [file, setFile] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData();
    formData.append('image', file);
    formData.append('prompt', prompt);

    try {
      const response = await fetch(
        'https://qwen-image-edit-api.onrender.com/api/edit-image',
        {
          method: 'POST',
          body: formData
        }
      );
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files[0])}
        required
      />
      <input
        type="text"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter editing prompt..."
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Processing...' : 'Edit Image'}
      </button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </form>
  );
}

export default ImageEditor;
```

### Python Integration

```python
import requests
from pathlib import Path

def edit_image_api(image_path, prompt=None):
    """
    Send image to API for editing
    
    Args:
        image_path (str): Path to image file
        prompt (str): Optional editing instruction
    
    Returns:
        dict: API response
    """
    api_url = "https://qwen-image-edit-api.onrender.com/api/edit-image"
    
    with open(image_path, 'rb') as f:
        files = {'image': f}
        data = {'prompt': prompt or 'Enhance this image'}
        
        response = requests.post(api_url, files=files, data=data)
        response.raise_for_status()
        
    return response.json()

# Usage
result = edit_image_api('photo.jpg', 'Make it brighter')
print(result)
```

---

## ⚙️ Local Development

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

```bash
# Clone repository
git clone https://github.com/cyberxapi/qwen-image-edit-api.git
cd qwen-image-edit-api

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

**Server runs at:** `http://localhost:5000`

### Testing Locally

```bash
# Health check
curl http://localhost:5000/api/health

# Edit image
curl -X POST http://localhost:5000/api/edit-image \
  -F "image=@test_image.jpg" \
  -F "prompt=Enhance colors"

# Upload and analyze
curl -X POST http://localhost:5000/api/upload-and-analyze \
  -F "image=@test_image.jpg" \
  -F "prompt=Remove background"
```

---

## 🌐 Deployment on Render

The API is already deployed on Render's free plan.

**Live URL:** `https://qwen-image-edit-api.onrender.com`

### Deploy Your Own Copy

1. **Fork the repository** on GitHub
2. **Go to** [render.com](https://render.com)
3. **Create New** → **Web Service**
4. **Connect GitHub** and select your forked repo
5. **Configure:**
   - **Name:** `qwen-image-edit-api`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Free Plan:** Yes (Recommended for testing)
6. **Deploy**

### Environment Variables

No additional environment variables required for basic functionality. The API works out-of-the-box on Render's free plan.

---

## 📊 API Response Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Missing required parameters or invalid image |
| 404 | Not Found | Endpoint not found |
| 500 | Server Error | Internal server error |

---

## 📈 Rate Limits

Render's free plan has reasonable rate limits. For production use, consider upgrading to a paid plan.

**Recommendations:**
- Free Plan: ~50 requests/hour
- For higher volume: Upgrade to Render's paid plans

---

## 🔒 Features

✅ Simple image upload via POST
✅ Optional prompt-based editing suggestions
✅ CORS enabled for cross-origin requests
✅ JSON responses
✅ Error handling with HTTP status codes
✅ Free deployment on Render
✅ No API key required
✅ Automatic image format detection

---

## 🛠️ Troubleshooting

### Image Upload Fails
- Ensure file is a valid image (JPEG, PNG, etc.)
- Check file size (should be < 10MB)
- Use correct content-type header

### 404 Error
- Check the API base URL: `https://qwen-image-edit-api.onrender.com`
- Verify endpoint path is correct
- Ensure trailing slashes match

### CORS Issues
- The API has CORS enabled for all origins
- If still experiencing issues, check browser console for errors

### Timeout Errors
- Free Render instances may spin down after inactivity
- First request after spin-down may take 30-50 seconds
- Upgrade to paid plan for guaranteed uptime

---

## 📚 Project Structure

```
qwen-image-edit-api/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment config
├── API_USAGE.md          # This file
└── README.md             # Project overview
```

---

## 🔄 How It Works

1. **Client** sends POST request with image file and optional prompt
2. **API** receives and validates the image format
3. **Processing** applies basic image enhancement
4. **Response** returns status and image information
5. **Client** receives JSON response with results

---

## 📝 License

MIT License - Feel free to use, modify, and distribute

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📞 Support

**Issues?** Create a GitHub issue or contact the maintainer.

**Repository:** https://github.com/cyberxapi/qwen-image-edit-api
