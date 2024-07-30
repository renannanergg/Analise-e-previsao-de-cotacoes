import pandas as pd
from prophet import Prophet
import datetime as dt
import yfinance as yf


# Função de validar datas de acordo com API
def validar_datas(data_inicial_str, data_final_str):

    """Valida e converte as datas inicial e final para objetos datetime."""
    try:
        data_inicial = pd.to_datetime(data_inicial_str, format='%Y-%m-%d').date()
        data_final = pd.to_datetime(data_final_str, format='%Y-%m-%d').date()
    except ValueError:
        raise ValueError('Formato de data inválido. Utilize o formato aaaa-mm-dd.')
    if data_inicial > data_final:
        raise ValueError('Data inicial deve ser anterior à data final.')

    return data_inicial, data_final

# Funcção de validar o TICKER de acordo com API
def is_ticker_valid(ticker):
    '''
    Verifica se o Ticker é válido usando a API Yahoo Finance
    Args: Ticker (str) a ser validado
    Retorna : Bool True se for validado, False se der erro
    '''
    try:
        # Tenta obter dados do ticker usando YF
        yf.Ticker(ticker).info
        return True
    except Exception as e:
        print(f"Error checking ticker: {e}")
        # Retorne False para indicar ticker inválido
        return False

# Obtem dados dos ativos escolhidos pelo user
def obter_dados_ativos(ativos,data_inicial,data_final):
    """
    Função para obter os dados dos ativos no intervalo de datas especificado, utilizando a biblioteca yfinance.
    Args:
        ativos (lista): Lista de strings contendo os nomes dos ativos.
        data_inicial (datetime): Data inicial do período de análise.
        data_final (datetime): Data final do período de análise.
    Retorna:
        Um DataFrame Pandas contendo os dados dos ativos ou None em caso de erro
    """ 
    try:
        #Utiliza a lib yfinance para obter os dados
        df_historico=yf.download(ativos,start=data_inicial,end=data_final)
    except Exception as e:
        print(f'Erro ao obter dados dos ativos com yfinance: {e}')
        return None
    return df_historico

# Realiza previsão com IA
def prev_ia(df_historico):
     '''
        funcão que retorna um DataFrame com uma previsão do preço de um ativo feita pela Prophet dos próximos 365 dias
     
     '''
     # Pré-processe os dados para o Prophet
     dados_ativos=df_historico
     dados_ativos = dados_ativos.reset_index()
     dados_ativos.rename(columns={'index': 'Date'}, inplace=True)
     dados_ativos.rename(columns={'Date': 'ds'}, inplace=True)
     dados_ativos.dropna(subset=['ds'], inplace=True)  # Remove linhas com valores ausentes em 'ds'
     dados_ativos['ds'] = pd.to_datetime(dados_ativos['ds'])
     dados_ativos.rename(columns={'Adj Close': 'y'}, inplace=True)

    # Crie e ajuste o modelo Prophet
     model = Prophet()
     model.fit(dados_ativos)

    # Definir horizonte de previsão
     futuro = model.make_future_dataframe(periods=365, include_history=True)
    
    # Dataframe com as previsões
     df_previsões=model.predict(futuro)

    # Renomeando as colunas da previsão para melhor compreensão
     new_column_names = {
        'ds': 'Data',
        'trend': 'Tendência',
        'yhat_lower': 'Previsão_Mínima',
        'yhat_upper': 'Previsão_Máxima',
        'trend_lower': 'Tendência_Mínima',
        'trend_upper': 'Tendência_Máxima',
        'weekly_upper': 'Sazonalidade_Semanal_Máx',
        'multiplicative_terms': 'Termo_Multiplicativo',
        'multiplicative_terms_lower': 'Termo_Multiplicativo_Mín',
        'multiplicative_terms_upper': 'Termo_Multiplicativo_Máx',
        'yhat': 'Previsão'
}
     df_previsões.rename(columns=new_column_names, inplace=True)
   
    # Retorna DataFrame com previsões 
     return df_previsões

# Interpreta os dados das previsões
def interpret_previsões(df_previsões):
    """
    Interpreta os resultados da previsão do Prophet com análise detalhada.

    Args:
        df_previsões: DataFrame Pandas contendo as previsões do Prophet.

    Returns:
        Um dicionário contendo a interpretação textual e métricas relevantes.
    """

    # Extrai dados relevantes
    data_inicio = df_previsões['Data'].min()
    data_fim = df_previsões['Data'].max()
    data_referencia = df_previsões['Data'].iloc[0]
    yhat_inicial = df_previsões['Previsão'].iloc[0]
    yhat_final = df_previsões['Previsão'].iloc[-1]
    trend = df_previsões['Tendência'].iloc[-1]
    volatilidade = df_previsões['Previsão'].std()

    # Cálculo da variação percentual
    change_pct = (yhat_final - yhat_inicial) / yhat_inicial * 100

    # Análise da tendência com comentários
    if trend > 0.5:
        trend_descricao = "fortemente crescente"
    elif trend > 0:
        trend_descricao = "crescente"
    elif trend < -0.5:
        trend_descricao = "fortemente decrescente"
    elif trend < 0:
        trend_descricao = "decrescente"
    else:
        trend_descricao = "praticamente estável"

    # Análise da variação percentual com comentários
    if abs(change_pct) > 10:
        variação_descricao = "uma variação significativa"
    elif abs(change_pct) > 5:
        variação_descricao = "uma variação moderada"
    else:
        variação_descricao = "uma variação pequena"

    # Análise da volatilidade com comentários
    if volatilidade > 5:
        volatilidade_descricao = "alta volatilidade"
    elif volatilidade > 2:
        volatilidade_descricao = "moderada volatilidade"
    else:
        volatilidade_descricao = "baixa volatilidade"

    # Interpretação textual detalhada
    interpretação_texto = (
        f"O modelo prevê {variação_descricao} no preço do ativo, com uma variação percentual de {change_pct:.2f}%."
        f"Nos mostrando uma volatilidade de {volatilidade:.2f},ou seja uma {volatilidade_descricao} para o preço do ativo."
    )

    # Retorno da interpretação
    interpretação = interpretação_texto

    return interpretação

# Interpreta os dados dos históricos
def interpret_historico(df_historico):
    """
    Analisa um DataFrame com dados de preços de um ativo e gera comentários.

    Args:
        df_historico (pd.DataFrame): DataFrame com as colunas 'Date', 'Close', 'Adj Close', 'Volume'.

    Returns:
        str: String com os comentários sobre o desempenho do ativo.
    """

    # Calcular indicadores
    df=df_historico
    df['Retorno'] = df['Close'].pct_change() * 100
    retorno_medio = df['Retorno'].mean()
    volatilidade = df['Retorno'].std()
    maximo = df['Close'].max()
    minimo = df['Close'].min()
    fechamento = df['Close'].iloc[-1]

    # Analisar tendências
    if df['Close'].iloc[-1] > df['Close'].iloc[0]:
        tendencia = 'alta'
    elif df['Close'].iloc[-1] < df['Close'].iloc[0]:
        tendencia = 'baixa'
    else:
        tendencia = 'lateral'

 # Gerar comentários e observações adicionais
    comentarios = f"""
# O ativo apresentou uma tendência {tendencia} no período analisado.
O retorno médio foi de {retorno_medio:.2f}%.
A volatilidade foi de {volatilidade:.2f}%.
O preço máximo atingido foi de {maximo:.2f} e o mínimo foi de {minimo:.2f}.
O preço de fechamento foi de {fechamento:.2f}.
    """
    return comentarios


