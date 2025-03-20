from flask import Flask, request, jsonify
import os
import csv
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Configuration
PV_DIR = "/shivam_PV_dir"

@app.route('/calculate-product', methods=['POST'])
def calculate_product():
    app.logger.info("Received request to /calculate-product")
    data = request.get_json()
    
    # Validate input
    if not data or 'file' not in data:
        app.logger.error("Invalid JSON input - missing file parameter")
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400
    
    if 'product' not in data:
        app.logger.error("Invalid JSON input - missing product parameter")
        return jsonify({"file": data.get('file'), "error": "Invalid JSON input."}), 400
    
    file_name = data['file']
    product = data['product']
    
    # Check if file exists
    file_path = os.path.join(PV_DIR, file_name)
    if not os.path.exists(file_path):
        app.logger.error(f"File not found: {file_name}")
        return jsonify({"file": file_name, "error": "File not found."}), 404
    
    try:
        # Read and parse the CSV file
        with open(file_path, 'r') as f:
            content = f.read().strip()
            lines = content.split('\n')
            
            # Validate CSV format
            if len(lines) < 1:
                app.logger.error(f"Invalid CSV format: {file_name}")
                return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
            
            # Calculate sum for the specified product
            total = 0
            for i, line in enumerate(lines):
                # Skip header line
                if i == 0:
                    continue
                    
                parts = [part.strip() for part in line.split(',')]
                if len(parts) != 2:
                    app.logger.error(f"Invalid CSV format in line {i+1}: {line}")
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
                
                try:
                    if parts[0] == product:
                        total += int(parts[1])
                except ValueError:
                    app.logger.error(f"Invalid number format in line {i+1}: {parts[1]}")
                    return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
            
            app.logger.info(f"Calculation complete for {product} in {file_name}: sum = {total}")
            return jsonify({"file": file_name, "sum": total}), 200
    
    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}")
        return jsonify({"file": file_name, "error": "Error processing the file."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081) 