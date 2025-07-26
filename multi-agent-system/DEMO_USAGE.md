# Campaign Pilot Demo & Logging Usage Guide

## 🎯 Overview

The Campaign Pilot Multi-Agent System now includes comprehensive logging and demo capabilities designed specifically for presentations, pitches, and system analysis.

## 🚀 Quick Start Guide

### 1. Enhanced Demo Script

Run the full demo presentation with:

```bash
python demo.py
```

This provides a complete 5-phase demonstration:
- **Phase 1**: System validation & readiness check
- **Phase 2**: Agent intelligence showcase  
- **Phase 3**: Live autonomous campaign execution
- **Phase 4**: Demo results & performance metrics
- **Phase 5**: Artifact generation

### 2. Standard CLI with Logging

Run the system with enhanced logging:

```bash
# Full system with custom demo session name
python main.py --full --demo-session "client_presentation_2024"

# Export logs in HTML format for presentation
python main.py --full --export-logs html

# Campaign creation with logging
python main.py --create --demo-session "campaign_creation_demo"
```

### 3. Available CLI Options

```bash
# Core functionality
python main.py --full                    # Run complete multi-agent cycle
python main.py --create                  # Campaign creation only
python main.py --analyze                 # Analysis and management only
python main.py --status                  # Show system status

# Demo and logging features
python main.py --demo-session "name"     # Custom session name for logging
python main.py --export-logs [format]    # Export logs (json/csv/html)
python main.py --reset                   # Reset campaign data
python main.py --skip-checks             # Skip prerequisite validation
```

## 📊 Logging System Features

### Automatic Logging

The system automatically logs:
- **Agent Actions**: Every action taken by each AI agent
- **API Calls**: All interactions with external APIs
- **Decisions**: Strategic decisions made by agents
- **Performance Metrics**: Real-time performance data
- **System Events**: System status and operational events

### Log Formats

**1. JSON Export** - Technical analysis and data processing
```bash
python main.py --export-logs json
```

**2. CSV Export** - Data analysis and spreadsheet import
```bash
python main.py --export-logs csv
```

**3. HTML Report** - Executive presentations and demos
```bash
python main.py --export-logs html
```

### Session Management

Each execution creates a unique session with:
- **Session ID**: Unique identifier for tracking
- **Timestamps**: Precise timing of all events
- **Duration Tracking**: Performance measurement
- **Agent Activity**: Detailed breakdown of agent work
- **API Statistics**: Call counts and performance

## 🎬 Demo Script Features

### Professional Presentation Mode

The `demo.py` script provides:

**Visual Enhancements:**
- Rich console formatting with colors and progress bars
- Professional tables and panels
- Real-time progress tracking
- Impressive visual banners

**Comprehensive Coverage:**
- System architecture explanation
- Agent capability demonstrations
- Live system execution
- Performance metrics analysis
- ROI calculations
- Next steps guidance

**Artifact Generation:**
- Multiple export formats
- Executive summaries
- Technical documentation
- Audit trails

### Demo Phases Breakdown

**Phase 1: System Validation (2 minutes)**
- Prerequisites check
- API connectivity validation
- Agent initialization
- Data source connection

**Phase 2: Agent Showcase (3 minutes)**
- Individual agent capabilities
- Performance metrics
- Success rates
- Technical specifications

**Phase 3: Live Execution (5-8 minutes)**
- Real-time campaign creation
- Performance monitoring
- Decision making
- Optimization actions

**Phase 4: Results Analysis (2 minutes)**
- Performance metrics comparison
- ROI calculations
- Efficiency analysis
- Success statistics

**Phase 5: Artifact Generation (1 minute)**
- Report exports
- Documentation creation
- Follow-up materials

## 🔧 Technical Implementation

### Logger Integration

The logging system is automatically integrated into:

**Tools (`tools.py`):**
- API call logging with timing
- Request/response tracking
- Success/failure monitoring

**Main System (`main.py`):**
- Session initialization
- System event logging
- Error tracking

**Crew Orchestration (`crew.py`):**
- Agent action logging
- Workflow tracking
- Performance measurement

### Custom Session Names

For organized demo sessions:

```python
# Programmatic usage
from logger import get_logger

logger = get_logger(session_name="board_presentation_q4")
```

```bash
# CLI usage
python main.py --full --demo-session "board_presentation_q4"
```

## 📁 Output Artifacts

### File Organization

All outputs are stored in the `logs/` directory:

```
logs/
├── session_20240115_143000.log          # Raw log file
├── session_20240115_143000_session.json # Complete session data
├── session_20240115_143000_export_*.json # JSON export
├── session_20240115_143000_export_*.csv  # CSV export
└── session_20240115_143000_report_*.html # HTML report
```

### HTML Report Contents

The HTML report includes:
- **Executive Summary**: Key metrics and outcomes
- **Agent Activity**: Breakdown of each agent's work
- **Performance Timeline**: Chronological event tracking
- **API Statistics**: Call performance and success rates
- **Decision Log**: All strategic decisions made
- **ROI Analysis**: Business impact calculations

## 💡 Best Practices

### For Demos

1. **Preparation:**
   - Start fake API server first: `python fake_api_server.py`
   - Ensure clean environment with `--reset`
   - Use meaningful session names

2. **During Presentation:**
   - Use `python demo.py` for full presentation
   - Highlight real-time decision making
   - Emphasize autonomous operation

3. **Follow-up:**
   - Export HTML reports for stakeholders
   - Provide technical JSON/CSV for analysis
   - Share session data for audit trails

### For Development

1. **Debugging:**
   - Use JSON exports for detailed analysis
   - Check session logs for error tracking
   - Monitor API call performance

2. **Performance Analysis:**
   - Compare session durations
   - Track agent efficiency metrics
   - Analyze decision patterns

3. **System Monitoring:**
   - Regular session reviews
   - Performance trending
   - Error pattern analysis

## 🚀 Integration Examples

### WordPress Plugin Integration

```python
# Trigger from WordPress
import requests

response = requests.post("http://localhost:5000/api/trigger-agents", {
    "session_name": f"wordpress_trigger_{user_id}",
    "source": "wordpress_plugin"
})
```

### Scheduled Execution

```bash
# Cron job example
0 9 * * * cd /path/to/multi-agent-system && python main.py --full --demo-session "daily_optimization_$(date +%Y%m%d)"
```

### API Integration

```python
# Programmatic execution
from crew import run_full_campaign_cycle
from logger import get_logger

logger = get_logger(session_name="api_triggered_session")
results = run_full_campaign_cycle()
report_path = logger.export_logs("html")
```

## 📞 Support & Next Steps

**For Technical Issues:**
- Check logs in `logs/` directory
- Verify API server is running
- Ensure all dependencies installed

**For Demo Customization:**
- Modify `demo.py` for specific audiences
- Customize session names for tracking
- Adjust timing and content as needed

**For Integration:**
- Use JSON exports for data processing
- Implement webhook notifications
- Set up monitoring dashboards

---

Ready to showcase the future of autonomous campaign management! 🚀 