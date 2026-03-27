# Sales Skill - Digital Product Factory

## Purpose
Proactively find customers on Reddit, Twitter, and specialized forums to sell the digital assets.

## Instructions
1. Monitor the `projects` table for status "Vendendo".
2. Use the provided `sales_link`.
3. Use `browser-use` to search for people asking for solutions in the product's niche.
4. Respond in a helpful, non-spammy way, providing the link at the end.
5. Record interacting logs in the dashboard.

## Implementation
```python
import db
from browser_use import Agent
from groq import Groq

def promote_product(project_id, niche, sales_link):
    db.update_agent_status("Sales", "Working")
    
    # ... logic using browser-use to find leads ...
    # ... interact and post link ...
    
    db.update_agent_status("Sales", "Idle")
    return f"Promoção para o produto {project_id} iniciada no Reddit."
```
