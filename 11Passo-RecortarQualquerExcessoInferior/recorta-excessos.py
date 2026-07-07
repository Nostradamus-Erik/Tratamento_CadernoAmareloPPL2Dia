from PIL import Image
import os
import shutil

def verificar_se_e_fundo_branco(pixel, limite_branco=245):
    """
    Verifica se o pixel pertence ao fundo branco da folha de prova.
    """
    if len(pixel) == 4:  # RGBA
        r, g, b, _ = pixel
    else:  # RGB
        r, g, b = pixel[:3]
    return r >= limite_branco and g >= limite_branco and b >= limite_branco

def encontrar_fim_da_questao(imagem, margem_corte_lateral=30):
    """
    Percorre a imagem de baixo para cima.
    Encontra a primeira linha horizontal que contém algum pixel que NÃO é branco
    (ou seja, onde termina o rascunho/vazio e começa o texto da alternativa E).
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    # Ignora as bordinhas das extremidades laterais para evitar capturar 
    # possíveis linhas pretas verticais de digitalização nas margens da página.
    x_inicio = margem_corte_lateral
    x_fim = largura - margem_corte_lateral
    
    # Varre de baixo para cima
    for y in range(altura - 1, 0, -1):
        linha_totalmente_branca = True
        
        # Checa a linha horizontal atual
        for x in range(x_inicio, x_fim):
            if not verificar_se_e_fundo_branco(pixels[x, y]):
                # Se achou qualquer pixel escuro (texto/figura), a linha não é vazia!
                linha_totalmente_branca = False
                break
                
        # No momento em que a linha NÃO for totalmente branca, significa que
        # subimos todo o rascunho/vazio e batemos na base da alternativa E!
        if not linha_totalmente_branca:
            # Dá um respiro de 15 pixels para baixo para o texto não ficar colado no corte
            posicao_corte = y + 15
            
            # Garante que o corte não vai estourar o tamanho máximo original da imagem
            if posicao_corte >= altura:
                return None  # Não precisa cortar, a imagem já está no limite ideal
                
            return posicao_corte
            
    return None

def processar_imagens(pasta_origem, pasta_destino):
    """
    Processa todas as imagens, removendo o excesso branco inferior.
    """
    os.makedirs(pasta_destino, exist_ok=True)
    
    arquivos = [f for f in os.listdir(pasta_origem) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Encontrados {len(arquivos)} arquivos para processar na pasta '{pasta_origem}'")
    
    for arquivo in arquivos:
        caminho_origem = os.path.join(pasta_origem, arquivo)
        caminho_destino = os.path.join(pasta_destino, arquivo)
        
        try:
            with Image.open(caminho_origem) as imagem:
                # Encontra onde o rascunho em branco acaba
                posicao_corte = encontrar_fim_da_questao(imagem)
                
                if posicao_corte is not None and posicao_corte > 0:
                    # Recorta removendo o excesso de baixo
                    area_corte = (0, 0, imagem.width, posicao_corte)
                    imagem_recortada = imagem.crop(area_corte)
                    imagem_recortada.save(caminho_destino)
                    print(f"✂️ {arquivo}: Recortado excesso inferior. Altura reduzida de {imagem.height}px para {posicao_corte}px.")
                else:
                    # Se a imagem já estiver justa, apenas copia o arquivo original
                    shutil.copy2(caminho_origem, caminho_destino)
                    print(f"📄 {arquivo}: Mantido original (sem excesso branco detectado).")
                    
        except Exception as e:
            print(f"❌ Erro ao processar {arquivo}: {e}")
            shutil.copy2(caminho_origem, caminho_destino)

if __name__ == "__main__":
    # Configurações de pastas (certifique-se de que os nomes estão idênticos aos seus)
    pasta_origem = "./questoes"  # Pasta com as imagens do passo anterior
    pasta_destino = "finalizadas" # Pasta onde vão salvar os arquivos perfeitos
    
    print("Iniciando fatiamento inteligente de rebarbas inferiores...")
    
    if not os.path.exists(pasta_origem):
        print(f"Erro: A pasta '{pasta_origem}' não existe! Verifique o nome da pasta.")
        exit(1)
        
    processar_imagens(pasta_origem, pasta_destino)
    print("\n==================================================")
    print(f"🎉 Concluído! Imagens perfeitas salvas em: {pasta_destino}")