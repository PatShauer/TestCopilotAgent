"""
Simple tests for the LLM API function.
"""

import unittest
from unittest.mock import patch, Mock
import json
from llm_api import call_llm_api, extract_response_text, get_usage_info


class TestLLMAPI(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_response_data = {
            "choices": [
                {
                    "message": {
                        "content": "This is a test response from the LLM."
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 8,
                "total_tokens": 18
            }
        }
    
    def test_extract_response_text(self):
        """Test extracting response text from API response."""
        text = extract_response_text(self.mock_response_data)
        self.assertEqual(text, "This is a test response from the LLM.")
    
    def test_get_usage_info(self):
        """Test extracting usage information from API response."""
        usage = get_usage_info(self.mock_response_data)
        expected_usage = {
            "prompt_tokens": 10,
            "completion_tokens": 8,
            "total_tokens": 18
        }
        self.assertEqual(usage, expected_usage)
    
    def test_invalid_prompt(self):
        """Test that invalid prompts raise ValueError."""
        with self.assertRaises(ValueError):
            call_llm_api("", "https://api.example.com")
        
        with self.assertRaises(ValueError):
            call_llm_api(None, "https://api.example.com")
    
    def test_invalid_api_url(self):
        """Test that invalid API URLs raise ValueError."""
        with self.assertRaises(ValueError):
            call_llm_api("Test prompt", "")
        
        with self.assertRaises(ValueError):
            call_llm_api("Test prompt", None)
    
    def test_invalid_temperature(self):
        """Test that invalid temperature values raise ValueError."""
        with self.assertRaises(ValueError):
            call_llm_api("Test prompt", "https://api.example.com", temperature=-0.1)
        
        with self.assertRaises(ValueError):
            call_llm_api("Test prompt", "https://api.example.com", temperature=2.1)
    
    def test_invalid_max_tokens(self):
        """Test that invalid max_tokens values raise ValueError."""
        with self.assertRaises(ValueError):
            call_llm_api("Test prompt", "https://api.example.com", max_tokens=0)
        
        with self.assertRaises(ValueError):
            call_llm_api("Test prompt", "https://api.example.com", max_tokens=-1)
    
    @patch('llm_api.requests.post')
    def test_successful_api_call(self, mock_post):
        """Test a successful API call."""
        # Mock the response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = self.mock_response_data
        mock_post.return_value = mock_response
        
        # Make the API call
        result = call_llm_api(
            prompt="Test prompt",
            api_url="https://api.example.com/v1",
            api_key="test-key",
            model="test-model"
        )
        
        # Verify the result
        self.assertEqual(result, self.mock_response_data)
        
        # Verify the request was made correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # Check URL
        self.assertEqual(args[0], "https://api.example.com/v1/chat/completions")
        
        # Check headers
        expected_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer test-key"
        }
        self.assertEqual(kwargs['headers'], expected_headers)
        
        # Check payload
        payload = kwargs['json']
        self.assertEqual(payload['model'], "test-model")
        self.assertEqual(payload['messages'][0]['role'], "user")
        self.assertEqual(payload['messages'][0]['content'], "Test prompt")
    
    @patch('llm_api.requests.post')
    def test_api_call_with_system_message(self, mock_post):
        """Test API call with system message."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = self.mock_response_data
        mock_post.return_value = mock_response
        
        result = call_llm_api(
            prompt="Test prompt",
            api_url="https://api.example.com/v1",
            system_message="You are a helpful assistant."
        )
        
        # Check that system message was included
        args, kwargs = mock_post.call_args
        payload = kwargs['json']
        
        self.assertEqual(len(payload['messages']), 2)
        self.assertEqual(payload['messages'][0]['role'], "system")
        self.assertEqual(payload['messages'][0]['content'], "You are a helpful assistant.")
        self.assertEqual(payload['messages'][1]['role'], "user")
        self.assertEqual(payload['messages'][1]['content'], "Test prompt")
    
    @patch('llm_api.requests.post')
    def test_api_call_without_api_key(self, mock_post):
        """Test API call without API key (for local APIs)."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = self.mock_response_data
        mock_post.return_value = mock_response
        
        result = call_llm_api(
            prompt="Test prompt",
            api_url="http://localhost:8080/v1"
        )
        
        # Check that no Authorization header was added
        args, kwargs = mock_post.call_args
        expected_headers = {
            "Content-Type": "application/json"
        }
        self.assertEqual(kwargs['headers'], expected_headers)


if __name__ == '__main__':
    unittest.main()