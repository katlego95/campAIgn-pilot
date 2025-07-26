# Campaign Pilot Multi-Agent System

A sophisticated multi-agent system using Crew AI to automate e-commerce campaign creation, monitoring, and optimization.

## 🎯 Overview

This system consists of three specialized AI agents that work together to:

1. **Campaign Creator Agent** - Analyzes store products and creates targeted advertising campaigns
2. **Data Analyzer Agent** - Monitors campaign performance and generates actionable insights
3. **Campaign Manager Agent** - Makes data-driven decisions to optimize or pause campaigns

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Campaign       │    │  Data Analyzer  │    │  Campaign       │
│  Creator Agent  │───▶│     Agent       │───▶│ Manager Agent   │
│                 │    │                 │    │                 │
│ • Fetch products│    │ • Monitor perf. │    │ • Make decisions│
│ • Create campaigns│   │ • Generate data │    │ • Pause/Resume  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Fake API Server                             │
│  ┌─────────────────┐         ┌─────────────────────────────────┐│
│  │   Store API     │         │        Impact.com API           ││
│  │ • Products      │         │ • Campaign Creation             ││
│  │ • Analytics     │         │ • Performance Metrics          ││
│  │ • Sales Data    │         │ • Campaign Management          ││
│  └─────────────────┘         └─────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

1. **Python 3.8+**
2. **OpenAI API Key** - Required for Crew AI agents
3. **Required Python packages** (see requirements.txt)

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Navigate to the multi-agent system directory
cd multi-agent-system

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment file
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Start the Fake API Server

```bash
# In terminal 1
python fake_api_server.py
```

The server will start at `http://localhost:5000` with endpoints:
- Store API: `/api/store/*`
- Impact.com API: `/api/impact/*`
- Health Check: `/api/health`

### 3. Run the Multi-Agent System

```bash
# In terminal 2 - Run complete cycle
python main.py --full

# Or use interactive mode
python main.py
```

## 🛠️ Usage Options

### Command Line Interface

```bash
# Run complete campaign cycle (all 3 agents)
python main.py --full

# Run only campaign creation
python main.py --create

# Run only analysis and management
python main.py --analyze

# Show API status and current data
python main.py --status

# Reset all campaign data
python main.py --reset

# Interactive mode (default)
python main.py
```

### Programmatic Usage

```python
from crew import CampaignPilotCrew

# Create and run crew
crew = CampaignPilotCrew()
results = crew.run_campaign_flow()

# Or run specific workflows
from crew import run_campaign_creation_only, run_analysis_only
creation_results = run_campaign_creation_only()
analysis_results = run_analysis_only()
```

## 🤖 Agent Details

### Agent 1: Campaign Creator Specialist

**Role**: Analyzes store products and creates targeted advertising campaigns

**Tools Available**:
- `fetch_all_products` - Get all store products
- `fetch_product_details` - Get specific product info
- `fetch_product_analytics` - Get product performance data
- `create_campaign` - Create new ad campaigns
- `check_api_health` - Verify API connectivity

**Workflow**:
1. Fetch and analyze all store products
2. Identify high-potential products based on:
   - Stock levels (>50 units)
   - Page views vs. conversion potential
   - Price points supporting ad costs
   - Popular categories
3. Create targeted campaigns with optimized budgets
4. Generate compelling ad copy

### Agent 2: Performance Data Analyst

**Role**: Monitors campaign performance and store metrics for dashboard insights

**Tools Available**:
- `fetch_all_campaigns` - Get all campaign data
- `fetch_campaign_details` - Get specific campaign metrics
- `fetch_product_details` - Get current product data
- `fetch_product_analytics` - Get product performance analytics
- `check_api_health` - Verify API connectivity

**Workflow**:
1. Monitor all active campaigns
2. Fetch corresponding product performance data
3. Calculate key performance indicators:
   - Sales increase/decrease percentages
   - Page views increase/decrease percentages
   - ROAS (Return on Ad Spend)
   - CPA (Cost Per Acquisition)
4. Generate dashboard-ready data tables
5. Identify trends and optimization opportunities

### Agent 3: Strategic Campaign Manager

**Role**: Makes data-driven decisions to optimize campaign performance

**Tools Available**:
- `fetch_all_campaigns` - Get campaign performance data
- `fetch_campaign_details` - Get detailed campaign metrics
- `fetch_product_analytics` - Get product performance data
- `pause_campaign` - Pause underperforming campaigns
- `resume_campaign` - Resume paused campaigns
- `check_api_health` - Verify API connectivity

