from django.shortcuts import render
from .forms import PaperGenerationForm

#importing API clients for AI interactions
from .api_clients import groq, openrouter, ollama_version, together_ai

from rag_index.rag_searcher import retrieve_context_and_pages

# Importing prompt creation functions
from students.prompting.chat_prompt import create_chat_prompt
from students.prompting.paper_generation_prompt import paper_generation_prompt
from students.prompting.guide_generation_prompt import guide_generation_prompt

#import formatting functions
from students.formatting import cleaning

def ask_ai(request):
    ai_response = ""
    images = []
    user_input = ""
    if request.method == "POST":
        user_input = request.POST.get("prompt")

        context, pages = retrieve_context_and_pages(user_input, index_path="sources/physics2/faiss_index")  

        print("==== Retrieved Context ====")
        print(context)
        print("\ncontext source")
        print(pages)

        final_prompt =  create_chat_prompt(user_input, context)
        ai_response = cleaning(openrouter(final_prompt)) 

        if "I do not have enough information" not in ai_response:
            images = [f"p2_notes_screenshots/page_{page}.png" for page in pages]

    return render(request, 
                  "students/ask_ai.html",
                  {"ai_response": ai_response,
                   "images": images,
                   "user_input": user_input,
                   })


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
            question_prompt = paper_generation_prompt(topics_string, selected_difficulty)
            
            ai_paper = openrouter(question_prompt)

            marking_prompt= guide_generation_prompt(ai_paper)
            
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


