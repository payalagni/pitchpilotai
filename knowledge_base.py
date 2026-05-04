"""
Knowledge Base Manager
Upload and manage documents that the AI can reference for pitch deck generation
"""

import os
import json
import streamlit as st
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import hashlib


@dataclass
class KnowledgeDocument:
    """Represents a knowledge base document"""
    id: str
    name: str
    content: str
    doc_type: str  # 'company_info', 'market_research', 'competitor', 'template'
    uploaded_at: str
    file_type: str
    size: int


class KnowledgeBase:
    """Knowledge Base manager for storing and retrieving documents"""
    
    def __init__(self, storage_path: str = None):
        """Initialize knowledge base"""
        if storage_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            storage_path = os.path.join(base_dir, "knowledge_base")
        
        self.storage_path = storage_path
        self.uploaded_path = os.path.join(storage_path, "uploaded")
        self.index_file = os.path.join(storage_path, "index.json")
        self._ensure_storage()
    
    def _ensure_storage(self):
        """Ensure storage directory exists"""
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(os.path.join(self.storage_path, "documents"), exist_ok=True)
        os.makedirs(self.uploaded_path, exist_ok=True)
    
    def _load_index(self) -> Dict[str, Any]:
        """Load knowledge base index"""
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {"documents": [], "last_updated": None}
    
    def _save_index(self, index: Dict[str, Any]):
        """Save knowledge base index"""
        index["last_updated"] = datetime.now().isoformat()
        with open(self.index_file, 'w') as f:
            json.dump(index, f, indent=2)
    
    def _generate_id(self, content: str) -> str:
        """Generate unique document ID"""
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def add_document(
        self,
        name: str,
        content: str,
        doc_type: str = "company_info",
        file_type: str = "txt"
    ) -> KnowledgeDocument:
        """Add a document to knowledge base"""
        doc_id = self._generate_id(content + name)
        
        doc = KnowledgeDocument(
            id=doc_id,
            name=name,
            content=content,
            doc_type=doc_type,
            uploaded_at=datetime.now().isoformat(),
            file_type=file_type,
            size=len(content)
        )
        
        # Save document content
        doc_path = os.path.join(self.storage_path, "documents", f"{doc_id}.json")
        with open(doc_path, 'w') as f:
            json.dump(asdict(doc), f)
        
        # Update index
        index = self._load_index()
        index["documents"].append({
            "id": doc_id,
            "name": name,
            "doc_type": doc_type,
            "uploaded_at": doc.uploaded_at
        })
        self._save_index(index)
        
        return doc
    
    def get_documents(self, doc_type: str = None) -> List[KnowledgeDocument]:
        """Get all documents, optionally filtered by type"""
        index = self._load_index()
        docs = []
        
        for doc_info in index.get("documents", []):
            if doc_type and doc_info.get("doc_type") != doc_type:
                continue
            
            doc_path = os.path.join(self.storage_path, "documents", f"{doc_info['id']}.json")
            if os.path.exists(doc_path):
                with open(doc_path, 'r') as f:
                    doc_data = json.load(f)
                    docs.append(KnowledgeDocument(**doc_data))
        
        return docs
    
    def get_document(self, doc_id: str) -> Optional[KnowledgeDocument]:
        """Get a specific document by ID"""
        doc_path = os.path.join(self.storage_path, "documents", f"{doc_id}.json")
        if os.path.exists(doc_path):
            with open(doc_path, 'r') as f:
                doc_data = json.load(f)
                return KnowledgeDocument(**doc_data)
        return None
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from knowledge base"""
        doc_path = os.path.join(self.storage_path, "documents", f"{doc_id}.json")
        if os.path.exists(doc_path):
            os.remove(doc_path)
            
            # Update index
            index = self._load_index()
            index["documents"] = [d for d in index.get("documents", []) if d["id"] != doc_id]
            self._save_index(index)
            return True
        return False
    
    def search(self, query: str) -> List[KnowledgeDocument]:
        """Search documents by query"""
        docs = self.get_documents()
        query_lower = query.lower()
        
        results = []
        for doc in docs:
            if query_lower in doc.content.lower() or query_lower in doc.name.lower():
                results.append(doc)
        
        return results
    
    def get_context_for_prompt(self, company_name: str = None) -> str:
        """Get formatted context from knowledge base for AI prompt"""
        docs = self.get_documents()
        
        if not docs:
            return ""
        
        context_parts = ["=== KNOWLEDGE BASE CONTEXT ==="]
        
        # Group by type
        by_type = {}
        for doc in docs:
            if doc.doc_type not in by_type:
                by_type[doc.doc_type] = []
            by_type[doc.doc_type].append(doc)
        
        for doc_type, type_docs in by_type.items():
            context_parts.append(f"\n--- {doc_type.upper().replace('_', ' ')} ---")
            for doc in type_docs:
                context_parts.append(f"\n[{doc.name}]")
                context_parts.append(doc.content[:2000])  # Limit content length
        
        return "\n".join(context_parts)
    
    def scan_uploaded_folder(self):
        """Scan the uploaded folder for new files and add them to knowledge base"""
        import PyPDF2
        import docx
        from io import BytesIO
        
        added_count = 0
        
        for filename in os.listdir(self.uploaded_path):
            file_path = os.path.join(self.uploaded_path, filename)
            if not os.path.isfile(file_path):
                continue
            
            ext = os.path.splitext(filename)[1].lower()
            content = ""
            
            try:
                if ext in ['.txt', '.md']:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                elif ext == '.pdf':
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        content = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
                elif ext == '.docx':
                    doc = docx.Document(file_path)
                    content = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
                
                if content:
                    # Determine doc type from filename
                    doc_type = self._infer_doc_type(filename)
                    self.add_document(filename, content, doc_type, ext)
                    added_count += 1
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        
        return added_count
    
    def _infer_doc_type(self, filename: str) -> str:
        """Infer document type from filename"""
        filename_lower = filename.lower()
        if 'template' in filename_lower or 'layout' in filename_lower:
            return 'template'
        elif 'market' in filename_lower or 'research' in filename_lower:
            return 'market_research'
        elif 'competitor' in filename_lower or 'competition' in filename_lower:
            return 'competitor'
        elif 'company' in filename_lower or 'about' in filename_lower:
            return 'company_info'
        else:
            return 'other'


# Streamlit UI for Knowledge Base Management
def render_knowledge_base_manager():
    """Render knowledge base management UI"""
    st.subheader("📚 Knowledge Base")
    st.markdown("Upload documents that the AI will reference when generating pitch decks.")
    
    # Initialize knowledge base
    kb = KnowledgeBase()
    
    # Tab interface
    tab1, tab2, tab3 = st.tabs(["📤 Upload", "📁 My Documents", "🔍 Search"])
    
    with tab1:
        st.markdown("#### Upload New Document")
        
        # Document type selection
        doc_type = st.selectbox(
            "Document Type",
            ["company_info", "market_research", "competitor", "template", "other"],
            format_func=lambda x: {
                "company_info": "🏢 Company Information",
                "market_research": "📊 Market Research",
                "competitor": "⚔️ Competitor Analysis",
                "template": "📋 Pitch Template",
                "other": "📄 Other"
            }.get(x, x)
        )
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Document",
            type=['txt', 'md', 'pdf', 'docx']
        )
        
        # Or manual text input
        use_manual = st.checkbox("Or enter text manually")
        
        content = ""
        file_name = ""
        
        if use_manual:
            content = st.text_area("Document Content", height=200)
            file_name = st.text_input("Document Name", placeholder="My Company Info")
        elif uploaded_file:
            # Read file content
            if uploaded_file.name.endswith('.txt') or uploaded_file.name.endswith('.md'):
                content = uploaded_file.read().decode('utf-8', errors='ignore')
            elif uploaded_file.name.endswith('.pdf'):
                try:
                    import PyPDF2
                    from io import BytesIO
                    pdf_bytes = uploaded_file.read()
                    pdf_file = BytesIO(pdf_bytes)
                    reader = PyPDF2.PdfReader(pdf_file)
                    content = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")
                    content = ""
            elif uploaded_file.name.endswith('.docx'):
                try:
                    import docx
                    from io import BytesIO
                    doc_file = BytesIO(uploaded_file.read())
                    doc = docx.Document(doc_file)
                    content = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
                except Exception as e:
                    st.error(f"Error reading DOCX: {e}")
                    content = ""
            
            file_name = uploaded_file.name
        
        # Upload button
        if st.button("📥 Add to Knowledge Base", type="primary"):
            if content and file_name:
                doc = kb.add_document(
                    name=file_name,
                    content=content,
                    doc_type=doc_type,
                    file_type=os.path.splitext(file_name)[1] if '.' in file_name else 'txt'
                )
                st.success(f"✅ Added: {doc.name}")
                st.rerun()
            else:
                st.warning("Please provide both a document name and content.")
    
    with tab2:
        st.markdown("#### My Documents")
        
        # Get all documents
        docs = kb.get_documents()
        
        if not docs:
            st.info("No documents uploaded yet. Go to the Upload tab to add documents.")
        else:
            # Group by type
            by_type = {}
            for doc in docs:
                if doc.doc_type not in by_type:
                    by_type[doc.doc_type] = []
                by_type[doc.doc_type].append(doc)
            
            for doc_type, type_docs in by_type.items():
                with st.expander(f"📁 {doc_type.replace('_', ' ').title()} ({len(type_docs)} documents)"):
                    for doc in type_docs:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.markdown(f"**{doc.name}**")
                            st.caption(f"Uploaded: {doc.uploaded_at[:10]} | Size: {doc.size} chars")
                        with col2:
                            if st.button("👁️ View", key=f"view_{doc.id}"):
                                st.text_area("Content", doc.content, height=150, key=f"content_{doc.id}")
                        with col3:
                            if st.button("🗑️ Delete", key=f"del_{doc.id}"):
                                kb.delete_document(doc.id)
                                st.success("Deleted!")
                                st.rerun()
    
    with tab3:
        st.markdown("#### Search Knowledge Base")
        
        search_query = st.text_input("Search query", placeholder="Enter keywords...")
        
        if search_query:
            results = kb.search(search_query)
            
            if results:
                st.markdown(f"**Found {len(results)} matching documents:**")
                for doc in results:
                    with st.expander(f"📄 {doc.name}"):
                        st.markdown(f"**Type:** {doc.doc_type}")
                        st.markdown(f"**Content:**\n{doc.content[:500]}...")
            else:
                st.info("No matching documents found.")
    
    # Show context that will be used
    st.divider()
    with st.expander("ℹ️ How Knowledge Base is Used"):
        st.markdown("""
        When generating pitch decks, the AI will automatically include relevant 
        context from your knowledge base. This helps it understand:
        
        - **Company Info**: Your company's background, team, product details
        - **Market Research**: Industry data, market size figures
        - **Competitor Analysis**: Information about competitors
        - **Templates**: Preferred pitch deck structures
        """)


# Standalone functions
def get_knowledge_context(company_name: str = None) -> str:
    """Get knowledge base context for AI prompts"""
    kb = KnowledgeBase()
    return kb.get_context_for_prompt(company_name)


def add_to_knowledge(name: str, content: str, doc_type: str = "company_info") -> bool:
    """Add a document to knowledge base"""
    try:
        kb = KnowledgeBase()
        kb.add_document(name, content, doc_type)
        return True
    except Exception as e:
        print(f"Error adding to knowledge base: {e}")
        return False


if __name__ == "__main__":
    # Test
    kb = KnowledgeBase()
    print(f"Knowledge base initialized at: {kb.storage_path}")
    print(f"Documents: {len(kb.get_documents())}")