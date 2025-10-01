import pandas as pd
import matplotlib.pyplot as plt


# ------------------------------------
# DEFINIÇÃO DE FUNÇÕES (Toda a lógica de tratamento)
# ------------------------------------

def carregar_dados(caminho_arquivo):
    """Lê o CSV e retorna o DataFrame de vendas. Trata o erro FileNotFoundError."""
    try:
        df = pd.read_csv(caminho_arquivo)
        return df
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{caminho_arquivo}' não foi encontrado. Verifique o caminho.")
        return None


def limpar_dados(df):
    """
    Trata valores ausentes, preenchendo o preço com a média, e remove linhas com ID de cliente nulo.
    """
    if df is None:
        return None

    # Corrigido: Preenche nulos do preço com a média (evita o FutureWarning)
    media_preco = df['Preco_Unitario'].mean()
    df['Preco_Unitario'] = df['Preco_Unitario'].fillna(media_preco)

    # Remover linhas com nulos em ID_Cliente (inplace=True faz a alteração no próprio df)
    df.dropna(subset=['ID_Cliente'], inplace=True)
    print("\nSucesso: Valores nulos tratados.")

    return df


def converter_para_datetime(df, nome_coluna='Data'):
    """Converte uma coluna específica de um DataFrame para o tipo datetime."""
    if df is None:
        return None

    if nome_coluna not in df.columns:
        print(f"ERRO: A coluna '{nome_coluna}' não foi encontrada no DataFrame. Ignorando conversão.")
        return df

    # errors='coerce' transforma strings inválidas em NaT (Not a Time)
    df[nome_coluna] = pd.to_datetime(df[nome_coluna], errors='coerce')
    print(f"Sucesso: Coluna '{nome_coluna}' convertida para o tipo datetime.")

    return df


def padronizar_colunas(df):
    """Padroniza a coluna 'Categoria' e cria a coluna 'Total_Venda'."""
    if df is None:
        return None

    # Padronizar a coluna 'Categoria' (ex: "eletronicos" vira "Eletronicos")
    df['Categoria'] = df['Categoria'].str.title()
    print("Sucesso: Coluna 'Categoria' padronizada.")

    # Cria coluna 'Total_Venda' (Receita = Preço * Quantidade)
    df['Total_Venda'] = df['Preco_Unitario'] * df['Quantidade']
    print("Sucesso: Coluna 'Total_Venda' calculada.")

    return df


# ------------------------------------
# EXECUÇÃO PRINCIPAL DO PROGRAMA
# ------------------------------------

if __name__ == "__main__":

    # 1. CARREGAR DADOS
    print("--- 1. CARREGANDO DADOS ---")
    df_vendas = carregar_dados('dados_vendas.csv')

    if df_vendas is None:
        exit()  # Encerra se o arquivo não for encontrado

    print("\nInformações iniciais:")
    df_vendas.info()

    # 2. LIMPAR E CONVERTER
    print("\n--- 2. LIMPEZA E CONVERSÃO ---")
    df_limpo = limpar_dados(df_vendas)
    df_limpo = converter_para_datetime(df_limpo, nome_coluna='Data')
    df_final = padronizar_colunas(df_limpo)

    print("\nAs 5 primeiras linhas do DataFrame FINAL (limpo e tratado):")
    print(df_final.head())

    # 3. ANÁLISE E AGRUPAMENTOS
    print("\n--- 3. RESULTADOS DA ANÁLISE ---")

    # A) Produtos mais vendidos (em quantidade)
    produtos_mais_vendidos = df_final.groupby('Produto')['Quantidade'].sum().sort_values(ascending=False)
    print("\nProdutos mais vendidos (Top 5 em quantidade):")
    print(produtos_mais_vendidos.head())

    # B) Receita por categoria
    receita_por_categoria = df_final.groupby('Categoria')['Total_Venda'].sum().sort_values(ascending=False)
    print("\nReceita por Categoria:")
    print(receita_por_categoria)

    # C) Top Clientes por Gasto
    top_clientes = df_final.groupby('ID_Cliente')['Total_Venda'].sum().sort_values(ascending=False)
    print("\nTop 3 Clientes por Gasto:")
    print(top_clientes.head(3))

    # 4. VISUALIZAÇÃO DO GRÁFICO (DESAFIO BÔNUS)
    print("\n--- 4. VISUALIZAÇÃO ---")

    # Plota o gráfico de barras da receita por categoria
    receita_por_categoria.plot(kind='bar', figsize=(10, 6))

    plt.title('Receita Total por Categoria de Produto')  # Título do gráfico
    plt.xlabel('Categoria')  # Nome do eixo X
    plt.ylabel('Receita (R$)')  # Nome do eixo Y
    plt.xticks(rotation=45)  # Rotaciona os nomes no eixo X

    plt.tight_layout()  # Ajusta o layout para caber todos os rótulos

    # Salva o gráfico como arquivo PNG
    plt.savefig('receita_por_categoria.png')
    print("Gráfico salvo com sucesso como 'receita_por_categoria.png' na pasta do projeto.")

# Fim do script