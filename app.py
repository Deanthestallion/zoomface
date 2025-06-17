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
        return send_file(output_path, mimetype="video/mp4", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
