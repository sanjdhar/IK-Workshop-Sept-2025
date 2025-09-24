#!/usr/bin/env python3
"""
Setup script for Generic Job Search Tool
Helps users configure their job search preferences interactively.
"""

import os
import json
from config_examples import get_config_by_role

def display_welcome():
    """Display welcome message and instructions"""
    print("=" * 60)
    print("🚀 GENERIC JOB SEARCH TOOL SETUP")
    print("=" * 60)
    print("\nWelcome! This tool will help you set up your job search preferences.")
    print("You can either:")
    print("1. Use a pre-configured template for common job roles")
    print("2. Create a custom configuration")
    print("3. Use the default Software Engineer configuration")
    print("-" * 60)

def show_available_templates():
    """Show available job role templates"""
    templates = {
        "1": ("Software Engineer", "software_engineer"),
        "2": ("Data Scientist", "data_scientist"),
        "3": ("Marketing Manager", "marketing_manager"),
        "4": ("Database Engineer", "database_engineer"),
        "5": ("Entry Level Software Engineer", "entry_level_swe"),
        "6": ("Product Manager", "product_manager"),
        "7": ("DevOps Engineer", "devops_engineer"),
        "8": ("UX Designer", "ux_designer")
    }
    
    print("\nAvailable job role templates:")
    for key, (display_name, _) in templates.items():
        print(f"{key}. {display_name}")
    print("9. Custom configuration")
    print("0. Use default (Software Engineer)")
    
    return templates

def get_user_input(prompt, default=""):
    """Get user input with optional default"""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()

def create_custom_config():
    """Create a custom job search configuration"""
    print("\n📝 Creating custom configuration...")
    print("Press Enter to use default values shown in brackets.")
    
    config = {}
    
    # Basic job info
    config["title"] = get_user_input("Job title", "Software Engineer")
    
    # Alternative titles
    alt_titles_input = get_user_input("Alternative job titles (comma-separated)", 
                                     "Software Developer, Full Stack Developer")
    config["alternative_titles"] = [title.strip() for title in alt_titles_input.split(',')]
    
    # Experience
    config["years"] = get_user_input("Years of experience", "2-5")
    config["level"] = get_user_input("Experience level (entry-level/beginner/intermediate/advanced/expert)", 
                                   "intermediate")
    
    # Skills
    config["required_skills"] = get_user_input("Required skills (comma-separated)", 
                                             "Python, JavaScript, React")
    
    preferred_skills_input = get_user_input("Preferred skills (comma-separated)", 
                                          "Node.js, AWS, Docker")
    config["preferred_skills"] = [skill.strip() for skill in preferred_skills_input.split(',')]
    
    # Location and salary
    config["location_preference"] = get_user_input("Location preference", "remote")
    config["salary_expectation"] = get_user_input("Salary expectation", "$80,000 - $120,000")
    config["min_salary"] = get_user_input("Minimum salary (numbers only)", "80000")
    config["max_salary"] = get_user_input("Maximum salary (numbers only)", "120000")
    
    # Career goals
    config["career_goals"] = get_user_input("Career goals", 
                                          "Growth in software engineering and technical leadership")
    
    # Target companies
    config["target_companies"] = get_user_input("Target companies (comma-separated)", 
                                              "Google, Microsoft, Amazon, Apple, Meta")
    
    # Other settings
    config["include_internships"] = get_user_input("Include internships? (yes/no)", "no")
    config["search_keywords"] = get_user_input("Quick search keywords", 
                                             f"{config['title']} remote")
    
    return config

