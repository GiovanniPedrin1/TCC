# Relatório — Validação corrigida LDA na NinaPro DB5 (Exercise 2)

## Escopo e correção

Esta execução substitui integralmente a validação LDA anterior feita indevidamente em E1. Nenhum resultado LDA anterior foi reutilizado para seleção entre LDA-RMS e LDA-TD. Foram usados exclusivamente os arquivos `Sx_E2_A1.mat` dos 10 participantes. As repetições 2 e 5 permaneceram fora de segmentação, features, normalização, treinamento, validação e escolha do pipeline.

## Auditoria dos arquivos E2

Todos os 10 arquivos carregados foram `Sx_E2_A1.mat`. Em todos os participantes, os valores brutos encontrados em `restimulus` foram:

`0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17`

Após a seleção de classes do experimento, o conjunto de rótulos foi exatamente `{0, 1, 5, 6}` em todos os participantes. Em todos os arquivos, `rerepetition` continha `0,1,2,3,4,5,6`; apenas `1,3,4,6` foram admitidas no conjunto de janelas desta etapa.

| Participante | Arquivo E2 | restimulus bruto | Alvos presentes |
|---:|---|---|---|
| 1 | `S1_E2_A1.mat` | 0–17 | 0,1,5,6 |
| 2 | `S2_E2_A1.mat` | 0–17 | 0,1,5,6 |
| 3 | `S3_E2_A1.mat` | 0–17 | 0,1,5,6 |
| 4 | `S4_E2_A1.mat` | 0–17 | 0,1,5,6 |
| 5 | `S5_E2_A1.mat` | 0–17 | 0,1,5,6 |
| 6 | `S6_E2_A1.mat` | 0–17 | 0,1,5,6 |
| 7 | `S7_E2_A1.mat` | 0–17 | 0,1,5,6 |
| 8 | `S8_E2_A1.mat` | 0–17 | 0,1,5,6 |
| 9 | `S9_E2_A1.mat` | 0–17 | 0,1,5,6 |
| 10 | `S10_E2_A1.mat` | 0–17 | 0,1,5,6 |

## Verificações obrigatórias

- **E2 exclusivamente:** aprovado nos 10 participantes.
- **Classes selecionadas:** exatamente 0, 1, 5 e 6.
- **Repetições 2 e 5:** ausentes de todas as janelas e, consequentemente, de features, normalização, treino e validação.
- **Fronteiras:** cada janela de 40 amostras foi validada para conter uma única classe e uma única repetição.
- **Z-score:** média e desvio-padrão ajustados exclusivamente nas repetições 1, 3 e 4 e reaplicados à repetição 6.
- **Priors:** `[0.25, 0.25, 0.25, 0.25]` verificados no modelo ajustado.
- **Mesmas janelas/canais:** RMS e TD recebem os mesmos IDs de janela e os mesmos subconjuntos de canais.
- **Shrinkage:** 0/80 configurações.
- **Salvaguarda de σ≈0:** 0 dimensões.
- **Subamostragem do repouso:** não acionada; o protocolo principal foi mantido.

## Resultado agregado da validação (repetição 6)

| Canais | Pipeline | Macro-F1 (média ± DP) | Balanced accuracy (média ± DP) | Acurácia (média ± DP) |
|---:|---|---:|---:|---:|
| 1 | LDA-RMS | 0,4575 ± 0,0807 | 0,5020 ± 0,0883 | 0,8253 ± 0,1440 |
| 1 | LDA-TD | 0,5204 ± 0,0938 | 0,5593 ± 0,0791 | 0,8473 ± 0,1319 |
| 2 | LDA-RMS | 0,6325 ± 0,1234 | 0,6631 ± 0,1067 | 0,8832 ± 0,1122 |
| 2 | LDA-TD | 0,6506 ± 0,0895 | 0,6808 ± 0,0838 | 0,9063 ± 0,0735 |
| 4 | LDA-RMS | 0,7922 ± 0,0527 | 0,7805 ± 0,0381 | 0,9626 ± 0,0184 |
| 4 | LDA-TD | 0,7924 ± 0,0586 | 0,7760 ± 0,0549 | 0,9618 ± 0,0212 |
| 8 | LDA-RMS | 0,8374 ± 0,0646 | 0,8175 ± 0,0545 | 0,9687 ± 0,0226 |
| 8 | LDA-TD | 0,8524 ± 0,0555 | 0,8316 ± 0,0519 | 0,9720 ± 0,0186 |

### Comparação direta de Macro-F1

| Canais | LDA-RMS | LDA-TD | Δ TD−RMS | TD melhor (participantes) | RMS melhor |
|---:|---:|---:|---:|---:|---:|
| 1 | 0,4575 | 0,5204 | 0,0629 | 9/10 | 1/10 |
| 2 | 0,6325 | 0,6506 | 0,0181 | 7/10 | 3/10 |
| 4 | 0,7922 | 0,7924 | 0,0002 | 5/10 | 5/10 |
| 8 | 0,8374 | 0,8524 | 0,0150 | 7/10 | 3/10 |

O ganho do TD é mais pronunciado em 1 canal (+0,0629 de Macro-F1). Em 2 canais a vantagem média é pequena (+0,0181), em 4 canais há essencialmente empate (+0,0002) e em 8 canais o TD apresenta vantagem modesta (+0,0150). A análise pareada exploratória de Wilcoxon foi registrada em `pipeline_comparison.csv`; ela não foi usada como novo critério de tuning.

