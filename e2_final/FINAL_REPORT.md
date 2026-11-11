# Teste final congelado — NinaPro DB5 E2

## Escopo e integridade do protocolo

O teste final foi executado com o protocolo previamente congelado, usando exclusivamente `Sx_E2_A1.mat` dos 10 participantes. O treino utilizou somente as repetições 1, 3 e 4 e o teste final somente as repetições 2 e 5. A repetição 6 foi excluída da segmentação, extração de features, normalização, treinamento e teste. Nenhum parâmetro, canal, feature, threshold ou modelo foi alterado após observar o teste.

Verificações: E2 exclusivo; classes {0,1,5,6}; janela 40 amostras, passo 20; nenhuma janela atravessa classe/repetição; thresholds calculados somente com repouso do treino; z-score ajustado somente no treino; priors LDA exatamente 0,25 por classe; mesmos canais e identidades de janela entre os três métodos. Não houve shrinkage, subamostragem, salvaguarda de desvio-padrão nem instabilidade numérica.

## 1. Resultados medidos

### Macro-F1 — métrica principal

|   Canais | Threshold/Hamming   | LDA-RMS         | LDA-TD          | Δ TD−Threshold   | Δ TD−RMS   |
|---------:|:--------------------|:----------------|:----------------|:-----------------|:-----------|
|        1 | 0,1896 ± 0,0835     | 0,4905 ± 0,0885 | 0,5298 ± 0,0907 | 0,3402           | 0,0393     |
|        2 | 0,3255 ± 0,0890     | 0,6400 ± 0,1228 | 0,6678 ± 0,1009 | 0,3423           | 0,0278     |
|        4 | 0,5202 ± 0,2084     | 0,7783 ± 0,0564 | 0,7851 ± 0,0540 | 0,2649           | 0,0068     |
|        8 | 0,6820 ± 0,1707     | 0,8282 ± 0,0481 | 0,8404 ± 0,0423 | 0,1584           | 0,0121     |

O LDA-TD apresentou o maior macro-F1 médio nas quatro configurações. A vantagem sobre LDA-RMS foi +0,0393, +0,0278, +0,0068 e +0,0121 para 1, 2, 4 e 8 canais, respectivamente. O ganho do LDA-TD sobre Threshold/Hamming foi substancialmente maior: +0,3402, +0,3423, +0,2649 e +0,1584.

### Balanced accuracy e acurácia global

|   Canais | Método            | Balanced accuracy   | Acurácia        |
|---------:|:------------------|:--------------------|:----------------|
|        1 | Threshold/Hamming | 0,2041 ± 0,0787     | 0,5437 ± 0,4565 |
|        1 | LDA-RMS           | 0,5360 ± 0,0829     | 0,8418 ± 0,1171 |
|        1 | LDA-TD            | 0,5681 ± 0,0780     | 0,8531 ± 0,1144 |
|        2 | Threshold/Hamming | 0,3473 ± 0,0772     | 0,5559 ± 0,4516 |
|        2 | LDA-RMS           | 0,6706 ± 0,0959     | 0,8851 ± 0,0911 |
|        2 | LDA-TD            | 0,6924 ± 0,0726     | 0,9045 ± 0,0681 |
|        4 | Threshold/Hamming | 0,5153 ± 0,2169     | 0,9210 ± 0,0344 |
|        4 | LDA-RMS           | 0,7717 ± 0,0649     | 0,9578 ± 0,0172 |
|        4 | LDA-TD            | 0,7754 ± 0,0627     | 0,9574 ± 0,0211 |
|        8 | Threshold/Hamming | 0,6609 ± 0,1476     | 0,9436 ± 0,0154 |
|        8 | LDA-RMS           | 0,8144 ± 0,0441     | 0,9647 ± 0,0229 |
|        8 | LDA-TD            | 0,8249 ± 0,0323     | 0,9673 ± 0,0206 |

A acurácia global é apresentada apenas como auxiliar devido à forte predominância do repouso. A balanced accuracy acompanha melhor o comportamento das quatro classes.

### F1 por classe

