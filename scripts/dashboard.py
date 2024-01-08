import os
import pandas as pd
import dash
from dash import dcc, html
import plotly.graph_objects as go

def draw(news, dataframe):
    merged_file_path = os.path.join('data', 'merged_data.csv')

    if os.path.exists(merged_file_path):
        df = dataframe
        tickers = df['ticker'].unique()
        app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])
        my_options = [
            {
                "label": html.Span(
                    [
                        html.Span(ticker, style={'color': 'white'}),
                    ],
                    style={ "background-color":"black"}
                ),
                "value": ticker,
                "style": {'background-color': 'black'},  
                
            }
            for ticker in tickers
        ]

        app.layout = html.Div([
            html.Div([
                dcc.Dropdown(
                    id='ticker-dropdown',
                    options=my_options,
                    value=tickers[1],  
                    multi=False,
                    style={"color": "white", "background": "black"},
                ),
                dcc.Graph(id='candlestick-chart')
              ]),
            html.Div([
                html.H1("Notícias"),
                html.Ul(id='news-list')
                ])
        ], className="generic")

        @app.callback(
            [dash.Output('candlestick-chart', 'figure'),
             dash.Output('news-list', 'children')],
            [dash.Input('ticker-dropdown', 'value')]
        )

        def update_chart(selected_ticker):
            filtered_df = df[df['ticker'] == selected_ticker]

            last_365_days = pd.to_datetime(filtered_df['date']).max() - pd.DateOffset(days=365)
            filtered_df = filtered_df[pd.to_datetime(filtered_df['date']) > last_365_days]

            fig = go.Figure(data=[go.Candlestick(x=filtered_df['date'],
                            open=filtered_df['open'], high=filtered_df['high'],
                            low=filtered_df['low'], close=filtered_df['close'])
                                ])
            fig.update_layout(xaxis_rangeslider_visible=False,
            margin=dict(l=0, r=0, t=16, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False,tickfont=dict(color='white')),
            yaxis=dict(showgrid=False, tickfont=dict(color='white'))
            )
          
            filtered_news = [item for item in news[selected_ticker]]

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
        app.run_server(debug=False)
    else:
        print(f'O arquivo combinado "{merged_file_path}" não existe.')
