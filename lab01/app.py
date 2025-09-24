from strands.models.ollama import OllamaModel
from strands import Agent, tool
from strands_tools import calculator
import os

# File Operation Tools


@tool
def file_read(file_path: str) -> str:
    """Read a file and return its content.

    Args:
        file_path (str): Path to the file to read

    Returns:
        str: Content of the file

    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def file_write(file_path: str, content: str) -> str:
    """Write content to a file.

    Args:
        file_path (str): The path to the file
        content (str): The content to write to the file

    Returns:
        str: A message indicating success or failure
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

        with open(file_path, "w") as file:
            file.write(content)
        return f"File '{file_path}' written successfully."
    except Exception as e:
        return f"Error writing to file: {str(e)}"


@tool
def list_directory(directory_path: str = ".") -> str:
    """List files and directories in the specified path.

    Args:
        directory_path (str): Path to the directory to list

    Returns:
        str: A formatted string listing all files and directories
    """
    try:
        items = os.listdir(directory_path)
        files = []
        directories = []

        for item in items:
            full_path = os.path.join(directory_path, item)
            if os.path.isdir(full_path):
                directories.append(f"Folder: {item}/")
            else:
                files.append(f"File: {item}")

        result = f"Contents of {os.path.abspath(directory_path)}:\n"
        result += (
            "\nDirectories:\n" + "\n".join(sorted(directories))
            if directories
            else "\nNo directories found."
        )
        result += (
            "\n\nFiles:\n" + "\n".join(sorted(files)) if files else "\nNo files found."
        )

        return result
    except Exception as e:
        return f"Error listing directory: {str(e)}"


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

system_prompt = """
You are a helpful personal assistant capable of performing local file actions and simple tasks for the user.

Your key capabilities:
1. Read, understand, and summarize files.
2. Create and write to files.
3. List directory contents and provide information on the files.
4. Summarize text content

When using tools:
- Always verify file paths before operations
- Be careful with system commands
- Provide clear explanations of what you're doing
- If a task cannot be completed, explain why and suggest alternatives

Always be helpful, concise, and focus on addressing the user's needs efficiently.
"""

# Create the agent with tools
local_agent = Agent(
    system_prompt=system_prompt, # Define a system Prompt
    model=ollama_model,
    tools=[file_read, file_write, list_directory],  # Add your custom tools here
)


# Try each of the response types below one at a time
response = local_agent("Read the file ./app.py and explain to me what this code does")

# response = local_agent("Show me the files in the current directory ./ ")

# response = local_agent(
#     "Create a file called './hello.txt' with the content 'This is a test file created by my Ollama agent.'"
# )

print(response)