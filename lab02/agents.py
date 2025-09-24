from crewai import Agent, LLM
from tools import (docs_tool, file_tool, web_rag_tool, search_tool, progressive_search_tool, 
                  salary_job_search, company_specific_search, entry_level_search, 
                  quick_search, job_search)
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

serper_api_key = os.getenv("SERPER_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL")

# Set environment variable for Gemini
if gemini_api_key is not None:
    os.environ["GEMINI_API_KEY"] = gemini_api_key

# Configure the LLM with Gemini API
llm = LLM(
    model=f"gemini/{gemini_model}",
    api_key=gemini_api_key
)

JobSearchAgent = Agent(
    role="Senior Job Researcher",
    goal="Find high-quality {title} positions matching {years} years experience and salary expectations of {salary_expectation}.",
    backstory="""
        An expert job researcher with deep knowledge of various industries and job markets. 
        Skilled in using advanced search strategies to find positions that match specific technical skills like {required_skills} 
        and preferred technologies like {preferred_skills}. Understands career progression paths for {level} professionals 
        and can identify opportunities aligned with career goals: {career_goals}.
    """,
    tools=[job_search, salary_job_search, quick_search],
    verbose=True,
    llm=llm
)

CompanyTargetedAgent = Agent(
    role="Company-Focused Job Researcher",
    goal="Find {title} positions at specific target companies and analyze their hiring patterns.",
    backstory="""
        A specialized recruiter with deep connections across various industries and expertise in {title} roles.
        Excels at researching specific companies, understanding their tech stacks, and finding opportunities
        that align with candidate preferences. Maintains up-to-date knowledge of company cultures,
        compensation packages, and hiring practices for professionals in the {title} field.
    """,
    tools=[company_specific_search, job_search],
    verbose=True,
    llm=llm
)

EntryLevelAgent = Agent(
    role="Entry-Level Career Advisor",
    goal="Find entry-level and junior {title} positions and provide career guidance for new professionals.",
    backstory="""
        A career counselor specializing in helping new graduates and career changers break into the {title} field.
        Expert in identifying entry-level opportunities, internships, and junior positions that provide
        strong learning foundations. Understands the skills and certifications needed to start a successful
        career in {title} and can guide candidates through their first job search.
    """,
    tools=[entry_level_search, quick_search],
    verbose=True,
    llm=llm
)

AnalysisAgent = Agent(
    role="Career Strategist",
    goal="Provide strategic career guidance for {level} {title} professionals targeting {salary_expectation} salary range.",
    backstory="""
        A seasoned career strategist with 15+ years across various industries and professional roles. 
        Expert in analyzing job market trends, identifying skill gaps, and providing actionable career development advice. 
        Specializes in helping {level} professionals with {years} years experience advance their careers in {title}. 
        Deep understanding of industry ecosystems including {required_skills} and emerging technologies like {preferred_skills}.
        Focused on aligning opportunities with career goals: {career_goals}.
    """,
    tools=[docs_tool, file_tool],
    verbose=True,
    llm=llm
)

MessageWriterAgent = Agent(
    role="Outreach Message Writer",
    goal="Write effective LinkedIn messages and cold emails for top job picks.",
    backstory="""
        A persuasive tech-savvy communicator who crafts personalized, high-converting outreach messages 
        to help job seekers stand out and connect with recruiters.
    """,
    tools=[docs_tool, file_tool],
    verbose=True,
    llm=llm
)