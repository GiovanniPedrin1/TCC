#!/usr/bin/env python3
"""Compara saídas novas com os registros científicos congelados do repositório.

Exemplo (na raiz do repositório):
  python verificar_reproducao.py \\
    --final reproducoes/final \\
    --validacao-lda reproducoes/validacao_lda \\
    --validacao-threshold reproducoes/validacao_threshold

Não altera nem os resultados originais nem os reproduzidos. Saída diferente
é reportada, jamais ajustada ou sobrescrita automaticamente.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
REL_TOL = 1e-10
ABS_TOL = 1e-12

# Somente os arquivos efetivamente escritos pelos três scripts de execução.
EXPECTED_FILES = {
    'final': [
        'FINAL_PROTOCOL_AUDIT.json', 'channel_evolution.csv',
        'confusion_matrices.json', 'final_results_by_subject.csv',
        'final_summary_mean_std.csv', 'lda_warnings.csv',
        'macro_f1_primary_comparison.csv', 'raw_e2_audit.csv',
        'thresholds_and_templates_frozen.csv', 'window_audit.csv',
        'window_counts_by_subject_rep_class.csv',
    ],
    'validacao_lda': [
        'audit.json', 'confusion_matrices.json', 'e2_file_audit.csv',
        'results_by_subject.csv', 'summary.csv', 'window_audit.csv',
        'window_counts.csv',
    ],
    'validacao_threshold': [
        'threshold_audit.json', 'threshold_confusion_matrices.json',
        'threshold_results_by_subject.csv', 'threshold_summary.csv',
        'threshold_window_audit.csv', 'thresholds_and_templates.csv',
    ],
}
REFERENCES = {
    'final': ROOT / 'e2_final/results',
    'validacao_lda': ROOT / 'e2_validation/results',
    'validacao_threshold': ROOT / 'threshold_results',
}


def compare_json(reference, current, location='$'):
    """Compara estruturas JSON sem exigir representação textual idêntica."""
    if isinstance(reference, dict) and isinstance(current, dict):
        if reference.keys() != current.keys():
            raise AssertionError(f'{location}: campos JSON divergentes')
        for key in reference:
            compare_json(reference[key], current[key], f'{location}.{key}')
    elif isinstance(reference, list) and isinstance(current, list):
        if len(reference) != len(current):
            raise AssertionError(f'{location}: tamanhos de lista diferentes')
        for idx, (left, right) in enumerate(zip(reference, current)):
            compare_json(left, right, f'{location}[{idx}]')
    elif (isinstance(reference, (float, int)) and not isinstance(reference, bool)
          and isinstance(current, (float, int)) and not isinstance(current, bool)):
        if not math.isclose(reference, current, rel_tol=REL_TOL, abs_tol=ABS_TOL):
            raise AssertionError(f'{location}: {reference} != {current}')
    elif reference != current:
        raise AssertionError(f'{location}: {reference!r} != {current!r}')


def compare_file(reference: Path, current: Path):
    """Usa comparação de bytes quando possível, numérica quando necessário."""
    if not reference.is_file() or not current.is_file():
        raise FileNotFoundError(f'Arquivo ausente: {reference} ou {current}')
    if reference.read_bytes() == current.read_bytes():
        return 'idêntico em bytes'
    if reference.suffix == '.json':
        compare_json(
            json.loads(reference.read_text(encoding='utf-8')),
            json.loads(current.read_text(encoding='utf-8')),
        )
    elif reference.suffix == '.csv':
        pd.testing.assert_frame_equal(
            pd.read_csv(reference), pd.read_csv(current),
            check_dtype=False, check_exact=False, rtol=REL_TOL, atol=ABS_TOL,
        )
    else:
        raise ValueError(f'Formato não verificado: {reference}')
    return 'equivalente dentro da tolerância numérica'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--final', type=Path, help='Pasta de saída do teste final')
    parser.add_argument('--validacao-lda', type=Path, help='Saída da validação LDA')
    parser.add_argument('--validacao-threshold', type=Path,
                        help='Saída da validação Threshold/Hamming')
    args = parser.parse_args()
    dirs = {
        'final': args.final,
        'validacao_lda': args.validacao_lda,
        'validacao_threshold': args.validacao_threshold,
    }
    if not any(dirs.values()):
        parser.error('Informe ao menos uma pasta de resultados para verificar')

    successful = 0
    errors = []
    for stage, new_dir in dirs.items():
        if new_dir is None:
            continue
        for filename in EXPECTED_FILES[stage]:
            try:
                outcome = compare_file(REFERENCES[stage] / filename, new_dir / filename)
                successful += 1
                print(f'OK: {stage}/{filename} — {outcome}')
            except (OSError, ValueError, AssertionError) as exc:
                errors.append(f'{stage}/{filename}: {exc}')
                print(f'DIVERGENTE: {stage}/{filename}: {exc}')
    print(f'\nArquivos equivalentes: {successful}; divergências: {len(errors)}')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
