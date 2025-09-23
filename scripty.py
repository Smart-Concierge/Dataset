import json
import random
import re # Importando o módulo de expressões regulares para substituição de sinônimos

# --- BANCO DE DADOS FICTÍCIO EXPANDIDO E COMBINADO ---

MORADORES = [
    "Ana Silva", "Bruno Costa", "Carlos Dias", "Daniela Rocha", "Eduardo Lima", "Fernanda Alves",
    "Gustavo Souza", "Helena Andrade", "Igor Pereira", "Juliana Santos", "Lucas Rodrigues",
    "Mariana Oliveira", "Pedro Martins", "Sofia Barbosa", "Tiago Ferreira", "Valéria Gomes",
    "Wellington Santos", "Xavier Almeida", "Yasmin Costa", "Zara Lima", "Gabriel Menezes",
    "Laura Ribeiro", "Miguel Souza", "Isabella Santos", "Arthur Almeida", "Alice Carvalho",
    "João Pedro", "Manuela Dantas", "Davi Correia", "Lívia Fonseca", "Rafael Rocha", "Camila Castro",
    "Diego Nunes", "Giovanna Farias", "Leonardo Mendes", "Vitória Ramos", "Mateus Correia", "Julia Almeida"
]
APARTAMENTOS = (
    [str(andar * 100 + apto) for andar in range(1, 15) for apto in range(1, 6)] +
    [f"{andar}0{apto}A" for andar in range(1, 5) for apto in range(1, 3)] +
    [f"{andar}0{apto}B" for andar in range(1, 3) for apto in range(1, 3)] +
    ["cobertura", "apto ático", "subsolo 1", "apto Garden", "unidade 305", "apt 202", "sala 401", "sala 200B", "bloco A apto 10"]
)
EMPRESAS_DELIVERY_COMIDA = [
    "iFood", "Rappi", "Uber Eats", "99Food", "Aiqfome", "Delivery Much", "LalaFood",
    "James Delivery", "Restaurante X", "Marmitaria da Vó", "Disk Pizza", "Burger King", "McDonald's",
    "Subway", "Temakeria Y", "Churrascaria Z"
]
EMPRESAS_ECOMMERCE = [
    "Amazon", "Mercado Livre", "Magazine Luiza", "Americanas", "Shopee", "Shein",
    "Casas Bahia", "Ponto Frio", "Dafiti", "Submarino", "Netshoes", "AliExpress",
    "Ebay", "Enjoei", "Fast Shop", "Kabum"
]
EMPRESAS_SERVICO = [
    "Vivo", "Claro", "Copel", "Sanepar", "Intelbras", "Orkin", "Tim", "Oi", "Enel",
    "Neoenergia", "Sabesp", "CEDAE", "Elektro", "Descomplica", "TechService",
    "Bragatel", "Gás Natural", "Águas do Rio", "Eletropaulo"
]
TIPOS_SERVICO_APTO = [
    "instalação de internet", "conserto de vazamento", "pintura", "limpeza", "dedetização",
    "montagem de móveis", "manutenção de ar condicionado", "eletricista", "encanador",
    "instalação de TV", "reforma na cozinha", "instalação de cortinas", "desentupimento",
    "mudança de mobília", "entrega de água", "entrega de gás", "assistência técnica", "reparo de eletrodoméstico"
]
TIPOS_SERVICO_CONDOMINIO = [
    "manutenção do elevador", "leitura de luz", "corte de grama", "limpeza da piscina",
    "reparo no portão", "dedetização das áreas comuns", "limpeza da caixa d'água",
    "poda de árvores", "verificação de bombas", "vistoria predial", "reparo na fachada",
    "limpeza dos vidros", "reparos elétricos", "inspeção de segurança", "manutenção de interfone", "limpeza da caixa de gordura"
]
LOCAIS_EVENTO = [
    "salão de festas", "churrasqueira", "espaço gourmet", "academia", "quadra de esportes",
    "piscina coberta", "salão de jogos", "brinquedoteca", "auditório"
]

