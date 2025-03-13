from flask import Flask, request, jsonify
from flask_cors import CORS
import main
import traceback
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow all origins for /api/ routes

@app.route('/api/generate-email', methods=['POST'])
def generate_email():
    logger.info(f"Received request: {request.method} {request.path}")
    logger.debug(f"Headers: {dict(request.headers)}")
    
    try:
        # Get request data
        data = request.get_json()
        logger.info(f"Request data: {data}")
        
        if not data:
            logger.error("No JSON data in request")
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided in request'
            }), 400
        
        product_url = data.get('product_url')
        client_url = data.get('client_url')
        
        logger.info(f"Processing request with product_url={product_url}, client_url={client_url}")
        
        # Validate input
        if not product_url or not client_url:
            logger.error("Missing required parameters")
            return jsonify({
                'status': 'error',
                'message': 'Both product_url and client_url are required'
            }), 400
        
        # Call the main function with the provided URLs
        logger.info("Calling main.main with URLs")
        try:
            email_content = main.main(product_url=product_url, client_url=client_url)
            logger.info("Successfully generated email content")
        except Exception as e:
            logger.error(f"Error in main.main: {str(e)}")
            logger.error(traceback.format_exc())
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
        logger.error(traceback.format_exc())
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
    logger.info(f"Test endpoint called: {request.method}")
    return jsonify({
        'status': 'success',
        'message': 'Test endpoint working',
        'method': request.method,
        'headers': dict(request.headers),
        'data': request.get_json() if request.is_json else None
    })

if __name__ == '__main__':
    PORT = 5001
    logger.info(f"Starting API server on port {PORT}")
    app.run(debug=True, port=PORT, host='0.0.0.0') 