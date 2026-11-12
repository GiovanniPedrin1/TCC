# Protocolo, métricas e limitações

Esta página descreve o material disponibilizado e deve ser lida em conjunto com o TCC.

## Partições e canais

- Dez participantes, exercício E2 (`Sx_E2_A1.mat`).
- Treino: repetições 1, 3 e 4; validação: repetição 6; teste final: repetições 2 e 5.
- Quatro classes: {0, 1, 5, 6} (repouso, polegar levantado, mão aberta e mão fechada).
- Janelas de 40 amostras, passo de 20 amostras; os scripts as formam dentro de segmentos contíguos de classe e repetição.
- Subconjuntos fixos de canais: 1=[0], 2=[0,4], 4=[0,2,4,6], 8=[0,1,2,3,4,5,6,7] (índices Python de base zero).

## Métodos

- **Threshold/Hamming:** RMS por canal, limiares individualizados de repouso (`μ+3σ`) e templates binários por maioria nas repetições de treino; menor distância de Hamming. Empates resultam na **rejeição** identificada por -1, que não é classe verdadeira. Rejeições contam como erro no cálculo das métricas principais.
- **LDA-RMS:** classificador LDA aplicado às características RMS por canal.
- **LDA-TD:** classificador LDA aplicado às características temporais empregadas no script (RMS, MAV e WL, conforme implementação do protocolo); consulte `run_final_e2_frozen.py` para definição exata.
- **Macro-F1:** média não ponderada do F1 das quatro classes, com cálculo por participante e configuração; a média principal entre participantes é descrita no TCC. A acurácia global é auxiliar por causa do desequilíbrio de repouso.

## Métricas com rejeição: detalhe importante da V2

Quando o Threshold/Hamming atribui `-1`, a amostra não recebe uma das quatro classes reais. O macro-F1 continua sendo calculado para `labels=[0, 1, 5, 6]` com `zero_division=0`; a amostra rejeitada contribui como erro da classe verdadeira. A *balanced accuracy* corresponde à média dos recalls das quatro classes reais, calculados sobre **todas as observações da classe**, rejeitadas ou não. As taxas direcionais de confusão usam o mesmo denominador correto: o total da classe verdadeira, sem omitir rejeições.

A V2 expressa essas regras diretamente no código, sem depender de uma chamada que produz um aviso quando a predição `-1` está ausente em `y_true`. São formulas equivalentes às aplicadas no experimento original; **as saídas reproduzidas foram idênticas byte a byte**.

## Rastreabilidade e limites

- Os CSVs, JSONs, figuras e relatórios **históricos** permanecem sem alterações em relação ao TCC.
- A V2 alterou as funções de avaliação com rejeição em dois scripts e adicionou testes e um verificador de reprodução, sem mudar o protocolo nem as saídas científicas.
- A reexecução com S1–S10 foi realizada em Python 3.13.5. O `requirements.txt` fixa as versões **efetivamente usadas nessa reexecução**; as versões do ambiente histórico permanecem desconhecidas.
- O manifesto atualizado (`docs/MANIFESTO_SHA256.csv`) identifica os bytes da V2, enquanto a equivalência de saídas científicas foi conferida separadamente por `verificar_reproducao.py`.
- A base de dados foi fornecida pelo autor e não foi autenticada byte a byte contra uma distribuição oficial independente da NinaPro.
- A pasta `comparison/` contém os resultados históricos de consolidação; ainda não há script dedicado para reconstruir todos eles do zero.
