# Manager Skill - Digital Product Factory

## Purpose
Oversee the entire factory operation, check system health, and ensure agents are performing their duties correctly.

## Instructions
1. Check Database connection to PostgreSQL.
2. Verify API keys for Groq, Gemini, and Apify.
3. Monitor `agent_status` table to ensure no agent is stuck in "Working" for too long.
4. Provide a summarized report of "Ideias Pendentes" vs "Produtos Prontos".

## Implementation
```python
import os
import db
import requests

def check_health():
    try:
        # Check DB
        agents = db.get_all_agent_status()
        db_status = "OK"
    except Exception as e:
        db_status = f"Error: {str(e)}"
    
    # Check APIs (simulated or ping)
    groq_api = "OK" if os.getenv("GROQ_API_KEY") else "MISSING"
    gemini_api = "OK" if os.getenv("GEMINI_API_KEY") else "MISSING"
    
    # Status Summary
    stats = {
        "pending_ideas": len(db.get_projects_by_status("Ideia Pendente")),
        "ready_products": len(db.get_projects_by_status("Aguardando Link")),
        "live_sales": len(db.get_projects_by_status("Vendendo"))
    }
    
    return {
        "db": db_status,
        "api_groq": groq_api,
        "api_gemini": gemini_api,
        "stats": stats,
        "agents": agents
    }

if __name__ == "__main__":
    print(check_health())
```
