#!/usr/bin/env python3
"""Mostra se o ambiente atual corresponde ao ambiente reexecutado da V2.

Não garante igualdade binária em outras plataformas e não identifica as
versões empregadas no experimento histórico, que permanecem desconhecidas.
"""
from __future__ import annotations

import importlib.metadata as metadata
import sys

EXPECTED_PYTHON = (3, 13, 5)
DIRECT_DEPENDENCIES = {
    "numpy": "2.3.5",
    "pandas": "2.2.3",
    "scipy": "1.17.0",
    "scikit-learn": "1.8.0",
    "matplotlib": "3.10.8",
    "tabulate": "0.10.0",
}


def main():
    actual_python = sys.version_info[:3]
    matches = actual_python == EXPECTED_PYTHON
    print(
        f"Python: {'.'.join(map(str, actual_python))} "
        f"(reexecutado: {'.'.join(map(str, EXPECTED_PYTHON))}) "
        f"{'OK' if matches else 'DIFERENTE'}"
    )

    for package, expected in DIRECT_DEPENDENCIES.items():
        try:
            actual = metadata.version(package)
        except metadata.PackageNotFoundError:
            actual = "NÃO INSTALADO"
        same = actual == expected
        matches = matches and same
        print(f"{package}: {actual} (reexecutado: {expected}) "
              f"{'OK' if same else 'DIFERENTE'}")

    print("Ambiente reproduzido:", "OK" if matches else "DIFERENTE")
    return 0 if matches else 1


if __name__ == "__main__":
    raise SystemExit(main())
