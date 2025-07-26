#!/usr/bin/env python3
"""
Campaign Pilot Multi-Agent System - Main Runner
Command-line interface for running the campaign automation system
"""

import os
import sys
import argparse
import time
from datetime import datetime
from dotenv import load_dotenv
from colorama import init, Fore, Style
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from logger import get_logger, log_system_event, LogLevel

# Load environment variables
load_dotenv()

# Initialize colorama for cross-platform colored output
init(autoreset=True)
console = Console()

def check_prerequisites():
    """Check if all prerequisites are met before running agents"""
    
    console.print("\n🔍 Checking Prerequisites...", style="bold blue")
    
    # Check OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        console.print("❌ OpenAI API key not found. Please set OPENAI_API_KEY in .env file", style="bold red")
        return False
    
    # Check if fake API server is running
    try:
        import requests
        response = requests.get('http://localhost:6000/api/health', timeout=5)
        if response.status_code == 200:
            console.print("✅ Fake API server is running", style="bold green")
        else:
            console.print("❌ Fake API server responded with error", style="bold red")
            return False
    except requests.RequestException:
        console.print("❌ Fake API server is not running. Please start it first with:", style="bold red")
        console.print("   python fake_api_server.py", style="cyan")
        return False
    
    # Check required packages
    try:
        import crewai
        import langchain
        console.print("✅ Required packages installed", style="bold green")
    except ImportError as e:
        console.print(f"❌ Missing required package: {e}", style="bold red")
        console.print("   Install with: pip install -r requirements.txt", style="cyan")
        return False
    
    console.print("✅ All prerequisites met!", style="bold green")
    return True

