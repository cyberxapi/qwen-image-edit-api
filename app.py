from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import base64
import io
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Qwen Image Edit API is running"})

@app.route('/api/edit-image', methods=['POST'])
def edit_image():
    """Edit image using simple image processing (placeholder for Qwen model)"""
    try:
        # Check if image is provided
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        # Get prompt from form data (optional)
        prompt = request.form.get('prompt', 'Enhance this image')
        
        # Read image
        try:
            img = Image.open(image_file)
        except Exception:
            return jsonify({"error": "Invalid image format"}), 400
        
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Basic image enhancement (placeholder for actual Qwen editing)
        # In production, this would call Qwen Image Edit API
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        edited_img = enhancer.enhance(1.2)
        
        # Save edited image to bytes
        img_io = io.BytesIO()
        edited_img.save(img_io, 'JPEG', quality=95)
        img_io.seek(0)
        
        # Return response
        return jsonify({
            "status": "success",
            "message": "Image editing completed",
            "prompt_used": prompt,
            "image_size": f"{edited_img.width}x{edited_img.height}",
            "notes": "This uses basic image enhancement. For actual Qwen model integration, provide API credentials."
        })
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/upload-and-analyze', methods=['POST'])
def upload_and_analyze():
    """Upload image and get analysis with optional editing prompt"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        image_file = request.files['image']
        prompt = request.form.get('prompt', 'Analyze this image')
        
        if image_file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        # Read and validate image
        try:
            img = Image.open(image_file)
        except Exception:
            return jsonify({"error": "Invalid image format"}), 400
        
        img_format = img.format
        img_size = img.size
        
        # Return analysis
        return jsonify({
            "status": "success",
            "image_format": img_format,
            "image_size": f"{img_size[0]}x{img_size[1]}",
            "prompt_received": prompt,
            "message": "Image uploaded and analyzed successfully. To integrate Qwen Image Edit, provide API credentials in environment."
        })
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