## F1 por classe

| Canais | Pipeline | Repouso | Thumbs up | Mão aberta | Mão fechada |
|---:|---|---:|---:|---:|---:|
| 1 | LDA-RMS | 0,9129 | 0,1625 | 0,2750 | 0,4793 |
| 1 | LDA-TD | 0,9251 | 0,2915 | 0,3467 | 0,5182 |
| 2 | LDA-RMS | 0,9425 | 0,3868 | 0,6452 | 0,5555 |
| 2 | LDA-TD | 0,9583 | 0,4236 | 0,6311 | 0,5896 |
| 4 | LDA-RMS | 0,9867 | 0,6628 | 0,7969 | 0,7222 |
| 4 | LDA-TD | 0,9859 | 0,6594 | 0,7795 | 0,7448 |
| 8 | LDA-RMS | 0,9874 | 0,7492 | 0,8314 | 0,7817 |
| 8 | LDA-TD | 0,9887 | 0,7623 | 0,8331 | 0,8253 |

## Confusão mão fechada ↔ thumbs up

As taxas abaixo são médias entre participantes:

| Canais | Pipeline | Fechada→Thumbs | Thumbs→Fechada |
|---:|---|---:|---:|
| 1 | LDA-RMS | 0,1964 | 0,2575 |
| 1 | LDA-TD | 0,2485 | 0,1776 |
| 2 | LDA-RMS | 0,2062 | 0,1369 |
| 2 | LDA-TD | 0,2180 | 0,0796 |
| 4 | LDA-RMS | 0,2170 | 0,0252 |
| 4 | LDA-TD | 0,1918 | 0,0148 |
| 8 | LDA-RMS | 0,1835 | 0,0150 |
| 8 | LDA-TD | 0,1507 | 0,0037 |

### Matriz agregada — 8 canais — LDA-RMS

| Real \ Predita | Repouso | Thumbs | Aberta | Fechada |
|---|---:|---:|---:|---:|
| Repouso | 98.8% | 0.9% | 0.2% | 0.1% |
| Thumbs | 16.1% | 80.7% | 1.8% | 1.3% |
| Aberta | 15.5% | 5.6% | 78.9% | 0.0% |
| Fechada | 11.2% | 18.2% | 4.3% | 66.3% |

### Matriz agregada — 8 canais — LDA-TD

| Real \ Predita | Repouso | Thumbs | Aberta | Fechada |
|---|---:|---:|---:|---:|
| Repouso | 99.0% | 0.7% | 0.2% | 0.0% |
| Thumbs | 17.2% | 81.0% | 1.6% | 0.3% |
| Aberta | 14.5% | 6.6% | 78.9% | 0.0% |
| Fechada | 9.2% | 15.8% | 4.0% | 71.0% |

Em 8 canais, a confusão fechada→thumbs é menor no TD (média entre participantes 15,07%) do que no RMS (18,35%). Na direção inversa, thumbs→fechada também é menor no TD (0,37%) que no RMS (1,50%). Nas matrizes agregadas, as taxas correspondentes são 15,84% vs. 18,15% para fechada→thumbs e 0,26% vs. 1,32% para thumbs→fechada.

## Resultados individuais

O arquivo `results_by_subject.csv` contém todas as 80 combinações participante × canais × pipeline, com Macro-F1, balanced accuracy, acurácia, F1 por classe, confusões específicas, flags de shrinkage, salvaguardas de σ e priors. O arquivo `macro_f1_by_subject_wide.csv` fornece uma visão compacta de Macro-F1 por participante.

## Baseline Threshold/Hamming

Não foi localizado, entre os artefatos disponíveis nesta execução, um conjunto de resultados congelados do baseline Threshold/Hamming em E2 que pudesse ser comparado de forma auditável. O baseline não foi refeito nem otimizado a partir destes resultados LDA. Assim, a tabela conjunta Threshold/Hamming × LDA-RMS × LDA-TD fica pendente até que o artefato original do baseline congelado seja fornecido.

## Resultados medidos — síntese

- O TD apresentou Macro-F1 médio superior ao RMS em 1, 2 e 8 canais; em 4 canais os resultados foram praticamente idênticos.
- A maior diferença ocorreu em 1 canal (+0,0629).
- Em 8 canais, TD atingiu 0,8524 ± 0,0555 contra 0,8374 ± 0,0646 do RMS.
- Em 8 canais, o principal ganho de classe do TD foi em mão fechada (F1 0,8253 vs. 0,7817).
- Nenhuma configuração exigiu shrinkage ou correção de σ.

## Recomendação técnica (separada dos resultados medidos)

Para congelar **um único pipeline ML válido para 1/2/4/8 canais**, a evidência desta validação corrigida em E2 favorece **LDA-TD**: ele tem Macro-F1 médio maior em três das quatro configurações e empate prático em 4 canais, além de reduzir a confusão fechada→thumbs na condição de 8 canais. A vantagem é especialmente relevante em 1 canal e modesta em 2 e 8 canais.

A ressalva de complexidade permanece: LDA-RMS usa 1/2/4/8 dimensões, enquanto LDA-TD usa 3/6/12/24. Portanto, para uma aplicação restrita especificamente a 4 canais — onde a validação foi essencialmente equivalente — o RMS mantém vantagem de simplicidade. Essa consideração não altera o resultado medido; apenas qualifica a decisão de engenharia.

**O teste final nas repetições 2 e 5 não foi executado nesta correção.**