import os
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool, FilePurpose

# ✅ Load environment variables
load_dotenv()

# 🔐 Load config from environment
CONNECTION_STRING = os.getenv("AZURE_AI_CONN_STR")
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH", "nifty_500_quarterly_results.csv")

if not CONNECTION_STRING:
    raise EnvironmentError("Missing AZURE_AI_CONN_STR in .env")

# ✅ Initialize the Azure AI Project client
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=CONNECTION_STRING
)

# 📤 Upload CSV file
uploaded_file = project_client.agents.upload_file_and_poll(
    file_path=CSV_FILE_PATH, purpose=FilePurpose.AGENTS
)
print(f"✅ Uploaded file with ID: {uploaded_file.id}")

# 🧠 Initialize Code Interpreter tool with uploaded file
code_tool = CodeInterpreterTool(file_ids=[uploaded_file.id])

# 🤖 Create agent
agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-agent",
    instructions="You are a helpful agent that analyzes financial CSV data.",
    tools=code_tool.definitions,
    tool_resources=code_tool.resources,
)
print(f"🤖 Agent created: {agent.id}")

# 🧵 Create a thread for conversation
thread = project_client.agents.create_thread()
print(f"🧵 Thread created: {thread.id}")

# 💬 Send a user message to the thread
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content=(
        "Could you please create a bar chart in the TRANSPORTATION sector for the operating profit "
        "from the uploaded CSV file and provide the file to me?"
    ),
)
print(f"💬 Message sent: {message.id}")

# ▶️ Run the agent
run = project_client.agents.create_and_process_run(
    thread_id=thread.id, agent_id=agent.id
)
print(f"✅ Run completed with status: {run.status}")

# 🛑 If failed, print reason
if run.status == "failed":
    print(f"❌ Run failed: {run.last_error}")

# 🧹 Delete original uploaded file (agent-side)
project_client.agents.delete_file(uploaded_file.id)
print("🧹 Deleted uploaded file from agent context")

# 📥 Retrieve and save images/files from the agent
messages = project_client.agents.list_messages(thread_id=thread.id)

for content in messages.image_contents:
    file_id = content.image_file.file_id
    file_name = f"{file_id}_chart.png"
    project_client.agents.save_file(file_id=file_id, file_name=file_name)
    print(f"📁 Saved image file to: {Path.cwd() / file_name}")

# 🗑️ Cleanup resources
project_client.agents.delete_agent(agent.id)
project_client.agents.delete_thread(thread.id)
print("🗑️ Agent and thread deleted.")
