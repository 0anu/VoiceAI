"""
Flask Routes for AI Agent

This module defines all HTTP endpoints for the AI Agent API.
It handles:
- Audio transcription (Whisper model)
- CSV data loading and management
- Vector embeddings and context retrieval
- SQL query generation from natural language

Global State:
- audio_processor: Handles audio file transcription
- embeddings_manager: Manages vector embeddings and similarity search
- llm_agent: LLM agent for SQL generation (initialized when CSV is loaded)
"""
from flask import Blueprint, request, jsonify
import os, tempfile
from app.utils.audio_processor import AudioProcessor
from app.utils.embeddings_manager import EmbeddingsManager
from app.utils.llm_agent import LLMAgent

# Create Blueprint for organizing routes
main_bp = Blueprint('main', __name__)

# Initialize core components
audio_processor = AudioProcessor()  # Audio transcription service
embeddings_manager = EmbeddingsManager()  # Vector store and embeddings
llm_agent = None  # Initialized after CSV is loaded

# Supported audio file formats
ALLOWED_AUDIO = {'mp3', 'wav', 'ogg', 'm4a', 'flac'}


def _is_audio(f):
    """
    Validate if file has an audio extension.
    
    Args:
        f (str): Filename to validate
        
    Returns:
        bool: True if file has supported audio extension, False otherwise
    """
    return '.' in f and f.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO


def _save_temp(file, suffix=''):
    """
    Save uploaded file to temporary location.
    
    Args:
        file (FileStorage): Flask request file object
        suffix (str): File extension to append (e.g., '.wav', '.csv')
        
    Returns:
        str: Path to temporary file
    """
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    file.save(tmp.name)
    return tmp.name


def _cleanup(path):
    """
    Remove temporary file if it exists.
    Silently ignores if file doesn't exist.
    
    Args:
        path (str): Path to file to delete
    """
    os.path.exists(path) and os.remove(path)

@main_bp.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint to verify API is running.
    
    Returns:
        JSON: Status object with 'ok' status and running message
        HTTP 200: Always successful
    """
    return jsonify({"status": "ok", "message": "AI Agent API is running"}), 200

@main_bp.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Transcribe audio file to text using Whisper model.
    
    Expected form data:
        file (FileStorage): Audio file (mp3, wav, ogg, m4a, or flac)
        
    Returns:
        JSON: {"transcribed_text": "transcribed text content"}
        HTTP 200: Successful transcription
        HTTP 400: Missing or invalid file
        HTTP 500: Processing error
        
    Process:
        1. Validate file is present and has valid audio extension
        2. Save to temporary location
        3. Run Whisper transcription
        4. Clean up temporary file
        5. Return transcribed text
    """
    try:
        # Check if file exists and is not empty
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        # Validate audio format
        if not _is_audio(file.filename):
            return jsonify({"error": "Invalid format. Allowed: mp3, wav, ogg, m4a, flac"}), 400
        
        # Save file temporarily and transcribe
        tmp_path = _save_temp(file, os.path.splitext(file.filename)[1])
        try:
            return jsonify({"transcribed_text": audio_processor.transcribe(tmp_path)}), 200
        finally:
            _cleanup(tmp_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/load-csv', methods=['POST'])
def load_csv():
    """
    Load CSV data and initialize the LLM agent for SQL generation.
    
    This endpoint:
    1. Accepts a CSV file containing database schema information
    2. Converts documents into embeddings and stores in vector DB
    3. Initializes LLM agent with retrieval capability
    
    Expected form data:
        file (FileStorage): CSV file containing table/column descriptions
        source_column (str): Column name for document content (default: 'description')
        groq_api_key (str): Optional Groq API key for LLM (uses env var if not provided)
        
    Returns:
        JSON: {
            "message": "CSV loaded successfully",
            "documents_loaded": number of original documents,
            "document_chunks": number of text chunks after splitting
        }
        HTTP 200: Successful load
        HTTP 400: Missing or invalid file
        HTTP 500: Processing error
        
    Process:
        1. Validate CSV file is provided
        2. Load CSV and extract documents
        3. Split documents into chunks for embedding
        4. Add chunks to vector store (in-memory)
        5. Initialize LLM agent with embeddings manager
        6. Clean up temporary file
    """
    try:
        # Validate file exists and is not empty
        if 'file' not in request.files or request.files['file'].filename == '':
            return jsonify({"error": "No CSV file provided"}), 400
        
        file = request.files['file']
        
        # Validate file extension
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "File must be CSV"}), 400
        
        # Save and process CSV
        tmp_path = _save_temp(file, '.csv')
        try:
            # Load documents from CSV
            docs = embeddings_manager.load_csv_documents(
                tmp_path,
                source_column=request.form.get('source_column', 'description')
            )
            
            # Add documents to vector store (splits into chunks internally)
            doc_ids = embeddings_manager.add_documents(docs)
            
            # Initialize LLM agent with vector store and API key
            global llm_agent
            llm_agent = LLMAgent(embeddings_manager, request.form.get('groq_api_key'))
            
            return jsonify({
                "message": "CSV loaded successfully",
                "documents_loaded": len(docs),
                "document_chunks": len(doc_ids)
            }), 200
        finally:
            _cleanup(tmp_path)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/retrieve-context', methods=['POST'])
