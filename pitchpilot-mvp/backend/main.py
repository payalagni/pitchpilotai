"""
PitchPilot AI - FastAPI Backend
Main application entry point
"""

import os
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio

# Import modules
from database import Database, Session, Deck
from ai_engine import AIEngine
from deck_engine import DeckEngine
from verification_engine import VerificationEngine
from file_processor import FileProcessor
from websocket_manager import ConnectionManager


# Initialize managers
db = Database()
ai_engine = AIEngine()
deck_engine = DeckEngine()
verification_engine = VerificationEngine()
file_processor = FileProcessor()
ws_manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    # Startup
    await db.init_db()
    print("✅ Database initialized")
    yield
    # Shutdown
    print("🛑 Application shutting down")


# Create FastAPI app
app = FastAPI(
    title="PitchPilot AI API",
    description="Strategic Pitch Deck Architect API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== MODELS ====================

class DeckRequest(BaseModel):
    """Request model for deck generation"""
    company_name: str
    founder_name: Optional[str] = ""
    raw_content: Optional[str] = ""
    target_audience: Optional[str] = "VC"
    funding_amount: Optional[str] = ""
    deck_purpose: Optional[str] = "Seed Round"


class DeckResponse(BaseModel):
    """Response model for deck generation"""
    deck_id: str
    company_name: str
    slide_data: Dict[str, str]
    created_at: str
    status: str


class VerifyRequest(BaseModel):
    """Request model for verification"""
    content: str


# ==================== WEBSOCKET ====================

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time updates"""
    await ws_manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages if needed
            await ws_manager.send_personal_message({"type": "ack"}, session_id)
    except WebSocketDisconnect:
        ws_manager.disconnect(session_id)


# ==================== API ROUTES ====================

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "PitchPilot AI API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": "connected"}


# ==================== FILE UPLOAD ====================

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a file"""
    try:
        # Save uploaded file
        upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        content = await file.read()
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Process file based on type
        extracted_text = file_processor.process_file_content(
            file.filename, 
            content
        )
        
        return {
            "success": True,
            "filename": file.filename,
            "content": extracted_text,
            "size": len(content)
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.post("/api/upload/multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    """Upload and process multiple files"""
    results = []
    
    for file in files:
        try:
            content = await file.read()
            extracted = file_processor.process_file_content(file.filename, content)
            results.append({
                "filename": file.filename,
                "content": extracted,
                "success": True
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e),
                "success": False
            })
    
    return {"files": results}


# ==================== DECK GENERATION ====================

@app.post("/api/deck/generate")
async def generate_deck(request: DeckRequest):
    """Generate a pitch deck"""
    try:
        # Get knowledge base context
        from knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        kb_context = kb.get_context_for_prompt(request.company_name)
        
        # Combine inputs
        full_content = kb_context + "\n\n" + request.raw_content if kb_context else request.raw_content
        
        # Generate deck with AI
        deck_json = ai_engine.generate_deck(
            founder_name=request.founder_name,
            company_name=request.company_name,
            raw_content=full_content,
            target_audience=request.target_audience,
            funding_amount=request.funding_amount,
            deck_purpose=request.deck_purpose
        )
        
        if deck_json:
            # Verify market data
            verified_deck = verification_engine.verify_deck_data(deck_json)
            
            # Save to database
            deck_id = await db.save_deck(
                company_name=request.company_name,
                founder_name=request.founder_name,
                slide_data=verified_deck,
                status="generated"
            )
            
            return {
                "success": True,
                "deck_id": deck_id,
                "deck_data": verified_deck
            }
        
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Failed to generate deck"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.post("/api/deck/generate/stream")
async def generate_deck_stream(request: DeckRequest):
    """Generate a pitch deck with streaming updates"""
    session_id = request.company_name.replace(" ", "_").lower()
    
    try:
        # Send initial status
        await ws_manager.broadcast_to_session({
            "type": "status",
            "step": "intake",
            "message": "Processing input...",
            "progress": 10
        }, session_id)
        
        # Get knowledge base context
        from knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        kb_context = kb.get_context_for_prompt(request.company_name)
        
        full_content = kb_context + "\n\n" + request.raw_content if kb_context else request.raw_content
        
        # Step 1: File Intake
        await ws_manager.broadcast_to_session({
            "type": "status",
            "step": "intake",
            "message": "Analyzing inputs...",
            "progress": 25
        }, session_id)
        
        # Step 2: AI Verification
        await ws_manager.broadcast_to_session({
            "type": "status",
            "step": "verification",
            "message": "Verifying market data...",
            "progress": 50
        }, session_id)
        
        # Generate deck
        deck_json = ai_engine.generate_deck(
            founder_name=request.founder_name,
            company_name=request.company_name,
            raw_content=full_content,
            target_audience=request.target_audience,
            funding_amount=request.funding_amount,
            deck_purpose=request.deck_purpose
        )
        
        # Step 3: Deck Blueprint
        await ws_manager.broadcast_to_session({
            "type": "status",
            "step": "blueprint",
            "message": "Building slide structure...",
            "progress": 75
        }, session_id)
        
        if deck_json:
            verified_deck = verification_engine.verify_deck_data(deck_json)
            
            # Save to database
            deck_id = await db.save_deck(
                company_name=request.company_name,
                founder_name=request.founder_name,
                slide_data=verified_deck,
                status="generated"
            )
            
            # Step 4: Export
            await ws_manager.broadcast_to_session({
                "type": "status",
                "step": "export",
                "message": "Generating PowerPoint...",
                "progress": 90
            }, session_id)
            
            # Generate PPTX
            pptx_path = deck_engine.generate_presentation(verified_deck)
            
            await ws_manager.broadcast_to_session({
                "type": "complete",
                "step": "export",
                "message": "Deck ready!",
                "progress": 100,
                "deck_id": deck_id,
                "pptx_path": pptx_path
            }, session_id)
            
            return {
                "success": True,
                "deck_id": deck_id,
                "deck_data": verified_deck,
                "pptx_path": pptx_path
            }
        
    except Exception as e:
        await ws_manager.broadcast_to_session({
            "type": "error",
            "message": str(e)
        }, session_id)
        
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


# ==================== PPTX EXPORT ====================

@app.post("/api/deck/{deck_id}/export")
async def export_deck_pptx(deck_id: str):
    """Export deck as PowerPoint"""
    try:
        # Get deck from database
        deck_data = await db.get_deck(deck_id)
        
        if not deck_data:
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "Deck not found"}
            )
        
        # Generate PPTX
        pptx_path = deck_engine.generate_presentation(deck_data.slide_data)
        
        return {
            "success": True,
            "pptx_path": pptx_path
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/api/deck/{deck_id}/download")
async def download_deck_pptx(deck_id: str):
    """Download deck as PowerPoint file"""
    from fastapi.responses import FileResponse
    
    try:
        deck_data = await db.get_deck(deck_id)
        
        if not deck_data:
            return JSONResponse(
                status_code=404,
                content={"success": False, "error": "Deck not found"}
            )
        
        pptx_path = deck_engine.generate_presentation(deck_data.slide_data)
        
        return FileResponse(
            path=pptx_path,
            filename=f"{deck_data.company_name}_pitch_deck.pptx",
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


# ==================== DATABASE OPERATIONS ====================

@app.get("/api/decks")
async def list_decks():
    """List all decks"""
    decks = await db.list_decks()
    return {"decks": decks}


@app.get("/api/deck/{deck_id}")
async def get_deck(deck_id: str):
    """Get a specific deck"""
    deck = await db.get_deck(deck_id)
    if deck:
        return {"deck": deck}
    return JSONResponse(
        status_code=404,
        content={"error": "Deck not found"}
    )


@app.delete("/api/deck/{deck_id}")
async def delete_deck(deck_id: str):
    """Delete a deck"""
    success = await db.delete_deck(deck_id)
    return {"success": success}


# ==================== VERIFICATION ====================

@app.post("/api/verify")
async def verify_content(request: VerifyRequest):
    """Verify market data in content"""
    result = verification_engine._verify_market_data(request.content)
    return {
        "verified": result.is_verified,
        "confidence": result.confidence,
        "notes": result.notes
    }


# ==================== KNOWLEDGE BASE ====================

@app.get("/api/knowledge")
async def get_knowledge_documents():
    """Get all knowledge base documents"""
    from knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    docs = kb.get_documents()
    
    return {
        "documents": [
            {
                "id": d.id,
                "name": d.name,
                "doc_type": d.doc_type,
                "uploaded_at": d.uploaded_at
            }
            for d in docs
        ]
    }


@app.post("/api/knowledge/scan")
async def scan_knowledge_folder():
    """Scan knowledge base folder for new files"""
    from knowledge_base import KnowledgeBase
    kb = KnowledgeBase()
    count = kb.scan_uploaded_folder()
    
    return {"success": True, "added": count}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)