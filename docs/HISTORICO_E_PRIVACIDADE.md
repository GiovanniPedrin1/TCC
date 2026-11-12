# Auditoria preliminar do histórico e privacidade — 12/11/2026

## Materiais verificados

- `historico_detalhado.txt`, fornecido pelo autor: lista quatro commits (`a1b3c08`, `3f16fb7`, `8162b0c`, `aa4ef57`) com estatísticas de alteração por arquivo.
- Arquivos atualmente presentes nos pacotes `TCC.zip` (V1) e `TCC_Repositorio_V2.zip` (V2).
- Busca automatizada por nomes típicos de arquivos privados (`.mat`, `.env`, chaves), padrões usuais de tokens e credenciais, caminhos de usuário e endereços de e-mail **nos arquivos atuais do pacote**.

## Achados

- Nenhum `.mat` ou ZIP bruto da NinaPro consta dos nomes de arquivos no histórico fornecido ou dos ZIPs examinados.
- Nenhum arquivo de segredo óbvio nem padrão comum de token ou credencial foi encontrado nos arquivos atuais examinados.
- Os commits listados possuem metadados de autoria com um endereço de e-mail pessoal. Ao publicar esses commits, esse endereço pode ficar visível a terceiros. Não reproduzimos o endereço nesta auditoria.
- O pacote V2 não inclui uma pasta `.git`, logo **não contém os blobs antigos para inspeção direta**.

## Limites: não é certificado de ausência de vazamentos

A saída `git log --stat` lista caminhos e contagens de linhas, mas não inclui o conteúdo histórico completo dos arquivos, nem comprova que todas as referências/branches foram incluídas. Um token poderia ter sido acrescentado e posteriormente apagado de um arquivo `.py`, `.md`, `.csv` ou `.json` sem aparecer nas estatísticas. O histórico completo (objetos Git) precisa ser inspecionado antes de tornar o repositório público.

**Excluir a branch `Nao-verificado` após fazer merge NÃO apaga seus commits do histórico de `main`.** Se houver dados sensíveis históricos, devem ser tratados antes do merge/publicação.

## Como fornecer o histórico completo para conferência

Na pasta local do repositório Git, com todas as branches/tags relevantes disponíveis, execute:

```bash
git fetch --all --tags
git branch -a
git bundle create ../TCC_auditoria.bundle --all
git bundle verify ../TCC_auditoria.bundle
```

O `.bundle` contém os arquivos completos de todos os commits alcançáveis pelas referências incluídas, inclusive qualquer informação que porventura tenha sido removida em versões posteriores. Trate o arquivo como **privado** até a auditoria terminar. Revise também eventuais pull requests antigos, forks, Git LFS e outras referências remotas que não façam parte do bundle.

## Antes de publicar

1. Auditar objetos/blobs antigos e confirmar que não há credenciais e dados não redistribuíveis.
2. Caso apareça algum segredo válido, revogar ou rotacionar primeiro e tratar a remoção do histórico conforme a documentação do GitHub.
3. Verificar se deseja divulgar o e-mail de autoria embutido nos commits antigos; mudar a configuração para e-mail `noreply` não altera commits históricos.
4. Confirmar regras de uso da NinaPro e direitos de terceiros. A 0BSD cobre somente a parte do código sobre a qual o autor tem direitos.
5. Só então realizar o merge para `main`, excluir a branch de trabalho e tornar público.

Fontes:
- https://opensource.org/license/0bsd
- https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
