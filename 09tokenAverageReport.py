#!/usr/bin/env python3

# Script para a combinação das planilhas de relatório de custo em tokens por ferramenta.

import sys
import os
import csv
from collections import defaultdict

def main():
    if len(sys.argv) < 3:
        print("error: tokenReport.py <project root dir> <data-file> <test-set-file>")
        print("Example: tokenReport.py /home/auri/python_experiments2 files.txt")
        sys.exit(1)

    baseDir = sys.argv[1]
    dataFile = sys.argv[2]
    prjList = baseDir + "/" + dataFile

    # Dicionário para armazenar valores float de cada projeto
    combined_averages = defaultdict(list)

    dados = open(prjList, 'r')
        
    for x in dados:
        x = x.strip()
        info = x.split(':')
        prj = info[0]
        clazz = info[1]
            
        print(f"Processing project: {prj}")
        prjDir = baseDir + "/" + prj
            
        csv_file_path = os.path.join(prjDir, "gpt-3-5-tokens.csv")
            
        # Verifica se o arquivo CSV existe
        if not os.path.isfile(csv_file_path):
            print(f"Warning: {csv_file_path} not found.")
            break
            
        with open(csv_file_path, mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)  # Pular o cabeçalho
            combined_data = defaultdict(list)

            for row in reader:
                key = row[2]
                value = float(row[3])  # Converte o valor da quarta coluna para float
                combined_data[key].append(value)  # Armazena o valor na lista associada à chave

        # Calcula a média dos valores para cada chave e imprime o resultado
        for key, values in combined_data.items():
            if values:  # Certifica-se de que a lista não está vazia   
                #average = sum(values) / len(values)
                average = sum(values) 
                combined_averages[prj].append(float(average))

        # Caminho para o arquivo combinado de saída
        combined_csv_path = os.path.join(baseDir, "combined_token_report.csv")

        # Grava os dados combinados em um novo CSV
        with open(combined_csv_path, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            max_len = max(len(v) for v in combined_data.values())
            # Cabeçalho
            header = ["Project"] + [f"{0}.{i}" if i < 10 else "1.0" for i in range(max(len(v) for v in combined_averages.values()))]
            writer.writerow(header)

            # Dados
            for prj, values in combined_averages.items():
                row = [prj] + [f"{value:.2f}" for value in values]
                writer.writerow(row)

        print(f"Combined report created at: {combined_csv_path}")

if __name__ == "__main__":
    main()