#!/usr/bin/env python3
"""
Campaign Pilot Multi-Agent System Logger
Comprehensive logging system for demo and analytics purposes
"""

import os
import json
import logging
import time
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pathlib import Path
import threading
from dataclasses import dataclass, asdict
from enum import Enum

class LogLevel(Enum):
    """Log levels for different types of events"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    AGENT_ACTION = "AGENT_ACTION"
    DECISION = "DECISION"
    PERFORMANCE = "PERFORMANCE"
    API_CALL = "API_CALL"

@dataclass
class LogEntry:
    """Structured log entry for consistent logging"""
    timestamp: str
    level: str
    agent: str
    action: str
    data: Dict[str, Any]
    duration_ms: Optional[float] = None
    session_id: Optional[str] = None

class CampaignPilotLogger:
    """
    Comprehensive logging system for Campaign Pilot Multi-Agent System
    Captures all agent interactions, decisions, and system events for demo and analysis
    """
    
    def __init__(self, log_dir: str = "logs", session_name: Optional[str] = None):
        """
        Initialize the logging system
        
        Args:
            log_dir: Directory to store log files
            session_name: Optional custom session name
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Generate session ID and timestamp
        self.session_id = session_name or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.start_time = datetime.now(timezone.utc)
        
        # Initialize log storage
        self.log_entries: List[LogEntry] = []
        self.session_stats = {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "agent_actions": 0,
            "api_calls": 0,
            "decisions_made": 0,
            "campaigns_created": 0,
            "campaigns_paused": 0,
            "campaigns_resumed": 0,
            "total_budget_allocated": 0.0,
            "performance_metrics": {}
        }
        
        # Set up file logging
        self._setup_file_logging()
        
        # Thread safety
        self._lock = threading.Lock()
        
        print(f"🔍 Campaign Pilot Logger initialized")
        print(f"📊 Session ID: {self.session_id}")
        print(f"📁 Log Directory: {self.log_dir.absolute()}")
    
    def _setup_file_logging(self):
        """Set up file-based logging configuration"""
        log_file = self.log_dir / f"{self.session_id}.log"
        
        # Configure Python logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger("CampaignPilot")
        self.logger.info(f"Logging session started: {self.session_id}")
    
    def log_agent_action(self, agent: str, action: str, data: Dict[str, Any], 
                        duration_ms: Optional[float] = None):
        """
        Log an agent action with detailed information
        
        Args:
            agent: Name of the agent performing the action
            action: Description of the action
            data: Relevant data for the action
            duration_ms: Optional duration in milliseconds
        """
        with self._lock:
            entry = LogEntry(
                timestamp=datetime.now(timezone.utc).isoformat(),
                level=LogLevel.AGENT_ACTION.value,
                agent=agent,
                action=action,
                data=data,
                duration_ms=duration_ms,
                session_id=self.session_id
            )
            
            self.log_entries.append(entry)
            self.session_stats["agent_actions"] += 1
            
            # Log specific action types
            if "campaign" in action.lower():
                if "create" in action.lower():
                    self.session_stats["campaigns_created"] += 1
                elif "pause" in action.lower():
                    self.session_stats["campaigns_paused"] += 1
                elif "resume" in action.lower():
                    self.session_stats["campaigns_resumed"] += 1
            
            # Track budget allocation
            if "budget" in data:
                try:
                    budget = float(data["budget"])
                    self.session_stats["total_budget_allocated"] += budget
                except (ValueError, TypeError):
                    pass
            
            self.logger.info(f"[{agent}] {action}: {json.dumps(data, indent=2)}")
    
    def log_decision(self, agent: str, decision_type: str, criteria: Dict[str, Any], 
                    decision: str, rationale: str):
        """
        Log a decision made by an agent
        
        Args:
            agent: Agent making the decision
            decision_type: Type of decision (e.g., "campaign_management", "budget_allocation")
            criteria: Criteria used for decision making
            decision: The actual decision made
            rationale: Reasoning behind the decision
        """
        with self._lock:
            decision_data = {
                "decision_type": decision_type,
                "criteria": criteria,
                "decision": decision,
                "rationale": rationale
            }
            
            entry = LogEntry(
                timestamp=datetime.now(timezone.utc).isoformat(),
                level=LogLevel.DECISION.value,
                agent=agent,
                action=f"Decision: {decision_type}",
                data=decision_data,
                session_id=self.session_id
            )
            
            self.log_entries.append(entry)
            self.session_stats["decisions_made"] += 1
            
            self.logger.info(f"[{agent}] DECISION - {decision_type}: {decision} | {rationale}")
    
    def log_api_call(self, tool_name: str, endpoint: str, request_data: Dict[str, Any], 
                    response_data: Dict[str, Any], duration_ms: float, success: bool = True):
        """
        Log API calls made by tools
        
        Args:
            tool_name: Name of the tool making the call
            endpoint: API endpoint called
            request_data: Data sent in the request
            response_data: Response received
            duration_ms: Call duration in milliseconds
            success: Whether the call was successful
        """
        with self._lock:
            api_data = {
                "tool": tool_name,
                "endpoint": endpoint,
                "request": request_data,
                "response": response_data,
                "success": success,
                "duration_ms": duration_ms
            }
            
            entry = LogEntry(
                timestamp=datetime.now(timezone.utc).isoformat(),
                level=LogLevel.API_CALL.value,
                agent="SYSTEM",
                action=f"API Call: {endpoint}",
                data=api_data,
                duration_ms=duration_ms,
                session_id=self.session_id
            )
            
            self.log_entries.append(entry)
            self.session_stats["api_calls"] += 1
            
            status = "SUCCESS" if success else "FAILED"
            self.logger.info(f"[API] {tool_name} -> {endpoint} ({status}) - {duration_ms:.2f}ms")
    
    def log_performance_metrics(self, metrics: Dict[str, Any]):
        """
        Log performance metrics for analysis
        
        Args:
            metrics: Performance metrics dictionary
        """
        with self._lock:
            entry = LogEntry(
                timestamp=datetime.now(timezone.utc).isoformat(),
                level=LogLevel.PERFORMANCE.value,
                agent="ANALYTICS",
                action="Performance Update",
                data=metrics,
                session_id=self.session_id
            )
            
            self.log_entries.append(entry)
            self.session_stats["performance_metrics"].update(metrics)
            
            self.logger.info(f"[PERFORMANCE] Metrics updated: {json.dumps(metrics, indent=2)}")
    
    def log_system_event(self, event: str, data: Dict[str, Any], level: LogLevel = LogLevel.INFO):
        """
        Log general system events
        
        Args:
            event: Event description
            data: Event data
            level: Log level
        """
        with self._lock:
            entry = LogEntry(
                timestamp=datetime.now(timezone.utc).isoformat(),
                level=level.value,
                agent="SYSTEM",
                action=event,
                data=data,
                session_id=self.session_id
            )
            
            self.log_entries.append(entry)
            
            self.logger.info(f"[SYSTEM] {event}: {json.dumps(data, indent=2)}")
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current session
        
        Returns:
            Dictionary with session statistics and summary
        """
        current_time = datetime.now(timezone.utc)
        duration_seconds = (current_time - self.start_time).total_seconds()
        
        summary = {
            **self.session_stats,
            "end_time": current_time.isoformat(),
            "duration_seconds": duration_seconds,
            "total_log_entries": len(self.log_entries),
            "avg_action_duration": self._calculate_avg_duration(),
            "agent_activity": self._get_agent_activity(),
            "timeline": self._generate_timeline()
        }
        
        return summary
    
    def _calculate_avg_duration(self) -> float:
        """Calculate average duration of timed actions"""
        durations = [entry.duration_ms for entry in self.log_entries if entry.duration_ms]
        return sum(durations) / len(durations) if durations else 0.0
    
    def _get_agent_activity(self) -> Dict[str, int]:
        """Get activity count per agent"""
        activity = {}
        for entry in self.log_entries:
            activity[entry.agent] = activity.get(entry.agent, 0) + 1
        return activity
    
    def _generate_timeline(self) -> List[Dict[str, Any]]:
        """Generate a timeline of key events"""
        timeline = []
        for entry in self.log_entries:
            if entry.level in [LogLevel.AGENT_ACTION.value, LogLevel.DECISION.value]:
                timeline.append({
                    "timestamp": entry.timestamp,
                    "agent": entry.agent,
                    "action": entry.action,
                    "level": entry.level
                })
        return timeline[-20:]  # Last 20 events
    
    def export_logs(self, format_type: str = "json") -> str:
        """
        Export logs in different formats
        
        Args:
            format_type: Export format ("json", "csv", "html")
            
        Returns:
            Path to exported file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type == "json":
            return self._export_json(timestamp)
        elif format_type == "csv":
            return self._export_csv(timestamp)
        elif format_type == "html":
            return self._export_html(timestamp)
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def _export_json(self, timestamp: str) -> str:
        """Export logs as JSON"""
        filename = self.log_dir / f"{self.session_id}_export_{timestamp}.json"
        
        export_data = {
            "session_summary": self.get_session_summary(),
            "log_entries": [asdict(entry) for entry in self.log_entries]
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return str(filename)
    
    def _export_csv(self, timestamp: str) -> str:
        """Export logs as CSV"""
        import csv
        
        filename = self.log_dir / f"{self.session_id}_export_{timestamp}.csv"
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Level', 'Agent', 'Action', 'Data', 'Duration_MS'])
            
            for entry in self.log_entries:
                writer.writerow([
                    entry.timestamp,
                    entry.level,
                    entry.agent,
                    entry.action,
                    json.dumps(entry.data),
                    entry.duration_ms
                ])
        
        return str(filename)
    
    def _export_html(self, timestamp: str) -> str:
        """Export logs as HTML report"""
        filename = self.log_dir / f"{self.session_id}_report_{timestamp}.html"
        
        summary = self.get_session_summary()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Campaign Pilot Session Report - {self.session_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 10px; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat-box {{ background: #ecf0f1; padding: 15px; border-radius: 8px; text-align: center; }}
                .timeline {{ margin: 20px 0; }}
                .log-entry {{ border-left: 4px solid #3498db; padding: 10px; margin: 10px 0; background: #f8f9fa; }}
                .agent-action {{ border-left-color: #27ae60; }}
                .decision {{ border-left-color: #e74c3c; }}
                .api-call {{ border-left-color: #f39c12; }}
                .performance {{ border-left-color: #9b59b6; }}
                pre {{ background: #2c3e50; color: white; padding: 10px; border-radius: 5px; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Campaign Pilot Session Report</h1>
                <p>Session ID: {self.session_id}</p>
                <p>Duration: {summary['duration_seconds']:.2f} seconds</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <h3>{summary['agent_actions']}</h3>
                    <p>Agent Actions</p>
                </div>
                <div class="stat-box">
                    <h3>{summary['decisions_made']}</h3>
                    <p>Decisions Made</p>
                </div>
                <div class="stat-box">
                    <h3>{summary['campaigns_created']}</h3>
                    <p>Campaigns Created</p>
                </div>
                <div class="stat-box">
                    <h3>${summary['total_budget_allocated']:.2f}</h3>
                    <p>Total Budget</p>
                </div>
            </div>
            
            <h2>🤖 Agent Activity</h2>
            <pre>{json.dumps(summary['agent_activity'], indent=2)}</pre>
            
            <h2>📊 Session Timeline</h2>
            <div class="timeline">
        """
        
        for entry in self.log_entries[-30:]:  # Last 30 entries
            css_class = entry.level.lower().replace('_', '-')
            html_content += f"""
                <div class="log-entry {css_class}">
                    <strong>[{entry.timestamp}] {entry.agent}</strong> - {entry.action}
                    <pre>{json.dumps(entry.data, indent=2)}</pre>
                </div>
            """
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w') as f:
            f.write(html_content)
        
        return str(filename)
    
    def save_session(self):
        """Save the current session to disk"""
        session_file = self.log_dir / f"{self.session_id}_session.json"
        
        session_data = {
            "summary": self.get_session_summary(),
            "entries": [asdict(entry) for entry in self.log_entries]
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2, default=str)
        
        print(f"💾 Session saved to: {session_file}")
        return str(session_file)

# Global logger instance
_logger_instance = None

def get_logger(log_dir: str = "logs", session_name: Optional[str] = None) -> CampaignPilotLogger:
    """
    Get or create a global logger instance
    
    Args:
        log_dir: Directory to store log files
        session_name: Optional custom session name
        
    Returns:
        CampaignPilotLogger instance
    """
    global _logger_instance
    
    if _logger_instance is None:
        _logger_instance = CampaignPilotLogger(log_dir, session_name)
    
    return _logger_instance

def log_agent_action(agent: str, action: str, data: Dict[str, Any], duration_ms: Optional[float] = None):
    """Convenience function for logging agent actions"""
    logger = get_logger()
    logger.log_agent_action(agent, action, data, duration_ms)

def log_decision(agent: str, decision_type: str, criteria: Dict[str, Any], 
                decision: str, rationale: str):
    """Convenience function for logging decisions"""
    logger = get_logger()
    logger.log_decision(agent, decision_type, criteria, decision, rationale)

def log_api_call(tool_name: str, endpoint: str, request_data: Dict[str, Any], 
                response_data: Dict[str, Any], duration_ms: float, success: bool = True):
    """Convenience function for logging API calls"""
    logger = get_logger()
    logger.log_api_call(tool_name, endpoint, request_data, response_data, duration_ms, success)

def log_performance_metrics(metrics: Dict[str, Any]):
    """Convenience function for logging performance metrics"""
    logger = get_logger()
    logger.log_performance_metrics(metrics)

def log_system_event(event: str, data: Dict[str, Any], level: LogLevel = LogLevel.INFO):
    """Convenience function for logging system events"""
    logger = get_logger()
    logger.log_system_event(event, data, level) 