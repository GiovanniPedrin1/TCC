# Guia de reprodução — V2

## 1. Preparação

O ambiente reexecutado e documentado usa **CPython 3.13.5**. Em uma instalação desse Python:

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python verificar_ambiente.py
python verificar_integridade.py
python -m unittest discover -s tests -v
```

`requirements.txt` fixa apenas versões diretas. As bibliotecas e a versão original do experimento histórico não foram registradas. A configuração anteriormente proposta para Python 3.15.2 foi arquivada em `docs/requirements_propostos_2026-11-10.txt` e não foi testada nesta revisão.

## 2. Dados de entrada

Obtenha a NinaPro DB5 pela fonte oficial: https://ninapro.hevs.ch/instructions/DB5.html. Os scripts de classificação esperam um ZIP **externo** com `s1.zip` a `s10.zip`; em cada arquivo interno deve existir `Sx_E2_A1.mat`, com as variáveis `emg`, `restimulus` e `rerepetition`.

Se a distribuição tiver formato diferente, prepare a estrutura necessária fora do repositório. Respeite as condições da NinaPro e não inclua dados `.mat` ou ZIPs brutos em commits públicos.

## 3. Validação metodológica (repetição 6)

```bash
python -W error e2_validation/run_lda_e2_validation.py --db5-zip /caminho/DB5.zip --out reproducoes/validacao_lda
python -W error e2_validation/run_threshold_e2_validation.py --db5-zip /caminho/DB5.zip --out reproducoes/validacao_threshold
```

O treino usa repetições 1, 3 e 4. A validação usa a repetição 6. As repetições 2 e 5 não participam da validação.

## 4. Teste final congelado (repetições 2 e 5)

```bash
python -W error e2_final/run_final_e2_frozen.py --db5-zip /caminho/DB5.zip --out reproducoes/final
```

O teste utiliza as repetições 2 e 5; a repetição 6 não participa de sua segmentação ou ajuste. O resultado *não* deve ser usado para ajustar parâmetros do modelo após o congelamento.

## 5. Comparação automática com os resultados de referência

```bash
python verificar_reproducao.py \
  --final reproducoes/final \
  --validacao-lda reproducoes/validacao_lda \
  --validacao-threshold reproducoes/validacao_threshold
```

O verificador lê 24 arquivos diretamente gerados pelos scripts, exige a presença de todos eles e compara bytes ou, quando preciso, dados numéricos com tolerância `atol=1e-12`, `rtol=1e-10`. **Ele não escreve nos arquivos históricos nem ajusta números para forçar equivalência.** Cada pasta pode ser verificada separadamente quando as outras ainda não tiverem sido executadas.

## 6. Relatório e bootstrap

```bash
python e2_final/build_report.py --results reproducoes/final --out reproducoes/relatorio
python analises/bootstrap/recalcular_bootstrap_etapa2.py --csv reproducoes/final/final_results_by_subject.csv --out reproducoes/bootstrap.csv
```

`build_report.py` reconstrói o relatório e o gráfico a partir das saídas já calculadas; não reexecuta a classificação. O bootstrap usa 50.000 reamostragens pareadas dos participantes e tem caráter exploratório. O script também aceita a opção legada `--zip`.

## 7. Exploração auxiliar e limites

O script `analises/exploracao_threshold/run_db5_threshold_comparison.py` é uma exploração A–D separada do experimento final e requer arquivos `.mat` extraídos em subpastas por participante:

```bash
python analises/exploracao_threshold/run_db5_threshold_comparison.py --extracted-root /caminho/db5_extraido --out reproducoes/exploracao
```

O diretório `comparison/` preserva os relatórios e as tabelas históricas da consolidação da validação, mas **não há código dedicado para reconstruir todos os seus arquivos**. Consulte `docs/TESTES_V2.md` e `docs/PROVENIENCIA.md` para distinguir resultados reexecutados, artefatos preservados e limitações.
