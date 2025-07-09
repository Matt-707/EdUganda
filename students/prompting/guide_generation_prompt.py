def guide_generation_prompt(ai_paper):
    """
    Create a prompt for generating a full Uganda A-Level Physics exam paper GUIDE.

    Returns:
        str: The prompt to be sent to the AI model.
    """

    return (
        f"""You are a UNEB Physics assistant. Only base off the Ugandan A-Level syllabus.
    
        Here is an A-Level Physics UNEB-style exam paper:\n\n
        
        ---BEGIN PAPER---\n
        {ai_paper}\n\n
        ---END PAPER---\n\n

        Now generate a complete answer guide for this ENTIRE paper ALL AT ONCE.\n
        - Provide accurate and complete answers to all parts.\n
        Ensure that answers are correctly labelled with the corresponding question parts.\n
        - Avoid any fluff, headers, or endings like 'Hope this helps'.\n
        - Just output the LABELLED answer content and end the answer guide with the word: END.\n

        VERY IMPORTANT: Use LaTeX: \\(  \\) for inline, \\[  \\] for display of any equations and mathematical expressions.\n
        - Use LaTeX for all physics equations and symbols.\n

        NOTE: Make sure to label the answers to the questions EXPLICITLY as Question 1, Question 2, etc.\n

        Leave out any introduction or conclusion.
    
        Use UNEB exam tone and do not make up facts.

        Answer in full detail, following UNEB marking standards and proper LaTeX formatting.
    """
    )