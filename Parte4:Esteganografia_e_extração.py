import numpy as np
import cv2
import random
import os
import time

def embuta(block, payload, n=8, m=2, k=5, iteracoes=1):
    current_block = block.copy()

    #Injeção de Ruído Branco para evitar colapso em áreas lisas da imagem (Teorema 3.2)
    current_block = current_block + np.random.uniform(-0.5, 0.5, current_block.shape)

    for _ in range(iteracoes):
        U, S, Vt = np.linalg.svd(current_block, full_matrices=True)
        U, S, Vt = enforce_normal_svd(U, S, Vt)
        S_mod = space_singular_values(S, k, n)

        U_prime = U.copy()
        bit_idx = 0

        for j in range(m, n):
            for i in range(1, n - j):
                if bit_idx < len(payload):
                    U_prime[i, j] = payload[bit_idx] * abs(U[i, j])
                    bit_idx += 1

        U_prime = ortogonaliza(U_prime, m)
        A_prime = np.dot(U_prime, np.dot(np.diag(S_mod), Vt))
        current_block = np.clip(np.round(A_prime), 0, 255)

    return current_block

def extrai_o_bloco(block, num_bits=15, n=8, m=2):
    U, S, Vt = np.linalg.svd(block, full_matrices=True)
    U, S, Vt = svd(U, S, Vt)

    bits = []
    bit_idx = 0
    for j in range(m, n):
        for i in range(1, n - j):
            if bit_idx < num_bits:
                bits.append(1 if np.sign(U[i, j]) >= 0 else -1)
                bit_idx += 1

    return bits

def hide_message_image(cover_path, stego_path, bits_payload, iteracoes=8, n=8, m=2, k=5):
    img = cv2.imread(cover_path)
    if img is None: raise ValueError(f"Imagem não encontrada: {cover_path}")
    h, w, c_dim = img.shape

    stego_img = np.zeros_like(img, dtype=np.float64)
    bit_ptr = 0
    total_bits = len(bits_payload)

    for c in range(c_dim):
        channel = img[:, :, c].astype(np.float64)
        for row in range(0, h, n):
            for col in range(0, w, n):
                block = channel[row:row+n, col:col+n]
                block_payload = bits_payload[bit_ptr:bit_ptr+15]
                bit_ptr += 15

                if block_payload:
                    if len(block_payload) < 15:
                        block_payload.extend([1] * (15 - len(block_payload)))
                    stego_block = embuta(block, block_payload, n, m, k, iteracoes)
                    stego_img[row:row+n, col:col+n, c] = stego_block
                else:
                    stego_img[row:row+n, col:col+n, c] = block

    cv2.imwrite(stego_path, stego_img.astype(np.uint8))

def extract_raw_bits(stego_image_path, total_bits_esperados, n=8, m=2):
    img = cv2.imread(stego_image_path)
    h, w, c_dim = img.shape
    all_bits = []

    for c in range(c_dim):
        channel = img[:, :, c].astype(np.float64)
        for row in range(0, h, n):
            for col in range(0, w, n):
                block = channel[row:row+n, col:col+n]
                all_bits.extend(extract_block(block, num_bits=15, n=n, m=m))

                if len(all_bits) >= total_bits_esperados:
                    return all_bits[:total_bits_esperados]

    return all_bits[:total_bits_esperados]
