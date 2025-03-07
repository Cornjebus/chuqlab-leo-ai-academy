import os
import logging
import openai
from openai import OpenAI  # Import the client class
import requests
from dotenv import load_dotenv

# Load environment variables if not already loaded
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Set OpenAI API key if available
api_key = os.getenv("OPENAI_API_KEY", "").strip()  # Remove any whitespace
if api_key:
    # Log key details for debugging
    logger.debug(f"API key found (starts with: {api_key[:7]})")
    logger.debug(f"API key length: {len(api_key)}")
    logger.debug(f"API key format valid: {api_key.startswith('sk-')}")
    
    # Validate key format
    if not api_key.startswith('sk-'):
        logger.error("API key format invalid - must start with 'sk-'")
        client = None
    else:
        try:
            # Create client instance instead of setting global key
            client = OpenAI(api_key=api_key)
            logger.info("OpenAI client created successfully")
        except Exception as e:
            logger.error(f"Error creating OpenAI client: {str(e)}")
            client = None
else:
    logger.warning("No OpenAI API key found in environment variables. Check your .env file.")
    client = None

def get_available_models():
    """Get a list of available language models.
    
    Returns:
        list: A list of model identifiers
    """
    # For simplicity, we'll just return a static list of models
    # In a production environment, this would interact with the OpenAI API
    # to get the current list of available models
    models = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo",
        "claude-instant",
        "claude-2",
        "llama-2-7b",
    ]
    
    # If no API key, add a mock model for testing
    if not api_key:
        models.append("mock-response-model")
        
    return models

def get_llm_response(prompt, conversation_history=None, model="gpt-3.5-turbo", temperature=0.7, max_tokens=250):
    """Get a response from a language model.
    
    Args:
        prompt (str): The user prompt to send to the model
        conversation_history (list, optional): Previous conversation messages
        model (str): The model to use
        temperature (float): The creativity/randomness parameter (0-1)
        max_tokens (int): Maximum response length
        
    Returns:
        str: The model's response text
    """
    try:
        # If no API key is set or mock model selected, return a mock response
        if not api_key or model == "mock-response-model":
            logger.info("Using mock response (no API key or mock model selected)")
            return generate_mock_response(prompt)
        
        # Format the messages for the API
        messages = []
        
        # Add conversation history if provided
        if conversation_history:
            for message in conversation_history:
                messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })
        
        # Add the current prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Call the OpenAI API using the client instance
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extract and return the response text
            response_text = response.choices[0].message.content.strip()
            return response_text
            
        except openai.AuthenticationError:
            logger.error("Authentication error: Invalid API key")
            return "Error: Invalid API key. Please check your OpenAI API key in the .env file."
            
        except openai.APIConnectionError:
            logger.error("API Connection error: Could not connect to OpenAI API")
            return "Error: Could not connect to the AI service. Please check your internet connection or try again later."
            
        except openai.RateLimitError:
            logger.error("Rate limit error: Too many requests")
            return "Error: Rate limit exceeded. Please try again in a few moments."
            
        except openai.BadRequestError as e:
            logger.error(f"Bad request error: {str(e)}")
            return f"Error: The request to the AI service was invalid. Details: {str(e)}"
            
        except openai.APIError as e:
            logger.error(f"API error: {str(e)}")
            return "Error: The AI service is currently unavailable. Please try again later."
            
    except Exception as e:
        logger.error(f"Unexpected error in get_llm_response: {str(e)}")
        return f"An unexpected error occurred: {str(e)}\n\nUsing mock response instead: {generate_mock_response(prompt)}"

def generate_mock_response(prompt):
    """Generate a mock response for testing without an API key.
    
    Args:
        prompt (str): The user prompt
        
    Returns:
        str: A mock response
    """
    # A simple mock response that acknowledges the prompt
    prompt_length = len(prompt)
    
    if "police" in prompt.lower() or "law" in prompt.lower() or "enforcement" in prompt.lower():
        return (
            "This is a mock response for law enforcement related questions. "
            "In a real deployment, this would connect to the OpenAI API to generate "
            "a response about policing, criminal justice, or law enforcement. "
            "To use the real API, please add your OpenAI API key to the .env file.\n\n"
            "Your prompt was related to law enforcement and was "
            f"{prompt_length} characters long."
        )
    elif "ethics" in prompt.lower() or "bias" in prompt.lower():
        return (
            "This is a mock response about AI ethics or bias. "
            "In a real deployment, this would provide thoughtful analysis "
            "of ethical considerations in AI applications. "
            "To use the real API, please add your OpenAI API key to the .env file.\n\n"
            "Your question about ethics or bias would normally receive a "
            "detailed response covering potential concerns and mitigation strategies."
        )
    elif "report" in prompt.lower() or "investigation" in prompt.lower():
        return (
            "This is a mock response for a report or investigation. "
            "In a real deployment, this would generate a structured police report "
            "or investigation summary based on your input. "
            "The response would include relevant sections such as incident details, "
            "persons involved, evidence collected, and next steps.\n\n"
            "To use the real API with complete functionality, please add your OpenAI API key to the .env file."
        )
    else:
        return (
            "This is a mock response for testing purposes. "
            "In a real deployment, this would connect to the OpenAI API to generate "
            "a response based on your prompt. "
            "To use the real API, please add your OpenAI API key to the .env file.\n\n"
            f"Your prompt was {prompt_length} characters long. Here's a brief "
            "acknowledgment of what you asked about: " + prompt[:50] + "..."
        )

def simulate_llm_response(prompt, **kwargs):
    """
    Simulate an LLM response for testing or when API is unavailable.
    This is useful for development/demo purposes when you don't want to use the actual API.
    """
    # Simple simulation - in a real app you'd remove this
    responses = {
        "hello": "Hello! How can I assist you with your AI learning today?",
        "what is ai": "Artificial Intelligence (AI) refers to computer systems designed to perform tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and language translation.",
        "what is an llm": "A Large Language Model (LLM) is a type of AI system trained on vast amounts of text data to understand and generate human-like text. Examples include GPT models, Claude, and LLaMA. They work by predicting what text should come next in a sequence based on patterns they've learned.",
    }
    
    # Default response if no match
    default_response = (
        "I'm a simulated AI response for demonstration purposes. "
        "In a production environment, this would be connected to an actual LLM API like OpenAI. "
        "Your prompt was: " + prompt
    )
    
    # Check for simple keyword matches
    for key, response in responses.items():
        if key in prompt.lower():
            return response
    
    return default_response 