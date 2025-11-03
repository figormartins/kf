#!/usr/bin/env python3
"""
Script para criar uma conta no KnightFight usando Playwright
"""
from playwright.sync_api import sync_playwright
import random
import string
import time
import os
from pathlib import Path

def criar_pasta_screenshots():
    """Cria pasta para armazenar screenshots e arquivos"""
    pasta = Path('/home/igor/Documentos/kf/bot_screenshots')
    pasta.mkdir(exist_ok=True)
    return pasta

def gerar_nome_aleatorio():
    """Gera um nome aleatório único e concatenado para o personagem"""
    primeiros_nomes = [
        'Arthur', 'Lancelot', 'Percival', 'Galahad', 'Gawain',
        'Tristan', 'Bedivere', 'Kay', 'Gareth', 'Mordred',
        'Roland', 'Oliver', 'Baldwin', 'Godfrey', 'Richard',
        'William', 'Edward', 'Henry', 'Geoffrey', 'Robert',
        'Thor', 'Odin', 'Bjorn', 'Ragnar', 'Erik',
        'Sigurd', 'Harald', 'Magnus', 'Leif', 'Sven'
    ]
    
    sobrenomes = [
        'Pendragon', 'Lionheart', 'Ironside', 'Blackwood', 'Stormborn',
        'Dragonslayer', 'Nightblade', 'Thunderfist', 'Shadowcaster', 'Flameheart',
        'Frostbeard', 'Steelhammer', 'Wolfbane', 'Ravenwind', 'Goldenshield',
        'Darkheart', 'Swiftblade', 'Strongarm', 'Firebrand', 'Icevein',
        'Stonemace', 'Bloodaxe', 'Windwalker', 'Earthshaker', 'Stormbringer'
    ]
    
    primeiro = random.choice(primeiros_nomes)
    sobrenome = random.choice(sobrenomes)
    
    # Decide aleatoriamente se usa timestamp ou número aleatório
    usar_timestamp = random.choice([True, False])
    
    if usar_timestamp:
        # Usa os últimos 4-6 dígitos do timestamp
        timestamp = str(int(time.time()))
        sufixo = timestamp[-random.randint(4, 6):]
        nome_completo = f"{primeiro}{sobrenome}{sufixo}"
    else:
        # Usa um número aleatório de 3 a 5 dígitos
        numero = random.randint(100, 99999)
        nome_completo = f"{primeiro}{sobrenome}{numero}"
    
    return nome_completo

def gerar_credenciais():
    """Gera credenciais aleatórias para a conta"""
    timestamp = int(time.time())
    username = f"user_{timestamp}"
    email = f"{username}@example.com"
    # Gera uma senha forte que não foi vazada
    random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    password = f"KnightFight2025!{random_part}"
    return username, email, password

