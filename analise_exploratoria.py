import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS

# --- CONFIGURAÇÕES ---
INPUT_FILE = 'dataset_portaria_profissional_500.jsonl'
RESULTS_FOLDER = 'results'
STOPWORDS_ADICIONAIS = {'pra', 'pro', 'tá', 'né', 'aí', 'então', 'tipo', 'sabe', 'meu', 'minha', 'nome', 'vim', 'fazer', 'falar'}

# --- FUNÇÕES AUXILIARES ---

def carregar_dados(filepath):
    """Carrega o arquivo .jsonl para um DataFrame do Pandas."""
    print(f"Carregando dados de '{filepath}'...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f]
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{filepath}' não foi encontrado.")
        return None
    
    df = pd.json_normalize(data)
    print("Dados carregados com sucesso!")
    return df

def analise_geral(df):
    """Imprime estatísticas gerais sobre o dataset."""
    print("\n--- 1. Visão Geral do Dataset ---")
    print(f"Número total de exemplos: {len(df)}")
    # Cria uma lista de colunas principais para não poluir o output
    colunas_principais = ['intent', 'sugestao_acao', 'metadata.texto_original', 'metadata.idioma']
    print(f"Número total de colunas (incluindo sub-campos): {len(df.columns)}")
    print(f"Amostra de colunas principais: {colunas_principais}")
    
    # Salva as informações em um arquivo de texto para registro
    filepath = os.path.join(RESULTS_FOLDER, 'visao_geral.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("--- Visão Geral do Dataset ---\n")
        f.write(f"Número total de exemplos: {len(df)}\n")
        f.write(f"Número total de colunas (incluindo sub-campos): {len(df.columns)}\n\n")
        f.write("Lista completa de colunas extraídas do JSON:\n")
        for col in df.columns.tolist():
            f.write(f"- {col}\n")
    print(f"Arquivo 'visao_geral.txt' salvo na pasta '{RESULTS_FOLDER}'.")

def salvar_tabela_visual(df_tabela, titulo, filepath):
    """Salva um DataFrame do Pandas como uma imagem de tabela bem formatada."""
    fig, ax = plt.subplots(figsize=(8, max(2, len(df_tabela) * 0.5))) # Ajusta a altura da imagem
    ax.axis('tight')
    ax.axis('off')
    tabela = ax.table(cellText=df_tabela.values, colLabels=df_tabela.columns, rowLabels=df_tabela.index, cellLoc='center', loc='center')
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)
    tabela.scale(1.2, 1.2)
    plt.title(titulo, fontsize=16, y=1.05)
    plt.savefig(filepath, bbox_inches='tight', dpi=200)
    plt.close()
    print(f"Tabela visual salva em: '{filepath}'")

# --- FUNÇÕES DE ANÁLISE ---

def analise_de_intents(df):
    print("\n--- 2. Análise das Intenções (Intents) ---")
    intent_counts = df['intent'].value_counts().to_frame(name='Contagem')
    print("Distribuição de exemplos por intenção:")
    print(intent_counts)
    
    # Salva em CSV e como imagem
    intent_counts.to_csv(os.path.join(RESULTS_FOLDER, 'distribuicao_intents.csv'))
    salvar_tabela_visual(intent_counts, 'Distribuição de Intenções', os.path.join(RESULTS_FOLDER, 'tabela_distribuicao_intents.png'))
    
    plt.figure(figsize=(12, 7)); sns.barplot(x=intent_counts.index, y=intent_counts['Contagem'], palette="viridis")
    plt.title('Distribuição de Intenções no Dataset', fontsize=16); plt.ylabel('Número de Exemplos', fontsize=12); plt.xlabel('Intenção', fontsize=12)
    plt.xticks(rotation=45, ha='right'); plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, 'grafico_distribuicao_intents.png'))
    print(f"\nGráfico 'grafico_distribuicao_intents.png' salvo na pasta '{RESULTS_FOLDER}'.")

