# Guia de execução e verificação

## 1. Preparar o ambiente de referência (não histórico)

Instale **CPython 3.15.2** e crie um ambiente virtual. Linux/macOS: `python3.15 -m venv .venv && . .venv/bin/activate`. Windows PowerShell: `py -3.15 -m venv .venv; .\.venv\Scripts\Activate.ps1`. Confirme `python --version` (esperado: `3.15.2`).

```bash
python -m pip install -r requirements.txt
python verificar_ambiente.py
python verificar_integridade.py
```

As seis dependências diretas estão fixadas, mas as transitivas não; a compatibilidade completa só pode ser demonstrada por instalação e reexecução. **As versões usadas historicamente são desconhecidas**.

## 2. Preparar os dados originais

Obtenha separadamente a base NinaPro DB5 a partir de https://ninapro.hevs.ch/instructions/DB5.html, observando suas regras de uso. O código dos scripts `run_lda_e2_validation.py`, `run_threshold_e2_validation.py` e `run_final_e2_frozen.py` espera um ZIP externo (`--db5-zip`) contendo ZIPs internos `s1.zip` até `s10.zip`, cada um com `Sx_E2_A1.mat` (x=1...10). Verifique a organização do arquivo baixado, pois a distribuição pode diferir.

Não adicione arquivos `.mat` ou ZIPs brutos ao GitHub.

## 3. Validação metodológica (repetição 6)

Execute a partir da raiz do repositório, usando saídas novas:

```bash
python e2_validation/run_lda_e2_validation.py --db5-zip /caminho/DB5.zip --out reproducoes/validacao_lda
python e2_validation/run_threshold_e2_validation.py --db5-zip /caminho/DB5.zip --out reproducoes/validacao_threshold
```

Compare `reproducoes/validacao_lda/summary.csv` com `e2_validation/results/summary.csv` e os resultados de Threshold/Hamming com `threshold_results/`. As duas saídas não constroem automaticamente todos os artefatos da pasta `comparison/` (a consolidação conjunta não possui script dedicado no conjunto disponibilizado).

## 4. Teste final congelado (repetições 2 e 5)

```bash
python e2_final/run_final_e2_frozen.py --db5-zip /caminho/DB5.zip --out reproducoes/e2_final/results
python e2_final/build_report.py --results reproducoes/e2_final/results --out reproducoes/e2_final
```

**Nunca** sobrescreva `e2_final/results/`. Compare resultados de reprodução com `e2_final/results/final_results_by_subject.csv`, `final_summary_mean_std.csv`, `FINAL_PROTOCOL_AUDIT.json` e `confusion_matrices.json`. Diferenças possíveis de versões numéricas, plataforma ou dados devem ser reportadas; não reajuste parâmetros para forçar equivalência.

O script `build_report.py` foi alterado **somente para aceitar caminhos de entrada/saída** na Etapa 4. O código que calcula as métricas e gera tabelas permanece igual ao código de origem; imagens e relatórios históricos do pacote não foram reconstruídos.

## 5. Análise complementar de incerteza (posterior ao teste final)

```bash
python analises/bootstrap/recalcular_bootstrap_etapa2.py --csv e2_final/results/final_results_by_subject.csv --out reproducoes/bootstrap.csv
```

Essa análise usa 50.000 reamostragens pareadas dos dez participantes, com semente fixa. Os intervalos são exploratórios, não testes confirmatórios. A versão distribuída desse script aceita agora o CSV do repositório, além da opção histórica `--zip`.

## 6. Exploração preliminar auxiliar

O arquivo `analises/exploracao_threshold/run_db5_threshold_comparison.py` é **exploratório** (configurações A–D), não o script utilizado no teste final congelado. Requer arquivos `.mat` já extraídos em subpastas `s1/ ... s10/`, sendo informado o diretório com `--extracted-root` e uma pasta nova com `--out`. Seus caminhos foram parametrizados sem modificar cálculos. Não há saídas completas dessa exploração neste pacote para confronto automático.

```bash
python analises/exploracao_threshold/run_db5_threshold_comparison.py --extracted-root /caminho/db5_extraido --out reproducoes/exploracao
```

## 7. Escopo dos testes realizados na organização

A organização verifica hashes, sintaxe e formatos, além de comparações documentais existentes. **Não valida o desempenho na instalação nova e não substitui reexecução independente**, que requer os dados originais.
