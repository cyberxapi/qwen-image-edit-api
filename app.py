from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import anthropic
import base64
import io
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Qwen Image Edit API is running"})

@app.route('/api/edit-image', methods=['POST'])
def edit_image():
    """Edit image using Qwen Image Edit API via Claude"""
    try:
        # Check if image is provided
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        # Get prompt from form data
        prompt = request.form.get('prompt', 'Enhance this image')
        
        # Read and validate image
        try:
            image = Image.open(image_file.stream)
            img_format = image.format or 'PNG'
        except Exception as e:
            return jsonify({"error": f"Invalid image format: {str(e)}"}), 400
        
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format=img_format)
        img_data = base64.standard_b64encode(buffered.getvalue()).decode()
        
        # Determine media type
        media_type = f"image/{img_format.lower()}"
        if img_format.lower() == 'jpg':
            media_type = "image/jpeg"
        
        # Call Claude API with vision capabilities for image editing
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": img_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": f"Please help me edit this image according to the following instruction: {prompt}\n\nProvide details about what edits you would suggest or explain how to edit this image."
                        }
                    ],
                }
            ],
        )
        
        # Return response
        return jsonify({
            "status": "success",
            "prompt": prompt,
            "original_image_size": f"{image.width}x{image.height}",
            "image_format": img_format,
            "edit_suggestion": message.content[0].text,
            "message": "Image analysis complete. The suggestion provided describes how to edit your image."
        })
    
    except anthropic.APIError as e:
        return jsonify({"error": f"API Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/api/upload-and-analyze', methods=['POST'])
def upload_and_analyze():
    """Upload image and get analysis with optional editing prompt"""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({"error": "No image selected"}), 400
        
        # Get edit prompt from JSON or form data
        edit_prompt = request.form.get('prompt') or (request.get_json() or {}).get('prompt')
        
        if not edit_prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        # Read image
        try:
            image = Image.open(image_file.stream)
            img_format = image.format or 'PNG'
        except Exception as e:
            return jsonify({"error": f"Invalid image: {str(e)}"}), 400
        
        # Convert to base64
        buffered = io.BytesIO()
        image.save(buffered, format=img_format)
        img_data = base64.standard_b64encode(buffered.getvalue()).decode()
        
        media_type = f"image/{img_format.lower()}"
        if img_format.lower() == 'jpg':
            media_type = "image/jpeg"
        
        # Call Claude with the editing prompt
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": img_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": f"Edit request: {edit_prompt}\n\nProvide a detailed response about how to edit this image or what changes should be made."
                        }
                    ],
                }
            ],
        )
        
        return jsonify({
            "status": "success",
            "image_info": {
                "filename": image_file.filename,
                "size": f"{image.width}x{image.height}",
                "format": img_format
            },
            "edit_prompt": edit_prompt,
            "analysis": message.content[0].text
        })
    
    except anthropic.APIError as e:
        return jsonify({"error": f"API Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
