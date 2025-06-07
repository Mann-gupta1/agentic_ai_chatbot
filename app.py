import os
from dotenv import load_dotenv
from agents.team_agent import TeamAgent

load_dotenv()

def main():
    print("Agentic AI System")
    print("Type 'exit' or 'quit' to stop")
    print("-" * 40)
    
    team_agent = TeamAgent()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("\nProcessing...")
            result = team_agent.process(user_input)
            
            if isinstance(result, dict):
                response = result.get("response", "No response generated")
                agent_used = result.get("agent", "unknown")
                
                print(f"\nResponse ({agent_used}):")
                print(response)
                
                if result.get("error"):
                    print("Note: There was an error processing your request.")
            else:
                print("\nResponse:")
                print(result)
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main() 