**Decision Criteria**:
- **Continue**: Sales increase >15% AND views increase >10%
- **Monitor**: Sales increase 5-15% OR views increase 5-10%
- **Pause**: Sales decrease >10% OR views decrease >5%
- **Immediate Pause**: Negative ROAS or very high CPA

## 📊 API Endpoints

### Store API (`/api/store/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/products` | GET | Get all products |
| `/products/{id}` | GET | Get specific product |
| `/products/{id}/analytics` | GET | Get product analytics |

### Impact.com API (`/api/impact/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/campaigns` | GET | Get all campaigns |
| `/campaigns` | POST | Create new campaign |
| `/campaigns/{id}` | GET | Get campaign details |
| `/campaigns/{id}/pause` | POST | Pause campaign |
| `/campaigns/{id}/resume` | POST | Resume campaign |

### Utility Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | API health check |
| `/api/reset` | POST | Reset all campaign data |

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Required: OpenAI API key for Crew AI
OPENAI_API_KEY=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

# API Configuration
STORE_API_BASE_URL=http://localhost:5000/api/store
IMPACT_API_BASE_URL=http://localhost:5000/api/impact

# Agent Settings
CREW_VERBOSE_LEVEL=2
MAX_AGENT_ITERATIONS=5

# Campaign Defaults
DEFAULT_CAMPAIGN_BUDGET=25.0
DEFAULT_CAMPAIGN_DURATION=7

# Performance Thresholds
SALES_INCREASE_THRESHOLD_HIGH=15.0
VIEWS_INCREASE_THRESHOLD_HIGH=10.0
```

## 📁 Project Structure

```
multi-agent-system/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── fake_api_server.py       # Mock API server
├── tools.py                 # Custom agent tools
├── agents.py                # Agent definitions
├── tasks.py                 # Task definitions
├── crew.py                  # Crew coordination
└── main.py                  # CLI interface
```

## 🧪 Testing

### Test Individual Components

```bash
# Test API server
curl http://localhost:5000/api/health

# Test store products
curl http://localhost:5000/api/store/products

# Test campaign creation
curl -X POST http://localhost:5000/api/impact/campaigns \
  -H "Content-Type: application/json" \
  -d '{"product_id": 100, "campaign_name": "Test Campaign", "budget": 25}'
```

### Test Agents

```bash
# Test campaign creation only
python main.py --create

# Test analysis only (requires existing campaigns)
python main.py --analyze

# Check system status
python main.py --status
```

## 🔄 Integration with WordPress Plugin

The multi-agent system is designed to integrate with the WordPress Campaign Pilot plugin:

1. **WordPress Plugin** triggers the multi-agent flow via API call
2. **Multi-Agent System** processes the request and creates/manages campaigns
3. **Results** are formatted for dashboard consumption
4. **Plugin** displays real-time updates from agent decisions

### Integration Points

- WordPress plugin calls: `POST /api/trigger-agents`
- Agents fetch store data from WooCommerce via fake API
- Campaign decisions feed back to WordPress dashboard
- Real-time status updates via polling or webhooks

## 🛡️ Security Considerations

- API endpoints are currently open (fake/development environment)
- In production, implement authentication and rate limiting
- Secure OpenAI API key storage
- Validate all API inputs and outputs
- Monitor agent decisions for unexpected behavior

## 🚨 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key

2. **"Fake API server is not running"**
   - Start server: `python fake_api_server.py`
   - Check port 5000 is available

3. **"Missing required package"**
   - Install dependencies: `pip install -r requirements.txt`

4. **Agent timeouts or errors**
   - Check API server logs
   - Verify OpenAI API key is valid
   - Reduce `MAX_AGENT_ITERATIONS` if needed

### Debug Mode

```bash
# Run with verbose logging
python main.py --full --skip-checks

# Check API status
python main.py --status

# Reset data if needed
python main.py --reset
```

## 🔮 Future Enhancements

- **Real API Integration**: Connect to actual WooCommerce and Impact.com APIs
- **Advanced Analytics**: Machine learning for campaign optimization
- **Webhook Support**: Real-time notifications to WordPress plugin
- **A/B Testing**: Automated campaign variations and testing
- **Budget Optimization**: Dynamic budget allocation based on performance
- **Seasonal Adjustments**: Time-based campaign modifications

## 📄 License

This project is part of the Campaign Pilot system for rapid prototyping and development. 