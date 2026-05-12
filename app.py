import streamlit as st
from playwright.sync_api import sync_playwright

st.set_page_config(page_title="Cadastro de Filiais", page_icon="🏢")

st.title("🏢 Criar Nova Filial")
st.info("Preencha o nome abaixo para iniciar o processo automático no ERP.")

nome_filial = st.text_input("Nome da Filial", placeholder="Ex: Filial Cuiabá 02")

if st.button("🚀 Iniciar Automação"):
    if not nome_filial:
        st.error("Por favor, digite o nome da filial.")
    else:
        with st.spinner("Acessando ERP e realizando passos..."):
            try:
                with sync_playwright() as p:
                    # Roda em modo headless (obrigatório na nuvem)
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    
                    # --- EXEMPLO DE LOGICA ---
                    # page.goto("URL_DO_SEU_ERP")
                    # page.fill("#usuario", st.secrets["USER"])
                    # page.fill("#senha", st.secrets["PASS"])
                    # page.click("#btn-entrar")
                    
                    # Simulação de tempo para o teste inicial
                    import time
                    time.sleep(3) 
                    
                    browser.close()
                st.success(f"✅ Filial '{nome_filial}' criada com sucesso!")
            except Exception as e:
                st.error(f"Erro na automação: {e}")