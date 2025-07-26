#!/usr/bin/env python3
"""
Simple script to test OpenAI API key functionality with custom wrapper
"""
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_key():
    """Test the OpenAI API key with a simple request using custom wrapper."""
    
    # Get API key from environment
    api_key = os.environ.get("OPENAI_API_KEY")
    
    # Correct MetisAI wrapper URL
    base_url = "https://api.metisai.ir/openai/v1"
    
    print("=== OpenAI API Key Test (with MetisAI Wrapper) ===")
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    print(f"Base URL: {base_url}")
    
    if api_key:
        # Mask the key for security
        masked_key = api_key[:7] + "*" * (len(api_key) - 11) + api_key[-4:] if len(api_key) > 11 else "*" * len(api_key)
        print(f"API Key: {masked_key}")
    else:
        print("❌ No OPENAI_API_KEY found in environment variables")
        print("\nTo set your API key:")
        print("export OPENAI_API_KEY='your-wrapper-api-key-here'")
        print("or add it to a .env file")
        return False
    
    try:
        # Initialize OpenAI client with correct MetisAI base URL
        client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        print("\n✅ OpenAI client initialized successfully with MetisAI wrapper")
        
        # Test with a simple completion
        print("\n🧪 Testing API with a simple request...")
        
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello, API test successful!' if you can read this."}
            ],
            max_tokens=50,
            temperature=0.1
        )
        
        result = response.choices[0].message.content
        print(f"\n✅ API Response: {result}")
        print(f"✅ Model used: {response.model}")
        print(f"✅ Tokens used: {response.usage.total_tokens}")
        
        return True
        
    except openai.AuthenticationError as e:
        print(f"\n❌ Authentication Error: {e}")
        print("The API key is invalid or expired for the MetisAI wrapper service.")
        return False
        
    except openai.RateLimitError as e:
        print(f"\n⚠️  Rate Limit Error: {e}")
        print("You've hit the rate limit. The key works but requests are being throttled.")
        return True
        
    except openai.APIError as e:
        print(f"\n❌ API Error: {e}")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        return False

def test_alternative_models():
    """Test with alternative models if gpt-4-turbo fails."""
    api_key = os.environ.get("OPENAI_API_KEY")
    base_url = "https://api.metisai.ir/openai/v1"
    
    if not api_key:
        return False
        
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    
    models_to_try = ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4", "gpt-4o"]
    
    print("\n🔄 Testing alternative models with MetisAI wrapper...")
    
    for model in models_to_try:
        try:
            print(f"\n  Testing {model}...")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "Hello"}
                ],
                max_tokens=10
            )
            print(f"  ✅ {model} works!")
            return True
        except Exception as e:
            print(f"  ❌ {model} failed: {str(e)[:100]}...")
    
    return False

def test_different_providers():
    """Test different providers available through the wrapper."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return False
    
    providers = [
        ("openai", "gpt-4o-mini"),
        ("anthropic", "claude-3-haiku-20240307"),
        ("google", "gemini-pro")
    ]
    
    print("\n🔄 Testing different providers...")
    
    for provider, model in providers:
        try:
            base_url = f"https://api.metisai.ir/api/v1/wrapper/{provider}"
            print(f"\n  Testing {provider} with {model}...")
            
            client = openai.OpenAI(api_key=api_key, base_url=base_url)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "Hello"}
                ],
                max_tokens=10
            )
            print(f"  ✅ {provider} ({model}) works!")
            return True
        except Exception as e:
            print(f"  ❌ {provider} failed: {str(e)[:100]}...")
    
    return False

if __name__ == "__main__":
    print("Testing OpenAI API key with MetisAI wrapper...")
    
    success = test_openai_key()
    
    if not success:
        print("\n🔄 Trying alternative models...")
        alt_success = test_alternative_models()
        
        if not alt_success:
            print("\n🔄 Trying different providers...")
            test_different_providers()
    
    print("\n" + "="*50)
    if success:
        print("🎉 API key test completed successfully!")
    else:
        print("❌ API key test failed. Please check your key and try again.")
        print("\nNote: Make sure your API key is valid for the MetisAI wrapper service.") 