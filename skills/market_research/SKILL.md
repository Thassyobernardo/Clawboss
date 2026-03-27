# Researcher Skill - Digital Product Factory

## Purpose
Proactively find market gaps and product ideas in Australia that can be sold for $30-$40.

## Instructions
1. Use Apify or Google Search to find trending "pains" or "needs" in Australia (e.g., small business tools, personal finance templates, simplified travel guides).
2. Filter for ideas that can be turned into a digital product (Spreadsheet, PDF, Tool).
3. Suggested niches: Real Estate, Tradie Management, Personal Budgeting.
4. Save the idea to the `projects` table with status "Ideia Pendente".

## Implementation
```python
import db
import os
from groq import Groq

def search_niche_ideas():
    db.update_agent_status("Research", "Working")
    
    # Logic to find ideas (simulated here with LLM prompt)
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    prompt = "Encontre 3 nichos de micro-saas ou infoprodutos na Austrália que custem entre 30 e 40 AUD e resolvam dores de pequenos negócios."
    
    # ... Process research ...
    
    # Example addition:
    db.add_project("Tradies", "Auto-Quote Spreadsheet for Plumbers", 35.00)
    
    db.update_agent_status("Research", "Idle")
    return "Pesquisa concluída. Ideias enviadas ao CEO."
```
