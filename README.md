# Icebreaker - AI-Powered Sales Outreach System

This project is an AI-Powered system for generating personalized sales outreach emails based on product and client information. It uses web scraping, vector search, and language models to create targeted sales communications.

## Features

- Web scraping to extract product and client information
- Image and text embedding using CLIP model
- Hybrid search using BM25 and CLIP embeddings
- Visualization of search results
- AI-powered email generation
- Email quality evaluation
- Modern UI frontend with Next.js and React
- Flask API server for frontend-backend communication

## Setup

### Backend

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys and configuration
4. Place your inventory data in the `images` directory
5. Run the API server:
   ```
   python api_server.py
   ```

### Frontend

See [README-FRONTEND.md](README-FRONTEND.md) for detailed frontend setup instructions.

## Project Structure

- `main.py`: Core application logic
- `api_server.py`: Flask API server for frontend integration
- `src/`: Source code directory
  - `config.py`: Configuration and environment setup
  - `web_scraping.py`: Web scraping functionality
  - `data_processing.py`: Data processing functions
  - `models/`: Model-related code
    - `clip_model.py`: CLIP model functionality
    - `bm25_model.py`: BM25 functionality
  - `pinecone_utils.py`: Pinecone setup and operations
  - `search.py`: Search functionality
  - `visualization.py`: Result visualization with non-GUI output
  - `email_generator.py`: Email generation functionality
  - `evaluation.py`: Email evaluation functionality
- `frontend/`: Next.js frontend application

## API Endpoints

The Flask API server provides the following endpoints:

- `GET /api/health`: Health check endpoint
- `POST /api/generate-email`: Generate an email based on product and client URLs
  - Request body: `{ "product_url": "url", "client_url": "url" }`
  - Response: `{ "status": "success", "email_content": "Generated email..." }`

## Requirements

- Python 3.8+
- Node.js 14+ (for frontend)
- See `requirements.txt` for Python dependencies
- See `frontend/package.json` for frontend dependencies 