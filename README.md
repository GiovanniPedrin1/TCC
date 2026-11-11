# TCC — Canais de sEMG e classificação de gestos (NinaPro DB5, exercício E2)

Repositório de referência dos códigos, resultados e arquivos de auditoria associados ao TCC **“Avaliação da influência do número de canais de sEMG na classificação de gestos por limiar e aprendizado de máquina”**.

Este material contém os resultados **congelados** do experimento e scripts que permitem tentar a reexecução com a base NinaPro DB5 original. **Não inclui os dados brutos nem comprova que a reexecução no ambiente proposto gerará resultados numericamente idênticos**. A versão exata do ambiente histórico não foi registrada.

## Organização

| Pasta/arquivo | Conteúdo |
| --- | --- |
| `e2_final/` | Script e resultados do teste final (treino 1, 3 e 4; teste 2 e 5), relatório, figuras e auditorias |
| `e2_validation/` | Script de validação LDA, script Threshold/Hamming para E2, resultados da validação (repetição 6), relatório e auditorias |
| `comparison/` | Resultados e relatório da comparação conjunta de validação entre Threshold/Hamming e LDA |
| `threshold_results/` | Resultados de Threshold/Hamming na validação, inclusive auditoria e templates |
| `analises/bootstrap/` | Análise exploratória posterior ao teste final, com script e CSV da Etapa 2 |
| `analises/exploracao_threshold/` | Código auxiliar da exploração preliminar A–D, distinto do teste final |
| `docs/` | Guias, protocolo, proveniência e manifesto de integridade |
| `.python-version`, `requirements.txt`, `verificar_ambiente.py` | Ambiente **proposto** para novas execuções (não ambiente histórico) |

As pastas `e2_final/`, `e2_validation/`, `comparison/` e `threshold_results/` conservam os nomes relativos dos artefatos que fundamentam o Apêndice C do TCC. **Os arquivos CSV, JSON, PNG e relatórios originais não foram recalculados ou alterados nesta organização.**

## Instalação e reexecução

O ambiente de referência proposto em 10/11/2026 fixa **Python 3.15.2** e seis dependências diretas (`requirements.txt`). Essa combinação ainda **não foi validada por reexecução integral**. Não existe lockfile de dependências transitivas nem informação sobre versões históricas.

Após criar um ambiente virtual com Python 3.15.2:

```bash
python -m pip install -r requirements.txt
python verificar_ambiente.py
```

O nome e a localização da base devem ser informados pelo usuário. **Não coloque a base bruta dentro do repositório**. Exemplo de teste final, executado a partir da raiz do projeto:

```bash
python e2_final/run_final_e2_frozen.py --db5-zip /caminho/DB5.zip --out reproducoes/e2_final/results
python e2_final/build_report.py --results reproducoes/e2_final/results --out reproducoes/e2_final
```

Para preservar os resultados originais, **nunca execute com `--out e2_final/results`**. O relatório reconstruído pela segunda linha é derivado dos resultados de uma nova execução; ele não executa novamente o experimento.

Instruções de validação, análise bootstrap e limitações: [docs/GUIA_REPRODUCAO.md](docs/GUIA_REPRODUCAO.md).

## Escopo metodológico

- Base: NinaPro DB5, arquivos `Sx_E2_A1.mat` de dez participantes, exercícios E2.
- Classes: repouso (0), polegar levantado (1), mão aberta (5) e mão fechada (6).
- Número de canais: 1, 2, 4 e 8, com subconjuntos fixos.
- Treino: repetições 1, 3 e 4; validação: repetição 6; teste final: repetições 2 e 5.
- Métodos do teste final: Threshold/Hamming, LDA-RMS e LDA-TD. A rejeição (-1) do Threshold/Hamming não constitui uma quinta classe real.

Leia [docs/PROTOCOLO_E_LIMITACOES.md](docs/PROTOCOLO_E_LIMITACOES.md) antes de comparar os resultados.

## Reprodutibilidade, auditoria e acesso aos dados

As saídas fornecidas são registros históricos; os testes automatizados realizados para organizar este pacote verificam presença, identidade por hash e sintaxe de código, mas **não reexecutam a classificação com sinais NinaPro**. Parte da consolidação da comparação de validação não tem script dedicado nos materiais recebidos; ver [docs/PROVENIENCIA.md](docs/PROVENIENCIA.md). Consulte [docs/MANIFESTO_SHA256.csv](docs/MANIFESTO_SHA256.csv) para hashes e execute `python verificar_integridade.py`.

A base NinaPro DB5 é obtida a partir de sua fonte oficial, sob as condições de acesso e uso definidas pelo provedor. Este repositório não redistribui esses arquivos.

**Licenciamento do código do autor:** ainda não foi definido um arquivo `LICENSE`; a ausência de licença não deve ser interpretada como autorização irrestrita para reutilização. Antes da publicação pública, decidir a licença e revisar direitos de terceiros. Checklist em [docs/ANTES_DE_PUBLICAR.md](docs/ANTES_DE_PUBLICAR.md).
