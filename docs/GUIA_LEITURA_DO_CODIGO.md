# Guia de leitura do código — V2

Este documento explica onde encontrar as decisões técnicas do TCC sem exigir que o leitor comece pelos relatórios agregados. Os scripts foram mantidos próximos às versões que produziram os resultados históricos, para facilitar a auditoria por comparação.

## 1. Comece pelo protocolo

Leia `docs/PROTOCOLO_E_LIMITACOES.md`. Há três partições fixas: treino (repetições **1, 3, 4**), validação (**6**) e teste final (**2, 5**). A validação escolheu a configuração principal entre LDA-RMS e LDA-TD; **o teste final não serviu para escolher parâmetros**.

Os índices dos canais são de base zero em Python, mas de base um no texto do TCC: `0` corresponde ao canal 1, `[0, 4]` corresponde aos canais 1 e 5 etc.

## 2. Pipeline de teste final

Arquivo: `e2_final/run_final_e2_frozen.py`.

| Função | Papel |
| --- | --- |
| `_open_subject_inner` e `load_e2` | Localizam `sX.zip` no ZIP externo e carregam `Sx_E2_A1.mat` |
| `audit_raw` | Verifica nomes e variáveis dos arquivos de entrada |
| `segment_features` | Recorta janelas válidas de 40 amostras e calcula RMS, MAV e WL; exclui repetições 6 |
| `majority_bits` e `baseline_templates` | Constroem os templates binários com maioria estrita nas repetições de treino |
| `hamming_predict` | Escolhe a menor distância de Hamming; empate é `-1` |
| `design` | Constrói o vetor de entrada para LDA-RMS e LDA-TD |
| `zscore_train_only` | Ajusta média/desvio somente no treino e aplica o mesmo escalonamento ao teste |
| `fit_lda_strict` | Ajusta o LDA com priors 0,25 sem introduzir shrinkage como alternativa automática |
| `confusion_with_reject` | Matriz 4 × 5, incluindo a coluna de rejeição |
| `confusion_4` | Matriz parcial 4 × 4 das predições válidas |
| `balanced_accuracy_with_reject` | Recall médio das quatro classes, incluindo rejeições como erros |
| `metrics_common` | Macro-F1, F1 por classe, acurácia e confusões direcionais |
| `main` | Percorre os 10 participantes e as quatro configurações de canais e grava resultados |

A função `main` escreve os resultados individuais, agregados, matrizes e o arquivo `FINAL_PROTOCOL_AUDIT.json`. O segundo script, `e2_final/build_report.py`, **não treina modelos**: apenas transforma esses resultados em tabelas e figuras.

## 3. Validação

- `e2_validation/run_lda_e2_validation.py`: mesmas classes e canais, treino nas repetições 1/3/4 e validação exclusivamente na repetição 6. Compara LDA-RMS e LDA-TD e registra a utilização de shrinkage caso haja necessidade numérica na fase de validação (não observada na reexecução S1–S10).
- `e2_validation/run_threshold_e2_validation.py`: método Threshold/Hamming já definido; a validação não reajusta os limiares ou seleciona novas regras com base nos resultados. A V2 acrescentou o cálculo explícito da balanced accuracy para lidar com rejeições.

## 4. Como interpretar rejeições

- A classe `-1` é uma **saída**, não uma classe verdadeira da NinaPro. Uma janela rejeitada não é removida da avaliação.
- Para macro-F1, as quatro classes reais são avaliadas usando `zero_division=0`; rejeições entram como falsos negativos da classe correta.
- Para balanced accuracy, cada recall é `acertos_da_classe / total_de_janelas_reais_da_classe`. Uma rejeição reduz esse recall.
- Na matriz 4 × 4 sem coluna de rejeição, somar uma linha não fornece o total real da classe. Por isso `metrics_common` calcula os denominadores diretamente de `y`.
- `confusion_with_reject` preserva a quinta coluna descritiva, permitindo visualizar rejeições por classe.

Essas regras fazem parte do **protocolo original**, não são mudanças de critério introduzidas na V2. A alteração foi apenas na forma de calculá-las sem avisos numéricos.

## 5. Como auditar alterações futuras

1. Faça alterações numa cópia e execute `python -m unittest discover -s tests -v`.
2. Reexecute o fluxo de validação e o teste final em `reproducoes/`, nunca nas pastas congeladas.
3. Rode `python verificar_reproducao.py` com as saídas da nova execução. Qualquer diferença deve ser investigada e documentada; não a corrija ajustando números à mão.
4. Rode `python verificar_integridade.py` na distribuição original. O manifesto verifica os arquivos do pacote, não substitui a comparação com os resultados científicos.

Para distinguir evidência de reprodução e limitação, consulte `docs/TESTES_V2.md`.
