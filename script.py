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

# --- FUNÇÕES GERADORAS DE EXEMPLOS POR INTENT (INCLUINDO OS "DIFÍCEIS") ---

def gerar_entrega_refeicao():
    nome_morador = faker.name()
    morador_genero = 'F' # Simplificação para o exemplo
    empresa = random.choice(ENTIDADES_DB["empresas_delivery"])
    apto = str(random.randint(1, 20) * 100 + random.randint(1, 10))
    
    entities = {"morador": {"nome": nome_morador, "genero": morador_genero}, "empresa": empresa, "destino": {"tipo": "unidade", "identificador": apto}, "requer_pagamento": random.choice([True, False, None])}
    
    frases_possiveis = [f"entrega do {empresa} para o apartamento {apto}", f"tenho um pedido do {empresa} para {nome_morador}", f"é uma entrega para {nome_morador} no apartamento {apto}"]
    if random.random() < 0.3:
        frases_possiveis.append(f"delivery do {empresa} para o {apto}"); entities.pop("morador", None)
    if random.random() < 0.2:
        item = random.choice(ENTIDADES_DB["tipos_item_entrega"]); frases_possiveis.append(f"entrega de {item} para o apto {apto}"); entities.pop("empresa", None); entities["tipo_item"] = item

    return random.choice(frases_possiveis), entities, "solicitar_entrega_refeicao", "NOTIFICAR_MORADOR"

def gerar_anuncio_visitante():
    nome_morador = faker.name()
    morador_genero = 'M' # Simplificação para o exemplo
    nome_visitante = faker.name()
    visitante_genero = 'M' # Simplificação para o exemplo
    apto = str(random.randint(1, 20) * 100 + random.randint(1, 10))
    
    entities = {"morador": {"nome": nome_morador, "genero": morador_genero}, "visitante": {"nome": nome_visitante, "genero": visitante_genero}, "destino": {"tipo": "unidade", "identificador": apto}}
    
    frases_possiveis = [f"vim visitar {nome_morador} no {apto}, meu nome é {nome_visitante}", f"sou {nome_visitante} e vim ver o morador do {apto}", f"{nome_morador} está me esperando, sou {nome_visitante}"]
    frase = random.choice(frases_possiveis)
    
    if random.random() < 0.25:
        veiculo = {"placa": faker.license_plate(), "modelo": random.choice(ENTIDADES_DB["modelos_veiculo"]), "cor": random.choice(ENTIDADES_DB["cores_veiculo"])}
        entities["veiculo"] = veiculo
        frase += f", estou num {veiculo['modelo']} {veiculo['cor']}"
    return frase, entities, "anunciar_visitante", "NOTIFICAR_MORADOR"

def gerar_informacao_incompleta():
    frase_base, _, _, _ = random.choice([gerar_entrega_refeicao, gerar_anuncio_visitante])()
    palavras = frase_base.split()
    ponto_corte = random.randint(len(palavras) // 2, len(palavras) - 1)
    frase_cortada = " ".join(palavras[:ponto_corte]) + "..."
    return frase_cortada, {}, "informacao_incompleta", "SOLICITAR_MAIS_INFORMACOES"

def gerar_fora_de_escopo():
    frase = random.choice(ENTIDADES_DB["frases_fora_de_escopo"])
    return frase, {}, "fora_de_escopo", "IGNORAR_OU_RESPONDER_GENERICAMENTE"

def gerar_multiplas_intencoes():
    frase1, entities1, intent1, _ = gerar_anuncio_visitante()
    frase2, entities2, intent2, _ = gerar_entrega_refeicao()
    
    frase_combinada = f"{frase1}, e também vim deixar essa entrega do {entities2.get('empresa','')} para o mesmo apartamento"
    
    entities1.update(entities2)
    entities1['sub_intents'] = [intent1, intent2]

    return frase_combinada, entities1, "multiplas_intencoes", "NOTIFICAR_MORADOR_COM_MULTIPLAS_ACOES"

# --- FUNÇÃO PRINCIPAL DE ORQUESTRAÇÃO ---

def gerar_exemplo_completo(gerador_func, dificuldade):
    frase_base, entities, intent, sugestao_acao = gerador_func()
    frase_final = aplicar_variacoes(frase_base, dificuldade)
    
    return {
        "intent": intent, "sugestao_acao": sugestao_acao, "entities": entities,
        # CORREÇÃO 2: Usando o método moderno para obter o timestamp em UTC
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
            if i < num_por_intent * 0.2:
                dificuldade = random.uniform(0.0, 0.3) # Fácil
            elif i < num_por_intent * 0.8:
                dificuldade = random.uniform(0.3, 0.7) # Médio
            else:
                dificuldade = random.uniform(0.7, 1.0) # Difícil
            
            exemplo = gerar_exemplo_completo(funcao_geradora, dificuldade)
            dataset_final.append(exemplo)
            
    random.shuffle(dataset_final)
    
    nome_arquivo = f"dataset_portaria_profissional_{len(dataset_final)}.jsonl"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        for item in dataset_final:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            
    print(f"\nSucesso! Dataset com {len(dataset_final)} exemplos foi gerado no arquivo '{nome_arquivo}'.")