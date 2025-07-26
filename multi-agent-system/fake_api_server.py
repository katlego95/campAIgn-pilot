#!/usr/bin/env python3
"""
Fake API Server for Multi-Agent Campaign System
Simulates both Store API and Impact.com API responses
"""

from flask import Flask, jsonify, request
import random
import time
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# Mock data storage
products_db = {
    100: {
        "id": 100,
        "name": "Wireless Bluetooth Headphones",
        "category": "Electronics",
        "price": 79.99,
        "description": "High-quality wireless headphones with noise cancellation",
        "image_url": "https://example.com/headphones.jpg",
        "stock": 150,
        "page_views": 2341,
        "sales": 23,
        "revenue": 1839.77
    },
    101: {
        "id": 101,
        "name": "Organic Cotton T-Shirt",
        "category": "Clothing",
        "price": 24.99,
        "description": "Comfortable organic cotton t-shirt in various colors",
        "image_url": "https://example.com/tshirt.jpg",
        "stock": 200,
        "page_views": 5672,
        "sales": 89,
        "revenue": 2224.11
    },
    102: {
        "id": 102,
        "name": "Smart Water Bottle",
        "category": "Fitness",
        "price": 34.99,
        "description": "Smart water bottle with temperature control and app connectivity",
        "image_url": "https://example.com/bottle.jpg",
        "stock": 75,
        "page_views": 8934,
        "sales": 234,
        "revenue": 8187.66
    },
    103: {
        "id": 103,
        "name": "Premium Coffee Beans",
        "category": "Food & Beverage",
        "price": 18.99,
        "description": "Single-origin premium coffee beans, freshly roasted",
        "image_url": "https://example.com/coffee.jpg",
        "stock": 300,
        "page_views": 1876,
        "sales": 34,
        "revenue": 645.66
    },
    104: {
        "id": 104,
        "name": "Yoga Mat Premium",
        "category": "Fitness",
        "price": 45.99,
        "description": "Premium non-slip yoga mat with alignment lines",
        "image_url": "https://example.com/yoga.jpg",
        "stock": 120,
        "page_views": 3456,
        "sales": 67,
        "revenue": 3081.33
    }
}

campaigns_db = {}

# =============================================================================
# STORE API ENDPOINTS
# =============================================================================

@app.route('/api/store/products', methods=['GET'])
def get_all_products():
    """Get all products from the store"""
    time.sleep(0.2)  # Simulate network delay
    return jsonify({
        "status": "success",
        "data": list(products_db.values()),
        "count": len(products_db)
    })

@app.route('/api/store/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get specific product details"""
    time.sleep(0.1)  # Simulate network delay
    
    if product_id not in products_db:
        return jsonify({
            "status": "error",
            "message": "Product not found"
        }), 404
    
    product = products_db[product_id].copy()
    
    # Add some randomness to simulate real-time data
    base_views = product['page_views']
    base_sales = product['sales']
    
    product['page_views'] = base_views + random.randint(-50, 100)
    product['sales'] = base_sales + random.randint(-5, 15)
    product['revenue'] = product['sales'] * product['price']
    
    return jsonify({
        "status": "success",
        "data": product
    })

@app.route('/api/store/products/<int:product_id>/analytics', methods=['GET'])
def get_product_analytics(product_id):
    """Get detailed analytics for a product"""
    time.sleep(0.3)  # Simulate network delay
    
    if product_id not in products_db:
        return jsonify({
            "status": "error",
            "message": "Product not found"
        }), 404
    
    product = products_db[product_id]
    
    # Generate realistic analytics data
    analytics = {
        "product_id": product_id,
        "time_range": "last_7_days",
        "page_views": {
            "current": product['page_views'] + random.randint(-100, 200),
            "previous": product['page_views'],
            "change_percent": round(random.uniform(-25, 45), 2)
        },
        "sales": {
            "current": product['sales'] + random.randint(-10, 25),
            "previous": product['sales'],
            "change_percent": round(random.uniform(-20, 35), 2)
        },
        "revenue": {
            "current": (product['sales'] + random.randint(-10, 25)) * product['price'],
            "previous": product['revenue'],
            "change_percent": round(random.uniform(-20, 35), 2)
        },
        "conversion_rate": round(random.uniform(2.1, 8.5), 2),
        "bounce_rate": round(random.uniform(35, 75), 2),
        "avg_session_duration": random.randint(120, 500)
    }
    
    return jsonify({
        "status": "success",
        "data": analytics
    })

# =============================================================================
# IMPACT.COM API ENDPOINTS
# =============================================================================

@app.route('/api/impact/campaigns', methods=['POST'])
def create_campaign():
    """Create a new ad campaign"""
    time.sleep(0.5)  # Simulate API processing time
    
    data = request.get_json()
    
    if not data or 'product_id' not in data:
        return jsonify({
            "status": "error",
            "message": "Missing required fields"
        }), 400
    
    campaign_id = f"camp_{uuid.uuid4().hex[:8]}"
    
    campaign = {
        "campaign_id": campaign_id,
        "product_id": data['product_id'],
        "campaign_name": data.get('campaign_name', f"Campaign for Product {data['product_id']}"),
        "status": "active",
        "budget": data.get('budget', 20.0),
        "duration_days": data.get('duration_days', 7),
        "campaign_copy": data.get('campaign_copy', "Discover our amazing product!"),
        "created_at": datetime.now().isoformat(),
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=data.get('duration_days', 7))).isoformat(),
        "metrics": {
            "impressions": 0,
            "clicks": 0,
            "conversions": 0,
            "spend": 0.0,
            "ctr": 0.0,
            "cpc": 0.0,
            "roas": 0.0
        }
    }
    
    campaigns_db[campaign_id] = campaign
    
    return jsonify({
        "status": "success",
        "message": "Campaign created successfully",
        "data": campaign
    })

