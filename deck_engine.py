"""
Deck Engine - PowerPoint Generation Module
Transforms structured JSON data into downloadable PPTX files
Following Farmeal-Standard 10-Slide Methodology
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import nsmap
from pptx.oxml import parse_xml


class DeckEngine:
    """Engine for generating PowerPoint presentations from JSON data"""
    
    # Slide layout indices (standard in pptx)
    TITLE_SLIDE_LAYOUT = 0
    TITLE_CONTENT_LAYOUT = 1
    BLANK_LAYOUT = 6
    
    # Color scheme (Farmeal-Standard)
    PRIMARY_COLOR = RGBColor(0, 51, 102)      # Dark Blue
    ACCENT_COLOR = RGBColor(0, 120, 212)      # Bright Blue
    TEXT_COLOR = RGBColor(51, 51, 51)         # Dark Gray
    LIGHT_TEXT_COLOR = RGBColor(128, 128, 128) # Medium Gray
    BACKGROUND_COLOR = RGBColor(255, 255, 255) # White
    
    def __init__(self):
        self.slide_templates = self._define_slide_templates()
    
    def _define_slide_templates(self):
        """Define slide titles and descriptions for Farmeal-Standard"""
        return {
            1: {"title": "The Hook", "description": "Captivate attention with a compelling problem/solution"},
            2: {"title": "Empathy", "description": "Show understanding of customer pain points"},
            3: {"title": "Opportunity", "description": "Present the market opportunity"},
            4: {"title": "Solution", "description": "Introduce your product/service"},
            5: {"title": "Market", "description": "Market size and growth potential"},
            6: {"title": "Business Model", "description": "How you make money"},
            7: {"title": "Competition", "description": "Competitive landscape"},
            8: {"title": "Technology", "description": "Technical differentiation"},
            9: {"title": "Traction", "description": "Progress and metrics"},
            10: {"title": "The Ask", "description": "Funding requirements and use of funds"}
        }
    
    def generate_presentation(self, deck_data: dict, output_path: str = None) -> str:
        """
        Generate a PowerPoint presentation from deck JSON data
        
        Args:
            deck_data: Structured JSON with slide content
            output_path: Optional custom output path
            
        Returns:
            Path to generated PPTX file
        """
        # Create presentation
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        
        # Generate each slide
        for slide_num in range(1, 11):
            slide_key = f"slide_{slide_num}"
            content = deck_data.get(slide_key, "")
            
            if slide_num == 1:
                self._create_title_slide(prs, deck_data, content)
            else:
                self._create_content_slide(prs, slide_num, deck_data, content)
        
        # Determine output path
        if not output_path:
            company_name = deck_data.get("company_name", "pitch_deck")
            # Sanitize filename
            company_name = "".join(c for c in company_name if c.isalnum() or c in " -_").strip()
            output_dir = os.path.dirname(os.path.abspath(__file__)) if os.path.dirname(__file__) else "."
            output_path = os.path.join(output_dir, f"{company_name}_pitch_deck.pptx")
        
        # Save presentation
        prs.save(output_path)
        return output_path
    
    def _create_title_slide(self, prs: Presentation, deck_data: dict, content: str):
        """Create the title/hook slide"""
        slide_layout = prs.slide_layouts[self.TITLE_SLIDE_LAYOUT]
        slide = prs.slides.add_slide(slide_layout)
        
        # Company name
        company_name = deck_data.get("company_name", "")
        if company_name:
            title = slide.shapes.title
            title.text = company_name
        
        # Founder name and hook subtitle
        subtitle = slide.placeholders[1]
        founder_name = deck_data.get("founder_name", "")
        subtitle_text = founder_name + "\n" + content if founder_name else content
        subtitle.text = subtitle_text
    
    def _create_content_slide(self, prs: Presentation, slide_num: int, 
                              deck_data: dict, content: str):
        """Create a standard content slide"""
        slide_layout = prs.slide_layouts[self.TITLE_CONTENT_LAYOUT]
        slide = prs.slides.add_slide(slide_layout)
        
        # Slide title
        title = slide.shapes.title
        template = self.slide_templates.get(slide_num, {"title": f"Slide {slide_num}"})
        title.text = template["title"]
        
        # Apply title styling
        self._style_title(title)
        
        # Content
        content_placeholder = slide.placeholders[1]
        text_frame = content_placeholder.text_frame
        text_frame.clear()
        
        # Add content with proper formatting
        if content:
            self._add_formatted_content(text_frame, content)
        
        # Apply content styling
        self._style_content(content_placeholder)
    
    def _style_title(self, title_shape):
        """Apply styling to slide titles"""
        for paragraph in title_shape.text_frame.paragraphs:
            paragraph.font.size = Pt(32)
            paragraph.font.bold = True
            paragraph.font.color.rgb = self.PRIMARY_COLOR
            paragraph.alignment = PP_ALIGN.LEFT
    
    def _style_content(self, content_placeholder):
        """Apply styling to slide content"""
        for paragraph in content_placeholder.text_frame.paragraphs:
            paragraph.font.size = Pt(18)
            paragraph.font.color.rgb = self.TEXT_COLOR
            paragraph.space_before = Pt(12)
            paragraph.space_after = Pt(12)
    
    def _add_formatted_content(self, text_frame, content: str):
        """Add content with proper paragraph formatting"""
        # Split content into paragraphs
        paragraphs = content.split("\n\n")
        
        for i, para_text in enumerate(paragraphs):
            para_text = para_text.strip()
            if not para_text:
                continue
            
            # Create paragraph
            if i == 0:
                p = text_frame.paragraphs[0]
            else:
                p = text_frame.add_paragraph()
            
            p.text = para_text
            p.font.size = Pt(18)
            p.font.color.rgb = self.TEXT_COLOR
            p.space_before = Pt(12)
            p.space_after = Pt(12)
    
    def create_template(self, output_path: str):
        """
        Create a blank template presentation
        
        Args:
            output_path: Path to save the template
        """
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        
        # Add title slide
        slide_layout = prs.slide_layouts[self.TITLE_SLIDE_LAYOUT]
        slide = prs.slides.add_slide(slide_layout)
        title = slide.shapes.title
        title.text = "Company Name"
        
        subtitle = slide.placeholders[1]
        subtitle.text = "Founder Name | Tagline"
        
        # Add placeholder content slides
        for slide_num in range(1, 11):
            slide_layout = prs.slide_layouts[self.TITLE_CONTENT_LAYOUT]
            slide = prs.slides.add_slide(slide_layout)
            
            title = slide.shapes.title
            template = self.slide_templates.get(slide_num, {"title": f"Slide {slide_num}"})
            title.text = template["title"]
            
            content = slide.placeholders[1]
            content.text = template["description"]
        
        prs.save(output_path)
        return output_path
    
    def validate_deck_data(self, deck_data: dict) -> tuple[bool, list]:
        """
        Validate deck JSON data structure
        
        Args:
            deck_data: The JSON data to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Required top-level fields
        required_fields = ["founder_name", "company_name"]
        for field in required_fields:
            if field not in deck_data:
                errors.append(f"Missing required field: {field}")
        
        # Slide fields (1-10)
        for i in range(1, 11):
            slide_key = f"slide_{i}"
            if slide_key not in deck_data:
                errors.append(f"Missing slide content: {slide_key}")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def get_slide_preview(self, deck_data: dict) -> list:
        """
        Get preview of all slides
        
        Args:
            deck_data: The deck JSON data
            
        Returns:
            List of slide preview dictionaries
        """
        previews = []
        
        for slide_num in range(1, 11):
            slide_key = f"slide_{slide_num}"
            template = self.slide_templates.get(slide_num, {"title": f"Slide {slide_num}"})
            
            preview = {
                "slide_number": slide_num,
                "title": template["title"],
                "description": template["description"],
                "content": deck_data.get(slide_key, "")
            }
            previews.append(preview)
        
        return previews


