from PIL import Image
import os

def verificar_se_e_cinza_da_faixa(pixel):
    """
    Verifica se o pixel é o cinza exato da faixa oficial do ENEM.
    Ignora preto puro (borda de imagem/tabela) e branco puro (fundo).
    """
    if len(pixel) == 4:
        r, g, b, _ = pixel
    else:
        r, g, b = pixel[:3]
        
    # Canais precisam ser equilibrados (característica do cinza)
    if abs(r - g) <= 15 and abs(g - b) <= 15 and abs(r - b) <= 15:
        # PULO DO GATO: As linhas de tabelas/imagens são pretas (< 60).
        # A faixa oficial do ENEM é um cinza médio/claro (entre 100 e 215).
        if 100 < r < 215:  
            return True
    return False

def verificar_se_e_fundo_branco(pixel, limite_branco=240):
    """
    Verifica se o pixel é o fundo branco da folha de prova.
    """
    if len(pixel) == 4:
        r, g, b, _ = pixel
    else:
        r, g, b = pixel[:3]
    return r >= limite_branco and g >= limite_branco and b >= limite_branco

def encontrar_linhas_de_corte(imagem):
    """
    Varre a imagem procurando uma linha cinza contínua e longa horizontalmente.
    Ignora molduras pretas de gráficos e tabelas.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    posicoes_faixas = []
    
    # Região horizontal na metade direita onde passa a faixa ao lado de QUESTÃO XX
    x_inicio = int(largura * 0.55)
    comprimento_barra_teste = 130  # Mantém a exigência do traço longo contra textos
    
    y = 6
    while y < altura:
        pixels_cinzas_na_sequencia = 0
        
        # Varre horizontalmente para testar se é a faixa cinza contínua
        for dx in range(comprimento_barra_teste):
            if x_inicio + dx < largura:
                if verificar_se_e_cinza_da_faixa(pixels[x_inicio + dx, y]):
                    pixels_cinzas_na_sequencia += 1
                else:
                    break
        
        # Se encontrou a barra cinza longa horizontal:
        if pixels_cinzas_na_sequencia >= comprimento_barra_teste:
            
            # VALIDAÇÃO DE SEGURANÇA: Linhas divisórias têm papel branco logo acima delas
            # Borda interna de gráfico/imagem geralmente tem mais desenho ou cor colada acima
            if verificar_se_e_fundo_branco(pixels[x_inicio, y - 6]):
                posicoes_faixas.append(y)
                print(f"🎯 DIVISÓRIA OFICIAL CONFIRMADA em y={y} (Cinza longo de {pixels_cinzas_na_sequencia}px).")
                
                # Salta um bom espaço para não ler a mesma linha grossa
                y += 60  
                continue
            
        y += 1
            
    return posicoes_faixas

def dividir_prova_por_questoes(caminho_imagem, pasta_saida):
    """
    Corta a imagem em blocos perfeitos baseando-se nas faixas cinzas longas validadas
    """
    if not os.path.exists(caminho_imagem):
        print(f"Erro: O arquivo {caminho_imagem} não foi encontrado!")
        return

    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    print(f"Imagem carregada: {largura}x{altura} pixels.")
    
    faixas = encontrar_linhas_de_corte(imagem)
    
    if not faixas:
        print("⚠️ Nenhuma faixa cinza oficial longa foi localizada.")
        return
        
    print(f"Total de questões identificadas: {len(faixas) + 1}")
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Recorte da QUESTÃO 1
    fim_primeira = faixas[0] - 10 if len(faixas) > 0 else altura
    if fim_primeira > 0:
        area_corte = (0, 0, largura, fim_primeira)
        questao_recortada = imagem.crop(area_corte)
        questao_recortada.save(os.path.join(pasta_saida, "questao_001.png"))
        print(f"💾 Salvo: questao_001.png (0 até {fim_primeira}px)")

    # Recorte das demais QUESTÕES
    for i in range(len(faixas)):
        inicio_corte = faixas[i] - 10
        
        if i + 1 < len(faixas):
            fim_corte = faixas[i+1] - 10
        else:
            fim_corte = altura
            
        if fim_corte <= inicio_corte:
            continue
            
        area_corte = (0, inicio_corte, largura, fim_corte)
        questao_recortada = imagem.crop(area_corte)
        
        nome_arquivo = f"questao_{i+2:03d}.png"
        questao_recortada.save(os.path.join(pasta_saida, nome_arquivo))
        print(f"💾 Salvo: {nome_arquivo} ({inicio_corte} até {fim_corte}px)")

if __name__ == "__main__":
    IMAGEM_ENTRADA = "colunas_concatenadas_verticalmente.png" 
    PASTA_DESTINO = "questoes_recortadas_ppl_2018"
    
    print("Iniciando fatiador com isolamento de cinza oficial...")
    dividir_prova_por_questoes(IMAGEM_ENTRADA, PASTA_DESTINO)
    print("Processo finalizado!")