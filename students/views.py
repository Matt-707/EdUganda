from django.shortcuts import render
from .forms import PaperGenerationForm

#importing API clients for AI interactions
from .api_clients import groq, openrouter, ollama_version, together_ai

from rag_index.rag_searcher import select_best_index

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
    indexes_to_images = {
        "sources/physics1/wogibi/faiss_index":"p1_wogibi_screenshots",
        "sources/physics2/faiss_index":"p2_notes_screenshots",
    }
    if request.method == "POST":
        user_input = request.POST.get("prompt")

        result = select_best_index(user_input)
        context = result["context"]

        best_index = result["best_index"]

        if best_index!=None:
            best_index=best_index.replace("\\","/")
        
        pages = result["pages"]
        similarity = result["similarity_score"]

        print("🔍 Selected Index:", best_index)
        print("🔢 Similarity Score:", similarity)
        print("📄 Pages:", pages)

        try:
            img_dir = indexes_to_images[str(best_index)]
            print(img_dir)
        except Exception as e:
            print(f"error loading img directory {e}")

        final_prompt =  create_chat_prompt(user_input, context)

        raw_ai_response = openrouter(final_prompt)

        ai_response = cleaning(raw_ai_response)

        if "I do not have enough information" not in ai_response:
            images = [f"{img_dir}/page_{page}.png" for page in pages]

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

            ai_paper = openrouter(question_prompt, model="x-ai/grok-4-fast:free")

            marking_prompt= guide_generation_prompt(ai_paper)

            guide_text = openrouter(marking_prompt, model="x-ai/grok-4-fast:free")

            #total_time = generation_time+answer_guide_time

            #formatting the prompts for the paper and the guide
            formatted_paper_part = cleaning(ai_paper).split('\n')
            formatted_guide_part = cleaning(guide_text).split('\n')

            print("==== Cleaned Guide ====")
            print(formatted_guide_part)
            print("=======================")
            print("=====TIME ELAPSED=====")
            #print(total_time)
            
            return render(request, 'students/paper_result.html',
                          {"questions": formatted_paper_part,
                           "guide": formatted_guide_part,
                           }
                          )
    else:
        form = PaperGenerationForm()
    return render(request, 'students/generate_paper.html', {'form':form})


