from django.shortcuts import render
import requests

from groq import Groq

import requests

#adding security by keeping the API key to our open router account private
import os
from dotenv import load_dotenv
load_dotenv()
OPEN_API_KEY = os.getenv("OPENROUTER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

#Checking to see if the API keys are loaded correctly
print("OPENROUTER KEY LOADED:", OPEN_API_KEY is not None)
print("GROQ KEY LOADED:", GROQ_API_KEY is not None)


# importing time to test the response times
import time

'''OPENROUTER API'''

def openrouter(prompt, model="deepseek/deepseek-chat-v3.1:free"):
    # This function is for the openrouter API, which is a free alternative to the OpenAI API
    headers={
        "Authorization": f"Bearer {OPEN_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        start_time = time.time()  # Start timing the request

        # Make the POST request to the OpenRouter API
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        
        end_time = time.time()  # End timing the request
        duration = end_time - start_time

        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        response.raise_for_status()
        result= response.json()
        return result['choices'][0]['message']['content'], duration
    except Exception as e:
        return f"Error: {str(e)}"
    

'''GROQ API'''

def groq(prompt, model="openai/gpt-oss-120b"):
    Client = Groq(api_key=GROQ_API_KEY)

    start_time = time.time()  # Start timing the request
    response = Client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=2048,
        temperature=0.7,
        top_p=0.95,
    )

    end_time = time.time()  # End timing the request
    duration = end_time - start_time

    
    return response.choices[0].message.content, duration


'''OLLAMA API'''

def ollama_version(prompt, model="mistral"):
    # This function is for the ollama API, which is a local version of the openrouter API

    start_time = time.time()  # Start timing the request
    response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream":False,
                }
            )
    end_time = time.time()  # End timing the request
    duration = end_time - start_time

    try:
        ollama_response = response.json() 
        #print("Ollama raw response:", ollama_response)
    except Exception as e:
        print("Failed to parsw JSON:", str(e))
        print("Raw response:", response.text)
        return "Error: Failed to parse Ollama response"
    
    #try to return the response text if available
    if 'response' in ollama_response:
        return ollama_response['response'], duration
    elif 'message' in ollama_response:
        return ollama_response['message'], duration
    elif 'error' in ollama_response:
        return f"Error: {ollama_response['error']}", duration
    else:
        return "Error: Unexpected response format from Ollama API", duration
