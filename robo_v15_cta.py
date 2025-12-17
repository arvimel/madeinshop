from PIL import Image, ImageDraw, ImageFont
import os

# --- CONFIGURAÇÕES DO ROBÔ V15 ---
NOME_ARQUIVO_FINAL = "slide_final_seguir.png"
ARQUIVO_LOGO = "logo.jpeg"  # Sua logo deve estar na mesma pasta

# Cores da Marca (Made In Shop)
COR_FUNDO = "#0d1117"     # Preto Profundo (igual do site)
COR_LARANJA = "#ee4d2d"   # Laranja Oficial Shopee
COR_BRANCO = "#ffffff"
COR_AMARELO = "#fcee21"   # Amarelo para destaque

def criar_slide_cta():
    print("🤖 Robô V15 (CTA) Iniciado...")

    # 1. Cria o Fundo Vertical (1080x1920 - Padrão TikTok/Shopee)
    largura = 1080
    altura = 1920
    img = Image.new('RGB', (largura, altura), color=COR_FUNDO)
    draw = ImageDraw.Draw(img)

    # 2. Processa a Logo (Arredonda e coloca borda)
    if os.path.exists(ARQUIVO_LOGO):
        try:
            # Abre e prepara a logo
            logo = Image.open(ARQUIVO_LOGO).convert("RGBA")
            
            # Redimensiona para ficar num tamanho bom no topo
            tamanho_logo = 350
            logo = logo.resize((tamanho_logo, tamanho_logo), Image.Resampling.LANCZOS)
            
            # Cria a máscara redonda
            mascara = Image.new('L', (tamanho_logo, tamanho_logo), 0)
            draw_mascara = ImageDraw.Draw(mascara)
            draw_mascara.ellipse((0, 0, tamanho_logo, tamanho_logo), fill=255)
            
            # Calcula posição (Centralizado no topo)
            pos_x_logo = (largura - tamanho_logo) // 2
            pos_y_logo = 150 # Margem do topo
            
            # Cola a logo
            img.paste(logo, (pos_x_logo, pos_y_logo), mascara)

            # Desenha um aro Laranja em volta da logo para destacar
            draw.ellipse((pos_x_logo-5, pos_y_logo-5, pos_x_logo + tamanho_logo+5, pos_y_logo + tamanho_logo+5), outline=COR_LARANJA, width=8)
            
        except Exception as e:
            print(f"⚠️ Erro na logo: {e}")
    else:
        print("⚠️ Logo não encontrada. Pulando etapa.")

    # 3. Configuração de Fontes (Sistema de segurança para não dar erro)
    def carregar_fonte(tamanho, bold=False):
        try:
            # Tenta fontes comuns do Windows/Linux
            if bold:
                return ImageFont.truetype("arialbd.ttf", tamanho)
            else:
                return ImageFont.truetype("arial.ttf", tamanho)
        except:
            # Se falhar, tenta caminho Linux (comum em servidores)
            try:
                caminho = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
                return ImageFont.truetype(caminho, tamanho)
            except:
                return ImageFont.load_default()

    fonte_titulo = carregar_fonte(90, bold=True)
    fonte_destaque = carregar_fonte(110, bold=True)
    fonte_texto = carregar_fonte(70, bold=False)
    fonte_botao = carregar_fonte(90, bold=True)

    # 4. Escreve os Textos (Centralizados)
    def escrever_centralizado(texto, y, fonte, cor):
        bbox = draw.textbbox((0, 0), texto, font=fonte)
        largura_txt = bbox[2] - bbox[0]
        x = (largura - largura_txt) // 2
        draw.text((x, y), texto, font=fonte, fill=cor)
        return bbox[3] - bbox[1] # Retorna altura da linha

    # Bloco de Texto Superior
    y_atual = 600
    y_atual += escrever_centralizado("NÃO PERCA A", y_atual, fonte_titulo, COR_BRANCO) + 20
    y_atual += escrever_centralizado("PRÓXIMA OFERTA!", y_atual, fonte_destaque, COR_LARANJA) + 150

    # Texto Explicativo
    y_atual += escrever_centralizado("Minha IA rastreia erros", y_atual, fonte_texto, COR_BRANCO) + 20
    y_atual += escrever_centralizado("de preço 24h por dia.", y_atual, fonte_texto, COR_BRANCO) + 150

    # Simulação de Botão "Seguir"
    largura_botao = 800
    altura_botao = 200
    x_botao = (largura - largura_botao) // 2
    
    # Desenha o retângulo do botão
    draw.rectangle(
        [x_botao, y_atual, x_botao + largura_botao, y_atual + altura_botao],
        fill=COR_LARANJA,
        outline="white",
        width=5
    )
    
    # Texto dentro do botão
    bbox_btn = draw.textbbox((0, 0), "CLIQUE EM SEGUIR +", font=fonte_botao)
    largura_txt_btn = bbox_btn[2] - bbox_btn[0]
    altura_txt_btn = bbox_btn[3] - bbox_btn[1]
    
    x_txt_btn = x_botao + (largura_botao - largura_txt_btn) // 2
    y_txt_btn = y_atual + (altura_botao - altura_txt_btn) // 2 - 15 # Ajuste fino vertical
    
    draw.text((x_txt_btn, y_txt_btn), "CLIQUE EM SEGUIR +", font=fonte_botao, fill="white")
    
    y_atual += altura_botao + 80

    # Chamada Final
    escrever_centralizado("Para receber o alerta 🔔", y_atual, fonte_texto, COR_AMARELO)

    # 5. Salva a imagem
    img.save(NOME_ARQUIVO_FINAL)
    print(f"✅ SUCESSO! Imagem criada: {NOME_ARQUIVO_FINAL}")

# Executa o Robô
if __name__ == "__main__":
    criar_slide_cta()