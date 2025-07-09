def paper_generation_prompt(topics_string, selected_difficulty):
    """
    Create a prompt for generating a full Uganda A-Level Physics exam paper based on selected topics and difficulty level.

    Returns:
        str: The prompt to be sent to the AI model.
    """

    return (
        f"""You are a UNEB Physics assistant. Only base off the Ugandan A-Level syllabus.
    
        Generate a full Uganda A-Level Physics exam paper based on the following topics: {topics_string}.\n
        The difficulty level of the paper should be {selected_difficulty}.\n

        Format the questions clearly and structure it like a real UNEB exam paper, BUT, I don't want you to add fluff like instructions. Just give me mainly the LABELLED questions.\n

        Keep in mind that the UNEB format for physics in A-level has no multiple choice and only has essay questions.\n 

        Create STRICTLY 3 questions per topic.\n

        IMPORTANT: Each question is comprised of parts a through e (sometimes stopping at a part d or extending to part f).\n 
        REMEMBER: The first parts are usually asking for a definition or statement of a law, then come explanation questions and a calculation part and finally the description of an experimental setup.\n
        
        NOTE: Make sure to label the questions EXPLICITLY as Question 1, Question 2, etc.\n

        Leave out any introduction or conclusion, just give me the questions and nothing else.\n
    
        Use UNEB exam tone and do not make up facts.

        Answer in full detail, following UNEB marking standards and proper LaTeX formatting.
    """
    )