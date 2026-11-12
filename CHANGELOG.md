# Histórico de alterações

## V2.1 — 12/11/2026 — Preparação para publicação

- Adicionada a licença permissiva Zero-Clause BSD (0BSD) para o código autoral.
- Documentado o alcance e os limites da conferência do histórico fornecido (`git log --stat`).
- Atualizados README, checklist de publicação e manifesto SHA-256.
- Nenhum experimento, parâmetro, resultado científico ou código de classificação foi alterado nesta atualização.

---

# Histórico de versões do repositório

## V2 — 2026-11-11

### Correções de código sem alteração científica

- Em `e2_final/run_final_e2_frozen.py` e `e2_validation/run_threshold_e2_validation.py`, a *balanced accuracy* passou a ser calculada explicitamente como a média do recall das quatro classes reais. O rótulo `-1` (rejeição) continua valendo como erro de classificação, mas não dispara o aviso do scikit-learn sobre classe prevista ausente dos valores verdadeiros.
- No script final, as taxas direcionais entre mão fechada e thumbs up agora usam diretamente a contagem da classe verdadeira, incluindo as amostras rejeitadas no denominador. Foram removidas as divisões intermediárias que poderiam produzir avisos; os valores finais permanecem iguais.
- A rotina `confusion_4` agora documenta sua função e tolera o rótulo de rejeição (ignorando somente a coluna inexistente, como já era feito na construção da matriz parcial dentro do fluxo de teste).
- Não foram modificadas as decisões experimentais (classes, canais, repetições, janelas, características, limiares, templates, tratamento de empates, priors LDA e seleção de modelo).

### Legibilidade, verificabilidade e ambiente

- Comentários e funções de métricas receberam descrições explícitas da semântica de rejeição.
- Adicionados cinco testes automatizados em `tests/`.
- Adicionado `verificar_reproducao.py`, que compara 24 artefatos diretamente produzidos pelos três scripts com as referências congeladas, sem reescrever nenhum deles.
- `requirements.txt`, `.python-version` e `verificar_ambiente.py` passaram a apontar para o ambiente **efetivamente reexecutado** (Python 3.13.5); os requisitos previamente propostos para 3.15.2 foram preservados em `docs/requirements_propostos_2026-11-10.txt`.
- Reorganizadas as instruções do README, o guia, a procedência e o checklist de publicação. Acrescentado `docs/TESTES_V2.md`.
- Atualizado o manifesto SHA-256 para refletir o pacote V2 (o manifesto anterior era específico dos bytes da V1).

### Testes realizados

- Teste final com S1–S10, validação LDA e validação Threshold/Hamming: executados com `python -W error` e sem avisos.
- 24 de 24 arquivos de saída científica: **idênticos byte a byte** aos arquivos congelados.
- Relatório final e gráfico reconstruídos: **idênticos byte a byte**.
- Bootstrap (50.000 reamostragens, nove linhas): reproduzido sem divergências numéricas.
- Cinco testes unitários: aprovados.

### Limites preservados

- Não foram incluídos arquivos brutos NinaPro.
- As versões exatas de Python/bibliotecas usadas *originalmente* no TCC continuam desconhecidas.
- A consolidação histórica integral de `comparison/` ainda não conta com script dedicado.
- A licença de código ainda deve ser escolhida pelo autor.
