# Voice AI - CSV Query Assistant

A modern web application for uploading CSV files and asking questions using voice input, with AI-powered SQL query generation.

## 🎯 Features

- **CSV Upload**: Drag-and-drop or click to upload CSV files
- **Voice Input**: Record questions using your microphone
- **Real-time Transcription**: Converts voice to text using Whisper AI
- **AI SQL Generation**: Generates SQL queries from natural language using LangChain + Groq LLM
- **Semantic Search**: Retrieves relevant context from your CSV using embeddings
- **Interactive UI**: Modern, responsive interface with real-time feedback
- **Copy Functionality**: Easily copy generated SQL queries

## 📋 Project Structure

```
VoiceAI/
├── index.html          # Main HTML interface
├── styles.css          # Complete styling with animations
├── script.js           # Frontend JavaScript logic
├── app/
│   ├── __init__.py     # Flask application factory
│   ├── routes.py       # API endpoints
│   └── utils/
│       ├── audio_processor.py      # Audio transcription (Whisper)
│       ├── embeddings_manager.py   # Vector embeddings & retrieval
│       └── llm_agent.py            # LLM agent for SQL generation
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js (optional, for local development)
- Microphone access (for voice input)
- Groq API key (optional, but recommended for LLM)

### Installation

1. **Clone/Download the project**
   ```bash
   cd VoiceAI
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Groq API key (Optional)**
   - Get your API key from https://console.groq.com
   - Set as environment variable:
     ```bash
     # Windows (PowerShell)
     $env:GROQ_API_KEY = "your-api-key"
     
     # Windows (CMD)
     set GROQ_API_KEY=your-api-key
     
     # Linux/Mac
     export GROQ_API_KEY=your-api-key
     ```

### Running the Application

1. **Start the Flask backend**
   ```bash
   python -m flask run --app app
   ```
   The API will be available at `http://localhost:5000`

2. **Open the frontend**
   - **Option 1**: Open `index.html` in your browser
     ```bash
     # Windows
     start index.html
     
     # Mac
     open index.html
     
     # Linux
     xdg-open index.html
     ```
   
   - **Option 2**: Use a local web server
     ```bash
     # Python 3
     python -m http.server 8000
     ```
     Then open `http://localhost:8000`

## 📖 Usage Guide

### Step 1: Upload CSV File

1. Click the upload area or drag-and-drop a CSV file
2. Select your CSV file (must contain descriptions/metadata about your database)
3. (Optional) Enter your Groq API key for better SQL generation
4. Click "Upload & Initialize"

**CSV Format Example:**
```csv
table_name,column_name,description
users,id,Unique user identifier
users,name,User's full name
users,email,User's email address
orders,id,Unique order identifier
orders,user_id,Reference to user
orders,total,Order total amount
```

### Step 2: Ask Questions

Choose your input method:

#### Voice Input
1. Click "🎤 Voice" tab
2. Click "Click to Start Recording"
3. Speak your question clearly
4. The app will automatically transcribe your speech
5. Click "Generate SQL & Get Results"

#### Text Input
1. Click "⌨️ Text" tab
2. Type your question in the text area
3. Click "Generate SQL & Get Results"

**Example Questions:**
- "Show me all users who placed orders"
- "What is the total amount of orders from user 5?"
- "Give me the top 10 customers by order count"

### Step 3: View Results

The application will display:
- **Original Query**: Your question
- **Retrieved Context**: Relevant CSV data matching your query
- **Generated SQL**: The AI-generated SQL statement

You can:
- Copy the SQL query using the "📋 Copy SQL" button
- Ask another question using "Ask Another Question" button

## 🔌 API Endpoints

### Health Check
```
GET /health
```
Returns server status

### Upload CSV
```
POST /load-csv
Form Data:
  - file: CSV file
  - source_column: Column name for content (default: "description")
  - groq_api_key: Optional API key
```

### Transcribe Audio
```
POST /transcribe
Form Data:
  - file: Audio file (mp3, wav, ogg, m4a, flac)
```

