import pandas as pd
import plotly.graph_objects as go
import plotly_express as px


def plot_grafico_historico(nome,df_historico,intepretacao_historico):
    """
    Função: Plotar um gráfico de linhas com o historico de cotações de um ativo de um período usando a biblioteca Plotly 
    Args: Nome do ativo (str),DataFrame do pandas com historico de cotações do ativo, contendo as colunas: Date',
      'Close', 'Adj Close', 'Volume' e string textual com interpretação do historico.
    """
    #Filtrando dados e criando grafico do histórico
    df=df_historico.reset_index()
    df.rename(columns={'index': 'Date'}, inplace=True)
    historico_x=df['Date']
    historico_y=df['Close']

    fig=px.line(data_frame=df,x=historico_x,y=historico_y,title=(f'Histórico de cotações do ativo {nome}'))
    # Adicionando a interpretação como anotação (simulando uma legenda)
    fig.add_annotation(
        dict(
            xref="paper",
            yref="paper",
            x=0.05,
            y=1.05,
            text=intepretacao_historico,
            showarrow=False,
            font=dict(size=10, color="#000")
        )
    )

    fig.update_yaxes(title='Valor do ativo')
    fig.update_xaxes(title='Data')
    fig.show()

def plot_grafico_previsao(nome,df_previsao,intepretacao_previsao):
    """
    Funcao: Plotar um gráfico de linhas com a previsao de cotacoes de um ativo usando a lib Plotly
    Args: nome do ativo, DataFrame pandas contendo as previsoes de cotacoes do ativo.
    """
    #Filtrando os dados e gerando o gráfico
    df=df_previsao
    previsao_x=df['Data']
    previsao_y=df['Previsão']
    fig=px.line(data_frame=df,x=previsao_x,y=previsao_y,title=(f'Previsao de cotações do ativo {nome}'))

    # Adicionando a interpretação como anotação (simulando uma legenda)
    fig.add_annotation(
        dict(
            xref="paper",
            yref="paper",
            x=0.05,
            y=1.05,
            text=intepretacao_previsao,
            showarrow=False,
            font=dict(size=10, color="#000")
        )
    )

    fig.update_yaxes(title='Valor do ativo')
    fig.update_xaxes(title='Data')
    fig.show()