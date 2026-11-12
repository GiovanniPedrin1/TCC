#!/usr/bin/env python3
"""Verifica hashes SHA-256 dos arquivos distribuídos nesta versão."""
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / 'docs/MANIFESTO_SHA256.csv'


def main():
    with MANIFEST.open(encoding='utf-8', newline='') as fh:
        rows = list(csv.DictReader(fh))
    problems = []
    for row in rows:
        path = ROOT / row['caminho']
        if not path.is_file():
            problems.append(f"AUSENTE: {row['caminho']}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != row['sha256']:
            problems.append(f"DIVERGENTE: {row['caminho']}")
    if problems:
        print('\n'.join(problems))
        print(f'Falha: {len(problems)} problema(s) em {len(rows)} arquivo(s).')
        raise SystemExit(1)
    print(f'Integridade verificada: {len(rows)} arquivos correspondem ao manifesto.')


if __name__ == '__main__':
    main()
