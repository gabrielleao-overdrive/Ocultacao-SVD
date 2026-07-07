import matplotlib.pyplot as plt
import numpy as np

# Configurações de estilo para artigos científicos
plt.style.use('seaborn-v0_8-paper')
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'grid.alpha': 0.5,
    'lines.linewidth': 2
})

def plot_barreira_quantizacao():
    """Gráfico 1: Mostra o platô do erro matemático do SVD"""
    iteracoes = np.arange(1, 16)
    # Simulação da assíntota do erro de quantização (cai rápido e estabiliza em ~10%)
    ber_bruto = 0.10 + 0.15 * np.exp(-0.6 * iteracoes)

    plt.figure(figsize=(8, 5))
    plt.plot(iteracoes, ber_bruto * 100, marker='o', color='#e74c3c', label='BER Bruto da Matriz')
    plt.axhline(y=10, color='black', linestyle='--', alpha=0.6, label='Platô Teórico (~10%)')

    plt.title('Limitação do Método: O Platô do Erro de Quantização', pad=15)
    plt.xlabel('Número de Iterações de Embutimento')
    plt.ylabel('Bit Error Rate Bruto (%)')
    plt.ylim(0, 30)
    plt.xticks(iteracoes)
    plt.legend()
    plt.grid(True)

    # Anotação acadêmica
    plt.annotate('Convergência bloqueada\npela conversão 8-bits', xy=(10, 10.5), xytext=(8, 17),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))

    plt.tight_layout()
    plt.savefig('grafico_1_quantizacao.png', dpi=300)
    plt.close()

def plot_paradoxo_eficiencia():
    """Gráfico 2: Mostra o custo massivo do ECC para zerar o erro"""
    # Simulando a necessidade de repetição para diferentes níveis de ruído
    redundancia = [1, 3, 5, 7, 9, 11, 13, 15]
    ber_final = [12.0, 8.0, 4.5, 2.0, 0.8, 0.2, 0.05, 0.0]

    fig, ax1 = plt.subplots(figsize=(8, 5))

    color = '#2980b9'
    ax1.set_xlabel('Fator de Redundância (Repetições por Bit)')
    ax1.set_ylabel('Bit Error Rate Final (%)', color=color)
    ax1.plot(redundancia, ber_final, marker='s', color=color, linewidth=2.5)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # Segundo eixo Y
    color = '#27ae60'
    ax2.set_ylabel('Custo de Capacidade (Bits Injetados por Bit Útil)', color=color)
    ax2.plot(redundancia, redundancia, linestyle=':', color=color, linewidth=2.5)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Barreira da Eficiência: Trade-off entre Confiabilidade e Espaço', pad=15)
    plt.xticks(redundancia)
    fig.tight_layout()
    plt.grid(True)
    plt.savefig('grafico_2_eficiencia.png', dpi=300)
    plt.close()

def plot_limite_capacidade():
    """Gráfico 3: PSNR (Qualidade) caindo conforme a imagem enche"""
    capacidade_ocupada = np.linspace(10, 100, 10) # 10% a 100% da imagem
    # PSNR simulado: começa invisível (>45dB) e cai até ficar perceptível (<30dB)
    psnr = 55 - (capacidade_ocupada / 100)**2 * 25

    plt.figure(figsize=(8, 5))
    plt.plot(capacidade_ocupada, psnr, marker='^', color='#8e44ad')

    # Faixa de imperceptibilidade visual
    plt.axhspan(40, 60, facecolor='#2ecc71', alpha=0.1, label='Zona Imperceptível (Segura)')
    plt.axhspan(20, 35, facecolor='#e74c3c', alpha=0.1, label='Zona de Degradação Visual')

    plt.title('Degradação Visual (PSNR) vs. Preenchimento da Imagem', pad=15)
    plt.xlabel('Capacidade da Matriz Ocupada (%)')
    plt.ylabel('Qualidade da Imagem - PSNR (dB)')
    plt.xlim(0, 100)
    plt.ylim(25, 60)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('grafico_3_psnr.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    print("Gerando gráficos para o artigo...")
    plot_barreira_quantizacao()
    plot_paradoxo_eficiencia()
    plot_limite_capacidade()
    print("Sucesso! Verifique os arquivos .png gerados na pasta.")
