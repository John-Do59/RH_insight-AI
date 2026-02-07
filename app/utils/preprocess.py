import re

def clean_spaced_text(text: str) -> str:
    """
    Cleans text that has spaces between characters (common in some PDF extractions).
    Example: "D é v e l o p p e u r" -> "Développeur"
    """
    if not text:
        return ""
    
    # 1. First, detect if the text is likely spaced out.
    # We look for sequences of single letters separated by spaces.
    # This regex looks for 3 or more occurrences of: [letter] space
    spaced_pattern = re.compile(r'([A-Za-zÀ-ÿ]\s){3,}')
    
    if not spaced_pattern.search(text):
        return text

    # 2. Logic to reconstruct words:
    # We split by lines to handle formatting better
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Reconstruct words in the line
        # We replace spaces that are between single characters, but keep spaces that separate "reconstructed words".
        # A simple hack: replace "X Y Z" with "XYZ" if they are single chars.
        
        # New strategy: Use a more sophisticated regex to find blocks of spaced characters
        # Matches: One char, then optional space, then one char, etc.
        # But we want to preserve double spaces or significant gaps as word boundaries.
        
        # This regex matches a character followed by a single space, repeating.
        # We replace the "char space" with "char".
        reconstructed = re.sub(r'([A-Za-zÀ-ÿ])\s(?=[A-Za-zÀ-ÿ](\s|$))', r'\1', line)
        
        # Clean up multiple spaces that might have been created
        reconstructed = re.sub(r'\s+', ' ', reconstructed).strip()
        cleaned_lines.append(reconstructed)
        
    return '\n'.join(cleaned_lines)