|   Canais | Método            | Repouso         | Thumbs up       | Mão aberta      | Mão fechada     |
|---------:|:------------------|:----------------|:----------------|:----------------|:----------------|
|        1 | Threshold/Hamming | 0,5900 ± 0,5078 | 0,0000 ± 0,0000 | 0,0484 ± 0,1532 | 0,1199 ± 0,2527 |
|        1 | LDA-RMS           | 0,9257 ± 0,0762 | 0,2067 ± 0,1348 | 0,3250 ± 0,1819 | 0,5047 ± 0,1750 |
|        1 | LDA-TD            | 0,9306 ± 0,0757 | 0,2835 ± 0,1152 | 0,4022 ± 0,1520 | 0,5029 ± 0,1954 |
|        2 | Threshold/Hamming | 0,5887 ± 0,5067 | 0,3127 ± 0,3326 | 0,2174 ± 0,2984 | 0,1834 ± 0,3006 |
|        2 | LDA-RMS           | 0,9454 ± 0,0560 | 0,4044 ± 0,1983 | 0,6096 ± 0,2293 | 0,6005 ± 0,1428 |
|        2 | LDA-TD            | 0,9564 ± 0,0394 | 0,4458 ± 0,1723 | 0,6527 ± 0,1746 | 0,6164 ± 0,1456 |
|        4 | Threshold/Hamming | 0,9830 ± 0,0091 | 0,5281 ± 0,2483 | 0,2946 ± 0,3413 | 0,2749 ± 0,3394 |
|        4 | LDA-RMS           | 0,9843 ± 0,0092 | 0,6698 ± 0,0696 | 0,7449 ± 0,1404 | 0,7143 ± 0,1056 |
|        4 | LDA-TD            | 0,9834 ± 0,0116 | 0,6636 ± 0,0867 | 0,7606 ± 0,1312 | 0,7327 ± 0,0932 |
|        8 | Threshold/Hamming | 0,9856 ± 0,0062 | 0,5699 ± 0,2103 | 0,6335 ± 0,2857 | 0,5389 ± 0,3629 |
|        8 | LDA-RMS           | 0,9857 ± 0,0127 | 0,7220 ± 0,0921 | 0,8290 ± 0,0718 | 0,7762 ± 0,0787 |
|        8 | LDA-TD            | 0,9869 ± 0,0108 | 0,7431 ± 0,0927 | 0,8390 ± 0,0603 | 0,7924 ± 0,0708 |

Em 8 canais, o LDA-TD atingiu F1 médio de repouso=0,9869, thumbs up=0,7431, mão aberta=0,8390, mão fechada=0,7924.

### Confusão mão fechada ↔ thumbs up

|   Canais | Método            | Fechada→Thumbs   | Thumbs→Fechada   |
|---------:|:------------------|:-----------------|:-----------------|
|        1 | Threshold/Hamming | 0,0000 ± 0,0000  | 0,0324 ± 0,0754  |
|        1 | LDA-RMS           | 0,1730 ± 0,1210  | 0,2626 ± 0,2233  |
|        1 | LDA-TD            | 0,1929 ± 0,0958  | 0,2118 ± 0,1526  |
|        2 | Threshold/Hamming | 0,0882 ± 0,1679  | 0,0094 ± 0,0296  |
|        2 | LDA-RMS           | 0,1959 ± 0,0939  | 0,1159 ± 0,2003  |
|        2 | LDA-TD            | 0,1830 ± 0,0962  | 0,0818 ± 0,1388  |
|        4 | Threshold/Hamming | 0,1043 ± 0,1695  | 0,0113 ± 0,0296  |
|        4 | LDA-RMS           | 0,1847 ± 0,0572  | 0,0468 ± 0,0941  |
|        4 | LDA-TD            | 0,1674 ± 0,0808  | 0,0261 ± 0,0464  |
|        8 | Threshold/Hamming | 0,1321 ± 0,1847  | 0,0326 ± 0,0571  |
|        8 | LDA-RMS           | 0,1683 ± 0,0729  | 0,0368 ± 0,0673  |
|        8 | LDA-TD            | 0,1605 ± 0,0904  | 0,0238 ± 0,0389  |

A confusão permaneceu assimétrica: em geral, mão fechada → thumbs up foi mais frequente que thumbs up → mão fechada. Em 8 canais, as médias foram 16,05% vs 2,38% no LDA-TD; 16,83% vs 3,68% no LDA-RMS; e 13,21% vs 3,26% no Threshold/Hamming. No baseline, taxas baixas de confusão direta devem ser interpretadas junto com as rejeições, pois uma amostra rejeitada continua sendo erro para macro-F1.

### Rejeição do Threshold/Hamming

|   Canais | Rejeição        | Cobertura       | Acurácia não rejeitadas   |
|---------:|:----------------|:----------------|:--------------------------|
|        1 | 0,4381 ± 0,4582 | 0,5619 ± 0,4582 | 0,8103 ± 0,2615           |
|        2 | 0,4160 ± 0,4477 | 0,5840 ± 0,4477 | 0,7824 ± 0,2502           |
|        4 | 0,0501 ± 0,0467 | 0,9499 ± 0,0467 | 0,9702 ± 0,0189           |
|        8 | 0,0282 ± 0,0155 | 0,9718 ± 0,0155 | 0,9711 ± 0,0117           |

