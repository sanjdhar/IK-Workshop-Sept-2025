import os
import json
import requests
from pathlib import Path
from crewai.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool("directory_read_tool")
def docs_tool(query: str = "") -> str:
    """Read all markdown files in the job-posts directory"""
    directory = "./job-posts"
    results = []
    if os.path.exists(directory):
        for file_path in Path(directory).glob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    results.append(f"File: {file_path}\n{content}\n{'='*50}")
            except Exception as e:
                results.append(f"Error reading {file_path}: {e}")
    return "\n".join(results) if results else "No markdown files found in directory"

@tool("file_read_tool")
def file_tool(file_path: str) -> str:
    """Read the contents of a specific file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {e}"

@tool("progressive_search_tool")
def progressive_search_tool(primary_title: str, alternative_titles: str = "", experience_level: str = "", location: str = "remote") -> str:
    """Progressive search strategy for job roles - tries multiple approaches until results found"""
    serper_api_key = os.getenv("SERPER_API_KEY")
    
    if not serper_api_key:
        return "Error: SERPER_API_KEY not found in environment variables"
    
    # Progressive search strategies
    search_strategies = [
        f"{primary_title} {experience_level} {location}",
        f"{primary_title} {location}"
    ]
    
    # Add alternative titles to strategies
    if alternative_titles:
        try:
            alt_titles = eval(alternative_titles) if isinstance(alternative_titles, str) else alternative_titles
            for alt_title in alt_titles:
                search_strategies.insert(1, f"{alt_title} {experience_level} {location}")
        except:
            pass
    
    url = "https://serpapi.com/search.json"
    
    for i, strategy in enumerate(search_strategies):
        try:
            params = {
                "q": strategy,
                "engine": "google_jobs",
                "num": 8,
                "api_key": serper_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'jobs_results' in data and len(data['jobs_results']) > 0:
                results = []
                for job in data['jobs_results']:
                    # Enhanced remote filtering
                    job_location = job.get('location', '').lower()
                    job_title = job.get('title', '').lower()
                    job_desc = job.get('description', '').lower()
                    
                    remote_indicators = ['remote', 'work from home', 'telecommute', 'anywhere', 'wfh']
                    is_remote = any(indicator in job_location or indicator in job_title or indicator in job_desc 
                                  for indicator in remote_indicators)
                    
                    if location.lower() == "remote" and not is_remote:
                        continue
                    
                    detected_ext = job.get('detected_extensions', {})
                    
                    job_info = {
                        "title": job.get('title', 'N/A'),
                        "company": job.get('company_name', 'N/A'),
                        "location": job.get('location', 'N/A'),
                        "link": job.get('share_link', 'N/A'),
                        "description": job.get('description', 'N/A'),
                        "salary": detected_ext.get('salary', 'Not specified'),
                        "job_type": detected_ext.get('schedule_type', 'N/A'),
                        "source": job.get('via', 'N/A'),
                        "posted_date": detected_ext.get('posted_at', 'N/A'),
                        "search_strategy_used": f"Strategy {i+1}: {strategy}"
                    }
                    results.append(job_info)
                
                if results:
                    formatted_results = f"Found {len(results)} job listings using search strategy: '{strategy}'\n\n"
                    
                    for j, job in enumerate(results, 1):
                        formatted_results += f"{j}. **{job['title']}**\n"
                        formatted_results += f"   Company: {job['company']}\n"
                        formatted_results += f"   Location: {job['location']}\n"
                        formatted_results += f"   Salary: {job['salary']}\n"
                        formatted_results += f"   Type: {job['job_type']}\n"
                        formatted_results += f"   Link: {job['link']}\n"
                        formatted_results += f"   Description: {job['description'][:200]}...\n\n"
                    
                    return formatted_results
                    
        except Exception as e:
            continue
    
    return f"No job listings found after trying {len(search_strategies)} different search strategies. Consider broadening search criteria."

@tool("search_tool")
def search_tool(query: str) -> str:
    """Enhanced search for job listings using SerpAPI Google Jobs API"""
    serper_api_key = os.getenv("SERPER_API_KEY")
    
    if not serper_api_key:
        return "Error: SERPER_API_KEY not found in environment variables"
    
    # Use SerpAPI Google Jobs endpoint
    url = "https://serpapi.com/search.json"
    
    params = {
        "q": f"{query} remote",
        "engine": "google_jobs",
        "num": 10,
        "api_key": serper_api_key
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract job results from Google Jobs API response
        results = []
        
        if 'jobs_results' in data:
            for job in data['jobs_results'][:8]:  # Limit to top 8 results
                # Extract salary and other details from detected_extensions
                detected_ext = job.get('detected_extensions', {})
                
                job_info = {
                    "title": job.get('title', 'N/A'),
                    "company": job.get('company_name', 'N/A'),
                    "location": job.get('location', 'N/A'),
                    "link": job.get('share_link', 'N/A'),
                    "description": job.get('description', 'N/A'),
                    "salary": detected_ext.get('salary', 'Not specified'),
                    "job_type": detected_ext.get('schedule_type', 'N/A'),
                    "source": job.get('via', 'N/A'),
                    "posted_date": detected_ext.get('posted_at', 'N/A')
                }
                results.append(job_info)
        
        if not results:
            return f"No job listings found for '{query}'. Try a different search term or check if the API key is valid."
        
        # Format results as structured text
        formatted_results = f"Found {len(results)} job listings for '{query}':\n\n"
        
        for i, job in enumerate(results, 1):
            formatted_results += f"{i}. **{job['title']}**\n"
            formatted_results += f"   Company: {job['company']}\n"
            formatted_results += f"   Location: {job['location']}\n"
            formatted_results += f"   Salary: {job['salary']}\n"
            formatted_results += f"   Type: {job['job_type']}\n"
            formatted_results += f"   Link: {job['link']}\n"
            formatted_results += f"   Description: {job['description'][:200]}...\n\n"
        
        return formatted_results
        
    except requests.exceptions.RequestException as e:
        return f"Error making request to SerpAPI: {str(e)}. Please check your API key and internet connection."
    except json.JSONDecodeError as e:
        return f"Error parsing response from SerpAPI: {str(e)}. The API may be returning invalid data."
    except Exception as e:
        return f"Unexpected error in search_tool: {str(e)}"



@tool("job_search")
def job_search(title: str, required_skills: str = "", alternative_titles: str = "", experience_level: str = "", location: str = "remote") -> str:
    """Generic job search tool with skill-based filtering"""
    serper_api_key = os.getenv("SERPER_API_KEY")
    
    if not serper_api_key:
        return json.dumps({"error": "SERPER_API_KEY not found in environment variables"}, indent=2)
    
    # Parse required skills and alternative titles
    try:
        skill_list = [skill.strip().lower() for skill in required_skills.split(',')] if required_skills else []
        alt_titles = [title.strip() for title in alternative_titles.split(',')] if alternative_titles else []
    except:
        skill_list = []
        alt_titles = []
    
    # Build search strategies
    search_queries = [f"{title} {experience_level} {location}".strip()]
    
    # Add alternative titles to search
    for alt_title in alt_titles:
        search_queries.append(f"{alt_title} {experience_level} {location}".strip())
    
    url = "https://serpapi.com/search.json"
    all_results = []
    
    for query in search_queries:
        try:
            params = {
                "q": query,
                "engine": "google_jobs",
                "num": 8,
                "api_key": serper_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'jobs_results' in data:
                for job in data['jobs_results']:
                    job_title = job.get('title', '').lower()
                    job_desc = job.get('description', '').lower()
                    
                    # Filter based on required skills if provided
                    if skill_list:
                        has_required_skills = any(skill in job_title or skill in job_desc for skill in skill_list)
                        if not has_required_skills:
                            continue
                    
                    # Check for remote work
                    job_location = job.get('location', '').lower()
                    remote_indicators = ['remote', 'work from home', 'telecommute', 'anywhere', 'wfh']
                    is_remote = any(indicator in job_location or indicator in job_title or indicator in job_desc 
                                  for indicator in remote_indicators)
                    
                    if location.lower() == "remote" and not is_remote:
                        continue
                    
                    detected_ext = job.get('detected_extensions', {})
                    
                    # Extract matching skills from description
                    found_skills = []
                    if skill_list:
                        for skill in skill_list:
                            if skill in job_desc:
                                found_skills.append(skill.title())
                    
                    job_info = {
                        "title": job.get('title', 'N/A'),
                        "company": job.get('company_name', 'N/A'),
                        "location": job.get('location', 'N/A'),
                        "link": job.get('share_link', 'N/A'),
                        "description": job.get('description', 'N/A'),
                        "salary": detected_ext.get('salary', 'Not specified'),
                        "job_type": detected_ext.get('schedule_type', 'N/A'),
                        "source": job.get('via', 'N/A'),
                        "posted_date": detected_ext.get('posted_at', 'N/A'),
                        "matching_skills": found_skills,
                        "relevance_score": len(found_skills)
                    }
                    
                    # Avoid duplicates
                    duplicate = False
                    for existing_job in all_results:
                        if (existing_job['title'].lower() == job_info['title'].lower() and 
                            existing_job['company'].lower() == job_info['company'].lower()):
                            duplicate = True
                            break
                    
                    if not duplicate:
                        all_results.append(job_info)
                        
        except Exception as e:
            continue
    
    if not all_results:
        return json.dumps({
            "message": f"No jobs found for '{title}' with {experience_level} experience.",
            "suggestion": "Try broadening your search criteria or using alternative job titles."
        }, indent=2)
    
    # Sort by relevance (more matching skills = higher relevance)
    all_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    return json.dumps(all_results[:10], indent=2)





@tool("web_tool")
def web_rag_tool(url: str) -> str:
    """Search websites for job information (placeholder implementation)"""
    return f"Web search functionality not implemented. URL was: {url}"


@tool("company_specific_search")
def company_specific_search(company_names: str, job_title: str, location: str = "remote") -> str:
    """Search for jobs at specific companies"""
    serper_api_key = os.getenv("SERPER_API_KEY")
    
    if not serper_api_key:
        return "Error: SERPER_API_KEY not found in environment variables"
    
    # Parse company names
    try:
        companies = [name.strip() for name in company_names.split(',')]
    except:
        companies = [company_names]
    
    url = "https://serpapi.com/search.json"
    all_results = []
    
    for company in companies:
        search_queries = [
            f"{job_title} {company} {location}",
            f"{job_title} at {company} {location}"
        ]
        
        for query in search_queries:
            try:
                params = {
                    "q": query,
                    "engine": "google_jobs",
                    "num": 5,
                    "api_key": serper_api_key
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if 'jobs_results' in data:
                    for job in data['jobs_results']:
                        # Check if company matches
                        job_company = job.get('company_name', '').lower()
                        if company.lower() not in job_company:
                            continue
                        
                        detected_ext = job.get('detected_extensions', {})
                        
                        job_info = {
                            "title": job.get('title', 'N/A'),
                            "company": job.get('company_name', 'N/A'),
                            "location": job.get('location', 'N/A'),
                            "salary": detected_ext.get('salary', 'Not specified'),
                            "link": job.get('share_link', 'N/A'),
                            "description": job.get('description', 'N/A')[:250] + "...",
                            "job_type": detected_ext.get('schedule_type', 'N/A'),
                            "posted_date": detected_ext.get('posted_at', 'N/A')
                        }
                        
                        # Avoid duplicates
                        duplicate = False
                        for existing_job in all_results:
                            if (existing_job['title'].lower() == job_info['title'].lower() and 
                                existing_job['company'].lower() == job_info['company'].lower()):
                                duplicate = True
                                break
                        
                        if not duplicate:
                            all_results.append(job_info)
                            
            except Exception as e:
                continue
    
    if not all_results:
        return f"No {job_title} jobs found at specified companies: {company_names}"
    
    # Format results
    formatted_results = f"Found {len(all_results)} {job_title} jobs at target companies:\\n\\n"
    
    for i, job in enumerate(all_results, 1):
        formatted_results += f"{i}. **{job['title']}**\\n"
        formatted_results += f"   Company: {job['company']}\\n"
        formatted_results += f"   Location: {job['location']}\\n"
        formatted_results += f"   Salary: {job['salary']}\\n"
        formatted_results += f"   Link: {job['link']}\\n"
        formatted_results += f"   Description: {job['description']}\\n\\n"
    
    return formatted_results


@tool("entry_level_search")
def entry_level_search(job_title: str, required_skills: str = "", location: str = "remote", include_internships: str = "no") -> str:
    """Search specifically for entry-level positions in any field"""
    serper_api_key = os.getenv("SERPER_API_KEY")
    
    if not serper_api_key:
        return "Error: SERPER_API_KEY not found in environment variables"
    
    # Entry-level focused search terms
    search_queries = [
        f"entry level {job_title} {location}",
        f"junior {job_title} {location}",
        f"{job_title} associate {location}",
        f"{job_title} trainee {location}",
        f"graduate {job_title} {location}"
    ]
    
    if include_internships.lower() == "yes":
        search_queries.extend([
            f"{job_title} intern {location}",
            f"{job_title} internship {location}"
        ])
    
    url = "https://serpapi.com/search.json"
    all_results = []
    
    for query in search_queries:
        try:
            params = {
                "q": query,
                "engine": "google_jobs",
                "num": 8,
                "api_key": serper_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'jobs_results' in data:
                for job in data['jobs_results']:
                    job_title = job.get('title', '').lower()
                    job_desc = job.get('description', '').lower()
                    
                    # Parse required skills
                    skill_list = [skill.strip().lower() for skill in required_skills.split(',')] if required_skills else []
                    
                    # Filter for entry-level indicators
                    entry_keywords = ['entry', 'junior', 'associate', 'trainee', 'intern', 'graduate', '0-2 years', 'new grad']
                    
                    has_entry_level = any(keyword in job_title or keyword in job_desc for keyword in entry_keywords)
                    
                    # Check for required skills if provided
                    has_required_skills = True
                    if skill_list:
                        has_required_skills = any(skill in job_title or skill in job_desc for skill in skill_list)
                    
                    # Skip senior/lead positions
                    senior_keywords = ['senior', 'lead', 'principal', 'architect', 'manager', '5+ years', '3+ years']
                    is_senior = any(keyword in job_title or keyword in job_desc for keyword in senior_keywords)
                    
                    if not has_required_skills or is_senior:
                        continue
                    
                    detected_ext = job.get('detected_extensions', {})
                    
                    job_info = {
                        "title": job.get('title', 'N/A'),
                        "company": job.get('company_name', 'N/A'),
                        "location": job.get('location', 'N/A'),
                        "salary": detected_ext.get('salary', 'Not specified'),
                        "link": job.get('share_link', 'N/A'),
                        "description": job.get('description', 'N/A')[:300] + "...",
                        "job_type": detected_ext.get('schedule_type', 'N/A'),
                        "posted_date": detected_ext.get('posted_at', 'N/A'),
                        "entry_level_indicator": "Yes" if has_entry_level else "Likely"
                    }
                    
                    # Avoid duplicates
                    duplicate = False
                    for existing_job in all_results:
                        if (existing_job['title'].lower() == job_info['title'].lower() and 
                            existing_job['company'].lower() == job_info['company'].lower()):
                            duplicate = True
                            break
                    
                    if not duplicate:
                        all_results.append(job_info)
                        
        except Exception as e:
            continue
    
    if not all_results:
        return f"No entry-level {job_title} jobs found in {location}. Consider expanding location or including internships."
    
    # Format results
    formatted_results = f"Found {len(all_results)} entry-level {job_title} positions:\\n\\n"
    
    for i, job in enumerate(all_results, 1):
        formatted_results += f"{i}. **{job['title']}**\\n"
        formatted_results += f"   Company: {job['company']}\\n"
        formatted_results += f"   Location: {job['location']}\\n"
        formatted_results += f"   Salary: {job['salary']}\\n"
        formatted_results += f"   Entry Level: {job['entry_level_indicator']}\\n"
        formatted_results += f"   Link: {job['link']}\\n"
        formatted_results += f"   Description: {job['description']}\\n\\n"
    
    return formatted_results


@tool("quick_search")
def quick_search(keywords: str, location: str = "remote") -> str:
    """Quick and simple job search with minimal filtering"""
    serper_api_key = os.getenv("SERPER_API_KEY")
    
    if not serper_api_key:
        return "Error: SERPER_API_KEY not found in environment variables"
    
    url = "https://serpapi.com/search.json"
    
    try:
        params = {
            "q": f"{keywords} {location}",
            "engine": "google_jobs",
            "num": 10,
            "api_key": serper_api_key
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'jobs_results' not in data or not data['jobs_results']:
            return f"No jobs found for '{keywords}' in {location}"
        
        results = []
        for job in data['jobs_results']:
            detected_ext = job.get('detected_extensions', {})
            
            job_info = {
                "title": job.get('title', 'N/A'),
                "company": job.get('company_name', 'N/A'),
                "location": job.get('location', 'N/A'),
                "salary": detected_ext.get('salary', 'Not specified'),
                "link": job.get('share_link', 'N/A'),
                "posted": detected_ext.get('posted_at', 'N/A')
            }
            results.append(job_info)
        
        # Format results
        formatted_results = f"Quick search results for '{keywords}' ({len(results)} jobs):\\n\\n"
        
        for i, job in enumerate(results, 1):
            formatted_results += f"{i}. {job['title']} at {job['company']}\\n"
            formatted_results += f"   📍 {job['location']} | 💰 {job['salary']} | 📅 {job['posted']}\\n"
            formatted_results += f"   🔗 {job['link']}\\n\\n"
        
        return formatted_results
        
    except Exception as e:
        return f"Error in quick search: {str(e)}"


@tool("salary_job_search")
def salary_job_search(title: str, min_salary: str = "50000", max_salary: str = "100000", required_skills: str = "", location: str = "remote") -> str:
    """Search for jobs within specific salary range"""
    serper_api_key = os.getenv("SERPER_API_KEY")
    
    if not serper_api_key:
        return "Error: SERPER_API_KEY not found in environment variables"
    
    # Parse required skills
    skill_list = [skill.strip().lower() for skill in required_skills.split(',')] if required_skills else []
    
    # Search with salary keywords
    search_queries = [
        f"{title} {location} salary ${min_salary} ${max_salary}",
        f"{title} {location} ${min_salary}k ${max_salary}k",
        f"{title} {location} salary range",
        f"{title} {location} compensation"
    ]
    
    url = "https://serpapi.com/search.json"
    all_results = []
    
    for query in search_queries:
        try:
            params = {
                "q": query,
                "engine": "google_jobs",
                "num": 8,
                "api_key": serper_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'jobs_results' in data:
                for job in data['jobs_results']:
                    detected_ext = job.get('detected_extensions', {})
                    salary_info = detected_ext.get('salary', '')
                    
                    # Filter by salary if available
                    if salary_info and salary_info != 'Not specified':
                        # Extract numeric values from salary
                        import re
                        salary_numbers = re.findall(r'\\$?([0-9,]+)', salary_info)
                        if salary_numbers:
                            try:
                                salary_value = int(salary_numbers[0].replace(',', ''))
                                if salary_value < int(min_salary) or salary_value > int(max_salary):
                                    continue
                            except:
                                pass
                    
                    # Check for required skills if provided
                    job_title = job.get('title', '').lower()
                    job_desc = job.get('description', '').lower()
                    
                    if skill_list:
                        has_required_skills = any(skill in job_title or skill in job_desc for skill in skill_list)
                        if not has_required_skills:
                            continue
                    
                    job_info = {
                        "title": job.get('title', 'N/A'),
                        "company": job.get('company_name', 'N/A'),
                        "location": job.get('location', 'N/A'),
                        "salary": salary_info,
                        "link": job.get('share_link', 'N/A'),
                        "description": job.get('description', 'N/A')[:300] + "...",
                        "job_type": detected_ext.get('schedule_type', 'N/A'),
                        "posted_date": detected_ext.get('posted_at', 'N/A')
                    }
                    
                    # Avoid duplicates
                    duplicate = False
                    for existing_job in all_results:
                        if (existing_job['title'].lower() == job_info['title'].lower() and 
                            existing_job['company'].lower() == job_info['company'].lower()):
                            duplicate = True
                            break
                    
                    if not duplicate:
                        all_results.append(job_info)
                        
        except Exception as e:
            continue
    
    if not all_results:
        return f"No {title} jobs found with salary range ${min_salary}-${max_salary}. Try broader search terms."
    
    # Format results
    formatted_results = f"Found {len(all_results)} {title} jobs with salary information:\\n\\n"
    
    for i, job in enumerate(all_results, 1):
        formatted_results += f"{i}. **{job['title']}**\\n"
        formatted_results += f"   Company: {job['company']}\\n"
        formatted_results += f"   Location: {job['location']}\\n"
        formatted_results += f"   Salary: {job['salary']}\\n"
        formatted_results += f"   Link: {job['link']}\\n"
        formatted_results += f"   Description: {job['description']}\\n\\n"
    
    return formatted_results