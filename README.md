# TCC — sEMG, número de canais e classificação de gestos (NinaPro DB5)

**Versão do repositório: V2 — revisão de legibilidade e reprodutibilidade (11/11/2026).**

Código, resultados congelados e evidências de auditoria do trabalho **“Avaliação da influência do número de canais de sEMG na classificação de gestos por limiar e aprendizado de máquina”**.

> **Resultados preservados.** A V2 corrige avisos de avaliação sem alterar parâmetros, divisão de dados, decisões de classificação ou métricas. As saídas das três execuções foram confrontadas com os registros históricos: **24/24 arquivos gerados idênticos em bytes**. Os testes com S1–S10 usaram os dados NinaPro enviados separadamente pelo autor. A base bruta não integra este repositório.

## Estrutura e ordem de leitura

| Local | Para que serve |
| --- | --- |
| `docs/GUIA_REPRODUCAO.md` | Passo a passo para reproduzir os experimentos |
| `docs/TESTES_V2.md` | Ambiente, testes, resultados e limites da V2 |
| `docs/GUIA_LEITURA_DO_CODIGO.md` | Explicação passo a passo das funções e do tratamento de rejeições |
| `docs/PROTOCOLO_E_LIMITACOES.md` | Partições de repetições, métricas e rejeições |
| `e2_validation/run_lda_e2_validation.py` | Validação LDA-RMS / LDA-TD com repetição 6 |
| `e2_validation/run_threshold_e2_validation.py` | Validação do Threshold/Hamming com repetição 6 |
| `e2_final/run_final_e2_frozen.py` | Teste final congelado, usando somente repetições 2 e 5 |
| `e2_final/build_report.py` | Reconstrução de figura, matrizes e relatório do teste final |
| `verificar_reproducao.py` | Compara saídas novas com as saídas científicas preservadas |
| `verificar_integridade.py` | Verifica os arquivos do repositório pelo manifesto SHA-256 |
| `tests/` | Testes automatizados das métricas em presença de rejeição |
| `analises/bootstrap/` | Reamostragem exploratória posterior ao teste final |
| `analises/exploracao_threshold/` | Exploração auxiliar A–D anterior à seleção metodológica |
| `comparison/` | Comparação histórica conjunta da validação; sem script de consolidação integral |
| `threshold_results/` | Registros históricos do Threshold/Hamming na validação |

A localização e a finalidade de arquivos específicos do TCC constam de [docs/MAPA_ARTEFATOS.md](docs/MAPA_ARTEFATOS.md). O histórico de alterações da V2 está em [CHANGELOG.md](CHANGELOG.md).

## O protocolo não foi alterado

- **Dados:** NinaPro DB5, Exercise 2, S1–S10.
- **Classes reais:** 0 (repouso), 1 (thumbs up), 5 (mão aberta), 6 (mão fechada).
- **Treinamento:** repetições 1, 3 e 4. **Validação:** repetição 6. **Teste final:** repetições 2 e 5.
- **Janelas:** 200 ms, 50% de sobreposição (40 amostras, passo 20, 200 Hz).
- **Canais:** 1, 2, 4 e 8 em subconjuntos espaciais predeterminados.
- **Métodos:** Threshold/Hamming, LDA-RMS e LDA-TD. No Threshold/Hamming, `-1` significa rejeição, não uma quinta classe real; rejeições contam como erro nas métricas.

## Início rápido

Use CPython **3.13.5** com as dependências do `requirements.txt`, correspondentes ao ambiente em que a V2 foi reexecutada em 11/11/2026. A versão exata do ambiente *histórico original* não é conhecida. O ambiente proposto antes da V2 (Python 3.15.2) foi preservado apenas como referência em `docs/requirements_propostos_2026-11-10.txt` e não faz parte da configuração testada.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python verificar_ambiente.py
python verificar_integridade.py
python -m unittest discover -s tests -v
```

Prepare **fora do repositório** um ZIP com `s1.zip` a `s10.zip`, cada qual contendo `Sx_E2_A1.mat`. Substitua `/caminho/DB5.zip` pelo caminho real:

```bash
python e2_validation/run_lda_e2_validation.py --db5-zip /caminho/DB5.zip --out reproducoes/validacao_lda
python e2_validation/run_threshold_e2_validation.py --db5-zip /caminho/DB5.zip --out reproducoes/validacao_threshold
python e2_final/run_final_e2_frozen.py --db5-zip /caminho/DB5.zip --out reproducoes/final
python verificar_reproducao.py --final reproducoes/final --validacao-lda reproducoes/validacao_lda --validacao-threshold reproducoes/validacao_threshold
python e2_final/build_report.py --results reproducoes/final --out reproducoes/relatorio
```

**Não use os diretórios históricos `e2_final/results`, `e2_validation/results` ou `threshold_results` no argumento `--out`.** Eles contêm as referências congeladas. O `.gitignore` exclui `reproducoes/` por padrão.

## Resultados principais (macro-F1 médio, teste final)

| Canais | Threshold/Hamming | LDA-RMS | LDA-TD |
| ---: | ---: | ---: | ---: |
| 1 | 0,190 | 0,491 | 0,530 |
| 2 | 0,326 | 0,640 | 0,668 |
| 4 | 0,520 | 0,778 | 0,785 |
| 8 | 0,682 | 0,828 | 0,840 |

As métricas resumem **dez participantes**, sem misturar janelas de diferentes participantes como unidades independentes para a média principal. Consulte `e2_final/results/final_summary_mean_std.csv` e o TCC para os resultados completos e suas limitações.

## Reprodutibilidade, direitos e publicação

- A V2 foi reexecutada com dados locais fornecidos pelo autor, **não** com uma cópia da NinaPro autenticada externamente. Não compartilhe o banco bruto em commits, ZIPs ou releases.
- O manifesto `docs/MANIFESTO_SHA256.csv` documenta os arquivos incluídos no pacote V2; não é o manifesto histórico original (que pertencia à V1).
- `comparison/` conserva a consolidação histórica; o código de reprodução integral dessa etapa ainda não está disponível.
- Não foi definida uma licença de reutilização para o código autoral. **A ausência de `LICENSE` não é autorização de uso irrestrito.** Verifique os direitos de terceiros antes da publicação.
- Revise [docs/ANTES_DE_PUBLICAR.md](docs/ANTES_DE_PUBLICAR.md). O pacote não foi publicado no GitHub por esta revisão.
