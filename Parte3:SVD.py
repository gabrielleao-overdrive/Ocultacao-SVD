import numpy as np
import cv2
import random
import os
import time

def svd(U, S, Vt):
    #garante a unicidade matemática exigindo positividade lexicográfica nas colunas de U.
    for j in range(U.shape[1]):
        if U[0, j] < 0:
            U[:, j] *= -1
            Vt[j, :] *= -1
    return U, S, Vt

def space_singular_values(S, k, n=8):
    #Mitigar o wobbly afastando os valores singulares mais fracos.
    S_spaced = S.copy()
    if S[k-1] - S[n-1] != 0:
        h = (S[k-1] - S[n-1]) / (n - k)
        for idx in range(k, n):
            S_spaced[idx] = S[k-1] - (idx - k + 1) * h
    return S_spaced

def ortogonaliza(U_prime, m):
    #Resolve o sistema linear para re-ortogonalizar a matriz sem sobrescrever a mensagem.
    n = U_prime.shape[1]
    for j in range(m, n):
        fixed_end = n - j
        Q = U_prime[:, :j]

        M = Q[fixed_end:, :].T
        f = U_prime[:fixed_end, j]
        b = -np.dot(Q[:fixed_end, :].T, f)

        try:
            x = np.linalg.solve(M, b)
        except np.linalg.LinAlgError:
            x, _, _, _ = np.linalg.lstsq(M, b, rcond=None)

        U_prime[fixed_end:, j] = x

        norma = np.linalg.norm(U_prime[:, j])
        if norma > 0:
            U_prime[:, j] /= norma

    return U_prime
