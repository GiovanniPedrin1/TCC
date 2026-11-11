# Teste final congelado — NinaPro DB5 E2

Este diretório contém o script experimental original e as saídas já congeladas.
Treino: repetições 1, 3, 4. Teste final: 2, 5. Repetição 6: excluída.
Arquivos externos: Sx_E2_A1.mat dos dez participantes, dentro do DB5.zip.

Execute a partir da **raiz do repositório**, com saídas em pastas novas:

```bash
python e2_final/run_final_e2_frozen.py --db5-zip /caminho/DB5.zip --out reproducoes/e2_final/results
python e2_final/build_report.py --results reproducoes/e2_final/results --out reproducoes/e2_final
```

**Não execute com `--out e2_final/results`**: esta pasta contém registros históricos.
A segunda linha apenas gera relatório e figuras a partir dos resultados existentes.
O LDA do teste final não utiliza fallback automático para shrinkage; instabilidades reais interrompem a execução.
O ambiente de reexecução é posterior ao experimento; consulte `../docs/GUIA_REPRODUCAO.md`.
