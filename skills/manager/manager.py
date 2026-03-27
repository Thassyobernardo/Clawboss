import os
import sys
# Add parent dir to path to import db
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import db

def run_diagnostic():
    db.update_agent_status("Manager", "Working")
    try:
        # DB Check
        agents = db.get_all_agent_status()
        
        # Project Stats
        pending = db.get_projects_by_status("Ideia Pendente")
        ready = db.get_projects_by_status("Aguardando Link")
        sales = db.get_projects_by_status("Vendendo")
        
        report = f"""
FACTORY STATUS REPORT:
----------------------
Database: CONNECTED
Agents: {len(agents)} active
Pending Ideas: {len(pending)}
Ready Products: {len(ready)}
Live Sales: {len(sales)}

Agent Health:
"""
        for a in agents:
            report += f"- {a['agent_name']}: {a['current_status']} (Last active: {a['last_activity']})\n"
            
        db.update_agent_status("Manager", "Idle")
        return report
    except Exception as e:
        db.update_agent_status("Manager", f"Error: {str(e)}")
        return f"CRITICAL ERROR: {str(e)}"

if __name__ == "__main__":
    print(run_diagnostic())
