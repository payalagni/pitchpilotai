"""
Verification Engine - Web Search & Data Verification Module
Verifies market data and finds credible sources for pitch deck content
"""

import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class VerificationResult:
    """Result of a verification check"""
    is_verified: bool
    original_value: str
    verified_value: Optional[str]
    source: Optional[str]
    confidence: str  # high, medium, low
    notes: Optional[str] = None


class VerificationEngine:
    """Engine for verifying market data and finding credible sources"""
    
    # Keywords that trigger verification
    VERIFICATION_TRIGGERS = [
        "market size", "tam", "sam", "som", "billion", "million",
        "growth rate", "cagr", "market opportunity", "competitor",
        "competition", "industry leader", "market share"
    ]
    
    def __init__(self, api_key: str = None):
        """Initialize verification engine"""
        self.serp_api_key = api_key or os.environ.get("SERP_API_KEY")
        self.search_results = []
    
    def verify_deck_data(self, deck_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify all market-related data in deck JSON
        
        Args:
            deck_data: The deck JSON to verify
            
        Returns:
            Verified deck data with additional metadata
        """
        verified_data = deck_data.copy()
        verification_log = []
        
        # Check slides that typically contain market data
        market_slides = ["slide_3", "slide_5", "slide_7"]
        
        for slide_key in market_slides:
            if slide_key in deck_data and deck_data[slide_key]:
                content = deck_data[slide_key]
                
                # Check if verification is needed
                if self._needs_verification(content):
                    result = self._verify_market_data(content)
                    verification_log.append({
                        "slide": slide_key,
                        "result": result
                    })
                    
                    # Add verification note to content
                    if not result.is_verified:
                        verified_data[slide_key] = f"{content}\n\n*[Verification pending - data needs confirmation]*"
        
        # Store verification log
        verified_data["_verification_log"] = verification_log
        
        return verified_data
    
    def _needs_verification(self, content: str) -> bool:
        """Check if content needs verification"""
        content_lower = content.lower()
        return any(trigger in content_lower for trigger in self.VERIFICATION_TRIGGERS)
    
    def _verify_market_data(self, content: str) -> VerificationResult:
        """
        Verify market data using web search
        
        Args:
            content: The content to verify
            
        Returns:
            VerificationResult object
        """
        if not self.serp_api_key:
            # Return mock verification if no API key
            return self._mock_verification(content)
        
        try:
            # Perform search
            results = self._search_web(content)
            
            if results:
                # Analyze results and return verification
                return self._analyze_search_results(content, results)
            else:
                return VerificationResult(
                    is_verified=False,
                    original_value=content,
                    verified_value=None,
                    source=None,
                    confidence="low",
                    notes="No search results found"
                )
                
        except Exception as e:
            return VerificationResult(
                is_verified=False,
                original_value=content,
                verified_value=None,
                source=None,
                confidence="low",
                notes=f"Verification error: {str(e)}"
            )
    
    def _search_web(self, query: str) -> List[Dict]:
        """Perform web search using SerpAPI"""
        try:
            from serpapi import GoogleSearch
            
            params = {
                "q": query,
                "api_key": self.serp_api_key,
                "num": 5
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            return results.get("organic_results", [])
            
        except ImportError:
            # SerpAPI not installed
            return []
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def _analyze_search_results(self, content: str, results: List[Dict]) -> VerificationResult:
        """Analyze search results to verify content"""
        # Simple analysis - look for matching figures
        content_numbers = self._extract_numbers(content)
        
        for result in results:
            snippet = result.get("snippet", "").lower()
            result_numbers = self._extract_numbers(snippet)
            
            # Check for matching numbers
            if content_numbers and result_numbers:
                common = set(content_numbers) & set(result_numbers)
                if common:
                    return VerificationResult(
                        is_verified=True,
                        original_value=content,
                        verified_value=content,
                        source=results[0].get("link"),
                        confidence="medium",
                        notes=f"Found matching data: {common}"
                    )
        
        # No direct match found
        return VerificationResult(
            is_verified=False,
            original_value=content,
            verified_value=None,
            source=results[0].get("link") if results else None,
            confidence="low",
            notes="Could not verify specific figures"
        )
    
    def _extract_numbers(self, text: str) -> List[str]:
        """Extract numeric values from text"""
        import re
        # Match billion, million, percentages
        pattern = r'\$?\d+(?:\.\d+)?\s*(?:billion|million|b|m|%)?'
        return re.findall(pattern, text.lower())
    
    def _mock_verification(self, content: str) -> VerificationResult:
        """Return mock verification for testing"""
        return VerificationResult(
            is_verified=True,
            original_value=content,
            verified_value=content,
            source="mock_source",
            confidence="low",
            notes="Mock verification - API key not configured"
        )
    
    def verify_competitor(self, competitor_name: str) -> Dict[str, Any]:
        """
        Verify competitor information
        
        Args:
            competitor_name: Name of competitor to verify
            
        Returns:
            Competitor information
        """
        if not self.serp_api_key:
            return self._mock_competitor_info(competitor_name)
        
        try:
            query = f"{competitor_name} company funding valuation"
            results = self._search_web(query)
            
            if results:
                return {
                    "name": competitor_name,
                    "verified": True,
                    "data": results[0].get("snippet", ""),
                    "source": results[0].get("link")
                }
        except Exception as e:
            pass
        
        return self._mock_competitor_info(competitor_name)
    
    def _mock_competitor_info(self, name: str) -> Dict[str, Any]:
        """Return mock competitor info"""
        return {
            "name": name,
            "verified": False,
            "data": f"Information for {name}",
            "source": None,
            "notes": "Mock data - API not configured"
        }
    
    def find_market_data(self, industry: str) -> Dict[str, Any]:
        """
        Find market data for an industry
        
        Args:
            industry: Industry to find market data for
            
        Returns:
            Market data with sources
        """
        if not self.serp_api_key:
            return self._mock_market_data(industry)
        
        try:
            query = f"{industry} market size TAM SAM 2024 2025"
            results = self._search_web(query)
            
            if results:
                return {
                    "industry": industry,
                    "data": [r.get("snippet") for r in results[:3]],
                    "sources": [r.get("link") for r in results[:3]]
                }
        except Exception as e:
            pass
        
        return self._mock_market_data(industry)
    
    def _mock_market_data(self, industry: str) -> Dict[str, Any]:
        """Return mock market data"""
        return {
            "industry": industry,
            "tam": "To be researched",
            "sam": "To be researched",
            "som": "To be researched",
            "sources": [],
            "notes": "Mock data - Configure SERP_API_KEY for live data"
        }


# Standalone function
def verify_market_data(deck_data: Dict[str, Any], api_key: str = None) -> Dict[str, Any]:
    """
    Verify market data in deck
    
    Args:
        deck_data: Deck JSON to verify
        api_key: Optional API key
        
    Returns:
        Verified deck data
    """
    engine = VerificationEngine(api_key)
    return engine.verify_deck_data(deck_data)


if __name__ == "__main__":
    # Test
    test_deck = {
        "company_name": "TestCorp",
        "slide_5_market": "TAM: $150B, SAM: $45B, growing at 25% CAGR",
        "slide_7_competition": "vs UiPath and Automation Anywhere"
    }
    
    verified = verify_market_data(test_deck)
    print(json.dumps(verified, indent=2))