# Dataset/script.py

import json
import random
import uuid
from datetime import datetime, timezone

# Pré-requisito: pip install Faker
from faker import Faker

# Inicializa o Faker para gerar dados em Português do Brasil
faker = Faker('pt_BR')

# --- BANCO DE DADOS DE ENTIDADES E VOCABULÁRIO ---
ENTIDADES_DB = {
    "empresas_delivery": ["iFood", "Rappi", "Uber Eats", "99Food", "Loggi", "James Delivery", "Correios"],
    "empresas_ecommerce": ["Mercado Livre", "Amazon", "Shopee", "Magazine Luiza", "Shein", "AliExpress"],
    "empresas_servico": ["Vivo", "Claro", "Sanepar", "Copel", "Orkin", "ConsertaTudo Reparos", "GVT", "Oi"],
    "profissoes_masculinas": ["eletricista", "encanador", "pintor", "técnico de internet", "montador de móveis", "jardineiro", "marido de aluguel"],
    "profissoes_femininas": ["diarista", "pintora", "jardineira", "técnica de ar condicionado", "decoradora", "faxineira"],
    "tipos_servico": ["reparo", "instalação", "manutenção", "orçamento", "verificação", "conserto", "uma visita técnica"],
    "modelos_veiculo": ["Gol", "Onix", "HB20", "Mobi", "Kwid", "Strada", "Toro", "Corolla", "Civic", "Creta", " Renegade", "Compass"],
    "cores_veiculo": ["prata", "preto", "branco", "cinza", "vermelho", "azul", "grafite"],
    "locais_evento": ["salão de festas", "churrasqueira", "espaço gourmet", "piscina", "quadra de esportes", "salão de jogos"],
    "tipos_item_entrega": ["comida", "remédio", "documentos", "flores", "um presente", "uma pizza"],
    "tamanhos_volume": ["pequeno", "médio", "grande", "um envelope"],
    "saudacoes": ["Oi", "Olá", "Bom dia", "Boa tarde", "Boa noite", "Com licença", "Opa", "E aí", ""],
    "vicios_linguagem": ["tipo", "sabe?", "então...", "é que", "aí", "uhm", "tipo assim", "né", "veja bem", ""],
    "finalizacoes_polidas": ["por favor", "obrigado", "obrigada", "valeu", "agradecido", "ok?", ""],
    "erros_gramaticais_substituicoes": {
        "para o": ["pro", "pru"], "para a": ["pra"], "está": ["tá"], "estou": ["tô"],
        "nós vamos": ["a gente vai"], "para eu": ["pra mim"], "o apartamento": ["u apartamento"],
        "os moradores": ["os morador"], "as entregas": ["as entrega"]
    },
    "frases_fora_de_escopo": [
        "Nossa, que dia bonito hoje, né?", "Você sabe que horas são?", "Onde tem um ponto de ônibus por aqui?",
        "Esse condomínio é novo?", "Tem algum apartamento pra alugar aqui?", "O tempo hoje tá meio doido."
    ]
}

# --- FUNÇÕES DE VARIAÇÃO E "RUÍDO" COM CONTROLE DE DIFICULDADE ---

def aplicar_variacoes(frase, dificuldade=0.5):
    """Aplica uma série de variações aleatórias a uma frase base, controladas pelo parâmetro de dificuldade (0.0 a 1.0)."""
    
    if random.random() < 0.4 * dificuldade:
        vicio = random.choice(ENTIDADES_DB["vicios_linguagem"])
        if vicio:
            palavras = frase.split()
            palavras.insert(random.randint(0, len(palavras)), vicio)
            frase = " ".join(palavras)

    if random.random() < 0.5 * dificuldade:
        for original, substitutos in ENTIDADES_DB["erros_gramaticais_substituicoes"].items():
            if original in frase and random.random() < 0.5:
                frase = frase.replace(original, random.choice(substitutos), 1)

    if random.random() < 0.7:
        saudacao = random.choice(ENTIDADES_DB["saudacoes"])
        if saudacao:
            frase = f"{saudacao}, {frase.lower()}"

    if random.random() < 0.5:
        finalizacao = random.choice(ENTIDADES_DB["finalizacoes_polidas"])
        if finalizacao:
            frase = f"{frase}, {finalizacao}"
            
    frase = frase.strip()
    frase = frase[0].upper() + frase[1:]
    if not frase.endswith(('.', '?', '!')):
        frase += random.choice(['.', '...', '!', ''])

    return ' '.join(frase.split())

