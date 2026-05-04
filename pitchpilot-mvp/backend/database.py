"""
Database Module - SQLite with SQLAlchemy
"""

import os
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import select, delete


Base = declarative_base()


class Session(Base):
    """Session table"""
    __tablename__ = "sessions"
    
    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    company_name = Column(String(255))
    founder_name = Column(String(255))
    status = Column(String(50))
    metadata = Column(Text, nullable=True)


class Deck(Base):
    """Deck table"""
    __tablename__ = "decks"
    
    id = Column(String(36), primary_key=True)
    session_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    company_name = Column(String(255))
    founder_name = Column(String(255))
    slide_data = Column(Text)  # JSON string
    status = Column(String(50))
    pptx_path = Column(String(500), nullable=True)


class Database:
    """Database manager"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, "pitchpilot.db")
        
        self.db_path = db_path
        self.engine = None
        self.session_factory = None
    
    async def init_db(self):
        """Initialize database"""
        db_url = f"sqlite+aiosqlite:///{self.db_path}"
        self.engine = create_async_engine(db_url, echo=False)
        self.session_factory = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        
        # Create tables
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def _get_session(self) -> AsyncSession:
        """Get a database session"""
        if not self.session_factory:
            await self.init_db()
        return self.session_factory()
    
    async def save_deck(
        self,
        company_name: str,
        founder_name: str,
        slide_data: Dict[str, Any],
        status: str = "generated",
        session_id: str = None,
        pptx_path: str = None
    ) -> str:
        """Save a deck"""
        import uuid
        deck_id = str(uuid.uuid4())
        
        async with await self._get_session() as session:
            deck = Deck(
                id=deck_id,
                session_id=session_id,
                company_name=company_name,
                founder_name=founder_name,
                slide_data=json.dumps(slide_data),
                status=status,
                pptx_path=pptx_path
            )
            session.add(deck)
            await session.commit()
        
        return deck_id
    
    async def get_deck(self, deck_id: str) -> Optional[Deck]:
        """Get a deck by ID"""
        async with await self._get_session() as session:
            result = await session.execute(
                select(Deck).where(Deck.id == deck_id)
            )
            deck = result.scalar_one_or_none()
            
            if deck:
                # Convert to dict
                return Deck(
                    id=deck.id,
                    session_id=deck.session_id,
                    created_at=deck.created_at,
                    updated_at=deck.updated_at,
                    company_name=deck.company_name,
                    founder_name=deck.founder_name,
                    slide_data=json.loads(deck.slide_data) if deck.slide_data else {},
                    status=deck.status,
                    pptx_path=deck.pptx_path
                )
        return None
    
    async def list_decks(self) -> List[Dict[str, Any]]:
        """List all decks"""
        async with await self._get_session() as session:
            result = await session.execute(
                select(Deck).order_by(Deck.created_at.desc())
            )
            decks = result.scalars().all()
            
            return [
                {
                    "id": d.id,
                    "company_name": d.company_name,
                    "founder_name": d.founder_name,
                    "status": d.status,
                    "created_at": d.created_at.isoformat() if d.created_at else None,
                    "slide_count": len(json.loads(d.slide_data)) if d.slide_data else 0
                }
                for d in decks
            ]
    
    async def delete_deck(self, deck_id: str) -> bool:
        """Delete a deck"""
        async with await self._get_session() as session:
            result = await session.execute(
                delete(Deck).where(Deck.id == deck_id)
            )
            await session.commit()
            return result.rowcount > 0
    
    async def save_session(
        self,
        session_id: str,
        company_name: str,
        founder_name: str = "",
        status: str = "active",
        metadata: Dict = None
    ) -> bool:
        """Save a session"""
        async with await self._get_session() as session:
            session_obj = Session(
                id=session_id,
                company_name=company_name,
                founder_name=founder_name,
                status=status,
                metadata=json.dumps(metadata) if metadata else None
            )
            session.add(session_obj)
            await session.commit()
        return True
    
    async def get_session(self, session_id: str) -> Optional[Dict]:
        """Get a session"""
        async with await self._get_session() as session:
            result = await session.execute(
                select(Session).where(Session.id == session_id)
            )
            sess = result.scalar_one_or_none()
            
            if sess:
                return {
                    "id": sess.id,
                    "company_name": sess.company_name,
                    "founder_name": sess.founder_name,
                    "status": sess.status,
                    "metadata": json.loads(sess.metadata) if sess.metadata else {},
                    "created_at": sess.created_at.isoformat() if sess.created_at else None
                }
        return None