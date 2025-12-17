from PIL import Image, ImageDraw, ImageFont
import os

# --- CONFIGURAÇÕES DO ROBÔ V16 (AJUSTADO) ---
NOME_ARQUIVO_FINAL = "slide_final_seguir_v2.png"
ARQUIVO_LOGO = "logo.jpeg"

# Cores
COR_FUNDO = "#0d1117"     
COR_LARANJA = "#ee4d2d"   
COR_BRANCO = "#ffffff"
COR_AMARELO = "#fcee21"   

def criar_slide_cta():
    print("🤖 Robô V16 (Ajustado) Iniciado...")

    largura = 1080
    altura = 1920
    img = Image.new('RGB', (largura, altura), color=COR_FUNDO)
    draw = ImageDraw.Draw(img)

    # --- LOGO ---
    if os.path.exists(ARQUIVO_LOGO):
        try:
            logo = Image.open(ARQUIVO_LOGO).convert("RGBA")
            tamanho_logo = 300 # Diminui um pouco a logo
            logo = logo.resize((tamanho_logo, tamanho_logo), Image.Resampling.LANCZOS)
            
            mascara = Image.new('L', (tamanho_logo, tamanho_logo), 0)
            draw_mascara = ImageDraw.Draw(mascara)
            draw_mascara.ellipse((0, 0, tamanho_logo, tamanho_logo), fill=255)
            
            pos_x_logo = (largura - tamanho_logo) // 2
            pos_y_logo = 150 
            img.paste(logo, (pos_x_logo, pos_y_logo), mascara)
            draw.ellipse((pos_x_logo-5, pos_y_logo-5, pos_x_logo + tamanho_logo+5, pos_y_logo + tamanho_logo+5), outline=COR_LARANJA, width=6)
        except: pass

    # --- FONTES (Tamanhos Reduzidos) ---
    def carregar_fonte(tamanho, bold=False):
        try:
            # Tenta caminho Linux (Codespaces)
            caminho = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            return ImageFont.truetype(caminho, tamanho)
        except:
            # Se falhar, tenta genérico ou padrão
            try:
                return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", tamanho)
            except:
                 return ImageFont.load_default()

    # FONTES MENORES AQUI:
    fonte_titulo = carregar_fonte(70, bold=True)     # Era 90
    fonte_destaque = carregar_fonte(95, bold=True)    # Era 110
    fonte_texto = carregar_fonte(55, bold=False)     # Era 70
    fonte_botao = carregar_fonte(75, bold=True)      # Era 90
    # Tenta uma fonte específica para o emoji final
    fonte_emoji = carregar_fonte(55, bold=False)

    def escrever_centralizado(texto, y, fonte, cor):
        bbox = draw.textbbox((0, 0), texto, font=fonte)
        largura_txt = bbox[2] - bbox[0]
        x = (largura - largura_txt) // 2
        draw.text((x, y), texto, font=fonte, fill=cor)
        return bbox[3] - bbox[1]

    # --- TEXTOS ---
    y_atual = 550 # Subi um pouco
    y_atual += escrever_centralizado("NÃO PERCA A", y_atual, fonte_titulo, COR_BRANCO) + 15
    y_atual += escrever_centralizado("PRÓXIMA OFERTA!", y_atual, fonte_destaque, COR_LARANJA) + 120

    y_atual += escrever_centralizado("Minha IA rastreia erros", y_atual, fonte_texto, COR_BRANCO) + 15
    y_atual += escrever_centralizado("de preço 24h por dia.", y_atual, fonte_texto, COR_BRANCO) + 120

    # --- BOTÃO (Mais estreito) ---
    largura_botao = 700 # Era 800
    altura_botao = 180  # Era 200
    x_botao = (largura - largura_botao) // 2
    
    draw.rectangle([x_botao, y_atual, x_botao + largura_botao, y_atual + altura_botao], fill=COR_LARANJA, outline="white", width=4)
    
    bbox_btn = draw.textbbox((0, 0), "CLIQUE EM SEGUIR +", font=fonte_botao)
    x_txt_btn = x_botao + (largura_botao - (bbox_btn[2] - bbox_btn[0])) // 2
    y_txt_btn = y_atual + (altura_botao - (bbox_btn[3] - bbox_btn[1])) // 2 - 10
    
    draw.text((x_txt_btn, y_txt_btn), "CLIQUE EM SEGUIR +", font=fonte_botao, fill="white")
    
    y_atual += altura_botao + 60
    # Tentei usar a fonte normal para o sino, se falhar fica sem.
    try:
        escrever_centralizado("Para receber o alerta 🔔", y_atual, fonte_emoji, COR_AMARELO)
    except:
        escrever_centralizado("Para receber o alerta", y_atual, fonte_texto, COR_AMARELO)

    img.save(NOME_ARQUIVO_FINAL)
    print(f"✅ SUCESSO! Imagem ajustada criada: {NOME_ARQUIVO_FINAL}")

if __name__ == "__main__":
    criar_slide_cta()