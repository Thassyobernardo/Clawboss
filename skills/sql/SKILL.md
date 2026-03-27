---
name: sql
description: Persistir oportunidades no PostgreSQL (tabela projects) para o Dashboard — aba Ideias.
---

# SQL / Postgres — Ideias (Claw Factory)

## Tabela obrigatória

- **Tabela:** `projects`
- **O Dashboard (Streamlit, aba "Ideias")** lista linhas com `status = 'Ideia Pendente'`.

## Colunas que você DEVE preencher ao achar uma oportunidade

| Coluna | Significado |
|--------|-------------|
| `titulo` | Título curto da oportunidade |
| `descricao` | Descrição / contexto |
| `potencial_lucro` | Como isso pode gerar receita (texto) |
| `escalabilidade` | Como escalar a oferta (texto) |

O `INSERT` também deve manter `status = 'Ideia Pendente'` (ou use o helper abaixo).

## Como executar (recomendado via `exec`)

No workspace do projeto (`/app` no Railway):

```bash
python3 ideas_db.py save '{"titulo":"...","descricao":"...","potencial_lucro":"...","escalabilidade":"..."}'
```

Isso executa o `INSERT` na tabela `projects` com `responsible_agent = 'Research'` e preço AUD padrão.

## SQL direto (alternativa)

Se usar `psql` ou cliente SQL, o equivalente é:

```sql
INSERT INTO projects (titulo, descricao, potencial_lucro, escalabilidade, niche, product_idea, price_aud, responsible_agent, status)
VALUES ($1, $2, $3, $4, $1, $2, 35.0, 'Research', 'Ideia Pendente');
```

(`niche` e `product_idea` espelham título/descrição para compatibilidade com telas antigas.)

## Proibido

- Não salvar oportunidades em arquivos `.md` no lugar do banco.
