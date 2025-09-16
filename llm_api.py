"""
OpenAI-Compatible LLM API Client

This module provides a function to call OpenAI-compatible LLM APIs.
Supports various providers like OpenAI, Azure OpenAI, LocalAI, and others.
"""

import json
import requests
from typing import Dict, List, Optional, Union
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def call_llm_api(
    prompt: str,
    api_url: str,
    api_key: Optional[str] = None,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    system_message: Optional[str] = None,
    timeout: int = 30,
    **kwargs
) -> Dict:
    """
    Call an OpenAI-compatible LLM API.
    
    Args:
        prompt (str): The user prompt/message to send to the LLM
        api_url (str): The base URL of the API endpoint (e.g., "https://api.openai.com/v1")
        api_key (str, optional): API key for authentication. Can be None for local APIs.
        model (str): Model name to use (default: "gpt-3.5-turbo")
        temperature (float): Sampling temperature between 0 and 2 (default: 0.7)
        max_tokens (int, optional): Maximum number of tokens to generate
        system_message (str, optional): System message to set context
        timeout (int): Request timeout in seconds (default: 30)
        **kwargs: Additional parameters to pass to the API
    
    Returns:
        Dict: The API response containing the generated text and metadata
        
    Raises:
        requests.exceptions.RequestException: For network-related errors
        ValueError: For invalid parameters
        RuntimeError: For API errors
    """
    
    # Validate inputs
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Prompt must be a non-empty string")
    
    if not api_url or not isinstance(api_url, str):
        raise ValueError("API URL must be a non-empty string")
    
    if not (0 <= temperature <= 2):
        raise ValueError("Temperature must be between 0 and 2")
    
    if max_tokens is not None and max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    
    # Ensure the API URL ends with the correct endpoint
    if not api_url.endswith('/chat/completions'):
        api_url = api_url.rstrip('/') + '/chat/completions'
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Add authorization header if API key is provided
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    # Prepare messages
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})
    
    # Prepare request payload
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        **kwargs  # Include any additional parameters
    }
    
    # Add max_tokens if specified
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    
    try:
        logger.info(f"Sending request to {api_url} with model {model}")
        
        # Make the API request
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=timeout
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        
        logger.info("API request successful")
        return result
        
    except requests.exceptions.Timeout:
        error_msg = f"Request timed out after {timeout} seconds"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    except requests.exceptions.ConnectionError:
        error_msg = f"Failed to connect to API at {api_url}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    except requests.exceptions.HTTPError as e:
        error_msg = f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    except json.JSONDecodeError:
        error_msg = "Failed to parse API response as JSON"
        logger.error(error_msg)
        raise RuntimeError(error_msg)


def extract_response_text(api_response: Dict) -> str:
    """
    Extract the generated text from the API response.
    
    Args:
        api_response (Dict): The response from call_llm_api()
    
    Returns:
        str: The generated text content
        
    Raises:
        KeyError: If the response format is unexpected
    """
    try:
        return api_response["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise KeyError(f"Unexpected response format: {str(e)}")


def get_usage_info(api_response: Dict) -> Optional[Dict]:
    """
    Extract usage information from the API response.
    
    Args:
        api_response (Dict): The response from call_llm_api()
    
    Returns:
        Dict or None: Usage information including token counts, or None if not available
    """
    return api_response.get("usage")


# Example usage
if __name__ == "__main__":
    # Example with OpenAI API (requires API key)
    try:
        # Example 1: Basic usage
        response = call_llm_api(
            prompt="What is the capital of France?",
            api_url="https://api.openai.com/v1",
            api_key="your-api-key-here",  # Replace with actual API key
            model="gpt-3.5-turbo",
            temperature=0.7
        )
        
        generated_text = extract_response_text(response)
        usage_info = get_usage_info(response)
        
        print("Generated text:", generated_text)
        print("Usage info:", usage_info)
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: With system message
    try:
        response = call_llm_api(
            prompt="Explain quantum computing",
            api_url="https://api.openai.com/v1",
            api_key="your-api-key-here",  # Replace with actual API key
            model="gpt-3.5-turbo",
            system_message="You are a helpful physics teacher explaining complex topics simply.",
            temperature=0.5,
            max_tokens=200
        )
        
        generated_text = extract_response_text(response)
        print("Generated text with system message:", generated_text)
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Local API (no API key needed)
    try:
        response = call_llm_api(
            prompt="Hello, how are you?",
            api_url="http://localhost:8080/v1",  # Example local API
            model="local-model",
            temperature=0.7
        )
        
        generated_text = extract_response_text(response)
        print("Local API response:", generated_text)
        
    except Exception as e:
        print(f"Local API error: {e}")