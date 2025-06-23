from django.shortcuts import render
import requests
from .forms import PaperGenerationForm
import re

#adding security by keeping the API key to our open router account private
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

#for the pdf generation uncomment when you get it to finally work
'''from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile'''


def ask_ai(request):
    ai_response = ""
    if request.method == "POST":
        user_input = request.POST.get("prompt")     
        ai_response = cleaning(openrouter(user_input))    
    return render(request, 
                  "students/ask_ai.html",
                  {"ai_response": ai_response})


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
                    "model": "llama3",
                    "prompt": prompt,
                    "stream":False,
                }
            )
    ollama_response = response.json() 
    return ollama_response['response']


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
            question_prompt = (
                f"Generate a full Uganda A-Level Physics exam paper based on the following topics: "
                f"{topics_string}. The difficulty level should be {selected_difficulty}."
                f" Format the questions clearly and structure it like a real UNEB exam paper, though, I don't want you to add fluff like instructions. Just give me mainly the LABELLED questions."
                f"Keep in mind that the UNEB format for physics in A-level has no multiple choice and only has essay questions. Create STRICTLY 3 questions per topic.\n"
                f"Each question is comprised of parts a through e (sometimes stopping at a part d or extending to part f). the first parts are usually asking for a definition or statement of a law, then come explanation questions and a calculation part and finally the description of an experimental setup"
                f"Make sure to label the questions EXPLICITLY as Question 1, Question 2, etc.\n"
                f"Leave out any introduction or conclusion, just give me the questions and nothing else."
    )
            
            ai_paper = openrouter(question_prompt)
            

            marking_prompt=(f"Here is an A-Level Physics UNEB-style exam paper:\n\n"
                            f"{ai_paper}\n\n"
                            f"Now generate a complete answer guide for this ENTIRE paper ALL AT ONCE.\n"
                            f"- Provide accurate and complete answers to all parts.\n"
                            f"Ensure that answers are correctly labelled with the corresponding question parts.\n"
                            f"- Use LaTeX: \\(  \\) for inline, \\[  \\] for display of any equations and mathematical expressions.\n"
                            f"- Avoid any fluff, headers, or endings like 'Hope this helps'.\n"
                            f"- Just output the LABELLED answer content and end the answer guide with the word: END."
                        

                )
            
            guide_text = openrouter(marking_prompt)

            #formatting the prompts for the paper and the guide
            formatted_paper_part = cleaning(ai_paper).split('\n')
            formatted_guide_part = cleaning(guide_text).split('\n')

            print("==== Cleaned Guide ====")
            print(formatted_guide_part)
            print("=======================")

            
            return render(request, 'students/paper_result.html',
                          {"questions": formatted_paper_part,
                           "guide": formatted_guide_part,
                           }
                          )
    else:
        form = PaperGenerationForm()
    return render(request, 'students/generate_paper.html', {'form':form})


def cleaning(content):
    """
    Cleans AI-generated exam content (questions or answers).
    Returns a clean string with preserved line breaks, suitable for splitting later.
    """
    lines = content.split('\n')
    cleaned_lines = []

    for line in lines:
        # Remove markdown symbols
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)

        # Remove AI fluff
        if any(phrase in line.lower() for phrase in [
            "let me know",
            "hope this helps",
            "i hope that was helpful",
            "here's a",
            "would you like",
            "feel free",
            "as an ai",
            "in conclusion",
            "thanks for using",
        ]):
            continue

        # Remove lines like: ## Step 35: or ## Step 45: Question 9e
        line = re.sub(r"^##?\s*Step\s*\d+[:\-]?\s*", "", line)
        
        # Remove wrapping quotes
        line = line.strip('"\'')

        # Fix escaped LaTeX syntax (\\( becomes \(, etc.)
        line = line.replace('\\\\(', '\\(').replace('\\\\)', '\\)')
        line = line.replace('\\\\[', '\\[').replace('\\\\]', '\\]')

        # Convert raw dollar LaTeX to proper delimiters
        line = line.replace('$$', '\\[').replace('$', '\\(')

        if line:  # Skip blank lines
            cleaned_lines.append(line)

        

    # Return as a single string with preserved line breaks
    return '\n'.join(cleaned_lines).strip()



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


