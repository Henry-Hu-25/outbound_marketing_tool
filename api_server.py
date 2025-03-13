from flask import Flask, request, jsonify
from flask_cors import CORS
import main
import traceback
import logging
import sys
import os

# Set up logging - change level to INFO to reduce verbosity
logging.basicConfig(
    level=logging.INFO,  # Changed from DEBUG to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Simplified format
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Disable noisy loggers
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('matplotlib').setLevel(logging.WARNING)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for /api/ routes

@app.route('/api/generate-email', methods=['POST'])
def generate_email():
    logger.info(f"Processing email generation request")
    
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            logger.error("No JSON data in request")
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided in request'
            }), 400
        
        product_url = data.get('product_url')
        client_url = data.get('client_url')
        
        # Validate input
        if not product_url or not client_url:
            logger.error("Missing required parameters")
            return jsonify({
                'status': 'error',
                'message': 'Both product_url and client_url are required'
            }), 400
        
        # Call the main function with the provided URLs
        try:
            # Create a quiet environment for main.py execution
            original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')  # Redirect stdout to null
            
            email_content = main.main(product_url=product_url, client_url=client_url)
            
            # Restore stdout
            sys.stdout.close()
            sys.stdout = original_stdout
            
            logger.info("Successfully generated email content")
        except Exception as e:
            # Restore stdout if exception occurred
            if sys.stdout != original_stdout:
                sys.stdout.close()
                sys.stdout = original_stdout
                
            logger.error(f"Error in email generation: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f"Error in email generation: {str(e)}"
            }), 500
        
        # Return the generated email
        return jsonify({
            'status': 'success',
            'email_content': email_content
        })
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Add a simple health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'API server is running'
    })

# For debugging - simple test endpoint
@app.route('/api/test', methods=['GET', 'POST'])
def test_endpoint():
    return jsonify({
        'status': 'success',
        'message': 'Test endpoint working'
    })

if __name__ == '__main__':
    PORT = 5001
    logger.info(f"Starting API server on port {PORT}")
    app.run(debug=False, port=PORT, host='0.0.0.0') 