# Standalone function for direct usage
def generate_pitch_deck(deck_data: dict, output_path: str = None) -> str:
    """
    Generate a pitch deck from JSON data
    
    Args:
        deck_data: Structured JSON with slide content
        output_path: Optional output file path
        
    Returns:
        Path to generated PPTX file
    """
    engine = DeckEngine()
    return engine.generate_presentation(deck_data, output_path)


if __name__ == "__main__":
    # Test with sample data
    sample_deck = {
        "founder_name": "John Doe",
        "company_name": "Acme AI",
        "slide_1_hook": "Revolutionizing enterprise productivity with AI-powered automation",
        "slide_2_empathy": "Enterprises lose $2.5M annually due to inefficient workflows and manual processes",
        "slide_3_opportunity": "$150B enterprise automation market growing at 25% annually",
        "slide_4_solution": "AI platform that automates 70% of repetitive enterprise tasks",
        "slide_5_market": "TAM: $150B | SAM: $45B | SOM: $5B",
        "slide_6_model": "SaaS subscription: $50K-500K ARR per enterprise",
        "slide_7_competition": "vs UiPath, Automation Anywhere: 10x faster implementation",
        "slide_8_tech": "Proprietary LLM fine-tuned on enterprise data with 95% accuracy",
        "slide_9_traction": "$2M ARR | 45 enterprise customers | 3x YoY growth",
        "slide_10_ask": "Raising $5M at $20M pre-money for Series A"
    }
    
    output = generate_pitch_deck(sample_deck)
    print(f"Generated: {output}")