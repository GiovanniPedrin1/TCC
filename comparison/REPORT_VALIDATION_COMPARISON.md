# Relatório comparativo de validação — NinaPro DB5 E2

## Escopo
Comparação na repetição 6 entre o baseline congelado Threshold/Hamming, LDA-RMS e LDA-TD, usando exclusivamente E2. Treino: repetições 1, 3 e 4. As repetições 2 e 5 permaneceram intocadas. Nenhum parâmetro do baseline foi escolhido a partir dos resultados dos modelos LDA ou da validação.

### Implementação do baseline congelado
- RMS por canal nas mesmas janelas usadas pelos modelos LDA.
- Limiar individual por participante e canal: média do RMS de repouso no treino + 3 desvios-padrão.
- Binarização por canal: RMS > limiar.
- Para cada classe, template binário construído por maioria em cada repetição de treino e depois maioria entre os templates das repetições 1, 3 e 4.
- Classificação por menor distância de Hamming; empate entre classes = rejeição.
- Rejeições são mantidas como erros nas métricas e aparecem como coluna própria nas matrizes do baseline.

## Macro-F1 — comparação principal

| Canais | Threshold/Hamming | LDA-RMS | LDA-TD | Ganho RMS vs TH | Ganho TD vs TH | TD−RMS |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0,1911 | 0,4575 | 0,5204 | 0,2664 | 0,3292 | 0,0629 |
| 2 | 0,3171 | 0,6325 | 0,6506 | 0,3154 | 0,3335 | 0,0181 |
| 4 | 0,5320 | 0,7922 | 0,7924 | 0,2602 | 0,2604 | 0,0002 |
| 8 | 0,6800 | 0,8374 | 0,8524 | 0,1574 | 0,1724 | 0,0150 |

O ganho dos modelos supervisionados sobre Threshold/Hamming cresce em termos absolutos até 4 canais e permanece grande em 8 canais. O LDA-TD mantém a vantagem previamente observada sobre LDA-RMS em 1, 2 e 8 canais, com empate prático em 4 canais; a diferença TD−RMS é bem menor que a diferença de ambos os LDAs para o baseline.

## Balanced accuracy e acurácia auxiliar

| Canais | Método | Balanced accuracy (média ± DP) | Acurácia (média ± DP) | Rejeição |
|---:|---|---:|---:|---:|
| 1 | Threshold/Hamming | 0,2050 ± 0,0777 | 0,5458 ± 0,4584 | 43,71% |
| 1 | LDA-RMS | 0,5020 ± 0,0883 | 0,8253 ± 0,1440 | 0,00% |
| 1 | LDA-TD | 0,5593 ± 0,0791 | 0,8473 ± 0,1319 | 0,00% |
| 2 | Threshold/Hamming | 0,3458 ± 0,0808 | 0,5573 ± 0,4541 | 40,85% |
| 2 | LDA-RMS | 0,6631 ± 0,1067 | 0,8832 ± 0,1122 | 0,00% |
| 2 | LDA-TD | 0,6808 ± 0,0838 | 0,9063 ± 0,0735 | 0,00% |
| 4 | Threshold/Hamming | 0,5161 ± 0,2124 | 0,9249 ± 0,0315 | 4,90% |
| 4 | LDA-RMS | 0,7805 ± 0,0381 | 0,9626 ± 0,0184 | 0,00% |
| 4 | LDA-TD | 0,7760 ± 0,0549 | 0,9618 ± 0,0212 | 0,00% |
| 8 | Threshold/Hamming | 0,6520 ± 0,1327 | 0,9453 ± 0,0124 | 2,95% |
| 8 | LDA-RMS | 0,8175 ± 0,0545 | 0,9687 ± 0,0226 | 0,00% |
| 8 | LDA-TD | 0,8316 ± 0,0519 | 0,9720 ± 0,0186 | 0,00% |

A acurácia global permanece auxiliar por causa da predominância do repouso. No baseline, a taxa de rejeição é especialmente alta com poucos canais, o que contribui para o baixo Macro-F1 de 1–2 canais.

## F1 por classe

| Canais | Método | Repouso | Thumbs up | Mão aberta | Mão fechada |
|---:|---|---:|---:|---:|---:|
| 1 | Threshold/Hamming | 0,5897 | 0,0000 | 0,0455 | 0,1293 |
| 1 | LDA-RMS | 0,9129 | 0,1625 | 0,2750 | 0,4793 |
| 1 | LDA-TD | 0,9251 | 0,2915 | 0,3467 | 0,5182 |
| 2 | Threshold/Hamming | 0,5881 | 0,3042 | 0,1897 | 0,1865 |
| 2 | LDA-RMS | 0,9425 | 0,3868 | 0,6452 | 0,5555 |
| 2 | LDA-TD | 0,9583 | 0,4236 | 0,6311 | 0,5896 |
| 4 | Threshold/Hamming | 0,9830 | 0,5578 | 0,2507 | 0,3364 |
| 4 | LDA-RMS | 0,9867 | 0,6628 | 0,7969 | 0,7222 |
| 4 | LDA-TD | 0,9859 | 0,6594 | 0,7795 | 0,7448 |
| 8 | Threshold/Hamming | 0,9856 | 0,5669 | 0,6239 | 0,5436 |
| 8 | LDA-RMS | 0,9874 | 0,7492 | 0,8314 | 0,7817 |
| 8 | LDA-TD | 0,9887 | 0,7623 | 0,8331 | 0,8253 |

