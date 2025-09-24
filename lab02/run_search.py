#!/usr/bin/env python3
"""
Interactive Generic Job Search Tool
Run different types of job searches with specialized agents and tools.
"""

from main import run_job_search
import sys

def display_menu():
    """Display the search type menu"""
    print("\n" + "="*60)
    print("🔍 SIMPLE AGENTIC AI JOB FINDER")
    print("="*60)
    print("\nAvailable Search Types:")
    print("1. Quick Search - Fast search with minimal filtering")
    print("2. Salary Focused - Search jobs within specific salary range")
    print("3. Company Targeted - Search at specific companies")
    print("4. Entry Level - Search for entry-level and junior positions")
    print("5. Standard Search - Comprehensive job search with analysis")
    print("6. Full Search - Complete search with messaging")
    print("7. Exit")
    print("-"*60)

def get_user_choice():
    """Get user's search type choice"""
    while True:
        try:
            choice = input("Enter your choice (1-7): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                return int(choice)
            else:
                print("❌ Invalid choice. Please enter a number between 1-7.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
        except Exception:
            print("❌ Invalid input. Please enter a number between 1-7.")

def main():
    """Main interactive loop"""
    search_types = {
        1: "quick",
        2: "salary_focused", 
        3: "company_targeted",
        4: "entry_level",
        5: "standard",
        6: "full"
    }
    
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == 7:
            print("👋 Goodbye!")
            break
        
        search_type = search_types[choice]
        print(f"\n🚀 Starting {search_type.replace('_', ' ').title()} Search...")
        print("⏳ This may take a few minutes...")
        
        try:
            result = run_job_search(search_type)
            if result:
                print(f"\n✅ {search_type.replace('_', ' ').title()} search completed!")
                print("📁 Check the ./job-posts/ directory for results.")
            else:
                print(f"\n❌ {search_type.replace('_', ' ').title()} search failed.")
        except Exception as e:
            print(f"\n❌ Error during search: {e}")
        
        # Ask if user wants to run another search
        while True:
            continue_choice = input("\n🔄 Run another search? (y/n): ").strip().lower()
            if continue_choice in ['y', 'yes']:
                break
            elif continue_choice in ['n', 'no']:
                print("👋 Goodbye!")
                return
            else:
                print("❌ Please enter 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    main()