'''def ask_ai(request):
    ai_response = ""

    if request.method == "POST":
        user_input = request.POST.get("prompt")
         
        #the data to send to ollama
        data = {
            "model":"llama3",
            "prompt":user_input,
            "stream":False
        }

        #SEND TO OLLAMA and assign the result to the 'response vazriable'
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=data)
        
        result = response.json()
        ai_response = result.get("response","No response received")
        
    return render(request, 
                  "students/ask_ai.html",
                  {"ai_response": ai_response})'''