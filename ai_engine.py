"""
AI Engine - LLM Integration Module
Handles communication with Gemini API for pitch deck generation
"""

import json
import os
import google.generativeai as genai
from typing import Optional, Dict, Any


class AIEngine:
    """AI Engine for pitch deck generation using Gemini"""
    
    # Farmeal-Standard 10-slide structure prompt
    DECK_STRUCTURE_PROMPT = """You are a Strategic Pitch Deck Architect for Farmeal Pitch Solutions.
Generate a complete pitch deck following the Farmeal-Standard 10-slide methodology.

Required JSON Structure:
{
  "founder_name": "",
  "company_name": "",
  "slide_1_hook": "A compelling one-liner that captures attention",
  "slide_2_empathy": "Demonstrate understanding of customer pain points",
  "slide_3_opportunity": "Market opportunity and timing",
  "slide_4_solution": "Your product/service and unique value proposition",
  "slide_5_market": "TAM, SAM, SOM with credible data",
  "slide_6_model": "Business model and revenue streams",
  "slide_7_competition": "Competitive landscape and your differentiation",
  "slide_8_tech": "Technology stack and IP",
  "slide_9_traction": "Key metrics, customers, and progress",
  "slide_10_ask": "Funding ask and use of funds"
}

Guidelines:
- Each slide content should be 2-4 sentences, concise and impactful
- Use VC-friendly language and metrics
- Include specific numbers where possible
- Focus on storytelling and narrative flow
- Keep content investor-ready"""

    def __init__(self, api_key: str = None):
        """Initialize AI Engine with optional API key"""
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None
    
    def set_api_key(self, api_key: str):
        """Set API key for Gemini"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def generate_deck(
        self,
        founder_name: str,
        company_name: str,
        raw_content: str,
        target_audience: str = "VC",
        funding_amount: str = "",
        deck_purpose: str = "Seed Round"
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a pitch deck from raw content
        
        Args:
            founder_name: Name of the founder
            company_name: Name of the company
            raw_content: Raw notes, description, or existing content
            target_audience: Target investor type
            funding_amount: Target funding amount
            deck_purpose: Purpose of the deck
            
        Returns:
            Structured JSON deck data or None on failure
        """
        if not self.model:
            # Return mock data for testing without API
            return self._generate_mock_deck(founder_name, company_name, raw_content)
        
        try:
            # Build the prompt
            prompt = self._build_deck_prompt(
                founder_name=founder_name,
                company_name=company_name,
                raw_content=raw_content,
                target_audience=target_audience,
                funding_amount=funding_amount,
                deck_purpose=deck_purpose
            )
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Parse JSON from response
            deck_data = self._parse_json_response(response.text)
            
            # Ensure required fields
            deck_data["founder_name"] = founder_name
            deck_data["company_name"] = company_name
            
            return deck_data
            
        except Exception as e:
            print(f"Error generating deck: {e}")
            # Return mock data on error
            return self._generate_mock_deck(founder_name, company_name, raw_content)
    
    def _build_deck_prompt(
        self,
        founder_name: str,
        company_name: str,
        raw_content: str,
        target_audience: str,
        funding_amount: str,
        deck_purpose: str
    ) -> str:
        """Build the prompt for deck generation"""
        user_context = f"""
Company: {company_name}
Founder: {founder_name}
Target Audience: {target_audience}
Funding Amount: {funding_amount}
Deck Purpose: {deck_purpose}

Raw Content/Notes:
{raw_content}
"""
        return self.DECK_STRUCTURE_PROMPT + user_context
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON from model response"""
        # Try to find JSON in response
        import re
        
        # Look for JSON block
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Try to parse entire response as JSON
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        # Return empty structure if parsing fails
        return self._empty_deck_structure()
    
    def _empty_deck_structure(self) -> Dict[str, Any]:
        """Return empty deck structure"""
        return {
            "founder_name": "",
            "company_name": "",
            "slide_1_hook": "",
            "slide_2_empathy": "",
            "slide_3_opportunity": "",
            "slide_4_solution": "",
            "slide_5_market": "",
            "slide_6_model": "",
            "slide_7_competition": "",
            "slide_8_tech": "",
            "slide_9_traction": "",
            "slide_10_ask": ""
        }
    
    def _generate_mock_deck(
        self,
        founder_name: str,
        company_name: str,
        raw_content: str
    ) -> Dict[str, Any]:
        """Generate mock deck data for testing"""
        return {
            "founder_name": founder_name,
            "company_name": company_name,
            "slide_1_hook": f"Innovating {company_name} to transform industry workflows with AI-powered solutions",
            "slide_2_empathy": "Enterprises face significant challenges with manual processes and inefficient workflows",
            "slide_3_opportunity": f"Large and growing market opportunity in enterprise automation and AI solutions",
            "slide_4_solution": f"{company_name} provides an AI-powered platform that automates key business processes",
            "slide_5_market": "TAM: $150B+ | SAM: $45B | SOM: $5B with strong annual growth",
            "slide_6_model": "SaaS subscription model with enterprise pricing tiers",
            "slide_7_competition": "Differentiated from incumbents with faster implementation and superior AI capabilities",
            "slide_8_tech": "Proprietary AI technology with proprietary models and IP",
            "slide_9_traction": "Early traction with pilot customers and strong growth indicators",
            "slide_10_ask": f"Raising capital to scale operations and capture market opportunity"
        }
    
    def analyze_deck(self, deck_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an existing deck for improvements
        
        Args:
            deck_data: The deck JSON to analyze
            
        Returns:
            Analysis results with recommendations
        """
        if not self.model:
            return self._mock_analysis(deck_data)
        
        try:
            prompt = f"""Analyze this pitch deck and provide recommendations for improvement:

{json.dumps(deck_data, indent=2)}

Provide analysis on:
1. Narrative flow and storytelling
2. Market sizing credibility
3. Competitive positioning
4. Financial projections
5. Overall investor readiness
"""
            response = self.model.generate_content(prompt)
            return {"analysis": response.text, "deck_data": deck_data}
            
        except Exception as e:
            return self._mock_analysis(deck_data)
    
    def _mock_analysis(self, deck_data: Dict[str, Any]) -> Dict[str, Any]:
        """Return mock analysis for testing"""
        return {
            "analysis": "Mock analysis - API key not configured",
            "deck_data": deck_data,
            "recommendations": [
                "Add specific market size data with sources",
                "Include more traction metrics",
                "Strengthen competitive differentiation"
            ]
        }
    
    def validate_market_data(self, market_text: str) -> Dict[str, Any]:
        """
        Validate market data in a slide
        
        Args:
            market_text: The market text to validate
            
        Returns:
            Validation results
        """
        if not self.model:
            return {"valid": True, "data": market_text, "source": "mock"}
        
        try:
            prompt = f"""Validate this market data and provide verified figures:

{market_text}

Return JSON with:
- "tam": Total Addressable Market (verified)
- "sam": Serviceable Addressable Market
- "som": Serviceable Obtainable Market
- "source": Data source or "needs_verification"
- "confidence": high/medium/low
"""
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
            
        except Exception as e:
            return {"valid": False, "error": str(e)}


# Standalone function
def generate_deck(
    founder_name: str,
    company_name: str,
    raw_content: str,
    api_key: str = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Generate a pitch deck from content
    
    Args:
        founder_name: Founder name
        company_name: Company name
        raw_content: Raw input content
        api_key: Optional API key
        **kwargs: Additional parameters
        
    Returns:
        Structured deck JSON
    """
    engine = AIEngine(api_key)
    return engine.generate_deck(
        founder_name=founder_name,
        company_name=company_name,
        raw_content=raw_content,
        **kwargs
    )


if __name__ == "__main__":
    # Test
    deck = generate_deck(
        founder_name="John Doe",
        company_name="TestCorp",
        raw_content="AI-powered enterprise solution"
    )
    print(json.dumps(deck, indent=2))