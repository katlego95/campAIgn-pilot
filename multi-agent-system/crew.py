#!/usr/bin/env python3
"""
Multi-Agent Campaign Crew
Orchestrates the three specialized agents to work together
"""

import os
from datetime import datetime
from crewai import Crew, Process
from agents import campaign_creator_agent, data_analyzer_agent, campaign_manager_agent
from tasks import campaign_creation_task, data_analysis_task, campaign_management_task
from logger import log_agent_action, log_system_event, LogLevel

class CampaignPilotCrew:
    """
    Main crew class that coordinates the multi-agent campaign system
    """
    
    def __init__(self):
        self.crew = Crew(
            agents=[
                campaign_creator_agent,
                data_analyzer_agent, 
                campaign_manager_agent
            ],
            tasks=[
                campaign_creation_task,
                data_analysis_task,
                campaign_management_task
            ],
            process=Process.sequential,
            verbose=True,
            memory=True,
            max_rpm=10,  # Rate limiting
            share_crew=False
        )
    
    def run_campaign_flow(self, inputs=None):
        """
        Execute the complete multi-agent campaign flow
        
        Args:
            inputs: Optional input parameters for the crew
            
        Returns:
            Crew execution results
        """
        print("🚀 Starting Campaign Pilot Multi-Agent Flow...")
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        # Log crew workflow start
        log_system_event("Multi-Agent Crew Workflow Started", {
            "agents_count": len(self.crew.agents),
            "tasks_count": len(self.crew.tasks),
            "process_type": str(self.crew.process),
            "inputs": inputs or {}
        })
        
        try:
            # Log individual agent initialization
            for agent in self.crew.agents:
                log_agent_action(
                    agent=agent.role,
                    action="Agent Initialized",
                    data={
                        "goal": agent.goal,
                        "tools_available": len(agent.tools) if hasattr(agent, 'tools') else 0,
                        "memory_enabled": getattr(agent, 'memory', False)
                    }
                )
            
            # Execute the crew workflow
            result = self.crew.kickoff(inputs=inputs or {})
            
            # Log completion
            log_system_event("Multi-Agent Crew Workflow Completed", {
                "success": True,
                "result_length": len(str(result)) if result else 0
            })
            
            print("=" * 80)
            print("✅ Campaign Pilot Flow Completed Successfully!")
            print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            return result
            
        except Exception as e:
            # Log failure
            log_system_event("Multi-Agent Crew Workflow Failed", {
                "success": False,
                "error": str(e)
            }, LogLevel.ERROR)
            
            print("=" * 80)
            print(f"❌ Campaign Pilot Flow Failed: {str(e)}")
            print(f"⏰ Failed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            raise e
    
    def get_crew_info(self):
        """
        Get information about the crew configuration
        
        Returns:
            Dictionary with crew details
        """
        return {
            "agents": [
                {
                    "role": agent.role,
                    "goal": agent.goal,
                    "tools_count": len(agent.tools) if hasattr(agent, 'tools') else 0
                }
                for agent in self.crew.agents
            ],
            "tasks_count": len(self.crew.tasks),
            "process": str(self.crew.process),
            "verbose_level": self.crew.verbose
        }

# =============================================================================
# STANDALONE EXECUTION FUNCTIONS
# =============================================================================

def run_full_campaign_cycle():
    """
    Run the complete campaign cycle with all three agents
    """
    crew = CampaignPilotCrew()
    
    print("Campaign Pilot Multi-Agent System")
    print("=" * 50)
    print("🤖 Agent 1: Campaign Creator - Analyzes products and creates campaigns")
    print("📊 Agent 2: Data Analyzer - Monitors performance and generates insights") 
    print("⚖️  Agent 3: Campaign Manager - Makes optimization decisions")
    print("=" * 50)
    
    # Run the complete workflow
    results = crew.run_campaign_flow()
    
    return results

def run_analysis_only():
    """
    Run only the data analysis and campaign management tasks
    (assumes campaigns already exist)
    """
    crew = CampaignPilotCrew()
    
    # Create a modified crew with only analysis and management tasks
    analysis_crew = Crew(
        agents=[data_analyzer_agent, campaign_manager_agent],
        tasks=[data_analysis_task, campaign_management_task],
        process=Process.sequential,
        verbose=2
    )
    
    print("🔍 Running Analysis and Management Only...")
    results = analysis_crew.kickoff()
    
    return results

def run_campaign_creation_only():
    """
    Run only the campaign creation task
    """
    crew = CampaignPilotCrew()
    
    # Create a modified crew with only campaign creation
    creation_crew = Crew(
        agents=[campaign_creator_agent],
        tasks=[campaign_creation_task],
        process=Process.sequential,
        verbose=2
    )
    
    print("🎯 Running Campaign Creation Only...")
    results = creation_crew.kickoff()
    
    return results

if __name__ == "__main__":
    # Run the full cycle when script is executed directly
    run_full_campaign_cycle() 