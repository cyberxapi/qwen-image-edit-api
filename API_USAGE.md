# Qwen Image Edit API - Complete Guide

## Overview

This is a Flask-based REST API that integrates with Claude's vision capabilities to edit and analyze images. The API receives images via POST requests with optional prompts and returns image editing suggestions.

## API Endpoints

### 1. Health Check Endpoint

**GET** `/api/health`

Simple health check to verify API is running.

**Response:**
```json
{
  "status": "ok",
  "message": "Qwen Image Edit API is running"
}
```

### 2. Edit Image Endpoint

**POST** `/api/edit-image`

Upload an image and get editing suggestions.

**Parameters:**
- `image` (file, required): Image file (PNG, JPG, JPEG, etc.)
- `prompt` (string, optional): Editing instruction (default: "Enhance this image")

**Example Request with cURL:**
```bash
curl -X POST http://localhost:5000/api/edit-image \
  -F "image=@/path/to/image.jpg" \
  -F "prompt=Make the image brighter and add more contrast"
```

**Response:**
```json
{
  "status": "success",
  "prompt": "Make the image brighter and add more contrast",
  "original_image_size": "1920x1080",
  "image_format": "JPEG",
  "edit_suggestion": "To make this image brighter and add more contrast, you can: 1) Increase brightness/exposure by 20-30%...",
  "message": "Image analysis complete. The suggestion provided describes how to edit your image."
}
```

### 3. Upload and Analyze Endpoint

**POST** `/api/upload-and-analyze`

Upload an image with a required prompt for detailed analysis.

**Parameters:**
- `image` (file, required): Image file
- `prompt` (string, required): Detailed editing instruction

**Example Request with cURL:**
```bash
curl -X POST http://localhost:5000/api/upload-and-analyze \
  -F "image=@/path/to/image.jpg" \
  -F "prompt=Remove the background and add a gradient background"
```

**Response:**
```json
{
  "status": "success",
  "image_info": {
    "filename": "image.jpg",
    "size": "1920x1080",
    "format": "JPEG"
  },
  "edit_prompt": "Remove the background and add a gradient background",
  "analysis": "To remove the background and add a gradient: 1) Use background removal tools..."
}
```

## How It Works

1. Client sends a POST request with image and optional prompt
2. Server receives and validates the image
3. Image is converted to base64 for API transmission
4. Claude's vision model analyzes the image with the provided prompt
5. Model returns detailed editing suggestions
6. API responds with analysis and recommendations

## Local Testing

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/cyberxapi/qwen-image-edit-api.git
cd qwen-image-edit-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Locally

1. Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

2. Run the Flask app:
```bash
python app.py
```

3. Server will start at `http://localhost:5000`

### Test the API

```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test image editing
curl -X POST http://localhost:5000/api/edit-image \
  -F "image=@test_image.jpg" \
  -F "prompt=Enhance colors"
```

## Deployment on Render

### Steps:

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create a new "Web Service"
4. Connect your GitHub repository
5. Configure environment variables:
   - `ANTHROPIC_API_KEY`: Your Claude API key
6. Deploy!

### Render Configuration

The `render.yaml` file contains all deployment settings:
- Python version: 3.11
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Port: 5000

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Request successful
- `400 Bad Request`: Missing required parameters or invalid image
- `500 Internal Server Error`: API error or server issue

## Rate Limiting

The free Anthropic API tier has rate limits. Plan accordingly for production use.

## API Cost

Each image edit request uses Claude's vision API, which has pricing. Check [Anthropic's pricing page](https://www.anthropic.com/pricing) for current rates.

## Future Enhancements

- Actual image editing (currently provides suggestions)
- Batch processing
- Image caching
- Advanced filtering options
- WebSocket for real-time processing

## License

MIT License
