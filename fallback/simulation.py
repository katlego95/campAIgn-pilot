import time

def run_facebook_ad_campaign(product_name):
    """Simulates running a Facebook ad campaign."""
    print(f"Running Facebook ad campaign for {product_name}...")
    time.sleep(2)
    return {"status": "success", "message": f"Facebook campaign for {product_name} completed.", "ad_spend": 100, "clicks": 50}

def run_email_marketing_campaign(product_name):
    """Simulates running an email marketing campaign."""
    print(f"Running email marketing campaign for {product_name}...")
    time.sleep(2)
    return {"status": "success", "message": f"Email campaign for {product_name} completed.", "emails_sent": 1000, "opens": 200}
