# Auditoria do histórico Git e privacidade — 12/11/2026

Este documento registra a **auditoria concluída do bundle fornecido pelo autor**, não uma garantia absoluta sobre todos os objetos que possam existir no serviço remoto.

## Material e escopo

- Arquivo examinado: `TCC_auditoria.bundle`, entregue separadamente pelo autor e **não incluído** neste repositório.
- Verificação do bundle: `git bundle verify` aprovada; `git fsck --full --no-reflogs --unreachable` sem corrupção ou objetos inacessíveis relevantes nas referências exportadas.
- Referências incluídas: `main` em `a1b3c08` e `Nao-verificado` em `aa4ef57` (além das referências equivalentes presentes no bundle).
- Histórico alcançável: **4 commits**, **119 blobs** (141 objetos Git no total, incluindo trees e commits) e **147 caminhos históricos distintos**.
- Foram inspecionados os arquivos dos commits antigos, incluindo versões substituídas ou reorganizadas; não apenas os arquivos atuais ou a listagem `git log --stat`.

## Constatações

| Verificação | Resultado no bundle fornecido |
| --- | --- |
| Sinais brutos da NinaPro (`.mat`) ou ZIPs de participantes | Não encontrados |
| Arquivos `.env`, chaves privadas ou arquivos de autenticação | Não encontrados |
| Padrões reconhecíveis de tokens, senhas ou credenciais | Não encontrados |
| CPF ou endereços de e-mail no conteúdo de arquivos | Não encontrados |
| Resultados derivados identificados como S1–S10 | Presentes; não são os sinais originais |
| Caminhos absolutos em arquivo histórico | Dois caminhos genéricos `/mnt/data/e2_final/...`; sem identificador pessoal |
| Nome e e-mail do autor nos metadados dos commits | Presentes; o autor **confirmou que aceita** sua exposição pública |

As verificações não identificaram motivos técnicos para reescrever o histórico exportado. A branch `Nao-verificado` descendia da `main` no momento do bundle; o merge pode preservar seus commits. **Excluir a branch depois do merge não exclui os commits da `main`.**

## Limitações e precauções

1. A análise cobre o conteúdo e as referências **incluídos no bundle de 12/11/2026**, não eventuais refs omitidas, forks, pull requests, objetos órfãos ou alterações posteriores armazenadas remotamente.
2. Uma busca automatizada e revisão de conteúdo não provam a inexistência de credenciais ofuscadas ou padrões não reconhecidos.
3. A licença [0BSD](../LICENSE) aplica-se **somente ao código autoral**. Sinais, dados e outros materiais de terceiros, inclusive NinaPro DB5, continuam sujeitos às condições de uso e citação aplicáveis. A base bruta não é distribuída no pacote.
4. A versão auditada no bundle corresponde à V2; as alterações documentais posteriores da V2.1/V2.2 devem ser conferidas no commit efetivamente publicado.
5. Esta revisão de arquivos **não executou merge, push, exclusão de branch nem mudança de visibilidade** no GitHub.

## Verificação prática na publicação

Após incorporar a versão revisada, confira no GitHub a presença de `LICENSE`, os links do `README.md`, os arquivos versionados e a ausência de dados brutos. Compare também as referências atuais do remoto com as já auditadas, especialmente se houve novos commits desde o bundle. A publicação é uma decisão do autor.

Para o relatório técnico mais extenso, consulte a cópia privada da auditoria entregue ao autor em 12/11/2026 (não incluída no repositório).
