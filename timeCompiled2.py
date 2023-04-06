#!/usr/bin/env python3

# Script que junta todos os dados de tempo em uma única planilha
# Cada coluna do novo arquivo simboliza uma combinação dos algoritmos da pynguin

import sys
import csv
import pandas as pd

def main():
    if len(sys.argv) < 2:
        print("error: timeCompiled.py <project root dir> <mutation-tool>")
        print("Example: timeCompiled.py /home/auri/python_experiments2 cosmic-ray")
        sys.exit(1)

    baseDir = sys.argv[1]
    mutTool = sys.argv[2]

    prjReport = baseDir+"/compiled-time-report-"+mutTool+".csv"

    # cria uma lista vazia para armazenar os dados de cada arquivo
    dados = []

    file = baseDir+'/time-report-cosmic-ray-RANDOM.csv'
    df = pd.read_csv(file)

    dados = df.iloc[1:21, 2].tolist()

    dados_t = list(map(list, zip(*dados)))

    # escreve os dados em um novo arquivo CSV
    with open(prjReport, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # escreve cada linha do arquivo resultado com as colunas de dados
        for linha in dados_t:
            writer.writerow(linha)

if __name__ == "__main__":
    main()