import streamlit as st
from playwright.sync_api import sync_playwright
import os
import subprocess

# Configuração da página
st.set_page_config(page_title="Automação ERP - Filiais", page_icon="🏢")

# Função para instalar o navegador no servidor do Streamlit
@st.cache_resource
def install_playwright():
    subprocess.run(["playwright", "install", "chromium"])

# Executa a instalação silenciosamente
install_playwright()

st.title("🏢 Gestor de Filiais (ERP)")
st.markdown("Preencha os dados abaixo para automatizar a criação da filial no sistema.")

# --- INTERFACE DO USUÁRIO ---
with st.form("form_filial"):
    nome_filial = st.text_input("Nome da Filial", placeholder="Ex: Matriz Cuiabá")
    arquivo_upload = st.file_uploader("Upload de Documento/Logo (Opcional)", type=['pdf', 'png', 'jpg'])
    
    submit = st.form_submit_button("🚀 Iniciar Processo")

if submit:
    if not nome_filial:
        st.error("⚠️ O nome da filial é obrigatório.")
    else:
        status = st.empty()
        progresso = st.progress(0)
        
        try:
            with sync_playwright() as p:
                status.info("Iniciando navegador...")
                progresso.progress(20)
                
                # Lança o navegador em modo headless (sem interface visual)
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # --- PASSO A PASSO DA AUTOMAÇÃO ---
                status.info("Acessando o ERP...")
                # Use st.secrets para não deixar senhas no código
                # page.goto("https://seu-erp.com.br/login")
                # page.fill("#usuario", st.secrets["ERP_USER"])
                # page.fill("#senha", st.secrets["ERP_PASS"])
                # page.click("#btn-login")
                progresso.progress(40)
                
                status.info(f"Criando filial: {nome_filial}")
                # Exemplo de preenchimento:
                # page.click("#menu-filiais")
                # page.fill("input[name='nome']", nome_filial)
                progresso.progress(70)

                # Lógica de Upload se o usuário enviou arquivo
                if arquivo_upload:
                    status.info("Fazendo upload do arquivo...")
                    # Salva temporariamente para o Playwright ler
                    temp_path = os.path.join("/tmp", arquivo_upload.name)
                    with open(temp_path, "wb") as f:
                        f.write(arquivo_upload.getbuffer())
                    
                    # page.set_input_files("input[type='file']", temp_path)
                
                # Finalizar
                # page.click("#btn-salvar")
                progresso.progress(100)
                
                browser.close()
                st.success(f"✅ Filial '{nome_filial}' criada com sucesso!")
                st.balloons()

        except Exception as e:
            st.error(f"❌ Ocorreu um erro: {e}")