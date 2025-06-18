from flask import Flask, request, jsonify, send_file
import os
import uuid
from zoom_faces import zoom_on_faces

app = Flask(__name__)
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/zoom', methods=['POST'])
def zoom_video():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    unique_id = uuid.uuid4().hex
    input_filename = f"zoom_input_{unique_id}.mp4"
    output_filename = f"zoom_output_{unique_id}.mp4"
    input_path = os.path.join(OUTPUT_DIR, input_filename)
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    file.save(input_path)

    try:
        zoom_on_faces(input_path, output_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return send_file(output_path, as_attachment=True)

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "Zoom server running"}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
