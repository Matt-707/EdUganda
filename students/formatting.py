import re

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
        line = line.replace("##", "")
        line = line.replace("#", "")
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
        cleaned_text = '\n'.join(cleaned_lines).strip()
        
    
    return cleaned_text


