def get_underperforming_products_prompt(underperforming_df):
    """Returns the prompt for analyzing underperforming products."""
    return f"The following products have been identified as underperforming based on the logic: high hits and low sales. Please provide a brief explanation for why this might be the case for each product.\n\n{underperforming_df.to_string()}"

def get_campaign_planning_prompt(underperforming_df):
    """Returns the prompt for planning campaigns."""
    return f"For the following underperforming products, suggest a marketing campaign to improve their sales. Explain your reasoning for each suggestion.\n\n{underperforming_df.to_string()}"
