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

## Rastreabilidade e limites

- As CSV e JSON são **registros do experimento**, preservados por identidade de bytes ao organizar o repositório.
- Os relatórios consolidados já presentes refletem as execuções originais. Não é apresentado notebook, script único ou comando capaz de gerar todos os arquivos de `comparison/` a partir do zero.
- A versão do interpretador e das bibliotecas empregada nas execuções originais não foi registrada. O `requirements.txt` representa um ambiente posterior **ainda não reexecutado**.
- O código de teste final foi preservado byte a byte; apenas scripts auxiliares de relatório, exploração preliminar e análise bootstrap receberam adaptações de caminhos ou entrada.
- A existência de arquivos de auditoria não equivale à verificação independente dos resultados, que depende de obter a base NinaPro e comparar as saídas.
