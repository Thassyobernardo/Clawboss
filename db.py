import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    if not DATABASE_URL:
        raise ValueError("A variável de ambiente DATABASE_URL não está definida. Certifique-se de que o PostgreSQL está conectado ao serviço no Railway.")
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    # Create projects table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id SERIAL PRIMARY KEY,
            niche TEXT,
            product_idea TEXT,
            price_aud DECIMAL(10, 2),
            file_path TEXT,
            sales_link TEXT,
            responsible_agent TEXT,
            status TEXT DEFAULT 'Ideia Pendente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    # Colunas usadas pelo robô / aba Ideias (INSERT com titulo, descricao, potencial_lucro, escalabilidade)
    for col, typ in (
        ("titulo", "TEXT"),
        ("descricao", "TEXT"),
        ("potencial_lucro", "TEXT"),
        ("escalabilidade", "TEXT"),
    ):
        cur.execute(
            f"ALTER TABLE projects ADD COLUMN IF NOT EXISTS {col} {typ};"
        )
    
    # Hunter / Upwork lead intelligence (PostgreSQL obrigatório — não usar .md)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS hunter_leads (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            dor_cliente TEXT NOT NULL,
            como_escalar TEXT NOT NULL,
            faturar_2k_mes TEXT NOT NULL,
            fonte TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Create agent_status table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS agent_status (
            agent_name TEXT PRIMARY KEY,
            current_status TEXT DEFAULT 'Idle',
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Initialize agents
    agents = ['Research', 'Designer', 'Sales', 'Manager']
    for agent in agents:
        cur.execute("INSERT INTO agent_status (agent_name) VALUES (%s) ON CONFLICT DO NOTHING;", (agent,))
        
    conn.commit()
    cur.close()
    conn.close()

def update_agent_status(agent_name, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE agent_status 
        SET current_status = %s, last_activity = CURRENT_TIMESTAMP 
        WHERE agent_name = %s
    """, (status, agent_name))
    conn.commit()
    cur.close()
    conn.close()

def get_all_agent_status():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM agent_status")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def add_project(niche, idea, price):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO projects (niche, product_idea, price_aud, responsible_agent)
        VALUES (%s, %s, %s, 'Research')
    """, (niche, idea, price))
    conn.commit()
    cur.close()
    conn.close()


def insert_idea_from_research(
    titulo: str,
    descricao: str,
    potencial_lucro: str,
    escalabilidade: str,
    price_aud=35.0,
):
    """Insere linha na tabela projects (aba Ideias). Mantém niche/product_idea alinhados ao legado do dashboard."""
    conn = get_connection()
    cur = conn.cursor()
    t, d = titulo.strip(), descricao.strip()
    pl, es = potencial_lucro.strip(), escalabilidade.strip()
    cur.execute(
        """
        INSERT INTO projects (
            titulo, descricao, potencial_lucro, escalabilidade,
            niche, product_idea, price_aud, responsible_agent, status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Research', 'Ideia Pendente')
        RETURNING id;
        """,
        (t, d, pl, es, t, d, price_aud),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return int(row["id"])

def get_projects_by_status(status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM projects WHERE status = %s", (status,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def update_project_status(project_id, status, file_path=None, sales_link=None):
    conn = get_connection()
    cur = conn.cursor()
    if file_path:
        cur.execute("UPDATE projects SET status = %s, file_path = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (status, file_path, project_id))
    elif sales_link:
        cur.execute("UPDATE projects SET status = %s, sales_link = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (status, sales_link, project_id))
    else:
        cur.execute("UPDATE projects SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s", (status, project_id))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
