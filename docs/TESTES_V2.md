# Auditoria da V2 — reexecução do protocolo congelado

**Data:** 11 de novembro de 2026. **Fonte de dados:** ZIP fornecido pelo autor com os dez arquivos internos `s1.zip` a `s10.zip` (Exercise 2, `Sx_E2_A1.mat`). Os dados brutos permaneceram fora do repositório.

## Ambiente efetivamente utilizado

- CPython 3.13.5 em Linux x86_64.
- NumPy 2.3.5; pandas 2.2.3; SciPy 1.17.0; scikit-learn 1.8.0; Matplotlib 3.10.8; tabulate 0.10.0.
- Execução de aprendizado de máquina com `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1` e `MKL_NUM_THREADS=1`.
- Teste de compatibilidade de versões: `python verificar_ambiente.py` → **OK**.
- As versões do ambiente histórico original são desconhecidas. O arquivo de requisitos travados apenas fixa dependências diretas deste ambiente reexecutado, não as transitivas.

## Comandos para reproduzir a auditoria

```bash
python -m unittest discover -s tests -v
python -W error e2_validation/run_lda_e2_validation.py --db5-zip /caminho/DB5.zip --out reproducoes/validacao_lda
python -W error e2_validation/run_threshold_e2_validation.py --db5-zip /caminho/DB5.zip --out reproducoes/validacao_threshold
python -W error e2_final/run_final_e2_frozen.py --db5-zip /caminho/DB5.zip --out reproducoes/final
python verificar_reproducao.py --final reproducoes/final --validacao-lda reproducoes/validacao_lda --validacao-threshold reproducoes/validacao_threshold
python e2_final/build_report.py --results reproducoes/final --out reproducoes/relatorio
python analises/bootstrap/recalcular_bootstrap_etapa2.py --csv reproducoes/final/final_results_by_subject.csv --out reproducoes/bootstrap.csv
```

As saídas do projeto são preservadas em diretórios próprios. Use `reproducoes/` para não sobrescrever os arquivos históricos. A execução com `-W error` transforma avisos em erros de execução e foi concluída com sucesso.

## Comparações verificadas

| Evidência | Resultado |
| --- | --- |
| Teste final (11 arquivos CSV/JSON) | 11/11 idênticos byte a byte |
| Validação LDA (7 arquivos CSV/JSON) | 7/7 idênticos byte a byte |
| Validação Threshold/Hamming (6 arquivos CSV/JSON) | 6/6 idênticos byte a byte |
| `e2_final/FINAL_REPORT.md` | Idêntico byte a byte ao regenerado |
| `e2_final/macro_f1_vs_channels.png` | Idêntico byte a byte ao regenerado |
| Bootstrap exploratório, 9 linhas | Mesmos valores numéricos |
| Testes unitários para rejeições | 5/5 aprovados |

As 24 comparações se referem aos arquivos **efetivamente criados pelos scripts de validação e teste final**. Outros arquivos históricos, como a consolidação `comparison/`, foram mantidos intactos, mas não reconstruídos integralmente nesta V2.

## Métricas centrais (macro-F1 médio entre participantes)

| Canais | Threshold/Hamming | LDA-RMS | LDA-TD |
| ---: | ---: | ---: | ---: |
| 1 | 0,189574 | 0,490507 | 0,529782 |
| 2 | 0,325546 | 0,639979 | 0,667827 |
| 4 | 0,520164 | 0,778337 | 0,785100 |
| 8 | 0,681966 | 0,828230 | 0,840379 |

Nenhuma alteração de parâmetros foi necessária para obter os resultados. Os resultados do experimento final e de ambas as validações coincidiram exatamente em seus arquivos de saída, apesar das correções nos avisos.

## Limitações

1. Os arquivos de entrada foram fornecidos pelo autor; não houve conferência externa dos hashes da base contra a distribuição original da NinaPro.
2. A correspondência obtida em Python 3.13.5 não garante a mesma identidade de bytes em todo sistema operacional ou versão numérica.
3. O relatório e o gráfico são derivados da execução final; a análise bootstrap é exploratória posterior e não constitui teste confirmatório.
4. Não há script de reprodução integral de todos os arquivos históricos de `comparison/`.
5. Os resultados são de um experimento com os dez participantes disponíveis na DB5 e quatro classes selecionadas; não devem ser generalizados a todos os movimentos ou condições de aquisição.
