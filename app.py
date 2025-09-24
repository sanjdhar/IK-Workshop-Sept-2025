from strands.models.ollama import OllamaModel
from strands import Agent, tool
import os

@tool
def file_read(file_path: str) -> str:
    """Read a file and return its content."""
    # Enter your code here

@tool
def file_write(file_path: str, content: str) -> str:
    """Write content to a file."""
    # Enter your code here

@tool
def list_directory(directory_path: str = ".") -> str:
    """List files and directories in the specified path."""
    # Enter your code here


# Configure the Ollama model
ollama_model = OllamaModel(
    model_id="llama3.2:1b", # Make sure this is the model you downloaded from Ollama
    host="http://localhost:11434",
    params={
        "max_tokens": 4096,  # Adjust based on your model's capabilities
        "temperature": 0.7,  # Lower for more deterministic responses, higher for more creative
        "top_p": 0.9,        # Nucleus sampling parameter
        "stream": True,      # Enable streaming responses
    },
)

system_prompt="You are a helpful assistant that provides concise responses."

# Create the agent with tools
local_agent = Agent(
    system_prompt=system_prompt, # Define a system Prompt
    model=ollama_model,
    # tools=[file_read, file_write, list_directory],  # Add your custom tools here
)


# Send a message to the agent
response = local_agent("Who is Neil DeGrass Tyson?")
print(response)