def display_banner():
    """Display the application banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                  CAMPAIGN PILOT MULTI-AGENT SYSTEM          ║
    ║                                                              ║
    ║  🤖 Agent 1: Campaign Creator - Product analysis & campaigns ║
    ║  📊 Agent 2: Data Analyzer - Performance monitoring         ║
    ║  ⚖️  Agent 3: Campaign Manager - Optimization decisions      ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")

def run_full_system():
    """Run the complete multi-agent system"""
    from crew import run_full_campaign_cycle
    
    console.print("\n🚀 Starting Full Campaign Cycle...", style="bold blue")
    
    # Log system start
    log_system_event("Full Campaign Cycle Started", {"timestamp": datetime.now().isoformat()})
    
    try:
        start_time = time.time()
        results = run_full_campaign_cycle()
        end_time = time.time()
        duration = end_time - start_time
        
        # Log completion
        log_system_event("Full Campaign Cycle Completed", {
            "duration_seconds": duration,
            "success": True,
            "results_summary": str(results)[:500] if results else "No results"
        })
        
        console.print(f"\n✅ Campaign cycle completed in {duration:.2f} seconds", style="bold green")
        
        # Export logs
        logger = get_logger()
        html_report = logger.export_logs("html")
        console.print(f"📊 Demo report saved: {html_report}", style="bold cyan")
        
        return results
        
    except Exception as e:
        # Log failure
        log_system_event("Full Campaign Cycle Failed", {
            "error": str(e),
            "success": False
        }, LogLevel.ERROR)
        
        console.print(f"\n❌ Campaign cycle failed: {str(e)}", style="bold red")
        return None

def run_campaign_creation():
    """Run only campaign creation"""
    from crew import run_campaign_creation_only
    
    console.print("\n🎯 Starting Campaign Creation...", style="bold blue")
    
    try:
        results = run_campaign_creation_only()
        console.print("\n✅ Campaign creation completed", style="bold green")
        return results
        
    except Exception as e:
        console.print(f"\n❌ Campaign creation failed: {str(e)}", style="bold red")
        return None

def run_analysis_management():
    """Run analysis and management only"""
    from crew import run_analysis_only
    
    console.print("\n🔍 Starting Analysis and Management...", style="bold blue")
    
    try:
        results = run_analysis_only()
        console.print("\n✅ Analysis and management completed", style="bold green")
        return results
        
    except Exception as e:
        console.print(f"\n❌ Analysis and management failed: {str(e)}", style="bold red")
        return None

def show_api_status():
    """Display current API status and available data"""
    import requests
    
    console.print("\n📊 API Status and Data Overview", style="bold blue")
    
    try:
        # Check API health
        health_response = requests.get('http://localhost:6000/api/health', timeout=5)
        if health_response.status_code == 200:
            console.print("✅ API Server: Online", style="green")
        
        # Get products
        products_response = requests.get('http://localhost:6000/api/store/products', timeout=5)
        if products_response.status_code == 200:
            products_data = products_response.json()
            console.print(f"📦 Products Available: {products_data['count']}", style="cyan")
        
        # Get campaigns
        campaigns_response = requests.get('http://localhost:6000/api/impact/campaigns', timeout=5)
        if campaigns_response.status_code == 200:
            campaigns_data = campaigns_response.json()
            console.print(f"🎯 Active Campaigns: {campaigns_data['count']}", style="cyan")
            
            if campaigns_data['count'] > 0:
                table = Table(title="Active Campaigns")
                table.add_column("Campaign ID", style="cyan")
                table.add_column("Product", style="magenta")
                table.add_column("Status", style="green")
                table.add_column("Budget", style="yellow")
                
                for campaign in campaigns_data['data'][:5]:  # Show first 5
                    table.add_row(
                        campaign['campaign_id'],
                        campaign.get('campaign_name', 'N/A'),
                        campaign['status'],
                        f"${campaign['budget']:.2f}"
                    )
                
                console.print(table)
        
    except requests.RequestException as e:
        console.print(f"❌ Could not fetch API status: {e}", style="bold red")

def reset_system():
    """Reset all campaign data"""
    import requests
    
    console.print("\n🔄 Resetting Campaign Data...", style="bold yellow")
    
    try:
        response = requests.post('http://localhost:6000/api/reset', timeout=5)
        if response.status_code == 200:
            console.print("✅ All campaign data has been reset", style="bold green")
        else:
            console.print("❌ Failed to reset data", style="bold red")
            
    except requests.RequestException as e:
        console.print(f"❌ Could not reset data: {e}", style="bold red")

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="Campaign Pilot Multi-Agent System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --full                 # Run complete campaign cycle
  python main.py --create               # Only create campaigns
  python main.py --analyze              # Only analyze and manage campaigns
  python main.py --status               # Show API status and data
  python main.py --reset                # Reset all campaign data
        """
    )
    
    parser.add_argument('--full', action='store_true', 
                       help='Run the complete multi-agent campaign cycle')
    parser.add_argument('--create', action='store_true',
                       help='Run only campaign creation')
    parser.add_argument('--analyze', action='store_true',
                       help='Run only analysis and management')
    parser.add_argument('--status', action='store_true',
                       help='Show API status and current data')
    parser.add_argument('--reset', action='store_true',
                       help='Reset all campaign data')
    parser.add_argument('--skip-checks', action='store_true',
                       help='Skip prerequisite checks')
    parser.add_argument('--demo-session', type=str,
                       help='Custom session name for demo logging')
    parser.add_argument('--export-logs', choices=['json', 'csv', 'html'],
                       help='Export logs in specified format after execution')
    
    args = parser.parse_args()
    
    # Display banner
    display_banner()
    
    # Initialize logging with custom session name if provided
    if args.demo_session:
        logger = get_logger(session_name=args.demo_session)
        console.print(f"📊 Demo session: {args.demo_session}", style="bold cyan")
    else:
        logger = get_logger()
    
    # Check prerequisites unless skipped
    if not args.skip_checks:
        if not check_prerequisites():
            log_system_event("Prerequisites Check Failed", {"success": False}, LogLevel.ERROR)
            sys.exit(1)
    
    # Log session start
    log_system_event("Campaign Pilot Session Started", {
        "arguments": vars(args),
        "session_id": logger.session_id
    })
    
    # Execute requested action
    if args.status:
        show_api_status()
    elif args.reset:
        reset_system()
    elif args.create:
        run_campaign_creation()
    elif args.analyze:
        run_analysis_management()
    elif args.full:
        run_full_system()
    else:
        # Interactive mode
        console.print("\n🎛️  Interactive Mode", style="bold blue")
        console.print("Choose an action:")
        console.print("1. Run full campaign cycle")
        console.print("2. Create campaigns only")
        console.print("3. Analyze and manage campaigns")
        console.print("4. Show API status")
        console.print("5. Reset data")
        console.print("6. Exit")
        
        while True:
            try:
                choice = input(f"\n{Fore.CYAN}Enter your choice (1-6): {Style.RESET_ALL}")
                
                if choice == '1':
                    run_full_system()
                    break
                elif choice == '2':
                    run_campaign_creation()
                    break
                elif choice == '3':
                    run_analysis_management()
                    break
                elif choice == '4':
                    show_api_status()
                    break
                elif choice == '5':
                    reset_system()
                    break
                elif choice == '6':
                    console.print("👋 Goodbye!", style="bold blue")
                    break
                else:
                    console.print("❌ Invalid choice. Please enter 1-6.", style="bold red")
                    
            except KeyboardInterrupt:
                console.print("\n👋 Goodbye!", style="bold blue")
                break
    
    # Export logs if requested
    if args.export_logs:
        try:
            logger = get_logger()
            export_file = logger.export_logs(args.export_logs)
            console.print(f"📁 Logs exported to: {export_file}", style="bold green")
        except Exception as e:
            console.print(f"❌ Failed to export logs: {e}", style="bold red")
    
    # Save session data
    try:
        logger = get_logger()
        session_file = logger.save_session()
        console.print(f"💾 Session data saved for future reference", style="bold blue")
    except Exception as e:
        console.print(f"⚠️  Could not save session: {e}", style="yellow")

if __name__ == "__main__":
    main() 