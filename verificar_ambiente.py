#!/usr/bin/env python3
"""Conferência de versões DIRETAS para novas execuções; não testa resultados científicos."""
import importlib.metadata as md
import sys

EXPECTED_PYTHON = (3, 15, 2)
DIRECT = {
    "numpy": "2.5.4", "pandas": "3.1.1", "scipy": "1.18.1",
    "scikit-learn": "1.9.1", "matplotlib": "3.11.2", "tabulate": "0.10.0",
}

ok = sys.version_info[:3] == EXPECTED_PYTHON
print("Python:", '.'.join(map(str, sys.version_info[:3])),
      "(esperado: 3.15.2)", "OK" if ok else "DIFERENTE")
for pkg, expected in DIRECT.items():
    try:
        actual = md.version(pkg)
    except md.PackageNotFoundError:
        actual = "NÃO INSTALADO"
    same = actual == expected
    ok &= same
    print(f"{pkg}: {actual} (esperado: {expected}) {'OK' if same else 'DIFERENTE'}")
print("Verificação das dependências diretas:", "OK" if ok else "NÃO CONFORME")
raise SystemExit(0 if ok else 1)
