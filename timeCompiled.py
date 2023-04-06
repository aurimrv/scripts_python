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
    file = baseDir+'/time-report-cosmic-ray-RANDOM.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        next(reader)

        for indice, linha in enumerate(reader):
            if indice >= 1 and indice <= 20:
                valor = linha[2]
                dados.append(valor)

    file = baseDir+'/time-report-cosmic-ray-DYNAMOSA.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    file = baseDir+'/time-report-cosmic-ray-MIO.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)
    
    file = baseDir+'/time-report-cosmic-ray-MOSA.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    file = baseDir+'/time-report-cosmic-ray-WHOLE_SUITE.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    file = baseDir+'/time-report-cosmic-ray-DYNAMOSA-MIO.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)
    
    file = baseDir+'/time-report-cosmic-ray-DYNAMOSA-MOSA.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    file = baseDir+'/time-report-cosmic-ray-DYNAMOSA-WHOLE_SUITE.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    file = baseDir+'/time-report-cosmic-ray-MIO-MOSA.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    file = baseDir+'/time-report-cosmic-ray-MIO-WHOLE_SUITE.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    file = baseDir+'/time-report-cosmic-ray-MOSA-WHOLE_SUITE.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    file = baseDir+'/time-report-cosmic-ray-DYNAMOSA-MIO-MOSA.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    file = baseDir+'/time-report-cosmic-ray-DYNAMOSA-MIO-WHOLE_SUITE.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    file = baseDir+'/time-report-cosmic-ray-DYNAMOSA-MOSA-WHOLE_SUITE.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    file = baseDir+'/time-report-cosmic-ray-MIO-MOSA-WHOLE_SUITE.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    file = baseDir+'/time-report-cosmic-ray-DYNAMOSA-MIO-MOSA-WHOLE_SUITE.csv'
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        coluna = [float(row[2]) for row in reader]

        dados.append(coluna)

    dados_t = list(map(list, zip(*dados)))

    # escreve os dados em um novo arquivo CSV
    with open(prjReport, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # escreve cada linha do arquivo resultado com as colunas de dados
        for linha in dados_t:
            writer.writerow(linha)

if __name__ == "__main__":
    main()