# --- NOVA FUNÇÃO AUXILIAR ---
def _gerar_nome_opcional(genero):
    """Gera um nome, às vezes completo (60%), às vezes só o primeiro (40%)."""
    if random.random() < 0.6:
        # 60% de chance de nome completo
        return faker.name() 
    else:
        # 40% de chance de só o primeiro nome
        if genero == 'M':
            return faker.first_name_male()
        else:
            return faker.first_name_female()

# --- FUNÇÕES GERADORAS DE EXEMPLOS POR INTENT (ATUALIZADAS) ---

def gerar_entrega_refeicao():
    # --- Gerar dados base ---
    empresa = random.choice(ENTIDADES_DB["empresas_delivery"])
    morador_genero = 'F' # Mantendo a lógica original
    nome_morador = _gerar_nome_opcional(morador_genero) 
    apto = str(random.randint(1, 20) * 100 + random.randint(1, 10))
    
    # --- Entidades base ---
    entities = {"empresa": empresa, "requer_pagamento": random.choice([True, False, None])}
    frases_possiveis = []

    # --- Lógica de item especial (pode retornar cedo) ---
    if random.random() < 0.15: # Reduzi a chance para focar nos outros casos
        item = random.choice(ENTIDADES_DB["tipos_item_entrega"])
        frase_item = f"entrega de {item} para o apto {apto}"
        item_entities = {
            "tipo_item": item,
            "destino": {"tipo": "unidade", "identificador": apto},
            "requer_pagamento": random.choice([True, False, None])
        }
        return frase_item, item_entities, "solicitar_entrega_refeicao", "NOTIFICAR_MORADOR"

    # --- DECISÃO: O quão completa é a informação? (40% de chance de estar incompleto) ---
    if random.random() < 0.4:
        # --- CASO 1: Incompleto (sem apto) ---
        
        # Sub-caso: Tem nome do morador? (50% de chance)
        if random.random() < 0.5:
            entities["morador"] = {"nome": nome_morador, "genero": morador_genero}
            frases_possiveis.extend([
                f"entrega do {empresa} para {nome_morador}",
                f"tenho um pedido do {empresa} para {nome_morador}, sabe?"
            ])
        else:
            # O caso mais difícil: só a empresa
            frases_possiveis.extend([
                f"é uma entrega do {empresa}",
                f"delivery do {empresa}",
                f"tenho um pedido aqui do {empresa}"
            ])
    else:
        # --- CASO 2: Completo (com apto) ---
        entities["destino"] = {"tipo": "unidade", "identificador": apto}
        
        # Sub-caso: Tem nome do morador? (70% de chance)
        if random.random() < 0.7:
            entities["morador"] = {"nome": nome_morador, "genero": morador_genero}
            frases_possiveis.extend([
                f"entrega do {empresa} para o apartamento {apto}",
                f"tenho um pedido do {empresa} para {nome_morador} no {apto}",
                f"é uma entrega para {nome_morador} no apartamento {apto}"
            ])
        else:
            # Completo, mas sem nome (só apto)
            frases_possiveis.extend([
                f"delivery do {empresa} para o {apto}",
                f"entrega do {empresa} pro {apto}"
            ])

    return random.choice(frases_possiveis), entities, "solicitar_entrega_refeicao", "NOTIFICAR_MORADOR"

