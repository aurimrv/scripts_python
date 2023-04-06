#!/usr/bin/env python3

# Script que junta todos os dados de tempo em uma única planilha
# Cada coluna do novo arquivo simboliza uma combinação dos algoritmos da pynguin

import sys
import csv

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

    # percorre cada um dos 16 arquivos CSV
    arquivos_csv = [    'time-report-cosmic-ray-RANDOM.csv',
                 'time-report-cosmic-ray-DYNAMOSA.csv',    
                 'time-report-cosmic-ray-MIO.csv',    
                 'time-report-cosmic-ray-MOSA.csv',    
                 'time-report-cosmic-ray-WHOLE_SUITE.csv',    
                 'time-report-cosmic-ray-DYNAMOSA-MIO.csv',    
                 'time-report-cosmic-ray-DYNAMOSA-MOSA.csv',    
                 'time-report-cosmic-ray-DYNAMOSA-WHOLE_SUITE.csv',    
                 'time-report-cosmic-ray-MIO-MOSA.csv',    
                 'time-report-cosmic-ray-MIO-WHOLE_SUITE.csv',    
                 'time-report-cosmic-ray-MOSA-WHOLE_SUITE.csv',    
                 'time-report-cosmic-ray-DYNAMOSA-MIO-MOSA.csv',    
                 'time-report-cosmic-ray-DYNAMOSA-MIO-WHOLE_SUITE.csv',    
                 'time-report-cosmic-ray-DYNAMOSA-MOSA-WHOLE_SUITE.csv',    
                 'time-report-cosmic-ray-MIO-MOSA-WHOLE_SUITE.csv',    
                 'time-report-cosmic-ray-DYNAMOSA-MIO-MOSA-WHOLE_SUITE.csv']

    # lista para armazenar todos os dados
    dados = []

    # percorrer cada um dos 16 arquivos CSV e adicionar os valores de cada coluna à lista de dados
    for arquivo in arquivos_csv:
        with open(baseDir+'/'+arquivo, newline='') as csvfile:
            reader = csv.reader(csvfile)

            for linha, coluna in enumerate(reader):
                valor = coluna[0]
                dados.append(valor)

    # abrir um novo arquivo CSV para escrita
    with open(prjReport, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # escrever os dados em colunas
        for i in range(0, len(dados), 22):
            coluna = dados[i:i+22]
            writer.writerow(coluna)

if __name__ == "__main__":
    main()