# Adicionar listas para nomes genéricos que podem ser substituídos
NOMES_VISITANTES = [
    "João", "Maria", "José", "Beatriz", "Fernando", "Carla", "Ricardo", "Patrícia", "Antônio", "Paula",
    "Roberto", "Sandra", "Felipe", "Mônica", "Guilherme", "Luana", "Rafael", "Camila", "Gustavo", "Larissa",
    "Daniel", "Sofia", "Vitor", "Isabela", "Caio", "Lívia", "Elias", "Giovanna"
]
NOMES_PRESTADORES = [
    "Márcio", "Silvia", "Alexandre", "Camila", "Roberto", "Daniela", "Marcelo", "Viviane", "Carlos", "Renata",
    "Eduardo", "Lúcia", "Sérgio", "Fernanda", "André", "Cristina", "Jorge", "Talita",
    "Paulo", "Valéria", "Bruno", "Patrícia"
]

# --- BLOCOS DE CONSTRUÇÃO DE FRASES ---

SAUDACOES_INICIO = ["Olá", "Oi", "Bom dia", "Boa tarde", "Boa noite", "Com licença", "Opa, tudo bem?"]
COMPLEMENTOS_FINAIS = { # Intent-specific complements
    "solicitar_entrega_refeicao": ["pode interfonar?", "o morador já está ciente.", "é para pagar na entrega.", "ele está esperando a {refeição}.", "confirma o {pedido}?"],
    "informar_entrega_pacote": ["pode deixar na portaria?", "precisa de assinatura.", "é uma {caixa} grande.", "o morador não está.", "chegou hoje."],
    "anunciar_visitante": ["ele está me esperando.", "ela sabe da minha visita.", "já avisei que estava chegando.", "fui convidado.", "confirmado pelo {morador}."],
    "solicitar_acesso_evento": ["confirmamos presença.", "o {morador} nos convidou.", "está liberado."],
    "anunciar_prestador_servico": ["já está agendado.", "ele já autorizou.", "sou o {nome_prestador}.", "preciso de acesso.", "para {serviço} de urgência."],
    "anunciar_servico_condominio": ["já está agendado.", "fomos solicitados pela síndica.", "para manutenção de rotina."],
    "morador_solicita_acesso": ["esqueci minha chave.", "não estou com o crachá.", "pode {liberar} o portão?", "preciso {entrar} urgente."],
}
DESPEDIDAS_POLIDAS = ["por favor", "obrigado", "obrigada", "agradeço", "por gentileza", "valeu", "grato"] # General polite endings

# Dicionário de sinônimos para aumentar a variabilidade do vocabulário
SINONIMOS = {
    "apartamento": ["apartamento", "apto", "ap.", "unidade", "residência"],
    "entrega": ["entrega", "pedido", "encomenda", "remessa", "delivery"],
    "visitar": ["visitar", "ver", "falar com", "encontrar", "comparecer"],
    "técnico": ["técnico", "instalador", "profissional", "especialista", "engenheiro"],
    "morador": ["morador", "residente", "condômino", "proprietário"],
    "pacote": ["pacote", "caixa", "volume", "embrulho", "encomenda"],
    "serviço": ["serviço", "trabalho", "tarefa", "atividade", "reparo", "manutenção"],
    "refeição": ["refeição", "comida", "almoço", "jantar", "pizza", "sushi", "marmita", "lanche"],
    "liberar": ["liberar", "abrir", "autorizar", "permitir", "destrancar"],
    "abrir": ["abrir", "destrancar", "liberar"], # Adiciona "abrir" como sinônimo para "liberar"
    "entrar": ["entrar", "acessar", "ingressar"],
    "evento": ["evento", "festa", "confraternização", "reunião", "comemoração"],
    "local": ["local", "espaço", "área"],
    "pedido": ["pedido", "solicitação", "encomenda"],
    "comida": ["comida", "refeição", "alimento"],
    "caixa": ["caixa", "pacote", "volume"],
}

# --- ESTRUTURAS DE NÚCLEO PARA CADA INTENÇÃO (Expandido e adaptado) ---

