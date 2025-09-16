"""
Example usage of the OpenAI-compatible LLM API client.

This file demonstrates various ways to use the llm_api module.
"""

from llm_api import call_llm_api, extract_response_text, get_usage_info
import os


def example_openai_api():
    """Example using OpenAI API (requires API key)."""
    print("=== OpenAI API Example ===")
    
    # You would normally get this from environment variables or config
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        return
    
    try:
        response = call_llm_api(
            prompt="Write a haiku about programming",
            api_url="https://api.openai.com/v1",
            api_key=api_key,
            model="gpt-3.5-turbo",
            temperature=0.8,
            max_tokens=100
        )
        
        text = extract_response_text(response)
        usage = get_usage_info(response)
        
        print(f"Generated haiku:\n{text}")
        print(f"Token usage: {usage}")
        
    except Exception as e:
        print(f"Error: {e}")


def example_azure_openai():
    """Example using Azure OpenAI (requires API key and custom endpoint)."""
    print("\n=== Azure OpenAI Example ===")
    
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    
    if not api_key or not api_base:
        print("Azure OpenAI credentials not found. Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT.")
        return
    
    try:
        response = call_llm_api(
            prompt="Explain the concept of machine learning in simple terms",
            api_url=f"{api_base}/openai/deployments/your-deployment-name",
            api_key=api_key,
            model="gpt-35-turbo",  # Azure model name format
            temperature=0.3,
            system_message="You are an expert educator who explains complex topics simply."
        )
        
        text = extract_response_text(response)
        print(f"Explanation:\n{text}")
        
    except Exception as e:
        print(f"Error: {e}")


def example_local_api():
    """Example using a local API (like LocalAI or Ollama)."""
    print("\n=== Local API Example ===")
    
    try:
        response = call_llm_api(
            prompt="What are the benefits of using local LLMs?",
            api_url="http://localhost:8080/v1",  # Common LocalAI port
            model="local-gpt-model",
            temperature=0.7,
            system_message="You are a knowledgeable AI assistant."
        )
        
        text = extract_response_text(response)
        print(f"Local LLM response:\n{text}")
        
    except Exception as e:
        print(f"Local API not available or error occurred: {e}")


def example_custom_parameters():
    """Example with custom parameters and error handling."""
    print("\n=== Custom Parameters Example ===")
    
    try:
        # This will fail since it's a mock endpoint, but demonstrates parameter usage
        response = call_llm_api(
            prompt="Count from 1 to 5",
            api_url="https://mock-api.example.com/v1",
            model="custom-model",
            temperature=0.1,  # Low temperature for consistent output
            max_tokens=50,
            system_message="You are a counting assistant.",
            # Custom parameters specific to some providers
            top_p=0.9,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n\n"]  # Stop generation at double newline
        )
        
        text = extract_response_text(response)
        print(f"Response:\n{text}")
        
    except Exception as e:
        print(f"Expected error with mock API: {e}")


def example_conversation():
    """Example of simulating a conversation (requires manual implementation)."""
    print("\n=== Conversation Simulation Example ===")
    
    # Note: This is a simple example. For real conversations, you'd need to 
    # maintain conversation history and send it with each request.
    
    conversation_history = []
    
    def add_to_conversation(role, content):
        conversation_history.append({"role": role, "content": content})
    
    # Simulate a conversation
    questions = [
        "What is the capital of France?",
        "What is the population of that city?",
        "What are some famous landmarks there?"
    ]
    
    print("Simulated conversation (each question is independent in this example):")
    
    for i, question in enumerate(questions, 1):
        print(f"\nUser: {question}")
        
        try:
            # In a real conversation, you'd send the full conversation_history
            # Here we just send individual questions for demonstration
            response = call_llm_api(
                prompt=question,
                api_url="https://api.openai.com/v1",
                api_key=os.getenv("OPENAI_API_KEY", "mock-key"),
                model="gpt-3.5-turbo",
                temperature=0.7,
                system_message="You are a helpful geography assistant."
            )
            
            text = extract_response_text(response)
            print(f"Assistant: {text}")
            
            # Add to conversation history
            add_to_conversation("user", question)
            add_to_conversation("assistant", text)
            
        except Exception as e:
            print(f"Assistant: [Error occurred: {e}]")


if __name__ == "__main__":
    print("OpenAI-Compatible LLM API Examples")
    print("==================================")
    
    # Run examples
    example_openai_api()
    example_azure_openai()
    example_local_api()
    example_custom_parameters()
    example_conversation()
    
    print("\n=== Example Complete ===")
    print("Note: Most examples will show errors unless you have valid API keys configured.")
    print("The examples demonstrate proper usage patterns and error handling.")