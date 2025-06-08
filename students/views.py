from django.shortcuts import render
import requests
from .forms import PaperGenerationForm

#adding security by keeping the API key to our open router account private
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

#for the pdf generation uncomment when you get it to finally work
'''from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile'''


def ask_ai(request):
    ai_response = ""

    if request.method == "POST":
        user_input = request.POST.get("prompt")

        #offline ollama version
        '''data = {
            "model":"llama3",
            "prompt":user_input,
            "stream":False
        }

        #SEND TO OLLAMA and assign the result to the 'response vazriable'
        ai_response = requests.post(
            "http://localhost:11434/api/generate",
            json=data)'''
        
        ai_response = openrouter(user_input)
        
    return render(request, 
                  "students/ask_ai.html",
                  {"ai_response": ai_response})



def openrouter(prompt):
    headers={
        "Authorization": "Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek/deepseek-r1-distill-qwen-32b:free",
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



def generate_paper_view(request):
    response_data = None

    if request.method == 'POST':
        form = PaperGenerationForm(request.POST)
        if form.is_valid():
            selected_topics = form.cleaned_data['topics']
            selected_difficulty = form.cleaned_data['difficulty']

            #we have to format the topics into proper strings
            topics_string = ', '.join(selected_topics)

            #then we make a good prompt for both the questions and the guide
            prompt = (
                f"Generate a full Uganda A-Level Physics exam paper based on the following topics: "
                f"{topics_string}. The difficulty level should be {selected_difficulty}."
                f" Format the questions clearly and structure it like a real UNEB exam paper, though, I don't want you to add fluff like instructions. Just give me mainly the questions."
                f"Keep in mind that the UNEB format for physics in A-level has no multiple choice and only has essay questions"
                f"Each question is comprised of parts a through e (sometimes stopping at a part d or extending to part f). the first parts are usually asking for a definition or statement of a law, then come explanation questions and a calculation part and finally the description of an experimental setup"
                f"Finally, generate an accurate and detailed answer guide for the paper you have just generated. I want all the answers presented in the guide to be very well thought out and accurate. Be sure that the questions and the answer guide are separated by a clear heading/separator labelled 'Marking Guide'."
                f"Make sure that the paper and the answer guide are generated at the same time, one after the other"
            )
            #marking_prompt = (f"Generate a marking guide for the A-Level Ugandan Physics paper you just generated.")
            

            # send the data to the ollama API
            '''ollama_response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream":False,
                }
            )'''

            #using our openrouter function
            ai_response = openrouter(prompt)
            if "Marking Guide" in ai_response:
                paper_part, guide_part = ai_response.split("Marking Guide", 1)
            else:
                paper_part = ai_response
                guide_part = "No marking guide found."

            formatted_paper_part = paper_part.strip().split('\n')
            formatted_guide_part = guide_part.strip().split('\n')


            #offline ollama version
            '''response_data = ollama_response.json().get("response", "No Response Recieved")
            paper_part, guide_part = response_data.split("Marking Guide", 1)
            formatted_paper_part = paper_part.strip().split('\n')
            formatted_guide_part = guide_part.strip().split('\n')'''
            

            
            return render(request, 'students/paper_result.html',
                          {"questions": formatted_paper_part,
                           "guide": formatted_guide_part,
                           }
                          )
    else:
        form = PaperGenerationForm()
    return render(request, 'students/generate_paper.html', {'form':form})

#view function for the pdf generation
'''def download_pdf_from_response(request):
    if request.method == "POST":
        paper_content = request.POST.get("paper_content")


        html_string = render_to_string('paper_pdf_template.html',{
            'full_content':paper_content
        })

        with tempfile.NamedTemporaryFile(delete=True) as output:
            HTML(string=html_string).write_pdf(output.name)
            output.seek(0)
            response = HttpResponse(output.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="ExamPaper.pdf"'
            return response
    return HttpResponse("Invalid request method.")'''


