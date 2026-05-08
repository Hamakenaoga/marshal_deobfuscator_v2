from flask import Blueprint, request, jsonify, render_template
from core.marshal_decoder import decode_python_file
from core.binary_analyzer import decode_binary_file

decode_bp = Blueprint('decode', __name__)

@decode_bp.route('/')
def index():
    return render_template('index.html')

@decode_bp.route('/decode', methods=['POST'])
def decode_route():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "Empty filename"}), 400

        file_data = file.read()
        
        if file.filename.lower().endswith('.py'):
            content = file_data.decode('utf-8', errors='replace')
            result = decode_python_file(content, file.filename)
        else:
            result = decode_binary_file(file_data, file.filename)

        result['timestamp'] = __import__('datetime').datetime.utcnow().isoformat()
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
```