def save_config_to_file(config):
    """Save configuration to config.py file"""
    config_content = f'''"""
Configuration file for Generic Job Search Tool
Customize these settings to match your job search preferences.
"""

# Job Search Configuration
JOB_CONFIG = {{
    # Basic job preferences
    "title": "{config['title']}",
    "alternative_titles": {config['alternative_titles']},
    
    # Experience and skill level
    "years": "{config['years']}",
    "level": "{config['level']}",
    
    # Required skills (must have) - comma separated string for tools
    "required_skills": "{config['required_skills']}",
    
    # Preferred skills (nice to have)
    "preferred_skills": {config['preferred_skills']},
    
    # Location and work preferences
    "location_preference": "{config['location_preference']}",
    
    # Salary expectations
    "salary_expectation": "{config['salary_expectation']}",
    "min_salary": "{config['min_salary']}",
    "max_salary": "{config['max_salary']}",
    
    # Career goals
    "career_goals": "{config['career_goals']}",
    
    # Company targeting (for company-specific searches)
    "target_companies": "{config['target_companies']}",
    
    # Entry-level specific settings
    "include_internships": "{config['include_internships']}",
    
    # Quick search keywords
    "search_keywords": "{config['search_keywords']}"
}}

# Search Type Descriptions
SEARCH_DESCRIPTIONS = {{
    "standard": {{
        "name": "Standard Search",
        "description": "Comprehensive job search with detailed analysis",
        "best_for": "General job searching with balanced results",
        "output_files": ["job-results-2.json", "new-job-analysis-2.md"]
    }},
    
    "salary_focused": {{
        "name": "Salary Focused Search", 
        "description": "Search specifically for jobs within your salary range",
        "best_for": "When salary is your primary concern",
        "output_files": ["salary-focused-results.md", "new-job-analysis-2.md"]
    }},
    
    "company_targeted": {{
        "name": "Company Targeted Search",
        "description": "Search for roles at specific target companies",
        "best_for": "When you have preferred companies to work for",
        "output_files": ["company-targeted-results.md", "new-job-analysis-2.md"]
    }},
    
    "entry_level": {{
        "name": "Entry Level Search",
        "description": "Find entry-level positions and internships",
        "best_for": "New graduates or career changers",
        "output_files": ["entry-level-results.md", "new-job-analysis-2.md"]
    }},
    
    "quick": {{
        "name": "Quick Search",
        "description": "Fast search with minimal filtering for immediate results",
        "best_for": "Quick market overview or urgent job searching",
        "output_files": ["quick-search-results.md"]
    }},
    
    "full": {{
        "name": "Full Search",
        "description": "Complete search with analysis and outreach messages",
        "best_for": "Comprehensive job search with networking support",
        "output_files": ["job-results-2.json", "new-job-analysis-2.md", "new-job-post-2.md"]
    }}
}}

# API Configuration (loaded from .env file)
API_CONFIG = {{
    "serper_api_key_required": True,
    "gemini_api_key_required": True,
    "rate_limit_retry_attempts": 3,
    "rate_limit_retry_delay": 20  # seconds
}}

# Output Configuration
OUTPUT_CONFIG = {{
    "output_directory": "./job-posts/",
    "create_directory_if_missing": True,
    "timestamp_files": False,
    "max_results_per_search": 10
}}

def get_config_for_search_type(search_type):
    """Get configuration specific to a search type"""
    config = JOB_CONFIG.copy()
    
    # Adjust config based on search type
    if search_type == "entry_level":
        config.update({{
            "years": "0-2",
            "level": "entry-level",
            "title": f"Entry Level {{config['title']}}"
        }})
    elif search_type == "salary_focused":
        config.update({{
            "title": f"{{config['title']}} ${{config['min_salary']}}-${{config['max_salary']}}"
        }})
    
    return config

def validate_config():
    """Validate that required configuration is present"""
    required_fields = ["title", "required_skills", "location_preference"]
    
    for field in required_fields:
        if field not in JOB_CONFIG or not JOB_CONFIG[field]:
            raise ValueError(f"Required configuration field '{{field}}' is missing or empty")
    
    return True

if __name__ == "__main__":
    # Test configuration
    try:
        validate_config()
        print("✅ Configuration is valid")
        
        # Display current configuration
        print("\\n📋 Current Job Search Configuration:")
        print("-" * 50)
        for key, value in JOB_CONFIG.items():
            if isinstance(value, list):
                print(f"{{key}}: {{', '.join(value)}}")
            else:
                print(f"{{key}}: {{value}}")
                
    except ValueError as e:
        print(f"❌ Configuration error: {{e}}")
'''
    
    try:
        with open('config.py', 'w') as f:
            f.write(config_content)
        print("✅ Configuration saved to config.py")
        return True
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")
        return False

def main():
    """Main setup flow"""
    display_welcome()
    
    templates = show_available_templates()
    
    while True:
        try:
            choice = input("\\nSelect an option (0-9): ").strip()
            
            if choice == "0":
                # Use default
                print("\\n✅ Using default Software Engineer configuration.")
                print("You can customize it later by editing config.py")
                break
                
            elif choice in templates:
                # Use template
                display_name, template_key = templates[choice]
                config = get_config_by_role(template_key)
                
                print(f"\\n📋 Using {display_name} template:")
                print(f"Title: {config['title']}")
                print(f"Skills: {config['required_skills']}")
                print(f"Salary: {config['salary_expectation']}")
                
                confirm = input("\\nUse this template? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    if save_config_to_file(config):
                        print(f"\\n✅ {display_name} configuration saved!")
                    break
                    
            elif choice == "9":
                # Custom configuration
                config = create_custom_config()
                
                print("\\n📋 Review your configuration:")
                print(f"Title: {config['title']}")
                print(f"Skills: {config['required_skills']}")
                print(f"Salary: {config['salary_expectation']}")
                print(f"Location: {config['location_preference']}")
                
                confirm = input("\\nSave this configuration? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    if save_config_to_file(config):
                        print("\\n✅ Custom configuration saved!")
                    break
                    
            else:
                print("❌ Invalid choice. Please enter a number between 0-9.")
                
        except KeyboardInterrupt:
            print("\\n👋 Setup cancelled.")
            return
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\\n🎯 Setup complete! You can now run:")
    print("   python run_search.py")
    print("\\nOr customize your configuration further by editing config.py")

if __name__ == "__main__":
    main()