def criar_conta():
    """Cria uma nova conta no KnightFight"""
    username, email, password = gerar_credenciais()
    timestamp = int(time.time())
    
    # Cria pasta para screenshots
    pasta_screenshots = criar_pasta_screenshots()
    
    print(f"Criando conta com as seguintes credenciais:")
    print(f"Email: {email}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print("-" * 50)
    
    with sync_playwright() as p:
        # Inicia o navegador (headless=False para ver o que está acontecendo)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navega até a página inicial
        print("Navegando para o site...")
        page.goto('https://int7.knightfight.moonid.net/raubzug/')
        
        # Clica no botão de registro
        print("Clicando no botão de registro...")
        page.get_by_role('link', name='Register and Play!').click()
        
        # Aguarda a página de registro carregar
        page.wait_for_load_state('networkidle')
        
        # Preenche o formulário
        print("Preenchendo o formulário...")
        
        # Email
        page.get_by_role('textbox', name='Endereço de e-mail:').fill(email)
        
        # Username - usa a linha específica dentro da tabela
        page.get_by_role('row', name='Nome de utilizador:').locator('#id_username').fill(username)
        
        # Senha - usa exact=True para pegar apenas o campo de senha
        page.get_by_role('textbox', name='Senha:', exact=True).fill(password)
        
        # Confirmar senha
        page.get_by_role('textbox', name='Confirmar senha:').fill(password)
        
        # Aceitar termos e condições
        page.get_by_role('checkbox', name='Aceitar termos e condições:').check()
        
        # Clica no botão de registro
        print("Submetendo o formulário...")
        page.get_by_role('button', name='Registar agora').click()
        
        # Aguarda a navegação ou mensagem de sucesso/erro
        print("Aguardando resposta...")
        try:
            # Aguarda até 10 segundos pela navegação
            page.wait_for_load_state('networkidle', timeout=10000)
        except Exception as e:
            print(f"Aviso: {e}")
        
        # Aguarda um pouco mais para garantir que a página carregou
        page.wait_for_timeout(3000)
        
        # Captura a URL final para verificar se teve sucesso
        final_url = page.url
        print(f"\nURL final: {final_url}")
        
        # Verifica se foi redirecionado para a página principal (sucesso)
        if 'main' in final_url or 'game' in final_url or 'raubzug' in final_url:
            print("\n✅ Conta criada com sucesso!")
            print("Continuando com o processo de escolha de nome...")
            
            # Gera um nome aleatório
            nome_personagem = gerar_nome_aleatorio()
            print(f"Nome escolhido: {nome_personagem}")
            
            # Aguarda a página carregar completamente
            page.wait_for_timeout(2000)
            
            # Tira um screenshot da página atual
            screenshot_path = pasta_screenshots / f'antes_nome_{timestamp}.png'
            page.screenshot(path=str(screenshot_path))
            print(f"Screenshot (antes do nome) salvo em: {screenshot_path}")
            
            # Procura por campo de input para o nome
            print("Procurando campo de nome...")
            try:
                # Tenta encontrar campo de texto para nome
                # Vamos esperar um pouco e fazer um snapshot para ver o que tem na página
                page.wait_for_timeout(2000)
                
                # Procura por campos de input de texto visíveis
                inputs = page.locator('input[type="text"]').all()
                print(f"Encontrados {len(inputs)} campos de texto")
                
                if len(inputs) > 0:
                    # Preenche o primeiro campo de texto com o nome
                    inputs[0].fill(nome_personagem)
                    print(f"Nome '{nome_personagem}' inserido no campo")
                    
                    # Procura por botão de submit/confirmar
                    page.wait_for_timeout(1000)
                    
                    # Tenta encontrar e clicar em botão de confirmação
                    botoes = page.locator('button, input[type="submit"]').all()
                    if len(botoes) > 0:
                        print("Clicando no botão de confirmação...")
                        botoes[0].click()
                        page.wait_for_timeout(3000)
                        
                        print("✅ Nome registrado!")
                    else:
                        print("⚠️ Nenhum botão de confirmação encontrado")
                else:
                    print("⚠️ Nenhum campo de texto encontrado na página")
                    
            except Exception as e:
                print(f"⚠️ Erro ao tentar preencher o nome: {e}")
            
            # Após registrar o nome, vai até o link do oponente para atacar
            print("\n" + "=" * 50)
            print("Indo para a página do oponente...")
            try:
                page.goto('https://int7.knightfight.moonid.net/raubzug/gegner/?searchuserid=522000820', timeout=30000)
                page.wait_for_load_state('networkidle', timeout=10000)
                page.wait_for_timeout(2000)
                
                # Tira screenshot da página do oponente
                screenshot_path = pasta_screenshots / f'oponente_{timestamp}.png'
                page.screenshot(path=str(screenshot_path))
                print(f"Screenshot da página do oponente salvo em: {screenshot_path}")
                
                # Salva o HTML da página para análise
                html_path = pasta_screenshots / f'oponente_{timestamp}.html'
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(page.content())
                print(f"HTML da página salvo em: {html_path}")
                
                # Procura por botão de ataque
                print("Procurando botão de ataque...")
                page.wait_for_timeout(2000)
                
                # Procura por imagens, botões ou links que parecem ser de ataque
                ataque_realizado = False
                
                # Primeiro, procura por imagens clicáveis (geralmente ícones de espada/ataque)
                print("Procurando por imagens clicáveis de ataque...")
                imagens = page.locator('img[onclick], a img').all()
                print(f"Encontradas {len(imagens)} imagens")
                
                for img in imagens:
                    try:
                        src = img.get_attribute('src') or ''
                        alt = img.get_attribute('alt') or ''
                        onclick = img.get_attribute('onclick') or ''
                        
                        # Procura por imagens que contenham palavras relacionadas a ataque
                        if any(palavra in src.lower() for palavra in ['attack', 'sword', 'fight', 'angriff', 'kampf']) or \
                           any(palavra in alt.lower() for palavra in ['attack', 'atac', 'angriff']) or \
                           any(palavra in onclick.lower() for palavra in ['attack', 'angriff']):
                            print(f"Encontrada imagem de ataque: src={src}, alt={alt}")
                            
                            # Se a imagem tem onclick, clica nela
                            if onclick:
                                img.click()
                                page.wait_for_timeout(3000)
                                ataque_realizado = True
                                break
                            # Se não, tenta clicar no link pai
                            else:
                                parent = img.locator('xpath=..').first
                                if parent:
                                    parent.click()
                                    page.wait_for_timeout(3000)
                                    ataque_realizado = True
                                    break
                    except Exception as e:
                        print(f"Erro ao tentar clicar na imagem: {e}")
                        continue
                
                # Se não encontrou imagem, procura por links específicos
                if not ataque_realizado:
                    print("Procurando por links específicos de ataque...")
                    links_normais = page.locator('a[href]').all()
                    print(f"Encontrados {len(links_normais)} links")
                    
                    for link in links_normais:
                        try:
                            href = link.get_attribute('href') or ''
                            texto = link.inner_text() if link.is_visible() else ""
                            
                            # Procura especificamente por links que levam a ataques (não a página geral de missões)
                            # O link deve conter parâmetros ou IDs específicos de ataque
                            if ('attack' in href.lower() or 'angriff' in href.lower()) and \
                               ('?' in href or '&' in href):  # Deve ter parâmetros
                                print(f"Encontrado link específico de ataque: {href} | Texto: {texto}")
                                if link.is_visible():
                                    link.click()
                                    page.wait_for_timeout(3000)
                                    ataque_realizado = True
                                    break
                        except:
                            continue
                
                # Se ainda não encontrou, procura por botões visíveis com texto de ataque
                if not ataque_realizado:
                    print("Procurando por botões com texto de ataque...")
                    botoes_visiveis = page.locator('button:visible, input[type="submit"]:visible, a:visible').all()
                    print(f"Encontrados {len(botoes_visiveis)} elementos visíveis")
                    
                    for btn in botoes_visiveis:
                        try:
                            texto = btn.inner_text().lower()
                            
                            # Verifica se contém palavras específicas de ataque (não "missão")
                            if any(palavra in texto for palavra in ['atac', 'attack', 'angriff', 'fight', 'raid']) and \
                               'miss' not in texto:  # Exclui "missão"
                                print(f"Tentando clicar em botão com texto: {texto}")
                                btn.click()
                                page.wait_for_timeout(3000)
                                ataque_realizado = True
                                break
                        except:
                            continue
                
                if not ataque_realizado:
                    print("⚠️ Nenhum botão de ataque encontrado ou todos estavam invisíveis")
                else:
                    # Tira screenshot após o ataque
                    screenshot_path = pasta_screenshots / f'pos_ataque_{timestamp}.png'
                    page.screenshot(path=str(screenshot_path))
                    print(f"Screenshot após ataque salvo em: {screenshot_path}")
                    print("✅ Ataque realizado!")
                    
            except Exception as e:
                print(f"⚠️ Erro ao tentar acessar página do oponente ou atacar: {e}")
        
        # Tira um screenshot do resultado final
        screenshot_path = pasta_screenshots / f'registro_final_{timestamp}.png'
        page.screenshot(path=str(screenshot_path))
        print(f"Screenshot final salvo em: {screenshot_path}")
        
        # Mantém o navegador aberto por 10 segundos para ver o resultado
        page.wait_for_timeout(10000)
        
        browser.close()
        
    print("\n" + "=" * 50)
    print("Processo concluído!")
    print(f"Email: {email}")
    print(f"Username: {username}")
    print(f"Password: {password}")
    if 'main' in final_url or 'game' in final_url or 'raubzug' in final_url:
        print(f"Nome do Personagem: {nome_personagem}")
    print("=" * 50)

if __name__ == "__main__":
    criar_conta()
