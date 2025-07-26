#!/usr/bin/env python3
"""
Custom Tools for Multi-Agent Campaign System
Tools for interacting with Store API and Impact.com API
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from crewai.tools import tool
from logger import log_api_call

# API Configuration
STORE_API_BASE = "http://localhost:6000/api/store"
IMPACT_API_BASE = "http://localhost:6000/api/impact"

# =============================================================================
# STORE API TOOLS
# =============================================================================

@tool("fetch_all_products")
def fetch_all_products() -> str:
    """
    Fetch all products from the store API.
    Returns a JSON string with product details including id, name, category, price, stock, page_views, sales.
    """
    start_time = time.time()
    endpoint = f"{STORE_API_BASE}/products"
    
    try:
        response = requests.get(endpoint, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        duration_ms = (time.time() - start_time) * 1000
        
        # Log the API call
        log_api_call(
            tool_name="fetch_all_products",
            endpoint=endpoint,
            request_data={},
            response_data={"status": data["status"], "count": len(data.get("data", []))},
            duration_ms=duration_ms,
            success=data["status"] == "success"
        )
        
        if data["status"] == "success":
            return json.dumps(data["data"], indent=2)
        else:
            return f"Error: {data.get('message', 'Unknown error')}"
            
    except requests.RequestException as e:
        duration_ms = (time.time() - start_time) * 1000
        log_api_call(
            tool_name="fetch_all_products",
            endpoint=endpoint,
            request_data={},
            response_data={"error": str(e)},
            duration_ms=duration_ms,
            success=False
        )
        return f"API Error: Failed to fetch products - {str(e)}"

@tool("fetch_product_details")
def fetch_product_details(product_id: int) -> str:
    """
    Fetch detailed information for a specific product.
    
    Args:
        product_id: The ID of the product to fetch
        
    Returns:
        JSON string with detailed product information including real-time metrics
    """
    try:
        response = requests.get(f"{STORE_API_BASE}/products/{product_id}", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data["status"] == "success":
            return json.dumps(data["data"], indent=2)
        else:
            return f"Error: {data.get('message', 'Product not found')}"
            
    except requests.RequestException as e:
        return f"API Error: Failed to fetch product {product_id} - {str(e)}"

@tool("fetch_product_analytics")
def fetch_product_analytics(product_id: int) -> str:
    """
    Fetch detailed analytics for a specific product including performance metrics.
    
    Args:
        product_id: The ID of the product to get analytics for
        
    Returns:
        JSON string with analytics data including page views, sales, revenue changes
    """
    try:
        response = requests.get(f"{STORE_API_BASE}/products/{product_id}/analytics", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data["status"] == "success":
            return json.dumps(data["data"], indent=2)
        else:
            return f"Error: {data.get('message', 'Analytics not found')}"
            
    except requests.RequestException as e:
        return f"API Error: Failed to fetch analytics for product {product_id} - {str(e)}"

# =============================================================================
# IMPACT.COM API TOOLS
# =============================================================================

@tool("create_campaign")
def create_campaign(product_id: int, campaign_name: str, budget: float, 
                   duration_days: int = 7, campaign_copy: str = "") -> str:
    """
    Create a new ad campaign on Impact.com for a specific product.
    
    Args:
        product_id: The ID of the product to advertise
        campaign_name: Name for the campaign
        budget: Campaign budget in USD
        duration_days: How many days the campaign should run (default: 7)
        campaign_copy: Ad copy text (optional)
        
    Returns:
        JSON string with campaign creation response including campaign_id
    """
    start_time = time.time()
    endpoint = f"{IMPACT_API_BASE}/campaigns"
    
    try:
        payload = {
            "product_id": product_id,
            "campaign_name": campaign_name,
            "budget": budget,
            "duration_days": duration_days,
            "campaign_copy": campaign_copy
        }
        
        response = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        response.raise_for_status()
        
        data = response.json()
        duration_ms = (time.time() - start_time) * 1000
        
        # Log the API call
        log_api_call(
            tool_name="create_campaign",
            endpoint=endpoint,
            request_data=payload,
            response_data={"status": data["status"], "campaign_id": data.get("data", {}).get("campaign_id")},
            duration_ms=duration_ms,
            success=data["status"] == "success"
        )
        
        if data["status"] == "success":
            return json.dumps(data["data"], indent=2)
        else:
            return f"Error: {data.get('message', 'Campaign creation failed')}"
            
    except requests.RequestException as e:
        duration_ms = (time.time() - start_time) * 1000
        log_api_call(
            tool_name="create_campaign",
            endpoint=endpoint,
            request_data=payload,
            response_data={"error": str(e)},
            duration_ms=duration_ms,
            success=False
        )
        return f"API Error: Failed to create campaign - {str(e)}"

@tool("fetch_campaign_details")
def fetch_campaign_details(campaign_id: str) -> str:
    """
    Fetch detailed information and performance metrics for a specific campaign.
    
    Args:
        campaign_id: The ID of the campaign to fetch
        
    Returns:
        JSON string with campaign details and performance metrics
    """
    try:
        response = requests.get(f"{IMPACT_API_BASE}/campaigns/{campaign_id}", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data["status"] == "success":
            return json.dumps(data["data"], indent=2)
        else:
            return f"Error: {data.get('message', 'Campaign not found')}"
            
    except requests.RequestException as e:
        return f"API Error: Failed to fetch campaign {campaign_id} - {str(e)}"

@tool("fetch_all_campaigns")
def fetch_all_campaigns() -> str:
    """
    Fetch all active campaigns and their performance metrics.
    
    Returns:
        JSON string with list of all campaigns and their current metrics
    """
    try:
        response = requests.get(f"{IMPACT_API_BASE}/campaigns", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data["status"] == "success":
            return json.dumps(data["data"], indent=2)
        else:
            return f"Error: {data.get('message', 'Failed to fetch campaigns')}"
            
    except requests.RequestException as e:
        return f"API Error: Failed to fetch campaigns - {str(e)}"

@tool("pause_campaign")
def pause_campaign(campaign_id: str) -> str:
    """
    Pause a running campaign.
    
    Args:
        campaign_id: The ID of the campaign to pause
        
    Returns:
        JSON string with pause operation result
    """
    try:
        response = requests.post(f"{IMPACT_API_BASE}/campaigns/{campaign_id}/pause", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data["status"] == "success":
            return json.dumps({"action": "paused", "campaign_id": campaign_id, "status": "success"}, indent=2)
        else:
            return f"Error: {data.get('message', 'Failed to pause campaign')}"
            
    except requests.RequestException as e:
        return f"API Error: Failed to pause campaign {campaign_id} - {str(e)}"

@tool("resume_campaign")
def resume_campaign(campaign_id: str) -> str:
    """
    Resume a paused campaign.
    
    Args:
        campaign_id: The ID of the campaign to resume
        
    Returns:
        JSON string with resume operation result
    """
    try:
        response = requests.post(f"{IMPACT_API_BASE}/campaigns/{campaign_id}/resume", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data["status"] == "success":
            return json.dumps({"action": "resumed", "campaign_id": campaign_id, "status": "success"}, indent=2)
        else:
            return f"Error: {data.get('message', 'Failed to resume campaign')}"
            
    except requests.RequestException as e:
        return f"API Error: Failed to resume campaign {campaign_id} - {str(e)}"

# =============================================================================
# UTILITY TOOLS
# =============================================================================

@tool("check_api_health")
def check_api_health() -> str:
    """
    Check if the API server is running and healthy.
    
    Returns:
        JSON string with API health status
    """
    try:
        response = requests.get("http://localhost:6000/api/health", timeout=5)
        response.raise_for_status()
        
        data = response.json()
        return json.dumps(data, indent=2)
        
    except requests.RequestException as e:
        return f"API Error: API server is not responding - {str(e)}"

@tool("reset_campaign_data")
def reset_campaign_data() -> str:
    """
    Reset all campaign data (useful for testing).
    
    Returns:
        JSON string with reset confirmation
    """
    try:
        response = requests.post("http://localhost:6000/api/reset", timeout=5)
        response.raise_for_status()
        
        data = response.json()
        return json.dumps(data, indent=2)
        
    except requests.RequestException as e:
        return f"API Error: Failed to reset data - {str(e)}" 