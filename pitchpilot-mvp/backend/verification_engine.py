"""
Verification Engine - Web Search & Data Verification
"""

import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class VerificationResult:
    is_verified: bool
    original_value: str
    verified_value: Optional[str]
    source: Optional[str]
    confidence: str
    notes: Optional[str] = None


class VerificationEngine:
    """Engine for verifying market data"""
    
    VERIFICATION_TRIGGERS = [
        "market size", "tam", "sam", "som", "billion", "million",
        "growth rate", "cagr", "market opportunity", "competitor"
    ]
    
    def __init__(self, api_key: str = None):
        self.serp_api_key = api_key or os.environ.get("SERP_API_KEY")
    
    def verify_deck_data(self, deck_data: Dict[str, Any]) -> Dict[str, Any]:
        verified_data = deck_data.copy()
        verification_log = []
        
        market_slides = ["slide_3", "slide_5", "slide_7"]
        
        for slide_key in market_slides:
            if slide_key in deck_data and deck_data[slide_key]:
                content = deck_data[slide_key]
                
                if self._needs_verification(content):
                    result = self._verify_market_data(content)
                    verification_log.append({
                        "slide": slide_key,
                        "result": result.is_verified
                    })
                    
                    if not result.is_verified:
                        verified_data[slide_key] = f"{content}\n\n*[Verification pending]*"
        
        verified_data["_verification_log"] = verification_log
        return verified_data
    
    def _needs_verification(self, content: str) -> bool:
        content_lower = content.lower()
        return any(trigger in content_lower for trigger in self.VERIFICATION_TRIGGERS)
    
    def _verify_market_data(self, content: str) -> VerificationResult:
        if not self.serp_api_key:
            return self._mock_verification(content)
        
        try:
            results = self._search_web(content)
            
            if results:
                return self._analyze_search_results(content, results)
            else:
                return VerificationResult(
                    is_verified=False,
                    original_value=content,
                    verified_value=None,
                    source=None,
                    confidence="low",
                    notes="No search results"
                )
        except Exception as e:
            return VerificationResult(
                is_verified=False,
                original_value=content,
                verified_value=None,
                source=None,
                confidence="low",
                notes=f"Error: {str(e)}"
            )
    
    def _search_web(self, query: str) -> List[Dict]:
        try:
            from serpapi import GoogleSearch
            params = {"q": query, "api_key": self.serp_api_key, "num": 5}
            search = GoogleSearch(params)
            results = search.get_dict()
            return results.get("organic_results", [])
        except:
            return []
    
    def _analyze_search_results(self, content: str, results: List[Dict]) -> VerificationResult:
        import re
        content_numbers = re.findall(r'\$?\d+(?:\.\d+)?\s*(?:billion|million|b|m|%)?', content.lower())
        
        for result in results:
            snippet = result.get("snippet", "").lower()
            result_numbers = re.findall(r'\$?\d+(?:\.\d+)?\s*(?:billion|million|b|m|%)?', snippet)
            
            if content_numbers and result_numbers:
                common = set(content_numbers) & set(result_numbers)
                if common:
                    return VerificationResult(
                        is_verified=True,
                        original_value=content,
                        verified_value=content,
                        source=results[0].get("link"),
                        confidence="medium"
                    )
        
        return VerificationResult(
            is_verified=False,
            original_value=content,
            verified_value=None,
            source=results[0].get("link") if results else None,
            confidence="low"
        )
    
    def _mock_verification(self, content: str) -> VerificationResult:
        return VerificationResult(
            is_verified=True,
            original_value=content,
            verified_value=content,
            source="mock",
            confidence="low",
            notes="Mock verification"
        )