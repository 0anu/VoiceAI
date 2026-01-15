# Environment Configuration Examples

# ==================== API Configuration ====================

# Set your Groq API Key (get it from https://console.groq.com)
# You can either:
# 1. Set it as an environment variable:
#    Windows PowerShell:
#      $env:GROQ_API_KEY = "your-actual-api-key"
#    Windows CMD:
#      set GROQ_API_KEY=your-actual-api-key
#    Linux/Mac:
#      export GROQ_API_KEY=your-actual-api-key

# 2. Or pass it through the web UI when uploading CSV

# 3. Or create a .env file (using python-dotenv) with:
GROQ_API_KEY=your-actual-api-key

# ==================== Flask Configuration ====================

# Backend runs on:
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_ENV=development
FLASK_DEBUG=True

# ==================== Frontend Configuration ====================

# Update in script.js if backend is on different server:
const API_BASE_URL = 'http://localhost:5000';

# For production:
# const API_BASE_URL = 'https://your-domain.com:5000';

# ==================== Model Configuration ====================

# Whisper Model Size (app/utils/audio_processor.py)
# Options: tiny (39M), base (74M), small (244M), medium (769M), large (3.1GB)
# Default: small (best balance of speed and accuracy)
WHISPER_MODEL_SIZE=small
WHISPER_COMPUTE_TYPE=int8

# ==================== Vector Store Configuration ====================

# Embedding Model (app/utils/embeddings_manager.py)
# Using: sentence-transformers/all-MiniLM-L6-v2
# This is the default and works well for semantic search

# ==================== File Upload Configuration ====================

# Max upload size (in bytes): 100MB
MAX_CONTENT_LENGTH=104857600

# Allowed audio formats:
ALLOWED_AUDIO=mp3,wav,ogg,m4a,flac

# Allowed source column for CSV (default: description)
SOURCE_COLUMN=description

# ==================== Running the Application ====================

# Terminal 1: Start Backend
# python -m flask run --app app
# or
# python -m flask run --app app --host 0.0.0.0 --port 5000

# Terminal 2: Serve Frontend (optional)
# python -m http.server 8000
# Then visit: http://localhost:8000

# Or simply open index.html in browser

# ==================== Development Tips ====================

# 1. Keep Flask terminal open to see logs:
#    GET /health - Connection check
#    POST /load-csv - CSV loading
#    POST /transcribe - Audio transcription
#    POST /retrieve-context - Vector search
#    POST /generate-sql - SQL generation

# 2. Open browser DevTools (F12) to see:
#    - Network requests and responses
#    - Console errors and warnings
#    - Performance metrics

# 3. Test microphone:
#    - Check browser permissions
#    - Test microphone in system settings first
#    - Try different browsers

# 4. Test CSV:
#    - Make sure CSV is properly formatted
#    - Check column names match (table_name, column_name, description)
#    - Use sample_data.csv for initial testing

# ==================== Production Deployment ====================

# 1. Use a production WSGI server:
#    pip install gunicorn
#    gunicorn --bind 0.0.0.0:5000 app:create_app()

# 2. Enable CORS only for your domain in app/__init__.py:
#    CORS(app, resources={r"/api/*": {"origins": "yourdomain.com"}})

# 3. Use environment variables for secrets:
#    Never hardcode API keys

# 4. Enable HTTPS:
#    Use a reverse proxy like nginx
#    Install SSL certificate (Let's Encrypt)

# 5. Scale considerations:
#    - Use database for persistent storage
#    - Use Redis for caching
#    - Deploy with multiple workers
#    - Use load balancer
