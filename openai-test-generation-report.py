#!/usr/bin/env python3

import sys
import csv
import os
import re

def temperature_to_float(temperature):
    major, minor = map(int, temperature.split('-'))
    return major + minor / 10.0

def main():
    if len(sys.argv) < 4:
        print("error: openai-test-generation-report.py <base directory> <model> <files>")
        print("Example: openai-test-generation-report.py /home/auri/temp/lucca/python_experiments2/ 3-5 files.txt")
        sys.exit(1)

    base_dir = sys.argv[1]
    model = sys.argv[2]
    files_dir = os.path.join(base_dir, sys.argv[3])

    if not os.path.isfile(files_dir):
        print(f"error1: {files_dir} not found")
        sys.exit(1)

    with open(files_dir, 'r') as file:
        files_paths = [line.strip().split(':')[0] for line in file.readlines()]

    for path in files_paths:
        # Dicionário para armazenar contagens de arquivos por temperatura
        temperature_counts = {}

        test_dir = os.path.join(base_dir, path)
        model_dir = os.path.join(test_dir, f"ts-{model}")

        if not os.path.isdir(model_dir):
            print(f"error2: {model_dir} not found")
            continue

        for root, _, files in os.walk(model_dir):
            for file in files:
                match = re.match(r'test_{}_([^_]+)_\d+'.format(model), file)
                if match:
                    temperature = match.group(1)
                    if temperature not in temperature_counts:
                        temperature_counts[temperature] = {
                            'py': 0,
                            'py.orig': 0,
                            'py.err': 0,
                            'py_p0': 0,
                            'py_p1': 0,
                            'py_p2': 0,
                            'py_c0': 0,
                            'py_c1': 0,
                            'py_c2': 0,
                        }

                    if file.endswith('.py'):
                        temperature_counts[temperature]['py'] += 1
                    elif file.endswith('.py.orig'):
                        temperature_counts[temperature]['py.orig'] += 1
                    elif file.endswith('.py.err'):
                        temperature_counts[temperature]['py.err'] += 1
                    elif file.endswith('.py_p0'):
                        temperature_counts[temperature]['py_p0'] += 1
                    elif file.endswith('.py_p1'):
                        temperature_counts[temperature]['py_p1'] += 1
                    elif file.endswith('.py_p2'):
                        temperature_counts[temperature]['py_p2'] += 1
                    elif file.endswith('.py_c0'):
                        temperature_counts[temperature]['py_c0'] += 1
                    elif file.endswith('.py_c1'):
                        temperature_counts[temperature]['py_c1'] += 1
                    elif file.endswith('.py_c2'):
                        temperature_counts[temperature]['py_c2'] += 1

        # Ordenando as temperaturas
        sorted_temperatures = sorted(temperature_counts.keys(), key=temperature_to_float)

        # Calculando os totais
        total_counts = {
            'passed': 0,
            'failed': 0,
            'first_try': 0,
            'passed_on_one_attempt': 0,
            'passed_on_more_than_one_attempt': 0
        }

        # Processando e salvando os resultados para cada temperatura em CSV
        csv_filename = os.path.join(test_dir, f'file_counts_{model}_by_temperature.csv')
        with open(csv_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Temperature', 'Total Passed', 'Failed', 'Passed on First Try', 'Passed on One Retry', 'Passed on More Than One Retry'])

            for temperature in sorted_temperatures:
                counts = temperature_counts[temperature]
                passed = counts['py']
                failed = counts['py.err'] // 4
                passed_on_more_than_one_attempt = counts['py_p0'] + counts['py_c0']
                passed_on_one_attempt = counts['py.orig'] - passed_on_more_than_one_attempt
                first_try = passed - passed_on_one_attempt - passed_on_more_than_one_attempt

                writer.writerow([temperature, passed, failed, first_try, passed_on_one_attempt, passed_on_more_than_one_attempt])

                # Atualizando os totais
                total_counts['passed'] += passed
                total_counts['failed'] += failed
                total_counts['first_try'] += first_try
                total_counts['passed_on_one_attempt'] += passed_on_one_attempt
                total_counts['passed_on_more_than_one_attempt'] += passed_on_more_than_one_attempt

            # Escrevendo a linha de totais
            writer.writerow([
                'Total',
                total_counts['passed'],
                total_counts['failed'],
                total_counts['first_try'],
                total_counts['passed_on_one_attempt'],
                total_counts['passed_on_more_than_one_attempt']
            ])

        print(f"File counts by temperature saved to {csv_filename}")

if __name__ == "__main__":
    main()


