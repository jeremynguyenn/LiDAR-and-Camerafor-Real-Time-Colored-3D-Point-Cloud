import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob

def carregar_dados_arquivos(pasta):
    arquivos = sorted(glob(os.path.join(pasta, 'plot_*.txt')))
    dados = []
    
    for arquivo in arquivos:
        dados_arquivo = np.loadtxt(arquivo)
        dados.append(dados_arquivo)
    
    return np.vstack(dados)  # Empilha os dados em uma única matriz

def plotar_dados(dados):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Separate XYZ coordinates and RGB values.
    xyz = dados[:, :3]
    rgb = dados[:, 3:] / 255.0  # Normalize RGB values to the range [0, 1].
    
    # Plot all the points.
    ax.scatter(0, 0, 0, c='red', marker='o')
    ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], c=rgb, edgecolors='none', marker='o', s=10)
    
    # Set axis limits (adjust as needed).
    x_limits = (0, 2500)
    y_limits = (-1500, 1500)
    z_limits = (1000, -2500)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    # Set axis limits.
    ax.set_xlim(x_limits)
    ax.set_ylim(y_limits)
    ax.set_zlim(z_limits)
    
    # Set elevation and azimuth.
    ax.view_init(elev=10, azim=168)
    
    plt.show()

# Path to the folder where the files are located.
pasta_dados = '/home/user/plot_sala_12/'

# Load all data from the .txt files.
dados_todos = carregar_dados_arquivos(pasta_dados)

# Plot the data.
plotar_dados(dados_todos)
