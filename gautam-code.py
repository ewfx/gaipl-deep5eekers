import streamlit as st
import openai
import requests
import json

# Configuration
CLAUDE_API_KEY = "your_claude_api_key"
SERVICENOW_MCP_URL = "https://your-instance.service-now.com/api/mcp"
SERVICENOW_MCP_TOKEN = "your_mcp_token"
ANSIBLE_TOWER_URL = "https://your-ansible-server/api/v2/job_templates/YOUR_JOB_ID/launch/"
ANSIBLE_TOKEN = "your_ansible_token"

def get_claude_response(user_input):
    """Use Claude to process the issue and generate MCP-compliant output."""
    try:
        response = openai.ChatCompletion.create(
            model="claude-3",
            messages=[
                {"role": "system", "content": "Format the response in MCP JSON structure for ServiceNow incidents."},
                {"role": "user", "content": user_input}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error getting response from Claude: {e}")
        return None

def create_servicenow_incident_mcp(mcp_payload):
    """Create an incident in ServiceNow using Model Context Protocol (MCP)."""
    headers = {
        "Authorization": f"Bearer {SERVICENOW_MCP_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(SERVICENOW_MCP_URL, json=mcp_payload, headers=headers)
        if response.status_code == 201:
            return response.json()["result"]["sys_id"]
        else:
            st.error(f"Error creating incident: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to ServiceNow: {e}")
        return None

def trigger_ansible_playbook():
    """Trigger an Ansible playbook via Tower API."""
    headers = {
        "Authorization": f"Bearer {ANSIBLE_TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(ANSIBLE_TOWER_URL, headers=headers)
        if response.status_code == 201:
            st.success("Ansible playbook triggered successfully!")
        else:
            st.error(f"Error triggering Ansible playbook: {response.text}")
    except Exception as e:
        st.error(f"Error connecting to Ansible: {e}")

# Streamlit UI
st.title("Claude-Powered ServiceNow & Ansible Automation with MCP")

# Input box for user to describe the issue
user_input = st.text_area("Describe the issue:", "")

if st.button("Create Incident & Trigger Playbook"):
    if user_input.strip():
        # Step 1: Get MCP-compliant response from Claude
        st.info("Processing issue with Claude...")
        structured_response = get_claude_response(user_input)
        
        if structured_response:
            try:
                # Convert Claude's response to MCP JSON format
                mcp_payload = json.loads(structured_response)  # Assuming Claude returns MCP JSON

                # Step 2: Create ServiceNow incident using MCP
                st.info("Creating incident in ServiceNow using MCP...")
                incident_id = create_servicenow_incident_mcp(mcp_payload)

                if incident_id:
                    st.success(f"Incident created successfully in ServiceNow (ID: {incident_id})")

                    # Step 3: Trigger Ansible Playbook
                    st.info("Triggering Ansible playbook...")
                    trigger_ansible_playbook()
            except json.JSONDecodeError:
                st.error("Claude did not return a valid MCP JSON response. Please try again.")
        else:
            st.error("Failed to process input with Claude.")
    else:
        st.warning("Please describe the issue before submitting.")