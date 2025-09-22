# TestCopilotAgent

A Python implementation for calling OpenAI-compatible LLM APIs. This project provides a simple, flexible function that can work with various LLM providers including OpenAI, Azure OpenAI, LocalAI, Ollama, and other OpenAI-compatible APIs.


## Features

- **Universal Compatibility**: Works with any OpenAI-compatible API
- **Comprehensive Error Handling**: Robust error handling for network issues, API errors, and invalid parameters
- **Flexible Configuration**: Supports various models, parameters, and custom settings
- **Simple Interface**: Easy-to-use function with sensible defaults
- **Full Documentation**: Complete documentation and examples
- **Type Hints**: Full type annotations for better development experience
- **Testing**: Comprehensive unit tests included

## Installation

1. Clone this repository:
```bash
git clone https://github.com/PatShauer/TestCopilotAgent.git
cd TestCopilotAgent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

```python
from llm_api import call_llm_api, extract_response_text

# Basic usage with OpenAI
response = call_llm_api(
    prompt="What is the capital of France?",
    api_url="https://api.openai.com/v1",
    api_key="your-openai-api-key",
    model="gpt-3.5-turbo"
)

text = extract_response_text(response)
print(text)  # "The capital of France is Paris."
```

## API Reference

### `call_llm_api()`

The main function for calling OpenAI-compatible LLM APIs.

**Parameters:**
- `prompt` (str): The user prompt/message to send to the LLM
- `api_url` (str): The base URL of the API endpoint
- `api_key` (str, optional): API key for authentication (None for local APIs)
- `model` (str): Model name to use (default: "gpt-3.5-turbo")
- `temperature` (float): Sampling temperature 0-2 (default: 0.7)
- `max_tokens` (int, optional): Maximum tokens to generate
- `system_message` (str, optional): System message for context
- `timeout` (int): Request timeout in seconds (default: 30)
- `**kwargs`: Additional parameters for the API

**Returns:**
- `Dict`: Complete API response with generated text and metadata

### `extract_response_text()`

Extract the generated text from an API response.

**Parameters:**
- `api_response` (Dict): Response from `call_llm_api()`

**Returns:**
- `str`: The generated text content

### `get_usage_info()`

Extract token usage information from an API response.

**Parameters:**
- `api_response` (Dict): Response from `call_llm_api()`

**Returns:**
- `Dict` or `None`: Usage information including token counts

## Usage Examples

### OpenAI API
```python
response = call_llm_api(
    prompt="Explain quantum computing",
    api_url="https://api.openai.com/v1",
    api_key="sk-...",
    model="gpt-4",
    temperature=0.7,
    system_message="You are a physics professor."
)
```

### Azure OpenAI
```python
response = call_llm_api(
    prompt="Write a summary",
    api_url="https://your-resource.openai.azure.com/openai/deployments/your-deployment",
    api_key="your-azure-key",
    model="gpt-35-turbo"
)
```

### Local API (LocalAI, Ollama, etc.)
```python
response = call_llm_api(
    prompt="Hello, how are you?",
    api_url="http://localhost:8080/v1",
    model="local-model"
    # No API key needed for local APIs
)
```

### With Custom Parameters
```python
response = call_llm_api(
    prompt="Count from 1 to 10",
    api_url="https://api.openai.com/v1",
    api_key="sk-...",
    model="gpt-3.5-turbo",
    temperature=0.1,
    max_tokens=100,
    top_p=0.9,
    frequency_penalty=0.0,
    stop=["\n"]
)
```

## Error Handling

The function provides comprehensive error handling:

```python
try:
    response = call_llm_api(
        prompt="Test prompt",
        api_url="https://api.example.com/v1",
        api_key="invalid-key"
    )
    text = extract_response_text(response)
    print(text)
    
except ValueError as e:
    print(f"Invalid parameter: {e}")
except RuntimeError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Testing

Run the test suite:

```bash
python -m unittest test_llm_api.py -v
```

## File Structure

- `llm_api.py` - Main module with the LLM API function
- `test_llm_api.py` - Comprehensive unit tests
- `examples.py` - Usage examples and demonstrations
- `requirements.txt` - Python dependencies

## Supported Providers

This implementation works with any OpenAI-compatible API, including:

- **OpenAI** (GPT-3.5, GPT-4, etc.)
- **Azure OpenAI Service**
- **LocalAI** (self-hosted)
- **Ollama** (local models)
- **Together AI**
- **Anyscale Endpoints**
- **OpenRouter**
- **Perplexity AI**
- **And many others...**

## Environment Variables

For convenience, you can set environment variables:

```bash
export OPENAI_API_KEY="your-openai-key"
export AZURE_OPENAI_API_KEY="your-azure-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## License

This project is open source and available under the MIT License.
