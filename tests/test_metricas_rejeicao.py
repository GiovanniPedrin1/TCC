"""Testes de regressão para rejeição sem quinta classe verdadeira.

Executar a partir da raiz: python -m unittest discover -s tests -v
"""
from __future__ import annotations

import sys
import unittest
import warnings
from pathlib import Path

import numpy as np
from sklearn.metrics import balanced_accuracy_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "e2_final"))
sys.path.insert(0, str(ROOT / "e2_validation"))

from run_final_e2_frozen import (  # noqa: E402
    balanced_accuracy_with_reject as final_balanced_accuracy,
    confusion_4,
    metrics_common,
)
from run_threshold_e2_validation import (  # noqa: E402
    balanced_accuracy_with_reject as validation_balanced_accuracy,
)


class TestMetricasRejeicao(unittest.TestCase):
    def test_rejeicao_conta_como_erro_sem_warning(self):
        y = np.array([0, 0, 1, 1, 5, 5, 6, 6])
        predictions = np.array([0, -1, 1, -1, 5, -1, 6, -1])
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            self.assertEqual(final_balanced_accuracy(y, predictions), 0.5)
            self.assertEqual(validation_balanced_accuracy(y, predictions), 0.5)

    def test_sem_rejeicao_equivale_ao_sklearn(self):
        y = np.array([0, 0, 1, 1, 5, 5, 6, 6])
        predictions = np.array([0, 1, 1, 1, 5, 6, 6, 0])
        expected = balanced_accuracy_score(y, predictions)
        self.assertAlmostEqual(final_balanced_accuracy(y, predictions), expected)
        self.assertAlmostEqual(validation_balanced_accuracy(y, predictions), expected)

    def test_taxa_direcional_usa_todas_as_amostras_reais(self):
        y = np.array([0, 1, 5, 6, 6, 6])
        predictions = np.array([0, 1, 5, 1, -1, -1])
        cm = confusion_4(y, predictions)
        result = metrics_common(y, predictions, cm)
        self.assertAlmostEqual(result["closed_to_thumb_rate"], 1 / 3)
        self.assertEqual(result["thumb_to_closed_rate"], 0)
        self.assertAlmostEqual(result["balanced_accuracy"], (1 + 1 + 1 + 0) / 4)

    def test_todas_rejeitadas_na_classe_fechada_nao_divide_por_zero(self):
        y = np.array([0, 1, 5, 6, 6])
        predictions = np.array([0, 1, 5, -1, -1])
        result = metrics_common(y, predictions, confusion_4(y, predictions))
        self.assertEqual(result["closed_to_thumb_rate"], 0)
        self.assertEqual(result["balanced_accuracy"], 0.75)

    def test_ausencia_de_classe_verdadeira_e_erro(self):
        y = np.array([0, 1, 5])
        predictions = np.array([0, 1, 5])
        with self.assertRaises(ValueError):
            final_balanced_accuracy(y, predictions)


if __name__ == "__main__":
    unittest.main()
