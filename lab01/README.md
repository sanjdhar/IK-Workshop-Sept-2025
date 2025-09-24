# Lab 01 - Build Simple AI agent
The goal of this lab is to build an agentic app that can list, read, write, and answer questions about files on your local Mac/PC file system.

Hint: You will need to use tools to equip your agent

## Example prompts the app shoud be able to successfully process
- List all files in my current folder
- Read the contents of my `notes.txt` file and give me a summary
- Write "Hello, World!" to a new file called `hello.txt` in my current folder
- Read the file `app.py` in my current folder and explain what this code does

## Guidance

We will use the [Strands Agents](https://strandsagents.com/latest/) which is an open source SDK that takes a model-driven approach to building and running AI agents in just a few lines of code. We will additionally use Ollama witht the smallest Llama 3.2 model (llama3.2:1b) so it can run easliy on your local machine. Make sure you run `ollama pull llama3.2:1b` followed by `ollama serve` to ensure the service is running and listening on your localhost (port 1143 by default)

1. Install dependencies (mainly installing strands-agents strands-agents-tools and strands-agents[ollama])

```python
pip install -r requirements.txt
```

2. Run the code to make sure you don't get any errors `python ./app.py`
3. Open `app.py` and read through the code to understand how it works
4. Try each of the response types in `app.py` by commenting/uncommenting  on lines 129-135.