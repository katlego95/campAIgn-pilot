#!/usr/bin/env python3
"""
Tasks for Multi-Agent Campaign System
Defines specific tasks for each agent with clear objectives
"""

from crewai import Task
from agents import campaign_creator_agent, data_analyzer_agent, campaign_manager_agent

# =============================================================================
# TASK 1: CAMPAIGN CREATION
# =============================================================================

campaign_creation_task = Task(
    description="""
    Analyze all products in the store and create targeted advertising campaigns for products 
    that show potential for increased sales and visibility.

    Your workflow should be:
    1. First, check if the API is healthy and accessible
    2. Fetch all products from the store API
    3. For each product, analyze its current performance metrics (page views, sales, stock levels)
    4. Identify the top 3-5 products that would benefit most from advertising campaigns
    5. For each selected product:
       - Create a compelling campaign name
       - Set an appropriate budget (between $15-50 based on product price and current performance)
       - Write engaging ad copy that highlights the product's key benefits
       - Launch the campaign via the Impact.com API

    Focus on products with:
    - Good stock levels (>50 units)
    - Decent page views but room for improvement
    - Higher price points that can support advertising costs
    - Products in popular categories (Electronics, Fitness, Clothing)

    Important: Actually create the campaigns using the create_campaign tool. Don't just plan them.
    """,
    expected_output="""
    A detailed report showing:
    1. List of all products analyzed with their key metrics
    2. Selected products for campaign creation with justification
    3. For each campaign created:
       - Campaign ID and name
       - Product details and reasoning for selection
       - Budget allocation and expected ROI
       - Ad copy used
       - Campaign configuration (duration, targeting, etc.)
    4. Summary of total campaigns launched and total budget allocated
    
    Format the output as a structured report with clear sections and data tables.
    """,
    agent=campaign_creator_agent,
    verbose=True
)

# =============================================================================
# TASK 2: DATA ANALYSIS AND DASHBOARD PREPARATION
# =============================================================================

data_analysis_task = Task(
    description="""
    Monitor and analyze all active campaigns and their corresponding product performance to generate 
    comprehensive dashboard data for business intelligence reporting.

    Your analytical workflow:
    1. Check API health to ensure data integrity
    2. Fetch all active campaigns and their performance metrics from Impact.com API
    3. For each campaign, fetch the corresponding product analytics from the store API
    4. Perform correlation analysis between campaign performance and product metrics
    5. Calculate key performance indicators:
       - Sales increase/decrease percentage since campaign start
       - Page views increase/decrease percentage since campaign start
       - Return on Ad Spend (ROAS) calculations
       - Cost per acquisition (CPA) metrics
       - Campaign efficiency scores

    For dashboard preparation, synthesize the data into:
    - Campaign performance summaries
    - Product impact analysis
    - Trend identification and pattern recognition
    - Performance ranking and benchmarking
    - Recommendations for optimization

    Focus on creating actionable insights that help stakeholders understand which campaigns 
    are driving real business value and which need attention.
    """,
    expected_output="""
    A comprehensive performance analysis report containing:

    1. Campaign Performance Overview:
       - Total campaigns analyzed
       - Overall performance metrics summary
       - Top performing campaigns (by ROAS, sales increase, view increase)
       - Underperforming campaigns requiring attention

    2. Product Impact Analysis:
       - For each product with active campaigns:
         * Campaign ID and product details
         * Sales performance before vs. during campaign
         * Page views performance before vs. during campaign
         * Percentage changes in key metrics
         * Revenue impact and attribution

    3. Dashboard-Ready Data Tables:
       - Campaign ID, Product ID, Product Name
       - Current page views and sales numbers
       - Percentage increase/decrease in views and sales
       - Campaign status and budget utilization
       - Performance scores and recommendations

    4. Strategic Insights:
       - Trends and patterns identified
       - Correlation findings between campaign metrics and product performance
       - Recommendations for campaign optimization

    Format all data in clear, structured tables ready for dashboard integration.
    """,
    agent=data_analyzer_agent,
    verbose=True
)

# =============================================================================
# TASK 3: CAMPAIGN MANAGEMENT DECISIONS
# =============================================================================

campaign_management_task = Task(
    description="""
    Based on the performance analysis, make strategic decisions about campaign continuation, 
    optimization, or termination to maximize ROI and marketing efficiency.

    Your decision-making process:
    1. Review all campaign performance data and product analytics
    2. Apply performance thresholds and decision criteria:
       - Campaigns with sales increase >15% AND views increase >10%: Continue/Optimize
       - Campaigns with sales increase 5-15% OR views increase 5-10%: Monitor closely
       - Campaigns with sales decrease >10% OR views decrease >5%: Consider pausing
       - Campaigns with negative ROAS or very high CPA: Pause immediately
    
    3. For each campaign, make one of these decisions:
       - CONTINUE: High-performing campaigns that should keep running
       - PAUSE: Underperforming campaigns that need immediate attention
       - OPTIMIZE: Campaigns with mixed results that need budget/targeting adjustments

    4. Execute the decisions using the campaign management tools
    5. Provide clear rationale for each decision made

    Consider factors like:
    - Statistical significance of performance changes
    - Campaign duration and learning period
    - Product lifecycle and seasonality
    - Budget efficiency and spend rate
    - Competitive landscape and market conditions

    Take action - don't just recommend, actually pause underperforming campaigns and 
    document the decisions made.
    """,
    expected_output="""
    A strategic campaign management report with:

    1. Executive Summary:
       - Total campaigns reviewed
       - Decisions made (continue/pause/optimize counts)
       - Total budget reallocated
       - Expected impact of decisions

    2. Campaign-by-Campaign Decisions:
       For each campaign:
       - Campaign ID and product name
       - Key performance metrics reviewed
       - Decision made (CONTINUE/PAUSE/OPTIMIZE)
       - Detailed rationale for the decision
       - Action taken (if any API calls were made)
       - Expected outcome from the decision

    3. Performance Threshold Analysis:
       - Campaigns exceeding performance targets
       - Campaigns meeting baseline expectations
       - Campaigns requiring immediate intervention
       - Budget efficiency analysis

    4. Strategic Recommendations:
       - Overall portfolio health assessment
       - Recommendations for future campaign strategy
       - Budget allocation optimization suggestions
       - Risk mitigation strategies

    5. Action Log:
       - Specific API calls made (pause/resume actions)
       - Campaigns modified and their new status
       - Budget reallocations and adjustments

    Present findings in a clear, executive-ready format with actionable next steps.
    """,
    agent=campaign_manager_agent,
    verbose=True
) 