@app.route('/api/impact/campaigns/<campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """Get campaign details and performance"""
    time.sleep(0.2)  # Simulate network delay
    
    if campaign_id not in campaigns_db:
        return jsonify({
            "status": "error",
            "message": "Campaign not found"
        }), 404
    
    campaign = campaigns_db[campaign_id].copy()
    
    # Simulate realistic campaign performance
    days_running = (datetime.now() - datetime.fromisoformat(campaign['created_at'].replace('Z', ''))).days + 1
    base_impressions = random.randint(1000, 10000) * days_running
    
    campaign['metrics'] = {
        "impressions": base_impressions,
        "clicks": int(base_impressions * random.uniform(0.01, 0.05)),
        "conversions": int(base_impressions * random.uniform(0.001, 0.008)),
        "spend": round(random.uniform(5, campaign['budget'] * 0.8), 2),
        "ctr": round(random.uniform(1.2, 4.8), 2),
        "cpc": round(random.uniform(0.25, 2.50), 2),
        "roas": round(random.uniform(1.5, 6.2), 2)
    }
    
    return jsonify({
        "status": "success",
        "data": campaign
    })

@app.route('/api/impact/campaigns', methods=['GET'])
def get_all_campaigns():
    """Get all campaigns"""
    time.sleep(0.3)  # Simulate network delay
    
    campaigns = []
    for campaign_id, campaign in campaigns_db.items():
        # Update metrics for each campaign
        campaign_copy = campaign.copy()
        days_running = (datetime.now() - datetime.fromisoformat(campaign['created_at'].replace('Z', ''))).days + 1
        base_impressions = random.randint(1000, 8000) * days_running
        
        campaign_copy['metrics'] = {
            "impressions": base_impressions,
            "clicks": int(base_impressions * random.uniform(0.01, 0.05)),
            "conversions": int(base_impressions * random.uniform(0.001, 0.008)),
            "spend": round(random.uniform(5, campaign['budget'] * 0.9), 2),
            "ctr": round(random.uniform(1.2, 4.8), 2),
            "cpc": round(random.uniform(0.25, 2.50), 2),
            "roas": round(random.uniform(1.5, 6.2), 2)
        }
        campaigns.append(campaign_copy)
    
    return jsonify({
        "status": "success",
        "data": campaigns,
        "count": len(campaigns)
    })

@app.route('/api/impact/campaigns/<campaign_id>/pause', methods=['POST'])
def pause_campaign(campaign_id):
    """Pause a campaign"""
    time.sleep(0.2)  # Simulate processing time
    
    if campaign_id not in campaigns_db:
        return jsonify({
            "status": "error",
            "message": "Campaign not found"
        }), 404
    
    campaigns_db[campaign_id]['status'] = 'paused'
    
    return jsonify({
        "status": "success",
        "message": "Campaign paused successfully",
        "data": campaigns_db[campaign_id]
    })

@app.route('/api/impact/campaigns/<campaign_id>/resume', methods=['POST'])
def resume_campaign(campaign_id):
    """Resume a paused campaign"""
    time.sleep(0.2)  # Simulate processing time
    
    if campaign_id not in campaigns_db:
        return jsonify({
            "status": "error",
            "message": "Campaign not found"
        }), 404
    
    campaigns_db[campaign_id]['status'] = 'active'
    
    return jsonify({
        "status": "success",
        "message": "Campaign resumed successfully",
        "data": campaigns_db[campaign_id]
    })

# =============================================================================
# UTILITY ENDPOINTS
# =============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        "status": "success",
        "message": "API is running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "store": "/api/store/*",
            "impact": "/api/impact/*"
        }
    })

@app.route('/api/reset', methods=['POST'])
def reset_data():
    """Reset all campaign data (for testing)"""
    global campaigns_db
    campaigns_db = {}
    
    return jsonify({
        "status": "success",
        "message": "All campaign data reset"
    })

if __name__ == '__main__':
    print("🚀 Starting Fake API Server...")
    print("📍 Store API: http://localhost:5000/api/store/*")
    print("📍 Impact.com API: http://localhost:5000/api/impact/*")
    print("📍 Health Check: http://localhost:5000/api/health")
    print("📍 Reset Data: http://localhost:5000/api/reset")
    
    app.run(debug=True, host='0.0.0.0', port=6000) 