from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from rich.console import Console
from app.brain.memory import MemoryStore, MemoryItem
from app.brain.perception import LLMRequest, call_external_llm
from app.brain.decision_making import craft_prompt
from app.brain.action import perform_action
from app.brain.decision_making import DecisionInput
from app.brain.action import ActionInput
from google import genai
import os
import base64
from dotenv import load_dotenv



# Persistent memory store for all users
memory_store = MemoryStore()

def get_system_prompt():
    with open("app/system_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def image_to_base64(upload_file):
    if upload_file is None:
        return None
    contents = upload_file.file.read()
    return base64.b64encode(contents).decode('utf-8')

def orchestrate(message: str, username: str, download_summary: bool = False, send_email: bool = False, email: str = None, image=None):
    """
    Orchestrates the routing of the message to the appropriate brain module.
    Uses a persistent MemoryStore for all users.
    """
    system_prompt = get_system_prompt()
    if image is not None:
        image_b64 = image_to_base64(image)
    else:
        image_b64 = None
    # Pass image_b64 to LLMRequest if needed
    llm_request = LLMRequest(prompt=system_prompt, image_b64=image_b64)
    print(f"LLM Request: {llm_request}")
    llm_response = call_external_llm(llm_request)
    print(f"LLM Response: {llm_response}")
    system_prompt += f"\n\nAnalysis of image is \n\n{llm_response.response}"
    #print(f"Updated System Prompt: {system_prompt}")
    user_memories = memory_store.get_items_by_user(username)
    if user_memories:
        # User exists, append the new message
        print(f"User {username} exists. Appending new message.")
        memory_store.add_item(MemoryItem(user=username, content=message))
    else:
        # New user, create first entry
        print(f"New user {username}. Creating first entry.")
        memory_store.add_item(MemoryItem(user=username, content=message))
    # Pass only this user's memory to DecisionInput
    user_memory_store = MemoryStore(items=memory_store.get_items_by_user(username))
    # Read system prompt from file
    
    decision_input = DecisionInput(user_input=message, memory=user_memory_store)
    decision_output = craft_prompt(decision_input, system_prompt=system_prompt)
    print(f"Crafted Prompt: {decision_output.crafted_prompt}")
    # Pass image_b64 to LLMRequest if needed
    llm_request = LLMRequest(prompt=decision_output.crafted_prompt, image_b64=image_b64)
    llm_response = call_external_llm(llm_request)
    response = {"crafted_prompt": llm_response.response}
    
    if download_summary:
        crafted_prompt = f"{decision_output.crafted_prompt}\n\nSummarize Prompt:\nCould you please summarize the prompt?\n\n"
        llm_summary_response = call_external_llm(LLMRequest(prompt=crafted_prompt))
        # Write summary to summary.txt
        with open("summary.txt", "w", encoding="utf-8") as f:
            f.write(llm_summary_response.response)
        response["download_summary"] = llm_summary_response.response
        response["summary_file"] = os.path.abspath("summary.txt")
    if send_email and email:
        response["email_sent_to"] = email
    if image is not None:
        response["image_filename"] = image.filename
    return response

    
