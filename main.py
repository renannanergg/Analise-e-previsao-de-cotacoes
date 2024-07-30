import analise
import plot as pl

def main():
    """
    Função principal,cria um dicionário com todas análises feitas referente ao ativo e os adiciona numa lista chamada ativo,
    após isso, gera um gráfico com o historico de cotações do ativo e outro gráfico com previsões da cotação.
    
    
    """
    ativos=[]
    while True:
        # Obter e validar dados do usuário
        ativo = input("Digite o nome do ativo (ou 'sair' para encerrar): ").strip().upper()
        if ativo.lower() == 'sair':
            break
        try:
                if analise.is_ticker_valid(ativo):
                    print(f"Ativo/índice escolhido: {ativo}")
                    data_inicial_str = input('Digite o período inicial da análise (aaaa-mm-dd): ').strip()
                    data_final_str = input('Até qual data deseja analisar (aaaa-mm-dd): ').strip()
                    data_inicial, data_final = analise.validar_datas(data_inicial_str, data_final_str)
                    print('=/='*20)
                    print(f"- Ativo: {ativo}")
                    print(f"  Período: {data_inicial} até {data_final}")
                    # Cria um dicionário para armazenar todos dados do ativo
                    ativo_data = {
                                'nome': ativo,
                                'data_inicial': data_inicial,
                                'data_final': data_final
                            }
                    # Obter dados históricos e realizar interpretação dos dados e os armazena
                    df_historico= analise.obter_dados_ativos(ativo, data_inicial, data_final)
                    ativo_data['df_historico'] = df_historico
                    ativo_data['interpretacao_historico']=analise.interpret_historico(ativo_data['df_historico'])

                    # Realizar previsões e interpretação dos dados e os armazena
                    df_previsao=analise.prev_ia(ativo_data['df_historico'])
                    ativo_data['df_previsao']=df_previsao                
                    ativo_data['interpretacao_previsao'] = analise.interpret_previsões(ativo_data['df_previsao'])

                    # Adiciona todos os dados do dicionário ativo_data na lista ativos
                    ativos.append(ativo_data)

                    #Plota o gráfico com base nas informações da lista/dict fornecida
                    pl.plot_grafico_historico(ativo_data['nome'],df_historico,ativo_data['interpretacao_historico'])
                    pl.plot_grafico_previsao(ativo_data['nome'],df_previsao,ativo_data['interpretacao_previsao'])


                else:
                     print(f"Ocorreu um erro")                     
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()