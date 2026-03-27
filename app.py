import streamlit as st
import db
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Claw Factory ERP", layout="wide")

st.title("🦾 Claw Agency - Digital Product Factory")
st.markdown("### Bem-vindo, CEO. A sua equipe de elite está operando.")

# Sidebar - HR Status
st.sidebar.header("📋 Status da Equipe (RH)")
agents = db.get_all_agent_status()
for agent in agents:
    color = "green" if agent['current_status'] == "Idle" else "orange"
    st.sidebar.markdown(f"**{agent['agent_name']}**: :{color}[{agent['current_status']}]")
    st.sidebar.caption(f"Última atividade: {agent['last_activity']}")

# Main Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💡 Ideias (Pesquisador)", "📦 Produtos (Designer)", "📊 Vendas (Vendedor)", "🏥 Sistema (Manager)"])

with tab1:
    st.header("Ideias Pendentes de Aprovação")
    pending = db.get_projects_by_status("Ideia Pendente")
    if pending:
        for p in pending:
            title = (p.get("titulo") or p.get("niche") or "").strip() or "—"
            body = (p.get("descricao") or p.get("product_idea") or "").strip() or "—"
            label = f"{title} — {body[:80]}{'…' if len(body) > 80 else ''}"
            with st.expander(label):
                st.subheader(title)
                st.markdown("**Descrição**")
                st.write(body)
                if p.get("potencial_lucro"):
                    st.markdown("**Potencial de lucro**")
                    st.write(p["potencial_lucro"])
                if p.get("escalabilidade"):
                    st.markdown("**Escalabilidade**")
                    st.write(p["escalabilidade"])
                st.caption(f"Preço sugerido (legado): AUD {p['price_aud']}")
                if st.button(f"Aprovar Ideia #{p['id']}", key=f"app_{p['id']}"):
                    db.update_project_status(p['id'], "Construindo")
                    st.success(f"Ideia #{p['id']} aprovada! O Designer foi notificado.")
                    st.rerun()
    else:
        st.info("Nenhuma ideia nova no momento. O Pesquisador está trabalhando.")

with tab2:
    st.header("Produtos Prontos & Revisão")
    ready = db.get_projects_by_status("Aguardando Link")
    if ready:
        for r in ready:
            with st.container(border=True):
                st.subheader(f"Produto: {r['product_idea']}")
                st.write(f"Arquivo: `{r['file_path']}`")
                sales_link = st.text_input("Cole o Link de Venda (Stripe/Gumroad)", key=f"link_{r['id']}")
                if st.button(f"Publicar para Vendas #{r['id']}", key=f"pub_{r['id']}"):
                    if sales_link:
                        db.update_project_status(r['id'], "Vendendo", sales_link=sales_link)
                        st.success("Link atualizado! O Vendedor social iniciará a prospecção.")
                        st.rerun()
                    else:
                        st.error("Por favor, insira o link de venda antes de publicar.")
    else:
        st.info("Aguardando finalização do Designer.")

with tab3:
    st.header("Vendas e Tráfego Social")
    selling = db.get_projects_by_status("Vendendo")
    if selling:
        df = pd.DataFrame(selling)
        st.table(df[['niche', 'product_idea', 'sales_link', 'status']])
        st.caption("Logs de interação em tempo real: [Reddit/Twitter em andamento]")
    else:
        st.info("Nenhum produto em fase de venda ativa.")

with tab4:
    st.header("Monitoramento do Sistema")
    if st.button("Rodar Diagnóstico Completo"):
        from skills.manager.manager import run_diagnostic
        report = run_diagnostic()
        st.code(report)
