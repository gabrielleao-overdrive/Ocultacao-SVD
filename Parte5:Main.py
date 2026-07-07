import numpy as np
import cv2
import random
import os
import time

def executa():

    cover_path = "/imagem800x600.png"
    stego_path = "/imagem.png"

    mensagem = "O talking heads teve participação do Adrian Belew e produção pelo Brian Eno no disco Remain in Light, o que mostra a sua excelência musical."
    repeticoes_ecc = 15
    iteracoes_svd = 8

    print("INICIANDO ESTEGANOGRAFIA SVD")
    inicio = time.time()

    #1. Converter e Proteger
    bits_originais = texto_em_bits(mensagem)
    tamanho_bits = len(bits_originais)
    print(f"[*] Mensagem original: {len(mensagem)} caracteres ({tamanho_bits} bits).")

    bits_com_ecc = aplicar_ecc_intercalado(bits_originais, repeticoes=repeticoes_ecc)
    print(f"[*] Camada ECC aplicada. Payload expandido para {len(bits_com_ecc)} bits.")

    #2. Embutir (Ocultação)
    print(f"[*] Embutindo dados na matriz SVD ({iteracoes_svd} iterações por bloco)...")
    try:
        hide_message_image(cover_path, stego_path, bits_com_ecc, iteracoes=iteracoes_svd)
        print(f"    [+] Imagem salva com sucesso: {stego_path}")
    except Exception as e:
        print(f"    [-] Falha ao processar a imagem: {e}")
        return

    #3. Extrair e Corrigir
    print("[*] Extraindo bits da imagem gerada...")
    bits_extraidos = extrai(stego_path, len(bits_com_ecc))

    print("[*] Decodificando matriz e corrigindo erros de quantização...")
    bits_recuperados = decodificar_ecc_intercalado(bits_extraidos, tamanho_bits, repeticoes=repeticoes_ecc)
    texto_final = bits_para_texto(bits_recuperados)

    #4. Avaliação
    fim = time.time()
    erros = sum(1 for a, b in zip(bits_originais, bits_recuperados) if a != b)
    ber = erros / tamanho_bits if tamanho_bits > 0 else 1.0

    print("\n=== RESULTADOS DA EXTRAÇÃO ===")
    print(f"Texto Extraído: {texto_final}")
    print(f"Bit Error Rate (BER): {ber:.6f}")
    print(f"Tempo Total: {fim - inicio:.2f} segundos")

if __name__ == "__main__":
    # Garante que a semente do Numpy seja aleatória para o ruído branco
    np.random.seed()
    executa()
