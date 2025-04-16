# Educational Platform

A live tutoring platform using WebRTC for video conferencing and Groq for AI features.

## Features

- Live video conferencing with WebRTC
- Real-time chat with user presence indicators
- Live speech-to-text transcription
- AI-powered summarization using Groq
- Modern UI with Tailwind CSS and DaisyUI
- Multi-user support with real-time updates

## Tech Stack

- **Backend**: FastAPI, WebSockets, Groq API
- **Frontend**: Vue.js, WebRTC, Web Speech API
- **Styling**: Tailwind CSS, DaisyUI
- **Real-time Communication**: WebSockets, WebRTC

## Setup

### Prerequisites

- Python 3.8+
- Node.js 14+
- Groq API key (sign up at https://console.groq.com)

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file based on `.env.example` and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

6. Start the backend server:
   ```
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. Access the application at `http://localhost:3000`

## Usage

1. Open the application in your browser (Chrome or Edge recommended for speech recognition)
2. Create a new session or join an existing one
3. Allow camera and microphone access when prompted
4. Use the controls to toggle your microphone, camera, and start/stop transcription
5. Start transcription to automatically generate AI summaries

## Browser Support

- For full functionality including speech recognition, use Google Chrome or Microsoft Edge
- Safari and Firefox have limited support for the Web Speech API

## Future Enhancements

- Integration with Screenpipe's Terminator for user activity monitoring
- Integration with Fluvio for real-time data streaming
- Advanced AI features like content analysis and personalized learning paths
- Breakout rooms for group discussions 