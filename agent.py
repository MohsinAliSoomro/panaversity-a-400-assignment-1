# To run this code you need to install the following dependencies:
# uv add google-genai

import os
import sys
import warnings
from io import StringIO
from google import genai
from google.genai import types
from tools import Tools
from dotenv import load_dotenv

# Suppress specific warnings from the genai library
warnings.filterwarnings("ignore")

load_dotenv()

# Global session state to store JWT token
class Session:
    """Manage user session with JWT token"""
    def __init__(self):
        self.token = None
        self.user_email = None
    
    def set_token(self, token: str, email: str = None):
        """Store the JWT token after login"""
        self.token = token
        self.user_email = email
    
    def get_token(self):
        """Retrieve the stored JWT token"""
        return self.token
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return self.token is not None
    
    def clear(self):
        """Clear the session"""
        self.token = None
        self.user_email = None

# Global session instance
session = Session()

def define_tools():
    """Define all available tools for the task management system"""
    return [
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="login",
                    description="Login a user with email and password",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "email": types.Schema(type=types.Type.STRING, description="The email of the user"),
                            "password": types.Schema(type=types.Type.STRING, description="The password of the user"),
                        },
                        required=["email", "password"],
                    ),
                ),
                types.FunctionDeclaration(
                    name="create_user",
                    description="Create a new user",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "email": types.Schema(type=types.Type.STRING, description="The email of the user"),
                            "password": types.Schema(type=types.Type.STRING, description="The password of the user"),
                        },
                        required=["email", "password"],
                    ),
                ),
                types.FunctionDeclaration(
                    name="create_task",
                    description="Create a new task. Requires authentication - user must be logged in first.",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "title": types.Schema(type=types.Type.STRING, description="The title of the task"),
                            "description": types.Schema(type=types.Type.STRING, description="The description of the task"),
                            "priority": types.Schema(type=types.Type.STRING, description="The priority of the task (low, medium, high)"),
                        },
                        required=["title", "description"],
                    ),
                ),
                types.FunctionDeclaration(
                    name="get_tasks",
                    description="Get all tasks for the authenticated user. Requires authentication - user must be logged in first.",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={},
                    ),
                ),
                types.FunctionDeclaration(
                    name="update_task",
                    description="Update a task. Requires authentication - user must be logged in first.",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "task_id": types.Schema(type=types.Type.INTEGER, description="The id of the task to update"),
                            "title": types.Schema(type=types.Type.STRING, description="The new title of the task"),
                            "description": types.Schema(type=types.Type.STRING, description="The new description of the task"),
                            "priority": types.Schema(type=types.Type.STRING, description="The new priority of the task"),
                        },
                        required=["task_id"],
                    ),
                ),
                types.FunctionDeclaration(
                    name="delete_task",
                    description="Delete a task. Requires authentication - user must be logged in first.",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "task_id": types.Schema(type=types.Type.INTEGER, description="The id of the task to delete"),
                        },
                        required=["task_id"],
                    ),
                ),
            ]
        )
    ]


def execute_tool(tool_name: str, tool_input: dict):
    """Execute the appropriate tool based on the tool name and input"""
    if tool_name == "login":
        print(f"🔐 Executing login with input: {tool_input}")
        response = Tools.login(tool_input.get("email"), tool_input.get("password"))
        
        # Store the JWT token in session after successful login
        if "access_token" in response:
            session.set_token(response["access_token"], tool_input.get("email"))
            print(f"✅ Login successful! Token stored in session.")
            print(f"👤 User: {tool_input.get('email')}")
        else:
            print(f"❌ Login failed: {response}")
        
        return response
    
    elif tool_name == "create_user":
        print(f"📝 Creating new user: {tool_input.get('email')}")
        response = Tools.create_user(tool_input.get("email"), tool_input.get("password"))
        print(f"✅ User created: {response}")
        return response
    
    # For all other tools, check if user is authenticated
    elif not session.is_authenticated():
        error_msg = {
            "error": "Authentication required",
            "message": "Please login first before performing task operations"
        }
        print(f"❌ {error_msg['message']}")
        return error_msg
    
    # Use the stored token for authenticated operations
    token = session.get_token()
    
    if tool_name == "create_task":
        print(f"➕ Creating task: {tool_input.get('title')}")
        response = Tools.create_task(
            token,
            tool_input.get("title"),
            tool_input.get("description"),
            tool_input.get("priority", "medium")
        )
        print(f"✅ Task created: {response}")
        return response
    
    elif tool_name == "get_tasks":
        print(f"📋 Fetching all tasks...")
        response = Tools.get_tasks(token)
        print(f"✅ Retrieved {len(response) if isinstance(response, list) else 0} tasks")
        return response
    
    elif tool_name == "update_task":
        print(f"✏️ Updating task ID: {tool_input.get('task_id')}")
        response = Tools.update_task(
            token,
            tool_input.get("task_id"),
            tool_input.get("title"),
            tool_input.get("description"),
            tool_input.get("priority")
        )
        print(f"✅ Task updated: {response}")
        return response
    
    elif tool_name == "delete_task":
        print(f"🗑️ Deleting task ID: {tool_input.get('task_id')}")
        response = Tools.delete_task(token, tool_input.get("task_id"))
        print(f"✅ Task deleted: {response}")
        return response
    
    else:
        return {"error": f"Unknown tool: {tool_name}"}


