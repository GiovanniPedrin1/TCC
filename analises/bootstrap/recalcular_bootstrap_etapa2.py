#!/usr/bin/env python3
"""Analise EXPLORATORIA, posterior ao teste congelado do TCC.

Consome somente o CSV de resultados individuais ja produzido pelo experimento.
Nao executa aprendizagem de maquina nem altera arquivos do pacote original.

Exemplo:
    python recalcular_bootstrap_etapa2.py --zip 'DB5_E2_FINAL_FROZEN(2).zip' --out bootstrap.csv
"""
import argparse
import csv
import io
import random
import zipfile
from statistics import mean

SAMPLES = 50_000
SEED = 20261110
IN_ZIP = 'e2_final/results/final_results_by_subject.csv'


def percentile(values, proportion):
    ordered = sorted(values)
    index = (len(ordered) - 1) * proportion
    low = int(index)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (index - low) * (ordered[high] - ordered[low])


def compute(src, kind='csv'):
    if kind == 'zip':
        with zipfile.ZipFile(src) as archive:
            raw = archive.read(IN_ZIP).decode('utf-8-sig')
    else:
        from pathlib import Path
        raw = Path(src).read_text(encoding='utf-8-sig')
    rows = list(csv.DictReader(io.StringIO(raw)))
    data = {(int(row['subject']), int(row['channels']), row['method']): float(row['macro_f1']) for row in rows}
    if len(rows) != 120 or len(data) != 120:
        raise ValueError('Esperados 120 resultados unicos (10 sujeitos x 4 canais x 3 metodos)')
    rng = random.Random(SEED)
    samples = [[rng.randrange(10) for _ in range(10)] for _ in range(SAMPLES)]
    output = []
    for channels in (1, 2, 4, 8):
        for first, second in (('LDA-TD', 'Threshold/Hamming'), ('LDA-TD', 'LDA-RMS')):
            differences = [data[(i, channels, first)] - data[(i, channels, second)] for i in range(1, 11)]
            bootstrap_means = [sum(differences[j] for j in indices) / 10 for indices in samples]
            output.append(dict(channels=channels, contrast=f'{first} - {second}',
                mean_difference=mean(differences), percentile_2_5=percentile(bootstrap_means, .025),
                percentile_97_5=percentile(bootstrap_means, .975),
                subject_positive=sum(v > 0 for v in differences),
                subject_negative=sum(v < 0 for v in differences),
                subject_tie=sum(v == 0 for v in differences)))
    reductions = [(data[(i, 1, 'LDA-TD')] - data[(i, 1, 'Threshold/Hamming')]) -
                  (data[(i, 8, 'LDA-TD')] - data[(i, 8, 'Threshold/Hamming')]) for i in range(1, 11)]
    bootstrap_means = [sum(reductions[j] for j in indices) / 10 for indices in samples]
    output.append(dict(channels='1 to 8', contrast='Reduction in LDA-TD - Threshold/Hamming gap',
        mean_difference=mean(reductions), percentile_2_5=percentile(bootstrap_means, .025),
        percentile_97_5=percentile(bootstrap_means, .975),
        subject_positive=sum(v > 0 for v in reductions),
        subject_negative=sum(v < 0 for v in reductions),
        subject_tie=sum(v == 0 for v in reductions)))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--csv', help='CSV dos resultados individuais do pacote organizado')
    group.add_argument('--zip', help='Pacote original ZIP da execução final (compatibilidade histórica)')
    parser.add_argument('--out', default='Analise_Exploratoria_Etapa2_Bootstrap.csv')
    args = parser.parse_args()
    data = compute(args.csv or args.zip, kind='csv' if args.csv else 'zip')
    with open(args.out, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f'Gravadas {len(data)} comparacoes exploratorias em {args.out}')


if __name__ == '__main__':
    main()
