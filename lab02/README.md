# Lab 02 - Simple Agentic AI Job Finder

Build an agentic job search system designed to help professionals in any field find a job. The system should use specialized agents and multiple search strategies to find the best open jobs matching an individual's skills, experience, and any other preferences (salary, location, remote only, etc.).


## Guidance

1. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

2. Rename the `env.example` file to `.env` and place this in the root of your project folder if you're using python virtual environments.
3. Update the API keys with your API keys in the `.env` file
4. Edit `config.py` to customize your job search preferences
5. Run the interactive search tool:
    ```bash
    python run_search.py
    ```
6. For the first run try using the quick search option.
7. Observe the agent output and review the output files in `job-posts` folder
8. Tweak the `config.py` settings and try with other search options
9. Review the code in `agents.py` and `tasks.py`. Make adjustments to the back story and task descriptions and re-run to see the output



