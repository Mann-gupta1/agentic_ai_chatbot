import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Simple mock agent for testing if the real one fails
class SimpleAgent:
    def process(self, user_input):
        return {
            "response": f"Echo: {user_input}",
            "agent": "simple_test_agent"
        }

def main():
    st.title("Agentic AI System")
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Try to import the real agent, fall back to simple one if it fails
    if 'team_agent' not in st.session_state:
        try:
            from agents.team_agent import TeamAgent
            st.session_state.team_agent = TeamAgent()
            st.success("✅ Team Agent loaded successfully")
        except Exception as e:
            st.warning(f"⚠️ Could not load Team Agent: {str(e)}")
            st.info("Using simple test agent instead")
            st.session_state.team_agent = SimpleAgent()
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        else:
            st.write(f"**AI:** {message['content']}")
            if "agent" in message:
                st.caption(f"Agent: {message['agent']}")
    
    # Chat input
    user_input = st.chat_input("Type your message...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input
        })
        
        # Get AI response
        try:
            result = st.session_state.team_agent.process(user_input)
            
            if isinstance(result, dict):
                response = result.get("response", "No response")
                agent_used = result.get("agent", "unknown")
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "agent": agent_used
                })
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": str(result)
                })
                
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Error: {str(e)}"
            })
        
        # Refresh to show new messages
        st.rerun()

if __name__ == "__main__":
    main() 