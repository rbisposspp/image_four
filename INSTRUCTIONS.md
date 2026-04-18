Quero que você implemente o modo interativo no projeto Python atual com segurança arquitetural, preservando 100% do comportamento existente no modo baseado em arquivo.

Contexto:
- O objetivo é permitir gerar imagens a partir de palavras digitadas no terminal, sem editar manualmente o arquivo de prompts.
- O arquivo principal é `ai_studio_code.py`.
- A stack é Python + `google-genai`.
- Já existe uma lógica funcional de geração via argumentos/arquivo e ela não pode quebrar.

O que eu quero de você:
1. Primeiro, LEIA o código atual e faça uma análise curta da arquitetura existente antes de editar qualquer coisa.
2. Depois, implemente o modo interativo com a melhor arquitetura possível, evitando gambiarra.

Regras obrigatórias de implementação:
- NÃO use `if len(sys.argv) > 1` como chave principal de decisão.
- Prefira um argumento explícito como `--interactive` ou uma arquitetura equivalente mais robusta.
- NÃO crie `argparse.Namespace` fake com valores hardcoded para “simular args”.
- NÃO duplique lógica de geração entre modo arquivo e modo interativo.
- Extraia um núcleo único e reutilizável para processamento e geração.
- Preserve o fluxo atual por arquivo exatamente como já funciona hoje.
- Se houver leitura de template, implemente de forma robusta e clara, sem depender de um `replace()` ingênuo se isso fragilizar o sistema.
- Trate erros, cancelamento por `KeyboardInterrupt`, entrada vazia e arquivos ausentes.
- Mantenha o código legível, modular e fácil de evoluir.

Arquitetura desejada:
- Uma função/coordenador para o modo arquivo
- Uma função/coordenador para o modo interativo
- Um núcleo compartilhado para:
  - obter prompts
  - normalizar/validar prompts
  - chamar a geração de imagens
  - salvar resultados
- Uma configuração real e única, sem divergência entre modos

Fluxo desejado do modo interativo:
1. Coletar palavras-chave do usuário no terminal
2. Validar e normalizar a entrada
3. Gerar prompts a partir de um template ou estratégia equivalente
4. Mostrar uma prévia clara do que será gerado
5. Pedir confirmação
6. Executar a geração de imagens usando o mesmo núcleo do modo normal
7. Salvar no diretório de saída já suportado pelo projeto

Quero que você trabalhe em fases:
Fase 1:
- Analise o código atual
- Explique a arquitetura encontrada
- Aponte os pontos que precisam ser refatorados
- Proponha a arquitetura final antes de editar

Fase 2:
- Implemente a refatoração mínima necessária
- Preserve compatibilidade com o fluxo antigo

Fase 3:
- Implemente o modo interativo

Fase 4:
- Faça uma verificação final
- Mostre exatamente:
  - quais arquivos foram alterados
  - o que mudou em cada arquivo
  - como testar o modo antigo
  - como testar o modo interativo

Critérios de qualidade:
- sem regressão no fluxo antigo
- sem hardcode desnecessário
- sem duplicação de lógica
- sem “mock de args”
- código pronto para manutenção futura

Antes de alterar qualquer arquivo, me mostre:
1. diagnóstico do código atual
2. arquitetura alvo
3. plano de implementação enxuto

Só depois disso comece a editar.