# Linkedinrobo que adiciona pessoas com profissões desejadas ao seu linkedin
#
# ajuda para crescer sua rede social, porem o linkedin restringe a quantidade pessoas adicionadas por semana
#
# Copyright (c) Ricardo A. , 2025-2030
#
# Authors:
#  Ricardo <itanhaem@live.com>
#
# Com o tempo o codigo HTML do linkedin será mudado e esse script não irá funcionar mais..
#


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import time


def apresentacao():
    print("\n\n\n")
    print("------------------------------------------------------------------")
    print("------------ROBÔ DE ADIÇÃO DE PESSOAS NO LINKEDIN-----------------")
    print("-------conecte pessoas com profissões que lhe interessam----------")
    print("------------------------------------------------------------------")
    time.sleep(4)


# --- CONFIGURAÇÕES DO USUÁRIO ---
LINKEDIN_EMAIL = ""     # <-- SUBSTITUA SEU EMAIL
LINKEDIN_SENHA = ""     # <-- SUBSTITUA SUA SENHA
PAUSA_ENTRE_CLIQUES = 1 # 1 segundo entre as conexões.
PAUSA_APOS_PROXIMA = 3  # 3 segundos após clicar em "Próxima".

apresentacao()

# Pega as credernciais do linkedin caso elas estejam vazias
if(LINKEDIN_EMAIL==""):
    LINKEDIN_EMAIL = input("informe seu e-mail do linkedin: ")
if(LINKEDIN_SENHA==""): 
    LINKEDIN_SENHA = input("informe a sua senha do linkedin: ")


# Pega do usuário o cargo das pessoas que ele quer adicionar
TERMO_PESQUISA = input("Adicionar pessoas com qual cargo: ")
if(TERMO_PESQUISA == ""):
   TERMO_PESQUISA = "cybersecurity diretor"


# --- SELETORES DO LINKEDIN (Ajustados para o requisito) ---
LINK_VER_PESSOAS_SELECTOR = "//a[contains(., 'Ver todos os resultados de pessoas')]"
BOTOES_CONECTAR_SELECTOR = "//button[contains(., 'Conectar') and not(contains(., 'Mensagem'))]"

# Seletor para o botão "Próxima". O LinkedIn usa um botão que contém um span ou o texto "Próxima".
# Este seletor busca um elemento clicável (botão) que contenha o texto "Próxima" em qualquer lugar.
BOTAO_PROXIMA_SELECTOR = "//button[.//span[text()='Próxima']]" 


def fazer_conexao_na_pagina(driver):
    """Encontra e clica em todos os botões 'Conectar' na página atual."""
    
    # Rola a página para baixo para garantir que todos os botões de conexão sejam carregados
    # Rolar lentamente pode ajudar a carregar mais resultados dinamicamente
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2) 

    botoes_conectar = driver.find_elements(By.XPATH, BOTOES_CONECTAR_SELECTOR)
    
    if not botoes_conectar:
        print("Nenhum botão 'Conectar' encontrado nesta página.")
        return 0
    
    print(f"Total de botões 'Conectar' encontrados: {len(botoes_conectar)}")
    
    contador_cliques = 0
    for i, botao in enumerate(botoes_conectar, 1):
        try:
            # Rola até o botão
            driver.execute_script("arguments[0].scrollIntoView(true);", botao)
            
            # Clica no botão. Usamos um try/except para capturar pop-ups (como 'Adicionar nota')
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable(botao)).click()
            
            print(f"Conexão {i} enviada. Esperando {PAUSA_ENTRE_CLIQUES}s.")
            
            # Pausa
            time.sleep(PAUSA_ENTRE_CLIQUES)
            contador_cliques += 1
            
        except ElementClickInterceptedException:
            # Isso acontece se um pop-up, como 'Adicionar nota', interceptar o clique.
            print(f"AVISO: Pop-up interceptou o clique no Conectar {i}. Tentando fechar o pop-up (se houver).")
            # Tenta fechar um modal de "Adicionar nota" genérico que pode aparecer
            try:
                fechar_modal = driver.find_element(By.XPATH, "//button[@aria-label='Fechar']")
                fechar_modal.click()
                print("Modal fechado.")
            except:
                pass # Se não encontrar o botão fechar, ignora e segue
            
        except Exception as e:
            print(f"Falha ao clicar no botão 'Conectar' número {i}. Erro: {e}. Tentando o próximo.")
            
    return contador_cliques


# ====================================== O MAIN COMEÇA AQUI ==============================================
try:
    # 1. Configura e inicia o ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    print("Navegador Chrome iniciado.")

    driver.get("https://www.linkedin.com/login")

    wait = WebDriverWait(driver, 10)

    # --- LOGIN ---
    print("Iniciando o login...")
    email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    email_field.send_keys(LINKEDIN_EMAIL)
    password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    password_field.send_keys(LINKEDIN_SENHA)
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()
    
    # Espera a página principal carregar
    search_input_selector = "//input[@placeholder='Pesquisar' or @aria-label='Pesquisar']"
    search_field = wait.until(EC.presence_of_element_located((By.XPATH, search_input_selector)))
    print("Login bem-sucedido.")

    # --- PESQUISA E FILTRO ---
    print(f"Realizando a pesquisa por: '{TERMO_PESQUISA}'")
    search_field.send_keys(TERMO_PESQUISA)
    search_field.send_keys(webdriver.common.keys.Keys.RETURN)
    
    print("Aguardando 3 segundos para carregar a pré-visualização dos resultados...")
    time.sleep(3) 

    # Clica em "Ver todos os resultados de pessoas"
    try:
        ver_pessoas_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, LINK_VER_PESSOAS_SELECTOR))
        )
        ver_pessoas_link.click()
        print("Filtro 'Pessoas' aplicado.")
        wait.until(EC.url_contains("/people"))
        
    except (NoSuchElementException, TimeoutException):
        print("AVISO: Não foi possível encontrar o filtro 'Ver todos os resultados de pessoas'. Tentando prosseguir.")
    
    # Pausa de 6 segundos antes da primeira rodada de cliques
    print("Aguardando 6 segundos antes de iniciar os cliques da primeira página...")
    time.sleep(6) 
    
    # --- LOOP PRINCIPAL DE NAVEGAÇÃO ---
    pagina = 1
    while True:
        print(f"\n--- Processando Página {pagina} ---")
        
        # 1. Faz as conexões na página atual
        fazer_conexao_na_pagina(driver)

        # 2. Verifica e clica no botão "Próxima"
        try:
            # Rola para o final da página
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Encontra o botão "Próxima"
            proxima_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, BOTAO_PROXIMA_SELECTOR))
            )
            
            # Clica no botão "Próxima"
            proxima_button.click()
            print(f"Botão 'Próxima' encontrado e clicado. Esperando {PAUSA_APOS_PROXIMA} segundos para carregar a próxima página...")
            time.sleep(PAUSA_APOS_PROXIMA) 
            pagina += 1
            
        except (NoSuchElementException, TimeoutException):
            print("\nO botão 'Próxima' não foi encontrado ou não está mais ativo.")
            print("Fim da navegação e do script.")
            break # Sai do loop while True

    print("Script concluído. Todas as páginas foram processadas.")

except Exception as e:
    print(f"\nOcorreu um erro fatal: {e}")

finally:
    # Fecha o navegador após uma breve espera
    print("Fechando o navegador em 5 segundos...")
    time.sleep(5)
    driver.quit()