ESTRUTURAS_INTENT = {
    "solicitar_entrega_refeicao": {
        "nucleos": [
            "É uma {entrega} do {empresa} para o {apartamento} {apto}.",
            "Tenho um {pedido} do {empresa} para o {morador}, do {apartamento} {apto}.",
            "{empresa} para o {apartamento} {apto}.",
            "Vim trazer uma {refeição} para a {unidade} {apto}.",
            "Chegou o {delivery} do {empresa} para o {apto}.",
            "Comida para o {apartamento} {apto}.",
            "Entrega de {comida} do {empresa} para o {morador}.",
            "É o motoboy do {empresa} para o {morador} no {apto}.",
            "Uma {refeição} para o {apto}.",
            "O {morador} do {apto} pediu {comida} do {empresa}.",
            "Chegou a {pizza} para o {apto}." # Exemplo de sinônimo específico no núcleo
        ],
        "entidades": {
            "empresa": EMPRESAS_DELIVERY_COMIDA,
            "apto": APARTAMENTOS,
            "morador": MORADORES,
            "entrega": SINONIMOS["entrega"], # Usa sinônimos diretamente aqui como opção de entidade
            "pedido": SINONIMOS["pedido"],
            "refeição": SINONIMOS["refeição"],
            "unidade": SINONIMOS["apartamento"],
            "delivery": SINONIMOS["entrega"],
            "comida": SINONIMOS["refeição"],
            "pizza": ["pizza", "hambúrguer", "sushi"] # Entidades que podem ser "sinônimos" contextuais
        }
    },
    "informar_entrega_pacote": {
        "nucleos": [
            "Tenho um {pacote} da {empresa} para o {apartamento} {apto}.",
            "{entrega} do {empresa} para o {morador}, {apartamento} {apto}.",
            "Sou dos Correios, {entrega} para o {apto}.",
            "Uma {caixa} da {empresa} para o {apartamento} {apto} do {morador}.",
            "Chegou um {volume} para o {morador} no {apto}.",
            "É uma {encomenda} para o {morador} do {apto}.",
            "Pacote da {empresa} para o {apto}.",
            "Correspondência para o {morador}."
        ],
        "entidades": {
            "empresa": EMPRESAS_ECOMMERCE,
            "apto": APARTAMENTOS,
            "morador": MORADORES,
            "entrega": SINONIMOS["entrega"],
            "pacote": SINONIMOS["pacote"],
            "caixa": SINONIMOS["caixa"],
            "volume": SINONIMOS["pacote"],
            "encomenda": SINONIMOS["entrega"]
        }
    },
    "anunciar_visitante": {
        "nucleos": [
            "Eu vim {visitar} o {morador} do {apartamento} {apto}.",
            "Gostaria de {visitar} a {morador} no {apartamento} {apto}.",
            "Sou convidado do {morador}, do {apto}.",
            "Meu nome é {nome_visitante}, vim {ver} o {morador} do {apto}.",
            "Visita para o {apto}, o {morador} me espera.",
            "Sou a {nome_visitante}, sou {visita} do {morador} no {apto}.",
            "Vim {encontrar} o {morador} do {apto}.",
            "A {morador} do {apto} me chamou.",
            "Sou {nome_visitante}, para o {apartamento} {apto}."
        ],
        "entidades": {
            "morador": MORADORES,
            "apto": APARTAMENTOS,
            "visitar": SINONIMOS["visitar"],
            "ver": SINONIMOS["visitar"],
            "encontrar": SINONIMOS["visitar"],
            "nome_visitante": NOMES_VISITANTES,
            "visita": ["visita", "convidado", "amigo"] # Entidade para variação de palavra "visita"
        }
    },
    "solicitar_acesso_evento": { # Convertido para a estrutura de dicionário
        "nucleos": [
            "Meu nome é {nome_visitante}, vim para a {festa} no {local_evento}.",
            "Fui convidado para o {evento} no {local_evento} do anfitrião {morador}.",
            "Vim para o {churrasco} na {local_evento}.",
            "Sou {nome_visitante}, estou aqui para o {evento} no {local_evento}.",
            "A {festa} do {morador} é no {local_evento}.",
            "{evento} no {local_evento}.",
            "Sou {convidado} do {morador} para o {local_evento}.",
            "Vim para a {confraternização} no {local_evento}."
        ],
        "entidades": {
            "nome_visitante": NOMES_VISITANTES,
            "local_evento": LOCAIS_EVENTO,
            "morador": MORADORES,
            "festa": SINONIMOS["evento"],
            "evento": SINONIMOS["evento"],
            "churrasco": ["churrasco", "festa", "confraternização"], # Específico
            "convidado": ["convidado", "participante"],
            "confraternização": SINONIMOS["evento"]
        }
    },
    "anunciar_prestador_servico": {
        "nucleos": [
            "Sou o {técnico} da {empresa}, vim fazer um {serviço} de {tipo_servico} no {apartamento} {apto}.",
            "Vim realizar um {serviço} de {tipo_servico} no {apto} para o {morador}.",
            "Meu nome é {nome_prestador}, sou {profissão} para o {apto}.", # Adicionado profissão
            "Profissional da {empresa} para {tipo_servico} no {apto}.",
            "É o {nome_prestador}, para {tipo_servico} no {apto} do {morador}.",
            "O {eletricista} para o {apto}.", # Exemplo de tipo de técnico no núcleo
            "Vim para a {instalação} de internet no {apto}."
        ],
        "entidades": {
            "empresa": EMPRESAS_SERVICO,
            "tipo_servico": TIPOS_SERVICO_APTO,
            "apto": APARTAMENTOS,
            "morador": MORADORES,
            "técnico": SINONIMOS["técnico"],
            "serviço": SINONIMOS["serviço"],
            "nome_prestador": NOMES_PRESTADORES,
            "profissão": ["eletricista", "encanador", "diarista", "montador", "dedetizador"],
            "eletricista": ["eletricista"], # Entidade específica para o exemplo
            "instalação": ["instalação", "montagem"]
        }
    },
    "anunciar_servico_condominio": {
        "nucleos": [
            "Viemos fazer a {serviço_condominio}.",
            "Somos da {empresa}, viemos para a {serviço_condominio}.",
            "Leitura da {empresa_leitura}.",
            "Equipe de {serviço_condominio} do condomínio.",
            "Manutenção da {empresa} aqui no prédio.",
            "É para a {serviço_condominio} nas áreas comuns.",
            "Vistoria dos bombeiros.", # Frase sem placeholder
            "Limpeza geral do condomínio." # Frase sem placeholder
        ],
        "entidades": {
            "serviço_condominio": TIPOS_SERVICO_CONDOMINIO,
            "empresa": EMPRESAS_SERVICO,
            "empresa_leitura": ["Copel", "Sanepar", "Enel", "Sabesp", "CEDAE"]
        }
    },
    "morador_solicita_acesso": {
        "nucleos": [
            "Sou {morador} do {apto}, pode {liberar} pra mim?",
            "Esqueci minha chave, sou o {morador_residente} do {apartamento} {apto}.",
            "É o {morador_condomino}, do {apto}, pode {abrir} o portão?",
            "Preciso {entrar} no meu {apartamento}, {apto}.",
            "Olá, sou o {morador} do {apto}.",
            "Pode {liberar} aqui?",
            "Eu sou o {morador}.",
            "A {moradora} do {apartamento} {apto} precisa entrar.",
            "Sou do {apto}, {liberar} a entrada."
        ],
        "entidades": {
            "morador": MORADORES,
            "apto": APARTAMENTOS,
            "liberar": SINONIMOS["liberar"],
            "abrir": SINONIMOS["abrir"],
            "entrar": SINONIMOS["entrar"],
            "morador_residente": SINONIMOS["morador"],
            "morador_condomino": SINONIMOS["morador"],
            "moradora": MORADORES # Para variar o gênero se necessário
        }
    }
}


