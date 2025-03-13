import os
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    
    # Set environment variables
    os.environ["LANGSMITH_TRACING_V2"] = os.getenv("LANGSMITH_TRACING_V2")
    os.environ["LANGSMITH_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT") 
    os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
    os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    os.environ["GROQ_MODEL_NAME_1"] = os.getenv("GROQ_MODEL_NAME_1")
    os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")
    os.environ["INDEX_NAME"] = os.getenv("INDEX_NAME")
    os.environ["EMBEDDING_MODEL"] = os.getenv("EMBEDDING_MODEL")
    os.environ["LANGSMITH_DATASET_ID"] = os.getenv("LANGSMITH_DATASET_ID")

def print_environment_variables():
    """Print environment variables for debugging"""
    print("LANGSMITH_TRACING_V2:", os.getenv("LANGSMITH_TRACING_V2"))
    print("LANGSMITH_ENDPOINT:", os.getenv("LANGSMITH_ENDPOINT"))
    print("LANGSMITH_API_KEY:", os.getenv("LANGSMITH_API_KEY"))
    print("LANGSMITH_PROJECT:", os.getenv("LANGSMITH_PROJECT"))
    print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
    print("GROQ_API_KEY:", os.getenv("GROQ_API_KEY"))
    print("GROQ_MODEL_NAME_1:", os.getenv("GROQ_MODEL_NAME_1"))
    print("PINECONE_API_KEY:", os.getenv("PINECONE_API_KEY"))
    print("INDEX_NAME:", os.getenv("INDEX_NAME"))
    print("EMBEDDING_MODEL:", os.getenv("EMBEDDING_MODEL"))
    print("LANGSMITH_DATASET_ID:", os.getenv("LANGSMITH_DATASET_ID")) 