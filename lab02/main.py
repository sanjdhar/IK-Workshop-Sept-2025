from dotenv import load_dotenv
load_dotenv()
import time

from crewai import Crew, LLM
from agents import JobSearchAgent, AnalysisAgent, CompanyTargetedAgent, EntryLevelAgent
from tasks import JobSearch, Analysis, SalaryFocusedSearch, CompanyTargetedSearch, EntryLevelSearch, QuickSearch
from litellm.files.main import RateLimitError
import os

serper_api_key = os.getenv("SERPER_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL")

# Configure Gemini LLM
gemini_llm = LLM(
    model="gemini/{gemini_model}",
    api_key=gemini_api_key
)

def create_crew(search_type="standard"):
    """Create different crew configurations based on search type"""
    
    if search_type == "salary_focused":
        return Crew(
            agents=[JobSearchAgent, AnalysisAgent],
            tasks=[SalaryFocusedSearch, Analysis],
            verbose=True,
            planning=False
        )
    elif search_type == "company_targeted":
        return Crew(
            agents=[CompanyTargetedAgent, AnalysisAgent],
            tasks=[CompanyTargetedSearch, Analysis],
            verbose=True,
            planning=False
        )
    elif search_type == "entry_level":
        return Crew(
            agents=[EntryLevelAgent, AnalysisAgent],
            tasks=[EntryLevelSearch, Analysis],
            verbose=True,
            planning=False
        )
    elif search_type == "quick":
        return Crew(
            agents=[JobSearchAgent],
            tasks=[QuickSearch],
            verbose=True,
            planning=False
        )
    elif search_type == "full":
        return Crew(
            agents=[JobSearchAgent, AnalysisAgent,],
            tasks=[JobSearch, Analysis,],
            verbose=True,
            planning=False
        )
    else:  # standard
        return Crew(
            agents=[JobSearchAgent, AnalysisAgent],
            tasks=[JobSearch, Analysis],
            verbose=True,
            planning=False
        )

def get_search_inputs(search_type="standard"):
    """Get appropriate inputs based on search type"""
    try:
        from config import get_config_for_search_type
        return get_config_for_search_type(search_type)
    except ImportError:
        # Fallback to hardcoded config if config.py is not available
        base_inputs = {
            "title": "Oracle Database Engineer",
            "alternative_titles": ["Oracle DBA", "Database Administrator", "Oracle Developer", "PL/SQL Developer"],
            "years": "1-3",
            "level": "beginner/intermediate",
            "required_skills": ["Oracle", "SQL", "PL/SQL"],
            "preferred_skills": ["Performance Tuning", "Oracle RAC", "Backup & Recovery"],
            "location_preference": "remote",
            "salary_expectation": "$70,000 - $110,000",
            "career_goals": "Growth in database engineering and administration"
        }
        
        if search_type == "salary_focused":
            base_inputs.update({
                "min_salary": "70000",
                "max_salary": "110000"
            })
        elif search_type == "company_targeted":
            base_inputs.update({
                "target_companies": "Oracle, Microsoft, Amazon, Google, IBM"
            })
        elif search_type == "entry_level":
            base_inputs.update({
                "include_internships": "yes",
                "years": "0-2",
                "level": "entry-level"
            })
        elif search_type == "quick":
            base_inputs.update({
                "search_keywords": "Oracle DBA remote"
            })
        
        return base_inputs

def run_job_search(search_type="standard"):
    """Run job search with specified type"""
    print(f"🚀 Starting {search_type} job search...")
    
    crew = create_crew(search_type)
    inputs = get_search_inputs(search_type)
    
    for attempts in range(3):
        try:
            result = crew.kickoff(inputs=inputs)
            print(f"✅ {search_type.title()} search completed successfully.")
            return result
        except RateLimitError as e:
            print(f"Rate Limit hit. Retrying in 20s.... (Attempt: {attempts+1})")
            time.sleep(20)
        except Exception as e:
            print(f"❌ Unexpected error in {search_type} search: {e}")
            break
    
    return None

if __name__ == "__main__":
    # You can change this to run different search types
    # Options: "standard", "salary_focused", "company_targeted", "entry_level", "quick", "full"
    
    search_type = "standard"  # Change this to test different search types
    
    print("Available search types:")
    print("- standard: Basic Oracle job search with analysis")
    print("- salary_focused: Search jobs within specific salary range")
    print("- company_targeted: Search at specific companies")
    print("- entry_level: Search for entry-level positions")
    print("- quick: Fast search with minimal filtering")
    print("- full: Complete search with messaging")
    print(f"\nRunning: {search_type}")
    
    result = run_job_search(search_type)