def retrieve_context():
    """
    Retrieve context from loaded CSV using semantic similarity search.
    
    Expected JSON body:
        {
            "query": "natural language query to search for"
        }
        
    Returns:
        JSON: {
            "context": "formatted context from top matching documents",
            "documents_count": number of documents retrieved
        }
        HTTP 200: Successful retrieval
        HTTP 400: Missing query parameter
        HTTP 500: Processing error
        
    Process:
        1. Extract query from JSON body
        2. Search vector store for similar documents (default k=2)
        3. Format and return matching documents with metadata
        
    Note:
        This endpoint doesn't require CSV to be loaded (embeddings_manager
        works independently). To get meaningful results, use /load-csv first.
    """
    try:
        # Extract query parameter
        query = request.get_json().get('query')
        
        if not query:
            return jsonify({"error": "Query required"}), 400
        
        # Retrieve similar documents from vector store
        serialized, docs = embeddings_manager.retrieve_context(query)
        
        return jsonify({"context": serialized, "documents_count": len(docs)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/generate-sql', methods=['POST'])
def generate_sql():
    """
    Generate SQL query from natural language using LLM with retrieval.
    
    This endpoint uses an agentic LLM that:
    1. Takes a natural language query
    2. Retrieves relevant context from the loaded CSV
    3. Generates appropriate SQL query
    
    Expected JSON body:
        {
            "query": "natural language description of desired data"
        }
        
    Returns:
        JSON: {
            "natural_language_query": "original user query",
            "generated_sql": "generated SQL statement"
        }
        HTTP 200: Successful SQL generation
        HTTP 400: CSV not loaded or missing query
        HTTP 500: LLM processing error
        
    Prerequisites:
        Must call /load-csv endpoint first to initialize llm_agent
        
    Process:
        1. Check if LLM agent has been initialized (CSV loaded)
        2. Validate query parameter
        3. Call LLM agent with retrieval tool
        4. Return generated SQL query
    """
    try:
        # Check if CSV has been loaded and agent initialized
        if not llm_agent:
            return jsonify({"error": "Load CSV first"}), 400
        
        # Extract query parameter
        query = request.get_json().get('query')
        
        if not query:
            return jsonify({"error": "Query required"}), 400
        
        # Generate SQL using LLM agent with context retrieval
        sql = llm_agent.generate_sql(query)
        
        return jsonify({"natural_language_query": query, "generated_sql": sql}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/', methods=['GET'])
def index():
    """
    API documentation and endpoint listing.
    
    Returns:
        JSON: Structured documentation of all available endpoints
        HTTP 200: Always successful
        
    Provides information about:
    - /health: Server status check
    - /transcribe: Audio-to-text conversion
    - /load-csv: Initialize vector store and LLM agent
    - /retrieve-context: Semantic search in vector store
    - /generate-sql: Natural language to SQL conversion
    """
    return jsonify({
        "message": "AI Agent Flask API",
        "endpoints": {
            "GET /health": "Health check",
            "POST /transcribe": "Transcribe audio (file: audio)",
            "POST /load-csv": "Load CSV (file: csv, source_column: optional, groq_api_key: optional)",
            "POST /retrieve-context": "Retrieve context (json: {query})",
            "POST /generate-sql": "Generate SQL (json: {query})"
        }
    }), 200
