from .api_clients import groq, openrouter, ollama_version, together_ai


def response_times(
        user_input="Teach me about electromagnetic induction",
        openrouter_model = "deepseek/deepseek-chat-v3-0324:free",
        ollama_model = "mistral",
        together_model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        groq_model = "gemma2-9b-it",
        ):
    """
    This view is for testing the response times of different AI models.
   
    """     
    # Measure response times for each API
    groq_res, groq_time = groq(user_input, model=groq_model)
    openrouter_res, openrouter_time = openrouter(user_input, model=openrouter_model)
    #ollama_res, ollama_time = ollama_version(user_input, model=ollama_model)
    together_res, together_ai_time = together_ai(user_input, model=together_model)

    print("--- RESPONSE TIMES ---")
 
    #print(f"Ollama|{ollama_model}: ", ollama_time, "seconds")
    print(f"OpenRouter|{openrouter_model}: ", openrouter_time, "seconds")
    print(f"Together AI|{together_model}: ", together_ai_time, "seconds")
    print(f"Groq|{groq_model}: ", groq_time, "seconds")

    

   