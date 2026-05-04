"""
File Processor - Handle file uploads and extraction
"""

import os
import io
from typing import Optional


class FileProcessor:
    """Process uploaded files"""
    
    def process_file_content(self, filename: str, content: bytes) -> str:
        """Process file based on type"""
        ext = os.path.splitext(filename)[1].lower()
        
        if ext in ['.txt', '.md']:
            return content.decode('utf-8', errors='ignore')
        
        elif ext == '.pdf':
            return self._process_pdf(content)
        
        elif ext == '.docx':
            return self._process_docx(content)
        
        elif ext in ['.png', '.jpg', '.jpeg']:
            return self._process_image(content)
        
        return f"[Unsupported file type: {ext}]"
    
    def _process_pdf(self, content: bytes) -> str:
        try:
            import PyPDF2
            from io import BytesIO
            pdf_file = BytesIO(content)
            reader = PyPDF2.PdfReader(pdf_file)
            
            text_parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            
            return "\n\n".join(text_parts)
        except Exception as e:
            return f"[PDF processing error: {str(e)}]"
    
    def _process_docx(self, content: bytes) -> str:
        try:
            import docx
            from io import BytesIO
            doc_file = BytesIO(content)
            doc = docx.Document(doc_file)
            
            return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        except Exception as e:
            return f"[DOCX processing error: {str(e)}]"
    
    def _process_image(self, content: bytes) -> str:
        try:
            from PIL import Image
            import pytesseract
            from io import BytesIO
            
            image = Image.open(BytesIO(content))
            text = pytesseract.image_to_string(image)
            
            return f"[OCR Extracted]\n{text}"
        except Exception as e:
            return f"[Image processing error: {str(e)}]"