def generate(user_input: str):
    """Generate a response using the Gemini API with task management tools"""
    # Get API keys
    gemini_key = os.environ.get("GEMINI_API_KEY")
    google_key = os.environ.get("GOOGLE_API_KEY")
    
    # Use GEMINI_API_KEY if available, otherwise use GOOGLE_API_KEY
    api_key = gemini_key if gemini_key else google_key
    
    if not api_key:
        raise ValueError("Neither GEMINI_API_KEY nor GOOGLE_API_KEY is set")
    
    # Redirect stderr to suppress library warnings
    old_stderr = sys.stderr
    sys.stderr = StringIO()
    
    try:
        client = genai.Client(api_key=api_key)
    finally:
        sys.stderr = old_stderr

    model = "gemini-2.5-flash"
    
    # Create the message content
    auth_status = "🔐 Authenticated" if session.is_authenticated() else "🔓 Not authenticated"
    user_info = f" (User: {session.user_email})" if session.user_email else ""
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""You are an intelligent task management assistant with JWT-based authentication. You help users manage tasks securely using their authentication tokens.

## Current Session Status
{auth_status}{user_info}

## User Request
{user_input}

## Available Tools
- **login**: Authenticate a user with email and password. Returns a JWT token that is automatically stored in the session.
- **create_user**: Register a new user account with email and password.
- **create_task**: Create a new task (requires authentication). DO NOT pass token - it's handled automatically.
- **get_tasks**: Retrieve all tasks (requires authentication). DO NOT pass token - it's handled automatically.
- **update_task**: Modify task details (requires authentication). DO NOT pass token - it's handled automatically.
- **delete_task**: Remove a task (requires authentication). DO NOT pass token - it's handled automatically.

## Authentication Flow
1. Users MUST login first before performing any task operations
2. After successful login, the JWT token is automatically stored in the session
3. All subsequent task operations automatically use the stored JWT token
4. DO NOT ask for or pass tokens manually - the system handles this automatically
5. If a user tries task operations without logging in, they will receive an authentication error

## Instructions
1. For new users or if not authenticated, prompt them to login first
2. Analyze the user's request to determine which tool(s) are needed
3. For task operations, DO NOT include token parameter - it's injected automatically
4. Execute appropriate tools with correct parameters
5. Provide clear confirmations of successful operations
6. Handle errors gracefully and guide users appropriately

## Response Format
- Confirm successful operations with details
- For login: Mention that the session is now authenticated
- For task operations: Include relevant task details
- Use professional and friendly language"""),
            ],
        ),
    ]
    
    # Define tools
    tools = define_tools()
    
    # Configure content generation
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=False
        ),
    )

    # Stream the response and handle both text and function calls
    full_response = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        # Extract text from chunk if it exists
        if hasattr(chunk, 'text') and chunk.text:
            print(chunk.text, end="", flush=True)
            full_response += chunk.text
        
        # Handle function calls if present
        if hasattr(chunk, 'candidates') and chunk.candidates:
            for candidate in chunk.candidates:
                if hasattr(candidate, 'content') and candidate.content:
                    for part in candidate.content.parts:
                        if hasattr(part, 'function_call'):
                            # Process the function call
                            tool_name = part.function_call.name
                            tool_input = {k: v for k, v in part.function_call.args.items()}
                            result = execute_tool(tool_name, tool_input)
                            print(f"[Tool: {tool_name} executed with result: {result}]")
    
    print()  # Add newline at the end


if __name__ == "__main__":
    user_input = "user the tool to login the user with email mohsin@gmail.com and password Test@123"
    generate(user_input)


