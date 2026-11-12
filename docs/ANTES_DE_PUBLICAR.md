# Itens pendentes antes da publicação pública

Este pacote está organizado para revisão e **não foi publicado no GitHub nesta etapa**.

- [ ] Revisar **todos os objetos Git alcançáveis** (branches, tags e commits antigos). O arquivo de histórico em formato `git log --stat` não expõe o conteúdo dos blobs; ver `docs/HISTORICO_E_PRIVACIDADE.md`.
- [ ] Confirmar que nenhum dado bruto `.mat`, ZIP original NinaPro, credencial, token, endereço pessoal ou arquivo privado está **também no histórico**. A inspeção dos ZIPs V1/V2 não encontrou esses itens, mas não comprova a segurança dos blobs antigos.
- [ ] Verificar as condições de uso e de citação da NinaPro DB5 e dos demais materiais de terceiros.
- [x] Adicionar licença 0BSD ao código autoral (`LICENSE` na raiz), mantendo materiais de terceiros fora do escopo da licença.
- [x] Reexecutar os scripts com os dados S1–S10 fornecidos pelo autor no ambiente Python 3.13.5 (detalhes em `docs/TESTES_V2.md`).
- [x] Confrontar as 24 saídas diretamente geradas, o relatório, a figura e o bootstrap com as referências congeladas.
- [ ] Fazer uma última leitura do README e dos links na visualização real do GitHub após importar os arquivos, incluindo o reconhecimento da licença 0BSD.
- [ ] Se a comparação conjunta de validação precisar ser reproduzida automaticamente, acrescentar um script de consolidação verificável, sem alterar as saídas históricas.
- [ ] Publicar no endereço definido pelo autor: https://github.com/GiovanniPedrin1/TCC, somente após aprovação.

## Observação sobre resultados

A V2 reproduziu as saídas científicas com os dados fornecidos pelo autor. Isso não significa que a mesma compatibilidade esteja automaticamente assegurada em todos os ambientes de usuários, nem que o ZIP recebido tenha sido validado contra uma cópia oficial independente da NinaPro.
