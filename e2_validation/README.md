# Validação metodológica E2 — NinaPro DB5

Este diretório documenta a validação LDA e oferece o script Threshold/Hamming.
Treino: repetições 1, 3, 4; validação: repetição 6; teste final 2 e 5 não utilizado.

Execute **a partir da raiz**, sem sobrescrever as saídas históricas:

```bash
python e2_validation/run_lda_e2_validation.py --db5-zip /caminho/DB5.zip --out reproducoes/validacao_lda
python e2_validation/run_threshold_e2_validation.py --db5-zip /caminho/DB5.zip --out reproducoes/validacao_threshold
```

Os arquivos originais LDA constam em `results/`; a saída histórica Threshold/Hamming está em `../threshold_results/`.
A pasta `../comparison/` contém a comparação conjunta já consolidada, sem script único de reconstrução nos materiais fornecidos.
Mais detalhes: `../docs/GUIA_REPRODUCAO.md`.
