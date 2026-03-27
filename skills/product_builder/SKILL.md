# Designer Skill - Digital Product Factory

## Purpose
Translate approved ideas into high-quality digital products.

## Instructions
1. Monitor the `projects` table for status "Construindo".
2. Use Python libraries like `xlsxwriter` to generate the file.
3. Save the file locally in the `output/` directory.
4. Update the project status to "Aguardando Link".

## Implementation
```python
import db
import xlsxwriter
import os

def build_product(project_id, idea_name):
    db.update_agent_status("Designer", "Working")
    
    file_name = f"output/{idea_name.replace(' ', '_')}.xlsx"
    os.makedirs("output", exist_ok=True)
    
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Claw Agency - Premium Asset')
    # ... build complex logic ...
    workbook.close()
    
    db.update_project_status(project_id, "Aguardando Link", file_path=file_name)
    db.update_agent_status("Designer", "Idle")
    return f"Produto {idea_name} finalizado em {file_name}"
```
