Quero que você faça uma análise real do código e corrija regressões introduzidas no projeto `image_four`, principalmente em `ai_studio_code.py`.

Contexto:
- Projeto Python com `.venv`
- Arquivo principal: `ai_studio_code.py`
- Stack: Python + `google-genai`
- O modo antigo baseado em arquivo NÃO pode quebrar
- O novo modo `--interactive` foi implementado, mas está com múltiplos bugs

IMPORTANTE:
- Rode sempre os testes com `./.venv/bin/python`, não com `python` do sistema
- Preserve o comportamento existente do modo por arquivo
- Não faça remendos superficiais
- Corrija a arquitetura e o runtime com o menor número possível de mudanças limpas
- Antes de editar, analise o código atual e explique o que está errado

Problemas observados até agora:

1) BUG DO PREVIEW NO MODO INTERATIVO
Comando:
`./.venv/bin/python ai_studio_code.py --interactive`

Ao digitar palavras como:
`witch house, broom, wand, troll, prince, princess, castle`

o script diz que gerou prompts, mas o preview mostra o TEMPLATE bruto inteiro em vez dos prompts finais.
Isso indica que o pipeline do modo interativo está confundindo:
- texto do template
- prompts finais renderizados
- variável usada no preview
- ou está pulando a etapa de geração real dos prompts

2) REGRESSÃO NO MODO ANTIGO
Rodando:
`./.venv/bin/python ai_studio_code.py`

aparece:
`FileNotFoundError: Prompts file not found: PROMPTS.md`

O modo antigo precisa continuar funcionando como antes.
Você precisa descobrir se o problema é:
- diretório de trabalho
- caminho relativo quebrado
- mudança indevida na resolução do arquivo
- regressão na refatoração

3) USO INCORRETO DA SDK `google-genai`
Ocorreram erros como:
- `'Client' object has no attribute 'GenerativeModel'`
- `module 'google.genai' has no attribute 'configure'`

Isso sugere mistura de APIs antigas e novas, ou uso incorreto da biblioteca atual.
Você precisa verificar como a biblioteca realmente deve ser usada no código atual do projeto e corrigir a integração inteira de forma consistente.

4) ERROS DE AUTENTICAÇÃO / MODO DE ACESSO À API
Também ocorreram erros 403 como:
- `API_KEY_SERVICE_BLOCKED`
- bloqueio em `generativelanguage.googleapis.com`
- bloqueio em `aiplatform.googleapis.com`

Isso indica provável inconsistência entre:
- uso de API key
- uso de Vertex AI
- modo de autenticação esperado
- endpoint/modelo sendo chamado

Você precisa inspecionar como o projeto está tentando autenticar e decidir um fluxo correto e consistente.
Se necessário:
- padronize o modo de autenticação
- detecte configurações inválidas
- melhore as mensagens de erro
- evite fallback confuso que mascara o problema

5) COMPORTAMENTO INCONSISTENTE
Em um momento o preview mostrou o template bruto.
Depois o preview virou prompt simples genérico:
`A vivid image of bee bite by an apple for children.`
Mas a geração de imagem falhou por autenticação/API.
Ou seja, hoje o sistema está inconsistente:
- preview às vezes vem do template bruto
- às vezes vem de fallback simples
- o pipeline de prompt e o pipeline de geração não estão estáveis

O que eu quero que você faça:

FASE 1
- Inspecione `ai_studio_code.py` e arquivos relacionados
- Explique a arquitetura atual
- Liste os bugs encontrados
- Identifique a causa raiz de cada um
- Diga claramente quais são bugs de lógica e quais são bugs de integração/autenticação

FASE 2
- Corrija o modo `--interactive` para que ele produza uma `List[str]` real de prompts finais
- O preview deve mostrar um prompt final real, nunca o template bruto
- A geração deve usar exatamente essa lista final

FASE 3
- Corrija a regressão do modo por arquivo
- O fluxo antigo deve voltar a funcionar
- Corrija a resolução de caminho de `PROMPTS.md` se necessário

FASE 4
- Corrija a integração com `google-genai`
- Não misture APIs antigas e novas
- Escolha uma abordagem correta e consistente para geração de texto/prompt e imagem
- Se houver dependência de autenticação específica, deixe isso explícito no código e na mensagem de erro

FASE 5
- Rode validação final
- Mostre:
  - arquivos alterados
  - causa raiz de cada bug
  - o que foi corrigido
  - como testar modo arquivo
  - como testar modo interativo
  - quais pré-requisitos de autenticação são realmente necessários

Restrições obrigatórias:
- Não esconda os erros
- Não troque comportamento antigo sem justificar
- Não duplique lógica entre modo arquivo e modo interativo
- Não use hacks para “simular” prompt gerado
- Não use fallback genérico como solução final do bug
- Se precisar manter fallback, ele deve ser explícito, controlado e separado da lógica principal
- O código final deve ficar legível e sustentável

Exemplos reais de erros observados:
- preview mostrando o arquivo inteiro `PROMPT_GENERATOR_TEMPLATE.md`
- `FileNotFoundError: Prompts file not found: PROMPTS.md`
- `'Client' object has no attribute 'GenerativeModel'`
- `module 'google.genai' has no attribute 'configure'`
- `403 PERMISSION_DENIED`
- `API_KEY_SERVICE_BLOCKED`

Teste com estes casos:
1. `./.venv/bin/python ai_studio_code.py --interactive`
   input:
   `witch house, broom, wand, troll, prince, princess, castle`

2. `./.venv/bin/python ai_studio_code.py --interactive`
   input:
   `bee bite by an apple, psicodelic boy bedroom, witch house made by candy`

3. `./.venv/bin/python ai_studio_code.py`

Antes de editar, me mostre:
1. diagnóstico
2. causa raiz provável
3. plano enxuto de correção

Só depois comece a modificar os arquivos.