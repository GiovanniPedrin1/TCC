# NinaPro DB5 E2 — teste final congelado

Execução final do protocolo congelado para Threshold/Hamming, LDA-RMS e LDA-TD.

- Treino: repetições 1, 3, 4
- Teste: repetições 2, 5
- Repetição 6: excluída desta etapa
- Arquivos: Sx_E2_A1.mat, sujeitos 1..10

Executar:

```bash
python run_final_e2_frozen.py --db5-zip /caminho/DB5.zip --out results
python build_report.py
```

O script principal não contém fallback automático para shrinkage: qualquer instabilidade numérica real interrompe a execução, conforme protocolo congelado.
