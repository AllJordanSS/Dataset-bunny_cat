import os
import re

def reorganizar_arquivos(diretorio):
    """
    Reorganiza arquivos em um diretório para criar uma sequência numérica
    perfeita (1.jpg, 2.jpg, 3.jpg, ...), preenchendo lacunas e mantendo
    a ordem relativa dos arquivos.

    Esta função usa uma abordagem de renomeação temporária para evitar
    conflitos.

    Args:
        diretorio (str): O caminho do diretório contendo as imagens.
    """
    if not os.path.isdir(diretorio):
        print(f"Erro: O diretório '{diretorio}' não foi encontrado.")
        return

    padrao_numerico = re.compile(r'^(\d+)\.jpg$', re.IGNORECASE)

    # Passo 1: Renomear todos os arquivos numéricos para nomes temporários
    arquivos_originais = []
    for nome_arquivo in os.listdir(diretorio):
        if nome_arquivo.lower().endswith('.jpg'):
            match = padrao_numerico.match(nome_arquivo)
            if match:
                numero = int(match.group(1))
                arquivos_originais.append((numero, nome_arquivo))
            else:
                # Trata arquivos não-numéricos como se tivessem um número grande,
                # para que sejam processados por último
                arquivos_originais.append((float('inf'), nome_arquivo))

    # Ordenar numericamente para processar na ordem correta
    arquivos_originais.sort(key=lambda x: x[0])
    
    print("Renomeando arquivos para nomes temporários para evitar conflitos...")
    arquivos_temp = []
    for numero, nome_arquivo in arquivos_originais:
        caminho_antigo = os.path.join(diretorio, nome_arquivo)
        caminho_temp = os.path.join(diretorio, f"_temp_{nome_arquivo}")
        try:
            os.rename(caminho_antigo, caminho_temp)
            arquivos_temp.append(caminho_temp)
        except Exception as e:
            print(f"Erro ao renomear '{nome_arquivo}' para temporário: {e}")

    # Passo 2: Renomear os arquivos temporários para a sequência numérica correta
    print("\nRenomeando arquivos temporários para a sequência final...")
    proximo_numero = 1
    
    # É importante reordenar a lista de arquivos temporários,
    # caso a ordenação inicial do sistema não tenha sido numérica
    arquivos_temp.sort(key=lambda x: int(re.search(r'_temp_(\d+)\.jpg$', x).group(1)) if re.search(r'_temp_(\d+)\.jpg$', x) else float('inf'))

    for caminho_temp in arquivos_temp:
        # Pega o número do nome temporário para renomear
        match = re.search(r'_temp_(\d+)\.jpg$', caminho_temp)
        if match:
            numero_original = int(match.group(1))
        
        caminho_final = os.path.join(diretorio, f"{proximo_numero}.jpg")
        
        try:
            os.rename(caminho_temp, caminho_final)
            print(f"Renomeado: '{os.path.basename(caminho_temp)}' para '{os.path.basename(caminho_final)}'")
            proximo_numero += 1
        except Exception as e:
            print(f"Erro ao renomear '{caminho_temp}': {e}")
            
    print("\nReorganização da sequência concluída com sucesso.")

if __name__ == "__main__":
    caminho_da_pasta = r'./'
    reorganizar_arquivos(caminho_da_pasta)