def analise_de_texto(df):
    print("\n--- 3. Análise do Texto Original ---")
    df['comprimento_texto'] = df['metadata.texto_original'].str.len()
    stats_texto = df['comprimento_texto'].describe().to_frame(name='Estatísticas')
    print("Estatísticas do comprimento das frases:")
    print(stats_texto)

    # Salva em CSV e como imagem
    stats_texto.to_csv(os.path.join(RESULTS_FOLDER, 'estatisticas_texto.csv'))
    salvar_tabela_visual(stats_texto, 'Estatísticas do Comprimento do Texto', os.path.join(RESULTS_FOLDER, 'tabela_estatisticas_texto.png'))

    plt.figure(figsize=(10, 6)); sns.histplot(df['comprimento_texto'], bins=30, kde=True)
    plt.title('Distribuição do Comprimento das Frases', fontsize=16); plt.xlabel('Número de Caracteres'); plt.ylabel('Frequência')
    plt.tight_layout(); plt.savefig(os.path.join(RESULTS_FOLDER, 'grafico_comprimento_frases.png'))
    print(f"\nGráfico 'grafico_comprimento_frases.png' salvo na pasta '{RESULTS_FOLDER}'.")
    
    print("\nGerando nuvem de palavras...")
    texto_completo = ' '.join(df['metadata.texto_original'])
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=STOPWORDS.union(STOPWORDS_ADICIONAIS), min_font_size=10).generate(texto_completo)
    plt.figure(figsize=(10, 7)); plt.imshow(wordcloud, interpolation='bilinear'); plt.axis('off'); plt.title('Nuvem de Palavras Mais Frequentes', fontsize=16)
    plt.tight_layout(); plt.savefig(os.path.join(RESULTS_FOLDER, 'nuvem_de_palavras.png'))
    print(f"Imagem 'nuvem_de_palavras.png' salva na pasta '{RESULTS_FOLDER}'.")

def analise_vocabulario(df):
    """NOVA MÉTRICA: Calcula a riqueza de vocabulário (Type-Token Ratio)."""
    print("\n--- 4. Análise de Riqueza do Vocabulário ---")
    texto_completo = ' '.join(df['metadata.texto_original']).lower()
    tokens = texto_completo.split()
    types = set(tokens)
    ttr = len(types) / len(tokens) if tokens else 0
    
    resultado = f"Total de Palavras (Tokens): {len(tokens)}\n"
    resultado += f"Palavras Únicas (Types): {len(types)}\n"
    resultado += f"Riqueza Lexical (Type-Token Ratio): {ttr:.4f}\n"
    print(resultado)
    with open(os.path.join(RESULTS_FOLDER, 'analise_vocabulario.txt'), 'w', encoding='utf-8') as f:
        f.write(resultado)

def analise_entidades_e_coocorrencia(df):
    """Analisa a frequência das entidades e a co-ocorrência entre elas."""
    print("\n--- 5. Análise das Entidades e Co-ocorrência ---")
    entity_cols = sorted([col for col in df.columns if col.startswith('entities.') and len(df[col].dropna()) > 0])
    
    # Análise de frequência
    entity_counts = df[entity_cols].notna().sum().sort_values(ascending=False).to_frame(name='Contagem')
    entity_counts.index = entity_counts.index.str.replace('entities.', '')
    print("Frequência de preenchimento de cada entidade:")
    print(entity_counts)
    entity_counts.to_csv(os.path.join(RESULTS_FOLDER, 'frequencia_entidades.csv'))
    salvar_tabela_visual(entity_counts, 'Frequência de Entidades', os.path.join(RESULTS_FOLDER, 'tabela_frequencia_entidades.png'))

    # NOVA MÉTRICA: Análise de co-ocorrência
    print("\nGerando mapa de calor de co-ocorrência de entidades...")
    df_entities_bool = df[entity_cols].notna().astype(int)
    df_entities_bool.columns = df_entities_bool.columns.str.replace('entities.', '')
    co_occurrence_matrix = df_entities_bool.T.dot(df_entities_bool)
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(co_occurrence_matrix, annot=True, fmt='d', cmap='Blues')
    plt.title('Mapa de Calor de Co-ocorrência de Entidades', fontsize=16)
    plt.xticks(rotation=45, ha='right'); plt.yticks(rotation=0)
    plt.tight_layout(); plt.savefig(os.path.join(RESULTS_FOLDER, 'heatmap_coocorrencia_entidades.png'))
    print(f"Heatmap 'heatmap_coocorrencia_entidades.png' salvo na pasta '{RESULTS_FOLDER}'.")


if __name__ == '__main__':
    os.makedirs(RESULTS_FOLDER, exist_ok=True)
    df_dados = carregar_dados(INPUT_FILE)
    
    if df_dados is not None:
        analise_geral(df_dados)
        analise_de_intents(df_dados)
        analise_de_texto(df_dados)
        analise_vocabulario(df_dados)
        analise_entidades_e_coocorrencia(df_dados)
        print("\n--- Análise Exploratória de Dados (EDA) Concluída! ---")
        print(f"Todos os resultados (CSV, PNG, TXT) foram salvos na pasta '{RESULTS_FOLDER}'.")