### Retrieve Context
```
POST /retrieve-context
JSON Body:
  {
    "query": "Your search query"
  }
```

### Generate SQL
```
POST /generate-sql
JSON Body:
  {
    "query": "Your natural language question"
  }
```

## 🎤 Microphone Setup

### Granting Microphone Permission

The first time you click "Start Recording", your browser will ask for microphone permission:

- **Chrome/Edge**: Click "Allow" when prompted
- **Firefox**: Click "Allow" when prompted
- **Safari**: Go to Settings → Privacy → Microphone, enable for this site

### Supported Audio Formats
- MP3
- WAV
- OGG
- M4A
- FLAC

## 🛠️ Troubleshooting

### "Cannot connect to backend API"
- Make sure Flask server is running: `python -m flask run --app app`
- Check if port 5000 is available
- Verify no firewall is blocking the connection

### "Microphone access denied"
- Check browser permissions for microphone
- Make sure you're using HTTPS or localhost
- Some browsers require secure context (HTTPS) for microphone access

### "No speech detected"
- Speak clearly and closer to the microphone
- Check microphone volume levels
- Ensure you have a good internet connection (for Whisper AI)

### "Load CSV first" error
- Upload a CSV file before asking questions
- Make sure the CSV upload completed successfully

### "Failed to generate SQL"
- Check if you've set the GROQ_API_KEY environment variable
- Verify your API key is valid at https://console.groq.com
- Check internet connection for LLM API calls

## ⚙️ Configuration

### Backend Configuration

Edit `app/__init__.py` to modify:
- MAX_CONTENT_LENGTH: Maximum file upload size (default: 100MB)
- CORS settings: Allowed origins

### API Base URL

If running on a different host/port, update in `script.js`:
```javascript
const API_BASE_URL = 'http://your-server:port';
```

### Whisper Model Size

Edit `app/utils/audio_processor.py` to change model:
```python
self.model = WhisperModel("base")  # Options: tiny, base, small, medium, large
```

## 📊 Technology Stack

### Frontend
- **HTML5**: Modern semantic markup
- **CSS3**: Animations, gradients, responsive design
- **JavaScript**: ES6+ for DOM manipulation and API calls
- **Web APIs**: MediaRecorder API, Fetch API, getUserMedia

### Backend
- **Flask**: Python web framework
- **LangChain**: LLM orchestration and tools
- **Groq API**: Fast LLM inference (LanguageModel: groq-alpha)
- **Faster Whisper**: Accurate speech-to-text
- **Sentence Transformers**: Vector embeddings
- **ChromaDB**: Vector database for similarity search

### Deployment Requirements
- Python 3.8+
- CUDA/GPU support (optional, but recommended)
- 4GB+ RAM
- Modern web browser with microphone access

## 📝 Example Workflow

1. **Start the application**
   - Run: `python -m flask run --app app`
   - Open: `index.html` in browser

2. **Upload a CSV**
   - Prepare a CSV with table/column descriptions
   - Upload via drag-and-drop

3. **Ask a Question**
   - Click microphone button
   - Ask: "Show me all orders from January"
   - Watch it transcribe your speech

4. **Get SQL**
   - View generated SQL query
   - Copy to clipboard for execution
   - Ask another question

## 🔒 Security Notes

- Store API keys in environment variables, not in code
- Use HTTPS in production
- Implement authentication for multi-user scenarios
- Validate and sanitize all user inputs
- Set CORS policy appropriately in production

## 📄 License

This project is provided as-is for educational and development purposes.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Check Flask server logs for errors
4. Ensure API key is valid if using LLM features

## 🚀 Future Enhancements

- [ ] Database execution and result display
- [ ] Query history and favorites
- [ ] Multi-language support
- [ ] Export results to CSV/JSON
- [ ] Advanced search filters
- [ ] User authentication
- [ ] Result visualization/charts
- [ ] API documentation (Swagger/OpenAPI)

---

**Made with ❤️ using LangChain, Flask, and modern web technologies**
