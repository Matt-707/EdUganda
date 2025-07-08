from django.shortcuts import render
import requests
from .forms import PaperGenerationForm
import re
from groq import Groq


#adding security by keeping the API key to our open router account private
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def openrouter(prompt):
    # This function is for the openrouter API, which is a free alternative to the OpenAI API
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek/deepseek-chat:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        response.raise_for_status()
        result= response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"
    

def ollama_version(prompt):
    # This function is for the ollama API, which is a local version of the openrouter API
    response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    "model": "mistral",
                    "prompt": prompt,
                    "stream":False,
                }
            )
    try:
        ollama_response = response.json() 
        print("Ollama raw response:", ollama_response)
    except Exception as e:
        print("Failed to parsw JSON:", str(e))
        print("Raw response:", response.text)
        return "Error: Failed to parse Ollama response"
    
    #try to return the response text if available
    if 'response' in ollama_response:
        return ollama_response['response']
    elif 'message' in ollama_response:
        return ollama_response['message']
    elif 'error' in ollama_response:
        return f"Error: {ollama_response['error']}"
    else:
        return "Error: Unexpected response format from Ollama API"


def together_ai(prompt):
    # This function is for the Together AI API, which is another alternative to the openrouter API
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.95,
    }
    try:
        response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=data)
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"
    
import requests
import os

def groq(prompt):
    Client = Groq(api_key=GROQ_API_KEY)
    response = Client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=2048,
        temperature=0.7,
        top_p=0.95,
    )
    print(response)
    
    return response.choices[0].message.content


