"""
AI Engine - LLM Integration Module
"""

import json
import os
import google.generativeai as genai
from typing import Optional, Dict, Any


class AIEngine:
    """AI Engine for pitch deck generation using Gemini"""
    
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
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None
    
    def set_api_key(self, api_key: str):
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
        if not self.model:
            return self._generate_mock_deck(founder_name, company_name, raw_content)
        
        try:
            prompt = self._build_deck_prompt(
                founder_name=founder_name,
                company_name=company_name,
                raw_content=raw_content,
                target_audience=target_audience,
                funding_amount=funding_amount,
                deck_purpose=deck_purpose
            )
            
            response = self.model.generate_content(prompt)
            deck_data = self._parse_json_response(response.text)
            
            deck_data["founder_name"] = founder_name
            deck_data["company_name"] = company_name
            
            return deck_data
            
        except Exception as e:
            print(f"Error generating deck: {e}")
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
        import re
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        return self._empty_deck_structure()
    
    def _empty_deck_structure(self) -> Dict[str, Any]:
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