A rejeição é particularmente alta em 1 e 2 canais. A acurácia nas amostras não rejeitadas é secundária e não substitui macro-F1, pois ignora justamente os casos em que o baseline ficou indeterminado.

### Evolução com o número de canais

- **Threshold/Hamming:** 1→2 0,1360, 2→4 0,1946, 4→8 0,1618; ganho total 1→8 = 0,4924.
- **LDA-RMS:** 1→2 0,1495, 2→4 0,1384, 4→8 0,0499; ganho total 1→8 = 0,3377.
- **LDA-TD:** 1→2 0,1380, 2→4 0,1173, 4→8 0,0553; ganho total 1→8 = 0,3106.

O ganho de desempenho com mais canais é claro nos três métodos. A diferença entre os LDAs diminui bastante em 4 e 8 canais, enquanto a distância entre os LDAs e o baseline também se reduz com mais canais, mas permanece relevante em 8 canais.

### Resultados individuais — macro-F1

|   Participante |   1ch Threshold/Hamming |   1ch LDA-RMS |   1ch LDA-TD |   2ch Threshold/Hamming |   2ch LDA-RMS |   2ch LDA-TD |   4ch Threshold/Hamming |   4ch LDA-RMS |   4ch LDA-TD |   8ch Threshold/Hamming |   8ch LDA-RMS |   8ch LDA-TD |
|---------------:|------------------------:|--------------:|-------------:|------------------------:|--------------:|-------------:|------------------------:|--------------:|-------------:|------------------------:|--------------:|-------------:|
|         1.0000 |                  0.2433 |        0.5389 |       0.6102 |                  0.3935 |        0.8007 |       0.7875 |                  0.3020 |        0.8260 |       0.8211 |                  0.8097 |        0.8839 |       0.8758 |
|         2.0000 |                  0.1515 |        0.4331 |       0.4537 |                  0.3096 |        0.6892 |       0.7259 |                  0.8214 |        0.8050 |       0.8296 |                  0.8007 |        0.8823 |       0.8923 |
|         3.0000 |                  0.2482 |        0.4731 |       0.5453 |                  0.4140 |        0.5048 |       0.5733 |                  0.4070 |        0.7042 |       0.7002 |                  0.4109 |        0.7546 |       0.7887 |
|         4.0000 |                  0.2471 |        0.4471 |       0.4863 |                  0.2457 |        0.5954 |       0.6493 |                  0.2462 |        0.6846 |       0.7181 |                  0.3663 |        0.8157 |       0.8454 |
|         5.0000 |                  0.2467 |        0.6131 |       0.6340 |                  0.4246 |        0.8446 |       0.8441 |                  0.3893 |        0.8478 |       0.8357 |                  0.8268 |        0.8454 |       0.8383 |
|         6.0000 |                  0.0000 |        0.3757 |       0.3447 |                  0.1667 |        0.5718 |       0.5593 |                  0.6106 |        0.7522 |       0.7503 |                  0.6677 |        0.7461 |       0.7591 |
|         7.0000 |                  0.1481 |        0.4390 |       0.5255 |                  0.2362 |        0.4922 |       0.5685 |                  0.5970 |        0.7918 |       0.8037 |                  0.6905 |        0.8151 |       0.8154 |
|         8.0000 |                  0.1211 |        0.4504 |       0.4927 |                  0.2894 |        0.5249 |       0.5712 |                  0.6541 |        0.7437 |       0.7427 |                  0.6274 |        0.8636 |       0.8765 |
|         9.0000 |                  0.2437 |        0.4714 |       0.5668 |                  0.3800 |        0.6658 |       0.6842 |                  0.3561 |        0.7829 |       0.7918 |                  0.7811 |        0.8215 |       0.8413 |
|        10.0000 |                  0.2459 |        0.6631 |       0.6387 |                  0.3957 |        0.7105 |       0.7149 |                  0.8180 |        0.8452 |       0.8579 |                  0.8387 |        0.8542 |       0.8710 |

A tabela completa por participante, incluindo balanced accuracy, acurácia, F1 por classe, confusões direcionais e métricas de rejeição/cobertura, está em `results/final_results_by_subject.csv`.

### Matrizes de confusão

Foram exportadas matrizes por participante e método, além de matrizes agregadas em contagens e normalizadas por linha para 1/2/4/8 canais. As matrizes agregadas servem apenas como descrição do padrão de erros; as métricas principais continuam sendo calculadas por participante e depois resumidas por média ± desvio-padrão.

