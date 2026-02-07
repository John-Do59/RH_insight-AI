import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.graph.graph import app

def test_chat():
    questions = [
        "Quelles sont les compétences techniques de Amaury ?",  # Should trigger RAG or SQL
        "Combien d'expériences possède-t-il ?",           # Should trigger SQL
        "Bonjour, qui es-tu ?"                             # Should trigger General
    ]
    
    for q in questions:
        print(f"\n--- Question: {q} ---")
        initial_state = {"question": q, "messages": []}
        result = app.invoke(initial_state)
        print(f"Intent: {result.get('intent')}")
        print(f"Response: {result.get('response')}")

if __name__ == "__main__":
    test_chat()