def gerar_anuncio_visitante():
    # --- Gerar dados base ---
    morador_genero = 'M' # Original
    visitante_genero = 'M' # Original
    nome_morador = _gerar_nome_opcional(morador_genero)
    nome_visitante = _gerar_nome_opcional(visitante_genero)
    apto = str(random.randint(1, 20) * 100 + random.randint(1, 10))
    
    entities = {"visitante": {"nome": nome_visitante, "genero": visitante_genero}}
    frases_possiveis = []

    # --- DECISÃO: Tem informação do morador? (80% de chance) ---
    if random.random() < 0.8:
        entities["morador"] = {"nome": nome_morador, "genero": morador_genero}

        # DECISÃO: Tem informação do apto? (70% de chance)
        if random.random() < 0.7:
            # --- CASO 1: Completo (Morador + Apto) ---
            entities["destino"] = {"tipo": "unidade", "identificador": apto}
            frases_possiveis.extend([
                f"vim visitar {nome_morador} no {apto}, meu nome é {nome_visitante}",
                f"sou {nome_visitante} e vim ver o morador do {apto}, {nome_morador}",
                f"{nome_morador} está me esperando no {apto}, sou {nome_visitante}"
            ])
        else:
            # --- CASO 2: Parcial (Morador, sem Apto) ---
            frases_possiveis.extend([
                f"vim visitar {nome_morador}, meu nome é {nome_visitante}",
                f"sou {nome_visitante} e vim ver {nome_morador}",
                f"{nome_morador} está me esperando, sou {nome_visitante}"
            ])
    else:
        # --- CASO 3: Incompleto (Sem morador, só visitante) ---
        # Sub-caso: Tem apto? (50% chance)
        if random.random() < 0.5:
            entities["destino"] = {"tipo": "unidade", "identificador": apto}
            frases_possiveis.extend([
                f"sou {nome_visitante} e vim no apartamento {apto}",
                f"meu nome é {nome_visitante}, eu vou no {apto}"
            ])
        else:
            # O caso mais difícil: só o visitante
            frases_possiveis.extend([
                f"oi, meu nome é {nome_visitante}",
                f"sou {nome_visitante}, eu pedi pra liberar"
            ])

    # Escolhe a frase base
    frase = random.choice(frases_possiveis)
    
    # Lógica original do veículo (preservada)
    if random.random() < 0.25:
        veiculo = {"placa": faker.license_plate(), "modelo": random.choice(ENTIDADES_DB["modelos_veiculo"]), "cor": random.choice(ENTIDADES_DB["cores_veiculo"])}
        entities["veiculo"] = veiculo
        frase += f", estou num {veiculo['modelo']} {veiculo['cor']}"
        
    return frase, entities, "anunciar_visitante", "NOTIFICAR_MORADOR"