**8 canais — Threshold/Hamming, proporções por classe real**

|             |   Repouso |   Thumbs up |   Mão aberta |   Mão fechada |   Rejeição |
|:------------|----------:|------------:|-------------:|--------------:|-----------:|
| Repouso     |    0.9825 |      0.0038 |       0.0038 |        0.0003 |     0.0095 |
| Thumbs up   |    0.1880 |      0.5369 |       0.0123 |        0.0307 |     0.2322 |
| Mão aberta  |    0.0909 |      0.0438 |       0.6461 |        0.0308 |     0.1883 |
| Mão fechada |    0.0512 |      0.1296 |       0.1072 |        0.4944 |     0.2176 |

**8 canais — LDA-RMS, proporções por classe real**

|             |   Repouso |   Thumbs up |   Mão aberta |   Mão fechada |
|:------------|----------:|------------:|-------------:|--------------:|
| Repouso     |    0.9852 |      0.0124 |       0.0017 |        0.0007 |
| Thumbs up   |    0.1548 |      0.7998 |       0.0160 |        0.0295 |
| Mão aberta  |    0.1494 |      0.0471 |       0.8036 |        0.0000 |
| Mão fechada |    0.0896 |      0.1680 |       0.0656 |        0.6768 |

**8 canais — LDA-TD, proporções por classe real**

|             |   Repouso |   Thumbs up |   Mão aberta |   Mão fechada |
|:------------|----------:|------------:|-------------:|--------------:|
| Repouso     |    0.9868 |      0.0111 |       0.0012 |        0.0008 |
| Thumbs up   |    0.1536 |      0.8108 |       0.0160 |        0.0197 |
| Mão aberta  |    0.1396 |      0.0503 |       0.8084 |        0.0016 |
| Mão fechada |    0.0816 |      0.1600 |       0.0624 |        0.6960 |

## 2. Interpretação

O resultado do teste final confirma o padrão observado na validação sem exigir qualquer alteração do protocolo. O ganho mais importante é a passagem do Threshold/Hamming para um classificador LDA supervisionado; a inclusão de MAV e WL sobre o RMS acrescenta um ganho adicional menor, mas positivo em média nas quatro configurações. Em 4 canais, LDA-RMS e LDA-TD permanecem muito próximos. Em 8 canais, o LDA-TD mantém vantagem modesta no macro-F1 e melhora, em média, os F1 de thumbs up, mão aberta e mão fechada.

O baseline melhora substancialmente à medida que o número de canais aumenta e sua taxa de rejeição cai para cerca de 2,8% em 8 canais. Ainda assim, seu macro-F1 médio em 8 canais fica abaixo dos dois LDAs. A alta acurácia condicional entre amostras não rejeitadas mostra que a rejeição funciona como mecanismo conservador, mas essa métrica não deve ser confundida com desempenho global.

## 3. Conclusão / recomendação

Com o protocolo congelado, **LDA-TD permanece o pipeline ML principal**. No teste final ele alcançou macro-F1 médio de 0,8404 ± 0,0423 em 8 canais, contra 0,8282 ± 0,0481 do LDA-RMS e 0,6820 ± 0,1707 do Threshold/Hamming. A vantagem do LDA-TD sobre LDA-RMS é consistente em média, porém modesta — especialmente em 4 e 8 canais — e deve ser descrita dessa forma no TCC. O LDA-RMS continua útil como ablação por demonstrar quanto do ganho vem do classificador supervisionado usando somente RMS; o ganho adicional de TD quantifica o efeito de enriquecer a representação com MAV e WL.

Nenhuma nova otimização deve ser realizada com base neste teste final.

## Arquivos de auditoria e reprodutibilidade

- `run_final_e2_frozen.py`: execução reproduzível do teste final congelado.
- `results/FINAL_PROTOCOL_AUDIT.json`: auditoria formal das regras congeladas.
- `results/raw_e2_audit.csv`: confirmação dos arquivos E2 e rótulos brutos.
- `results/window_audit.csv`: treino/teste e exclusão da repetição 6.
- `results/window_counts_by_subject_rep_class.csv`: contagens de janelas.
- `results/thresholds_and_templates_frozen.csv`: thresholds e templates do baseline.
- `results/final_results_by_subject.csv`: tabela individual completa.
- `results/final_summary_mean_std.csv`: média ± DP entre participantes.
- `results/confusion_matrices.json`: matrizes por participante/método.
- `macro_f1_vs_channels.png`: gráfico principal.