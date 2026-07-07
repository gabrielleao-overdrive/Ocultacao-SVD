import numpy as np
import cv2
import random
import os
import time
#1
def texto_em_bits(text):
    #Converte texto em sinais algébricos (+1 e -1) para a matriz.
    bits = []
    for char in text:
        for bit in format(ord(char), '08b'):
            bits.append(1 if bit == '1' else -1)
    return bits

def bits_para_texto(bits):
    #Reconstrói a string 
    chars = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        if len(byte_bits) < 8: break
        bin_str = "".join(['1' if b >= 0 else '0' for b in byte_bits])
        chars.append(chr(int(bin_str, 2)))
    return "".join(chars)