def gerar_informacao_incompleta():
    # Esta função está boa, pois gera frases cortadas
    frase_base, _, _, _ = random.choice([gerar_entrega_refeicao, gerar_anuncio_visitante])()
    palavras = frase_base.split()
    # Garante que o corte não seja muito pequeno
    if len(palavras) < 3:
        frase_cortada = " ".join(palavras) + "..."
    else:
        ponto_corte = random.randint(len(palavras) // 2, len(palavras) - 1)
        frase_cortada = " ".join(palavras[:ponto_corte]) + "..."
    return frase_cortada, {}, "informacao_incompleta", "SOLICITAR_MAIS_INFORMACOES"

def gerar_fora_de_escopo():
    frase = random.choice(ENTIDADES_DB["frases_fora_de_escopo"])
    return frase, {}, "fora_de_escopo", "IGNORAR_OU_RESPONDER_GENERICAMENTE"

def gerar_multiplas_intencoes():
    # --- Parte 1: A Visita (Deve ser completa para a frase fazer sentido) ---
    
    # Gere os dados básicos
    morador_genero = 'M'
    visitante_genero = 'M'
    nome_morador = _gerar_nome_opcional(morador_genero)
    nome_visitante = _gerar_nome_opcional(visitante_genero)
    apto = str(random.randint(1, 20) * 100 + random.randint(1, 10))
    
    # Force a criação de uma frase de visita completa
    frase1_options = [
        f"vim visitar {nome_morador} no {apto}, meu nome é {nome_visitante}",
        f"sou {nome_visitante} e vim ver o morador do {apto}, {nome_morador}"
    ]
    frase1 = random.choice(frase1_options)
    
    # Force as entidades de visita completas
    entities1 = {
        "morador": {"nome": nome_morador, "genero": morador_genero},
        "visitante": {"nome": nome_visitante, "genero": visitante_genero},
        "destino": {"tipo": "unidade", "identificador": apto}
    }
    intent1 = "anunciar_visitante"

    # --- Parte 2: A Entrega (simples, só para complementar) ---
    empresa_entrega = random.choice(ENTIDADES_DB["empresas_delivery"])
    entities2 = {"empresa": empresa_entrega}
    intent2 = "solicitar_entrega_refeicao"
    
    # --- Combinação ---
    frase_combinada = f"{frase1}, e também vim deixar essa entrega do {empresa_entrega} para o mesmo apartamento"
    
    # Unir entidades
    entities1.update(entities2)
    entities1['sub_intents'] = [intent1, intent2]

    return frase_combinada, entities1, "multiplas_intencoes", "NOTIFICAR_MORADOR_COM_MULTIPLAS_ACOES"

# --- FUNÇÃO PRINCIPAL DE ORQUESTRAÇÃO ---

def gerar_exemplo_completo(gerador_func, dificuldade):
    frase_base, entities, intent, sugestao_acao = gerador_func()
    frase_final = aplicar_variacoes(frase_base, dificuldade)
    
    return {
        "intent": intent, "sugestao_acao": sugestao_acao, "entities": entities,
        "metadata": {"texto_original": frase_final, "timestamp": datetime.now(timezone.utc).isoformat(), "id_exemplo": str(uuid.uuid4())}
    }

# --- EXECUÇÃO DO SCRIPT ---

if __name__ == "__main__":
    geradores_de_intent = {
        "solicitar_entrega_refeicao": gerar_entrega_refeicao,
        "anunciar_visitante": gerar_anuncio_visitante,
        "informacao_incompleta": gerar_informacao_incompleta,
        "fora_de_escopo": gerar_fora_de_escopo,
        "multiplas_intencoes": gerar_multiplas_intencoes,
    }
    
    try:
        num_por_intent = int(input("Digite o número de exemplos a serem gerados por cada intent: "))
    except ValueError:
        print("Entrada inválida. Por favor, digite um número."); exit()

    dataset_final = []
    print("\nGerando dataset com distribuição de dificuldade...")
    
    for intent_nome, funcao_geradora in geradores_de_intent.items():
        print(f"  - Gerando {num_por_intent} exemplos para o intent '{intent_nome}'...")
        for i in range(num_por_intent):
            # Distribuição de dificuldade (como no original)
            if i < num_por_intent * 0.2:
                dificuldade = random.uniform(0.0, 0.3) # Fácil
            elif i < num_por_intent * 0.8:
                dificuldade = random.uniform(0.3, 0.7) # Médio
            else:
                dificuldade = random.uniform(0.7, 1.0) # Difícil
            
            exemplo = gerar_exemplo_completo(funcao_geradora, dificuldade)
            dataset_final.append(exemplo)
            
    random.shuffle(dataset_final)
    
    nome_arquivo = f"dataset_portaria_v2_{len(dataset_final)}.jsonl"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for item in dataset_final:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            
    print(f"\nSucesso! Dataset com {len(dataset_final)} exemplos foi gerado no arquivo '{nome_arquivo}'.")