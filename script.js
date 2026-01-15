// ==================== Configuration ====================
const API_BASE_URL = 'http://localhost:5000';

// ==================== DOM Elements ====================
const uploadArea = document.getElementById('uploadArea');
const csvInput = document.getElementById('csvInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const uploadBtn = document.getElementById('uploadBtn');
const uploadStatus = document.getElementById('uploadStatus');

const querySection = document.getElementById('querySection');
const apiKeyInput = document.getElementById('apiKey');
const voiceBtn = document.getElementById('voiceBtn');
const textBtn = document.getElementById('textBtn');
const voiceInputSection = document.getElementById('voiceInputSection');
const textInputSection = document.getElementById('textInputSection');
const recordBtn = document.getElementById('recordBtn');
const recordingStatus = document.getElementById('recordingStatus');
const recordingTime = document.getElementById('recordingTime');
const waveform = document.getElementById('waveform');
const transcription = document.getElementById('transcription');
const queryInput = document.getElementById('queryInput');
const submitBtn = document.getElementById('submitBtn');

const resultsSection = document.getElementById('resultsSection');
const originalQuery = document.getElementById('originalQuery');
const context = document.getElementById('context');
const generatedSQL = document.getElementById('generatedSQL');
const copySQLBtn = document.getElementById('copySQLBtn');
const askAnotherBtn = document.getElementById('askAnotherBtn');

const loadingOverlay = document.getElementById('loadingOverlay');
const loadingText = document.getElementById('loadingText');
const errorToast = document.getElementById('errorToast');
const successToast = document.getElementById('successToast');

// ==================== State Management ====================
let selectedFile = null;
let mediaRecorder = null;
let audioChunks = [];
let recordingStartTime = null;
let recordingInterval = null;
let currentQuery = '';
let isRecording = false;

// ==================== Utility Functions ====================
function showLoading(message = 'Processing...') {
    loadingText.textContent = message;
    loadingOverlay.style.display = 'flex';
}

function hideLoading() {
    loadingOverlay.style.display = 'none';
}

function showError(message) {
    errorToast.textContent = '❌ ' + message;
    errorToast.style.display = 'block';
    setTimeout(() => {
        errorToast.style.display = 'none';
    }, 4000);
}

function showSuccess(message) {
    successToast.textContent = '✅ ' + message;
    successToast.style.display = 'block';
    setTimeout(() => {
        successToast.style.display = 'none';
    }, 3000);
}

function updateStatus(message, type = 'loading') {
    uploadStatus.className = `status-message ${type}`;
    uploadStatus.textContent = message;
}

function resetRecording() {
    isRecording = false;
    recordBtn.classList.remove('recording');
    recordingStatus.style.display = 'none';
    waveform.style.display = 'none';
    recordBtn.innerHTML = '<span class="record-icon">🎤</span>Click to Start Recording';
    if (recordingInterval) clearInterval(recordingInterval);
}

// ==================== File Upload Events ====================
uploadArea.addEventListener('click', () => csvInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

csvInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    if (!file.name.endsWith('.csv')) {
        showError('Please select a CSV file');
        return;
    }
    selectedFile = file;
    fileName.textContent = file.name;
    fileInfo.style.display = 'flex';
}

// ==================== CSV Upload ====================
uploadBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        showError('Please select a CSV file first');
        return;
    }

    uploadBtn.disabled = true;
    updateStatus('Uploading CSV...', 'loading');
    showLoading('Uploading and initializing CSV...');

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        const apiKey = apiKeyInput.value.trim();
        if (apiKey) {
            formData.append('groq_api_key', apiKey);
        }

        const response = await fetch(`${API_BASE_URL}/load-csv`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to load CSV');
        }

        const data = await response.json();
        updateStatus(
            `✅ CSV loaded successfully! Documents: ${data.documents_loaded}, Chunks: ${data.document_chunks}`,
            'success'
        );
        showSuccess('CSV loaded successfully!');
        
        // Show query section
        querySection.style.display = 'block';
        querySection.scrollIntoView({ behavior: 'smooth' });
        
        // Disable upload section
        uploadArea.style.pointerEvents = 'none';
        uploadArea.style.opacity = '0.6';
        uploadBtn.disabled = true;

    } catch (error) {
        console.error('Upload error:', error);
        updateStatus(`Error: ${error.message}`, 'error');
        showError(error.message);
        uploadBtn.disabled = false;
    } finally {
        hideLoading();
    }
});

// ==================== Query Method Selection ====================
voiceBtn.addEventListener('click', () => {
    voiceBtn.classList.add('active');
    textBtn.classList.remove('active');
    voiceInputSection.style.display = 'block';
    textInputSection.style.display = 'none';
    resetRecording();
});

