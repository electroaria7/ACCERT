from flask import Flask, request, jsonify, send_from_directory, render_template_string
import os
import tempfile
import subprocess
import sys
from werkzeug.utils import secure_filename

# Author: Daeho Chang
# Email: daeho.chang@anl.gov
# Created: June 30, 2025
# Description: Flask server for ACCERT Output Processor

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure the dev directory is in the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload_processor.html')
def upload_processor():
    return send_from_directory('.', 'upload_processor.html')

@app.route('/table_display.html')
def table_display():
    return send_from_directory('.', 'table_display.html')

@app.route('/debug_table.html')
def debug_table():
    return send_from_directory('.', 'debug_table.html')

@app.route('/process_output', methods=['POST'])
def process_output():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(mode='w+b', delete=False, suffix='.out') as temp_file:
            file.save(temp_file.name)
            temp_file_path = temp_file.name
        
        try:
            # Import and run the CSV extractor
            from csv_extractor import extract_table_to_csv
            
            # Process the file
            extract_table_to_csv(temp_file_path)
            
            # Check if the CSV was created
            csv_path = os.path.join(current_dir, 'accel_2214_output_excel.csv')
            if os.path.exists(csv_path):
                return jsonify({
                    'success': True,
                    'filename': 'accel_2214_output_excel.csv',
                    'message': 'File processed successfully'
                })
            else:
                return jsonify({'error': 'CSV file was not created'}), 500
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<filename>')
def serve_file(filename):
    """Serve static files"""
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("Starting ACCERT Output Processor Server...")
    print("Access the application at: http://localhost:3000")
    print("Upload page: http://localhost:3000")
    print("Table display: http://localhost:3000/table_display.html")
    app.run(debug=True, host='0.0.0.0', port=3000) 