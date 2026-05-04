# PitchPilot AI - MVP

A full-stack MVP for an AI-powered pitch deck generation platform with a 4-step wizard interface.

## Project Structure

```
pitchpilot-mvp/
├── backend/                 # FastAPI backend
│   ├── main.py             # API entry point
│   ├── database.py        # SQLite database
│   ├── ai_engine.py        # Gemini AI integration
│   ├── deck_engine.py      # PPTX generation
│   ├── verification_engine.py  # Web search verification
│   ├── file_processor.py   # File upload handling
│   └── websocket_manager.py   # WebSocket connections
│
├── frontend/                # Next.js frontend
│   ├── app/
│   │   ├── page.tsx       # Main wizard page
│   │   ├── layout.tsx     # Root layout
│   │   └── globals.css    # Global styles
│   ├── tailwind.config.js # Design tokens
│   └── package.json       # Dependencies
│
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Features

- **4-Step Wizard**: File Intake → AI Verification → Deck Blueprint → Export
- **Gemini 1.5 Pro Integration**: Strategic pitch deck generation
- **WebSocket Support**: Real-time thinking state updates
- **SQLite Database**: Session and deck storage
- **PPTX Export**: 10-slide Farmeal-Standard methodology
- **Market Data Verification**: Web search for credible sources

## Prerequisites

- Python 3.10+
- Node.js 18+
- API Keys:
  - Google Gemini API Key
  - SerpAPI Key (for verification)

## Setup Instructions

### 1. Clone and Navigate

```bash
cd pitchpilot-mvp
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example backend/.env
# Edit backend/.env with your API keys:
# GOOGLE_API_KEY=your_gemini_key
# SERP_API_KEY=your_serpapi_key
```

### 3. Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Build for production
npm run build
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd pitchpilot-mvp/backend
python main.py
# Runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd pitchpilot-mvp/frontend
npm run dev
# Runs on http://localhost:3000
```

### 5. Access the App

Open http://localhost:3000 in your browser.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root API info |
| `/health` | GET | Health check |
| `/api/upload` | POST | Upload single file |
| `/api/upload/multiple` | POST | Upload multiple files |
| `/api/deck/generate` | POST | Generate pitch deck |
| `/api/deck/generate/stream` | POST | Generate with streaming |
| `/api/deck/{deck_id}/download` | GET | Download PPTX |
| `/api/decks` | GET | List all decks |
| `/ws/{session_id}` | WS | WebSocket for updates |

## Design System

The UI follows the PitchPilot AI Visual Language defined in `DESIGN.md`:

- **Primary**: #3fe56c (Green)
- **Surface**: #0d150d (Dark)
- **Background**: #0d150d
- **Font**: Work Sans

## 4-Step Wizard Flow

1. **File Intake**: Upload PDF/DOCX/TXT files or enter company details
2. **AI Verification**: Analyze inputs, verify market data via web search
3. **Deck Blueprint**: Generate 10-slide Farmeal-Standard structure
4. **Export**: Download as PowerPoint (.pptx)

## Database Schema

### Sessions Table
- `id`: Session UUID
- `company_name`: Company name
- `founder_name`: Founder name
- `status`: Session status
- `metadata`: JSON metadata

### Decks Table
- `id`: Deck UUID
- `session_id`: Associated session
- `company_name`: Company name
- `slide_data`: JSON slide content
- `status`: Deck status
- `pptx_path`: Generated file path

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Kill process
kill -9 <PID>
```

### API Key Errors
Ensure your `.env` file has valid keys:
- Get Gemini key from: https://aistudio.google.com/app/apikey
- Get SerpAPI key from: https://serpstack.com

### Database Errors
Delete the SQLite database and restart:
```bash
rm backend/pitchpilot.db
```

## License

MIT License