textBtn.addEventListener('click', () => {
    textBtn.classList.add('active');
    voiceBtn.classList.remove('active');
    textInputSection.style.display = 'block';
    voiceInputSection.style.display = 'none';
    resetRecording();
});

// ==================== Microphone & Voice Recording ====================
async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            await transcribeAudio(audioBlob);
        };

        mediaRecorder.start();
        isRecording = true;
        recordBtn.classList.add('recording');
        recordBtn.innerHTML = '<span class="record-icon">🎤</span>Click to Stop Recording';
        
        recordingStatus.style.display = 'flex';
        waveform.style.display = 'flex';
        
        recordingStartTime = Date.now();
        recordingInterval = setInterval(updateRecordingTime, 100);

    } catch (error) {
        console.error('Microphone access error:', error);
        showError('Unable to access microphone. Please check permissions.');
    }
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        resetRecording();
    }
}

function updateRecordingTime() {
    if (recordingStartTime) {
        const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        recordingTime.textContent = 
            `Recording... ${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
}

recordBtn.addEventListener('click', () => {
    if (isRecording) {
        stopRecording();
    } else {
        startRecording();
    }
});

// ==================== Audio Transcription ====================
async function transcribeAudio(audioBlob) {
    showLoading('Transcribing audio...');
    transcription.textContent = 'Transcribing...';

    try {
        const formData = new FormData();
        formData.append('file', audioBlob, 'audio.wav');

        const response = await fetch(`${API_BASE_URL}/transcribe`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Transcription failed');
        }

        const data = await response.json();
        const transcribedText = data.transcribed_text;
        
        transcription.textContent = transcribedText || '(No speech detected)';
        currentQuery = transcribedText;
        showSuccess('Audio transcribed successfully!');

    } catch (error) {
        console.error('Transcription error:', error);
        transcription.textContent = `Error: ${error.message}`;
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// ==================== Query Submission ====================
submitBtn.addEventListener('click', async () => {
    // Get query from active input method
    let query = voiceBtn.classList.contains('active') 
        ? currentQuery 
        : queryInput.value.trim();

    if (!query) {
        showError('Please enter or record a question');
        return;
    }

    submitBtn.disabled = true;
    showLoading('Generating SQL...');

    try {
        // Step 1: Retrieve context
        const contextResponse = await fetch(`${API_BASE_URL}/retrieve-context`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });

        if (!contextResponse.ok) {
            const error = await contextResponse.json();
            throw new Error(error.error || 'Failed to retrieve context');
        }

        const contextData = await contextResponse.json();

        // Step 2: Generate SQL
        const sqlResponse = await fetch(`${API_BASE_URL}/generate-sql`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });

        if (!sqlResponse.ok) {
            const error = await sqlResponse.json();
            throw new Error(error.error || 'Failed to generate SQL');
        }

        const sqlData = await sqlResponse.json();

        // Display results
        displayResults(query, contextData.context, sqlData.generated_sql);
        showSuccess('SQL generated successfully!');

    } catch (error) {
        console.error('Query error:', error);
        showError(error.message);
    } finally {
        hideLoading();
        submitBtn.disabled = false;
    }
}

function displayResults(query, contextData, sqlQuery) {
    originalQuery.textContent = query;
    context.textContent = contextData;
    generatedSQL.textContent = sqlQuery;
    
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// ==================== Copy SQL ====================
copySQLBtn.addEventListener('click', () => {
    const sqlText = generatedSQL.textContent;
    navigator.clipboard.writeText(sqlText).then(() => {
        showSuccess('SQL copied to clipboard!');
    }).catch(() => {
        showError('Failed to copy SQL');
    });
});

// ==================== Ask Another Question ====================
askAnotherBtn.addEventListener('click', () => {
    // Reset query input
    queryInput.value = '';
    currentQuery = '';
    transcription.textContent = 'Ready to record...';
    resetRecording();
    
    // Hide results
    resultsSection.style.display = 'none';
    
    // Scroll back to query section
    querySection.scrollIntoView({ behavior: 'smooth' });
});

// ==================== Initial Setup ====================
document.addEventListener('DOMContentLoaded', () => {
    // Check API connection
    fetch(`${API_BASE_URL}/health`)
        .then(response => response.json())
        .then(data => {
            console.log('✅ Connected to API:', data);
        })
        .catch(error => {
            console.error('❌ API Connection Error:', error);
            showError('Cannot connect to backend API. Make sure the server is running at ' + API_BASE_URL);
        });
});
