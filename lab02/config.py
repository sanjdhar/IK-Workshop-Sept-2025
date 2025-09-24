"""
Configuration file for Generic Job Search Tool
Customize these settings to match your job search preferences.
"""

# Job Search Configuration
JOB_CONFIG = {
    # Basic job preferences
    "title": "Software Engineer",
    "alternative_titles": [
        "Software Developer", 
        "Full Stack Developer", 
        "Backend Developer", 
        "Frontend Developer",
        "Web Developer",
        "Application Developer"
    ],
    
    # Experience and skill level
    "years": "2-5",  # Years of experience
    "level": "intermediate",  # entry-level, beginner, intermediate, advanced, expert
    
    # Required skills (must have) - comma separated string for tools
    "required_skills": "Python, JavaScript, React",
    
    # Preferred skills (nice to have)
    "preferred_skills": [
        "Node.js",
        "AWS", 
        "Docker"
    ],
    
    # Location and work preferences
    "location_preference": "San Francisco, California",  # remote, hybrid, onsite, or specific city
    
    # Salary expectations
    "salary_expectation": "$80,000 - $190,000",
    "min_salary": "80000",
    "max_salary": "250000",
    
    # Career goals
    "career_goals": "Growth in software engineering and technical leadership",
    
    # Company targeting (for company-specific searches)
    "target_companies": "Google, Microsoft, Amazon, Apple, Meta, Netflix, Spotify",
    
    # Entry-level specific settings
    "include_internships": "no",  # yes or no
    
    # Quick search keywords
    "search_keywords": "Software Engineer remote"
}

# Search Type Descriptions
SEARCH_DESCRIPTIONS = {
    "standard": {
        "name": "Standard Search",
        "description": "Comprehensive job search with detailed analysis",
        "best_for": "General job searching with balanced results",
        "output_files": ["job-results-2.json", "new-job-analysis-2.md"]
    },
    
    "salary_focused": {
        "name": "Salary Focused Search", 
        "description": "Search specifically for jobs within your salary range",
        "best_for": "When salary is your primary concern",
        "output_files": ["salary-focused-results.md", "new-job-analysis-2.md"]
    },
    
    "company_targeted": {
        "name": "Company Targeted Search",
        "description": "Search for roles at specific target companies",
        "best_for": "When you have preferred companies to work for",
        "output_files": ["company-targeted-results.md", "new-job-analysis-2.md"]
    },
    
    "entry_level": {
        "name": "Entry Level Search",
        "description": "Find entry-level positions and internships",
        "best_for": "New graduates or career changers",
        "output_files": ["entry-level-results.md", "new-job-analysis-2.md"]
    },
    
    "quick": {
        "name": "Quick Search",
        "description": "Fast search with minimal filtering for immediate results",
        "best_for": "Quick market overview or urgent job searching",
        "output_files": ["quick-search-results.md"]
    },
    
    "full": {
        "name": "Full Search",
        "description": "Complete search with analysis and outreach messages",
        "best_for": "Comprehensive job search with networking support",
        "output_files": ["job-results-2.json", "new-job-analysis-2.md", "new-job-post-2.md"]
    }
}

# API Configuration (loaded from .env file)
API_CONFIG = {
    "serper_api_key_required": True,
    "gemini_api_key_required": True,
    "rate_limit_retry_attempts": 3,
    "rate_limit_retry_delay": 20  # seconds
}

# Output Configuration
OUTPUT_CONFIG = {
    "output_directory": "./job-posts/",
    "create_directory_if_missing": True,
    "timestamp_files": False,
    "max_results_per_search": 10
}

def get_config_for_search_type(search_type):
    """Get configuration specific to a search type"""
    config = JOB_CONFIG.copy()
    
    # Adjust config based on search type
    if search_type == "entry_level":
        config.update({
            "years": "0-2",
            "level": "entry-level",
            "title": f"Entry Level {config['title']}"
        })
    elif search_type == "salary_focused":
        config.update({
            "title": f"{config['title']} ${config['min_salary']}-${config['max_salary']}"
        })
    
    return config

def validate_config():
    """Validate that required configuration is present"""
    required_fields = ["title", "required_skills", "location_preference"]
    
    for field in required_fields:
        if field not in JOB_CONFIG or not JOB_CONFIG[field]:
            raise ValueError(f"Required configuration field '{field}' is missing or empty")
    
    return True

if __name__ == "__main__":
    # Test configuration
    try:
        validate_config()
        print("✅ Configuration is valid")
        
        # Display current configuration
        print("\n📋 Current Job Search Configuration:")
        print("-" * 50)
        for key, value in JOB_CONFIG.items():
            if isinstance(value, list):
                print(f"{key}: {', '.join(value)}")
            else:
                print(f"{key}: {value}")
                
    except ValueError as e:
        print(f"❌ Configuration error: {e}")