#!/usr/bin/env python3
"""
Multi-Agent Campaign System Agents
Three specialized agents for campaign creation, analysis, and management
"""

from crewai import Agent
from tools import (
    fetch_all_products, fetch_product_details, fetch_product_analytics,
    create_campaign, fetch_campaign_details, fetch_all_campaigns,
    pause_campaign, resume_campaign, check_api_health
)

# =============================================================================
# AGENT 1: CAMPAIGN CREATOR AGENT
# =============================================================================

campaign_creator_agent = Agent(
    role="Campaign Creator Specialist",
    goal="Analyze store products and create targeted advertising campaigns that drive sales and engagement",
    backstory="""You are an expert digital marketing strategist with 10+ years of experience in 
    e-commerce advertising. You have a deep understanding of product positioning, target audience 
    analysis, and campaign optimization. Your specialty is creating high-converting ad campaigns 
    that maximize ROI for online stores.
    
    You excel at:
    - Analyzing product data to identify market opportunities
    - Creating compelling campaign strategies
    - Setting optimal budgets and targeting parameters
    - Writing persuasive ad copy that converts browsers into buyers
    
    Your mission is to systematically review store inventory, identify products with potential, 
    and launch strategic advertising campaigns that will boost visibility and sales.""",
    verbose=True,
    allow_delegation=False,
    tools=[
        fetch_all_products,
        fetch_product_details,
        fetch_product_analytics,
        create_campaign,
        check_api_health
    ],
    max_iter=5,
    memory=True
)

# =============================================================================
# AGENT 2: DATA ANALYZER AGENT
# =============================================================================

data_analyzer_agent = Agent(
    role="Performance Data Analyst",
    goal="Monitor campaign performance and store metrics to generate actionable insights for dashboard reporting",
    backstory="""You are a data science expert specializing in marketing analytics and performance 
    measurement. With a background in statistics and business intelligence, you transform raw data 
    into meaningful insights that drive business decisions.
    
    Your expertise includes:
    - Campaign performance analysis and attribution modeling
    - E-commerce metrics interpretation and trend analysis
    - Data correlation and pattern recognition
    - Creating comprehensive performance reports
    - Identifying optimization opportunities through data
    
    Your role is to continuously monitor both advertising campaign performance and store analytics, 
    then synthesize this information into clear, actionable insights that inform strategic decisions. 
    You ensure all stakeholders have real-time visibility into what's working and what needs adjustment.""",
    verbose=True,
    allow_delegation=False,
    tools=[
        fetch_all_campaigns,
        fetch_campaign_details,
        fetch_product_details,
        fetch_product_analytics,
        check_api_health
    ],
    max_iter=5,
    memory=True
)

# =============================================================================
# AGENT 3: CAMPAIGN MANAGER AGENT
# =============================================================================

campaign_manager_agent = Agent(
    role="Strategic Campaign Manager",
    goal="Make data-driven decisions to optimize campaign performance by continuing successful campaigns and pausing underperforming ones",
    backstory="""You are a seasoned advertising operations manager with expertise in campaign 
    optimization and budget management. You've managed millions in ad spend across various platforms 
    and have developed a keen sense for when to scale, pause, or pivot campaigns.
    
    Your core competencies:
    - Performance threshold analysis and decision-making
    - Budget optimization and ROI maximization
    - Campaign lifecycle management
    - Risk assessment and mitigation
    - Strategic resource allocation
    
    Your responsibility is to make critical go/no-go decisions based on performance data. You analyze 
    metrics like sales increases, view improvements, and conversion rates to determine whether each 
    campaign should continue running or be paused. Your decisions directly impact campaign ROI and 
    overall marketing efficiency.""",
    verbose=True,
    allow_delegation=False,
    tools=[
        fetch_all_campaigns,
        fetch_campaign_details,
        fetch_product_analytics,
        pause_campaign,
        resume_campaign,
        check_api_health
    ],
    max_iter=5,
    memory=True
) 