import os
import pandas as pd
import dash
from dash import dcc, html

# Adicione os imports necessários para a nova biblioteca 'dash_html_components'
#import dash_html_components as html
#from dash.dependencies import Input, Output
import plotly.graph_objects as go

def draw(news):
    # Caminho do arquivo combinado na pasta "data"
    merged_file_path = os.path.join('data', 'merged_data.csv')

    # Verificar se o arquivo existe antes de tentar lê-lo
    if os.path.exists(merged_file_path):
        # Ler o arquivo combinado
        df = pd.read_csv(merged_file_path)

        # Obter a lista de tickers únicos
        tickers = df['ticker'].unique()
        #external_stylesheets = ['assets/styles.css']
        # Layout da aplicação Dash
        app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])
        app.layout = html.Div([
            html.Div([
                dcc.Dropdown(
                    id='ticker-dropdown',
                    options=[{'label': ticker, 'value': ticker} for ticker in tickers],
                    value=tickers[1],  # Valor padrão é o primeiro ticker
                    multi=False    
                ),
                dcc.Graph(id='candlestick-chart')
              ]),
            html.Div([
                html.H1("Notícias"),
                html.Ul(id='news-list')
                ])
        ], className="generic")

        # Callback para atualizar o gráfico e as notícias com base na seleção do ticker
        @app.callback(
            [dash.dependencies.Output('candlestick-chart', 'figure'),
             dash.dependencies.Output('news-list', 'children')],
            [dash.dependencies.Input('ticker-dropdown', 'value')]
        )
        def update_chart(selected_ticker):
            filtered_df = df[df['ticker'] == selected_ticker]
            fig = go.Figure(data=[go.Candlestick(x=filtered_df['date'],
                            open=filtered_df['open'], high=filtered_df['high'],
                            low=filtered_df['low'], close=filtered_df['close'])
                                ])
            fig.update_layout(xaxis_rangeslider_visible=False)

            # Filtrar notícias com base no ticker selecionado
            filtered_news = [item for item in news[selected_ticker]]

            # Criar uma lista de elementos HTML para exibir notícias
            news_list = []
            for item in filtered_news:
                news_item = html.Li([
                    html.A(
                        href=item['link'],
                        children=[
                            html.Span(item['type']),
                            html.H3(item['title']),
                        ]
                    )
                ])
                news_list.append(news_item)

            return fig, news_list

        # Iniciar o servidor Dash
        app.run_server(debug=False)
    else:
        print(f'O arquivo combinado "{merged_file_path}" não existe.')

# Chamar a função para desenhar o dashboard
# Supondo que 'news_data' seja o retorno da função 'news_scrapper'
# draw(news_data)