def apply_text_variations(text_input):
    """
    Aplica variações de capitalização e pontuação final.
    """
    text = text_input.strip()

    # 1. Capitalização
    if random.random() < 0.7:  # 70% chance de começar com maiúscula
        text = text[0].upper() + text[1:]
    elif random.random() < 0.3: # 30% chance de ser todo em minúsculas
        text = text.lower()

    # 2. Pontuação final
    # Se a frase já termina com pontuação comum, não altera.
    # Verifica se a última palavra não é uma entidade que termina com ponto (ex: "ap.")
    if not text.endswith(('.', '?', '!', ';')):
        if random.random() < 0.6:  # 60% chance de adicionar . ou !
            text += random.choice(['.', '!'])
        elif random.random() < 0.3:  # 30% chance de ser uma pergunta
            text += '?'
        # 10% chance de não ter pontuação final

    # 3. Limpeza de espaços e pontuação
    text = re.sub(r'\s+', ' ', text).strip() # Remove múltiplos espaços e espaços nas extremidades
    text = re.sub(r'\s([.,?!;])', r'\1', text) # Corrige espaços antes de pontuação (ex: "texto .")
    
    return text


def gerar_exemplo_totalmente_variado(intent_name):
    """Gera um único exemplo de frase com alta variabilidade sintática e lexical."""
    
    intent_config = ESTRUTURAS_INTENT[intent_name]
    
    nucleo_template = random.choice(intent_config["nucleos"])
    all_possible_entities_for_intent = intent_config["entidades"]

    frase_gerada = nucleo_template
    entidades_extraidas = {}

    # 1. Substituir entidades pelos valores aleatórios
    # Itera sobre todas as entidades possíveis para a intenção
    # Usa um padrão de regex para encontrar o placeholder e substituir de forma segura.
    for entidade_nome, lista_valores in all_possible_entities_for_intent.items():
        placeholder_pattern = r"{" + re.escape(entidade_nome) + r"}"
        if re.search(placeholder_pattern, frase_gerada): # Verifica se o placeholder existe no nucleo
            valor_aleatorio = str(random.choice(lista_valores))
            # Substitui apenas a primeira ocorrência para evitar loop infinito com sinônimos no próprio valor
            frase_gerada = re.sub(placeholder_pattern, valor_aleatorio, frase_gerada, 1) 
            entidades_extraidas[entidade_nome] = valor_aleatorio


    # 2. Aplicar substituição de sinônimos (palavras completas)
    # Itera sobre as chaves do dicionário de sinônimos
    for palavra_chave, lista_sinonimos in SINONIMOS.items():
        # Cria um padrão de regex para encontrar a palavra_chave como uma palavra completa
        # (usando \b para limites de palavra)
        # E substitui por um sinônimo aleatório, mas apenas se a palavra-chave estiver presente
        if re.search(r'\b' + re.escape(palavra_chave) + r'\b', frase_gerada, re.IGNORECASE):
            sinonimo_aleatorio = random.choice(lista_sinonimos)
            frase_gerada = re.sub(r'\b' + re.escape(palavra_chave) + r'\b', sinonimo_aleatorio, frase_gerada, flags=re.IGNORECASE)

    # 3. Adicionar componentes opcionais (saudações, complementos, despedidas)
    final_text = frase_gerada

    # Saudações de início
    if random.random() < 0.5: # 50% de chance de ter saudação
        final_text = f"{random.choice(SAUDACOES_INICIO)}, {final_text}"
    
    # Complementos específicos da intenção
    if intent_name in COMPLEMENTOS_FINAIS and random.random() < 0.4: # 40% de chance de ter complemento
        complemento_base = random.choice(COMPLEMENTOS_FINAIS[intent_name])
        # Tenta substituir placeholders dentro do complemento
        for ent_name, ent_val in entidades_extraidas.items():
            complemento_base = complemento_base.replace(f"{{{ent_name}}}", ent_val)
        
        final_text = f"{final_text} {complemento_base}" # Sem ponto aqui, a função de variações vai adicionar.

    # Despedidas polidas (gerais)
    if random.random() < 0.3: # 30% de chance de ter despedida polida
        final_text = f"{final_text} {random.choice(DESPEDIDAS_POLIDAS)}" # Sem ponto aqui

    # 4. Aplica as variações de texto finais (capitalização, pontuação, limpeza)
    final_text = apply_text_variations(final_text)

    return {
        "intent": intent_name,
        "text": final_text,
        "entities": entidades_extraidas
    }


def gerar_dataset_inteligente(num_exemplos_por_intent):
    """Gera o dataset completo e balanceado."""
    dataset = []
    for intent_name in ESTRUTURAS_INTENT.keys():
        for _ in range(num_exemplos_por_intent):
            dataset.append(gerar_exemplo_totalmente_variado(intent_name))
    
    random.shuffle(dataset)
    return dataset




def salvar_dataset_em_jsonl(dataset,num_exemplos):
    """Salva o dataset gerado em um arquivo .jsonl."""
    nome_arquivo= "dataset_{}.jsonl".format(num_exemplos)
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for entrada in dataset:
            f.write(json.dumps(entrada, ensure_ascii=False) + '\n')
    print(f"Dataset com {len(dataset)} exemplos de alta variabilidade salvo em '{nome_arquivo}'")


if __name__ == "__main__":
    try:
        num_exemplos = int(input("Digite o número de exemplos a serem gerados POR intenção: "))
        if num_exemplos <= 0:
            print("Por favor, digite um número positivo.")
        else:
            dados_gerados = gerar_dataset_inteligente(num_exemplos)
            salvar_dataset_em_jsonl(dados_gerados,num_exemplos)
    except ValueError:
        print("Entrada inválida. Por favor, digite um número inteiro.")