## Confusão mão fechada ↔ thumbs up

| Canais | Método | Fechada→Thumbs | Thumbs→Fechada |
|---:|---|---:|---:|
| 1 | Threshold/Hamming | 0,00% | 2,50% |
| 1 | LDA-RMS | 19,64% | 25,75% |
| 1 | LDA-TD | 24,85% | 17,76% |
| 2 | Threshold/Hamming | 9,32% | 0,00% |
| 2 | LDA-RMS | 20,62% | 13,69% |
| 2 | LDA-TD | 21,80% | 7,96% |
| 4 | Threshold/Hamming | 5,94% | 0,00% |
| 4 | LDA-RMS | 21,70% | 2,52% |
| 4 | LDA-TD | 19,18% | 1,48% |
| 8 | Threshold/Hamming | 8,49% | 5,62% |
| 8 | LDA-RMS | 18,35% | 1,50% |
| 8 | LDA-TD | 15,07% | 0,37% |

Em 8 canais, o LDA-TD reduz a confusão média fechada→thumbs em relação ao LDA-RMS. O baseline apresenta menos confusão direta em alguns cenários, mas isso deve ser interpretado junto com sua rejeição e seus F1 de classe: uma predição rejeitada não aparece como troca direta entre as duas classes, porém continua sendo erro.

## Matrizes de confusão agregadas — 8 canais

### Threshold/Hamming
| Real \ Predita | Repouso | Thumbs | Aberta | Fechada | Rejeição |
|---|---:|---:|---:|---:|---:|
| Repouso | 98,36% | 0,31% | 0,38% | 0,03% | 0,93% |
| Thumbs | 20,32% | 51,72% | 1,06% | 5,54% | 21,37% |
| Aberta | 12,50% | 1,97% | 60,20% | 0,99% | 24,34% |
| Fechada | 6,27% | 7,92% | 7,59% | 48,51% | 29,70% |

### LDA-RMS
| Real \ Predita | Repouso | Thumbs | Aberta | Fechada |
|---|---:|---:|---:|---:|
| Repouso | 98,85% | 0,92% | 0,18% | 0,06% |
| Thumbs | 16,09% | 80,74% | 1,85% | 1,32% |
| Aberta | 15,46% | 5,59% | 78,95% | 0,00% |
| Fechada | 11,22% | 18,15% | 4,29% | 66,34% |

### LDA-TD
| Real \ Predita | Repouso | Thumbs | Aberta | Fechada |
|---|---:|---:|---:|---:|
| Repouso | 99,05% | 0,75% | 0,17% | 0,04% |
| Thumbs | 17,15% | 81,00% | 1,58% | 0,26% |
| Aberta | 14,47% | 6,58% | 78,95% | 0,00% |
| Fechada | 9,24% | 15,84% | 3,96% | 70,96% |

## Variação do ganho de ML com o número de canais

- **1 canal(is):** LDA-RMS +0,2664 e LDA-TD +0,3292 de Macro-F1 sobre Threshold/Hamming.
- **2 canal(is):** LDA-RMS +0,3154 e LDA-TD +0,3335 de Macro-F1 sobre Threshold/Hamming.
- **4 canal(is):** LDA-RMS +0,2602 e LDA-TD +0,2604 de Macro-F1 sobre Threshold/Hamming.
- **8 canal(is):** LDA-RMS +0,1574 e LDA-TD +0,1724 de Macro-F1 sobre Threshold/Hamming.

O incremento mais importante não é apenas TD versus RMS, mas a passagem do baseline binário para classificação supervisionada contínua. Em 4 e 8 canais, ambos os LDAs se afastam claramente do baseline; TD acrescenta um ganho adicional geralmente modesto em relação ao RMS.

## Verificações de integridade
- E2 exclusivamente nos 10 participantes.
- Classes 0, 1, 5 e 6.
- Treino 1/3/4 e validação 6; 2/5 ausentes da segmentação e da comparação.
- Mesmas contagens de janelas por participante/configuração entre Threshold/Hamming e LDA.
- Baseline usa somente RMS de treino para limiar e templates; nenhum parâmetro usa validação.
- LDA mantém z-score ajustado somente no treino e priors 0,25; nenhum shrinkage.

## Resultados medidos — síntese
- Em 8 canais, Macro-F1 médio: Threshold/Hamming 0,6800, LDA-RMS 0,8374, LDA-TD 0,8524.
- LDA-TD apresenta vantagem consistente, porém geralmente modesta, sobre LDA-RMS: maior em 1 canal, pequena em 2 e 8, e praticamente nula em 4 canais.
- O ganho de ambos os LDAs sobre Threshold/Hamming é substancialmente maior que a diferença entre os dois pipelines LDA.

## Recomendação técnica — separada dos resultados
Manter **LDA-TD (RMS + MAV + WL)** congelado como pipeline ML principal, com LDA-RMS como ablação interna. A comparação com o baseline reforça que o principal ganho vem do classificador supervisionado sobre features contínuas; TD oferece ganho adicional menor, mas consistente em três das quatro configurações. Nenhum resultado desta comparação justifica alterar janela, overlap, canais, normalização, priors, split ou abrir as repetições 2 e 5.

**As repetições 2 e 5 não foram executadas nem analisadas.**