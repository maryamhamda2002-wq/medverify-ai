import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Configured CORS to allow seamless traffic from your local Live Server instance
CORS(app, resources={r"/api/*": {
    "origins": "*",
    "methods": ["POST", "GET", "OPTIONS"],
    "allow_headers": ["Content-Type"]
}})

# Simulated Database for SDG 3 Pharmaceutical Product Validation
MEDICINE_DATABASE = {
    "panadol": {
        "name": "Panadol (Paracetamol)",
        "purpose": "Analgesic & Antipyretic",
        "sdg3_alignment": "Provides access to safe, essential affordable management for fever and pain.",
        "verified": True,
        "standard_dosage": "1-2 tablets every 4 to 6 hours as needed. Do not exceed 8 tablets in 24 hours."
    },
    "calpol": {
        "name": "Calpol (Paracetamol Pediatric)",
        "purpose": "Infant/Child Pain & Fever Relief",
        "sdg3_alignment": "Supports target 3.2: Reducing neonatal and under-5 child mortality by ensuring precise child dosage safety.",
        "verified": True,
        "standard_dosage": "Dosage depends on child weight and age. Consult the packaging matrix or a pediatrician."
    },
    "brufen": {
        "name": "Brufen (Ibuprofen)",
        "purpose": "Non-Steroidal Anti-inflammatory Drug (NSAID)",
        "sdg3_alignment": "Alleviates inflammatory conditions and pain safely when properly tracked.",
        "verified": True,
        "standard_dosage": "1 tablet (200mg-400mg) 3 times a day post meals. Maximum 1200mg/day unless directed."
    }
}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint to verify backend operational state."""
    return jsonify({"status": "healthy", "sdg_goal": "Goal 3: Good Health & Well-being"}), 200

@app.route('/api/verify-package', methods=['POST', 'OPTIONS'])
def verify_package():
    """
    Simulates Computer Vision analysis of pharmaceutical packaging.
    Parses incoming package labels to prevent medical errors and counterfeit distribution.
    """
    # Handle pre-flight browser checks automatically
    if request.method == 'OPTIONS':
        return jsonify({"success": True}), 200
        
    if 'image' not in request.files:
        return jsonify({"error": "No packaging image provided for validation"}), 400
    
    file = request.files['image']
    filename = file.filename.lower()
    
    # Analyze the filename or image payload metadata to determine the package type
    matched_key = None
    for medicine in MEDICINE_DATABASE.keys():
        if medicine in filename:
            matched_key = medicine
            break
            
    if matched_key:
        product_info = MEDICINE_DATABASE[matched_key]
        return jsonify({
            "success": True,
            "detected_label": matched_key.upper(),
            "data": product_info,
            "message": "Packaging verified authentic. Matches global pharmaceutical standards."
        }), 200
    else:
        return jsonify({
            "success": False,
            "detected_label": "UNKNOWN / UNVERIFIED",
            "message": "Warning: Packaging could not be recognized. Risk of counterfeit or unapproved batch.",
            "sdg3_alignment": "Critical Warning: Target 3.b warning triggered. Substandard or counterfeit medical products endanger health safety."
        }), 200

if __name__ == '__main__':
    # CHANGED: Switched host from 127.0.0.1 to localhost to bind cleanly with Live Server requests
    app.run(host='localhost', port=5000, debug=True)
