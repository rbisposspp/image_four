from google.cloud import language_v1

def analisar_tudo_passo_a_passo():
    # 1. Chamar o "Especialista" do Google
    client = language_v1.LanguageServiceClient()

    # O texto que vamos analisar (precisa ser um pouco longo para a Classificação funcionar bem)
    texto = (
        "A Google lançou um novo celular incrível em São Paulo. "
        "A bateria dura o dia todo e a câmera é fantástica! "
        "Estou muito feliz com a minha compra. "
        "A tecnologia dos smartphones está evoluindo muito rápido."
    )
    
    print(f"--- LENDO O TEXTO ---\n'{texto}'\n")

    # Preparar o "Papel" para o Especialista
    documento = {"content": texto, "type_": language_v1.Document.Type.PLAIN_TEXT, "language": "pt-BR"}

    # ==========================================
    # HABILIDADE 1: SENTIMENTO (Feliz/Triste)
    # ==========================================
    print("1. TESTANDO SENTIMENTO:")
    resp_sentimento = client.analyze_sentiment(request={'document': documento})
    nota = resp_sentimento.document_sentiment.score
    if nota > 0:
        print(f"   -> O texto é POSITIVO! (Nota: {nota:.2f})")
    elif nota < 0:
        print(f"   -> O texto é NEGATIVO! (Nota: {nota:.2f})")
    else:
        print(f"   -> O texto é NEUTRO. (Nota: {nota:.2f})")
    print("-" * 40)

    # ==========================================
    # HABILIDADE 2: ENTIDADES (Nomes, Lugares, Empresas)
    # ==========================================
    print("2. PROCURANDO ENTIDADES IMPORTANTES:")
    resp_entidades = client.analyze_entities(request={'document': documento})
    for entidade in resp_entidades.entities:
        print(f"   -> Encontrei: {entidade.name} (Tipo: {language_v1.Entity.Type(entidade.type_).name})")
    print("-" * 40)

    # ==========================================
    # HABILIDADE 3: SINTAXE (Gramática e Estrutura)
    # ==========================================
    print("3. ANALISANDO A GRAMÁTICA (Sintaxe):")
    resp_sintaxe = client.analyze_syntax(request={'document': documento})
    # Vamos mostrar apenas os 3 primeiros para não poluir a tela
    print("   -> (Mostrando apenas as 3 primeiras palavras)")
    for token in resp_sintaxe.tokens[:3]:
        palavra = token.text.content
        classe_gramatical = language_v1.PartOfSpeech.Tag(token.part_of_speech.tag).name
        print(f"   -> Palavra: '{palavra}' é um(a) {classe_gramatical}")
    print("-" * 40)

    # ==========================================
    # HABILIDADE 4: CLASSIFICAÇÃO DE ASSUNTO
    # ==========================================
    print("4. DESCOBRINDO O ASSUNTO (Classificação):")
    try:
        resp_classificacao = client.classify_text(request={'document': documento})
        for categoria in resp_classificacao.categories:
            print(f"   -> Assunto: {categoria.name} (Certeza: {categoria.confidence * 100:.0f}%)")
    except Exception as e:
        print("   -> (O texto foi muito curto para classificar ou houve um erro).")
    print("=" * 40)

# Executar a função
if __name__ == "__main__":
    analisar_tudo_passo_a_passo()
