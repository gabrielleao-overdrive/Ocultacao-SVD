import numpy as np
import cv2
import random
import os
import time

def aplicar_ecc_intercalado(bits_payload, repeticoes=15):
    #Repete cada bit N vezes e embaralha para proteger contra blocos SVD corrompidos.
    bits_protegidos = []
    for i, bit in enumerate(bits_payload):
        for _ in range(repeticoes):
            bits_protegidos.append((i, bit))

    # Embaralhamento determinístico (chave pública = 42)
    random.seed(42)
    random.shuffle(bits_protegidos)
    return [b[1] for b in bits_protegidos]

def decodificar_ecc_intercalado(bits_extraidos, tamanho_original_bits, repeticoes=15):
    #Desfaz o embaralhamento e aplica Votação Majoritária para recuperar o bit original.
    indices = []
    for i in range(tamanho_original_bits):
        for _ in range(repeticoes):
            indices.append(i)

    random.seed(42)
    random.shuffle(indices)

    votos_por_bit = {i: 0 for i in range(tamanho_original_bits)}

    for idx_embaralhado, bit_lido in zip(indices, bits_extraidos):
        votos_por_bit[idx_embaralhado] += bit_lido

    bits_corrigidos = []
    for i in range(tamanho_original_bits):
        vencedor = 1 if votos_por_bit[i] > 0 else -1
        bits_corrigidos.append(vencedor)

    return bits_corrigidos
