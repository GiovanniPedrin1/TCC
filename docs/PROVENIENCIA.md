# Proveniência, consolidação e decisões de organização

## Fontes fornecidas

O material desta versão foi consolidado a partir dos pacotes de referência usados durante a elaboração do TCC:

- `DB5_E2_FINAL_FROZEN_PY3152.zip`: teste final, saídas, relatório e auditorias.
- `DB5_pacotes_TCC_PY3152.zip`: validação LDA E2, comparação conjunta, validação Threshold/Hamming e uma **cópia** do teste final.
- `CODIGOS_TCC_DB5_PY3152.zip`: cópias dos scripts finais/de validação, além do código de exploração preliminar.
- `Analise_Exploratoria_TCC_Etapa2.zip`: script e resultados da análise bootstrap posterior.

Os dados brutos NinaPro não fazem parte desses pacotes.

## Alterações de organização

1. Uma só cópia dos scripts `run_final_e2_frozen.py`, `run_lda_e2_validation.py` e `run_threshold_e2_validation.py` permanece nas pastas do fluxo a que pertencem. Seus conteúdos foram conservados exatamente.
2. A cópia aninhada do pacote final e os arquivos repetidos de ambiente (`requirements.txt`, `.python-version` e `verificar_ambiente.py`) foram eliminados; suas versões de referência estão na raiz do repositório.
3. Os arquivos de resultados, relatórios de resultados e auditoria foram preservados exatamente. Os READMEs de execução foram reescritos para evitar sobrescrever saídas originais. Alguns CSV idênticos aparecem em dois contextos (validação LDA e comparação conjunta) para conservar sua localização documental original.
4. `e2_final/build_report.py`: mudaram somente as instruções que definem as pastas de entrada/saída e a análise de argumentos, preservando a lógica das tabelas, matrizes e figuras.
5. `analises/exploracao_threshold/run_db5_threshold_comparison.py`: mudaram somente as instruções de pastas de entrada/saída e a análise de argumentos, preservando os cálculos exploratórios.
6. `analises/bootstrap/recalcular_bootstrap_etapa2.py`: adicionada leitura direta de CSV, mantendo a alternativa histórica ZIP e a função de reamostragem/estatísticas. A nota legada dependente de ZIP foi substituída por um README atualizado.
7. Não há script dedicado entre os arquivos recebidos para reconstruir automaticamente cada resultado de `comparison/` combinando as saídas dos dois scripts de validação. A pasta contém os registros gerados, não uma promessa de reprodução integral da etapa de consolidação.

## Integridade

As tabelas/relatórios originais não foram recalculados. O manifesto `docs/MANIFESTO_SHA256.csv` permite detectar alterações posteriores no conteúdo de cada arquivo, e `verificar_integridade.py` verifica os hashes atuais.

**Ambiente histórico:** desconhecido. A fixação Python 3.15.2 e bibliotecas de `requirements.txt` é posterior ao experimento e não foi validada com NinaPro neste pacote.
