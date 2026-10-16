from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# 1. Carga de dados
df = pd.read_csv('ecommerce_estatistica.csv', encoding='utf-8')

# Lista de gêneros para o filtro interativo
lista_genero = df['Gênero'].unique()
options_genero = [{'label': genero, 'value': genero} for genero in lista_genero]

# 2. Inicialização do app Dash
app = Dash(__name__)

# 3. Layout da aplicação
app.layout = html.Div([
    html.H1("Dashboard Interativo de E-Commerce"),
    html.Div("Análise visual e estatística dos produtos cadastrados."),
    html.Br(),
    
    html.H2("Filtro por Gênero"),
    dcc.Checklist(
        id='id_selecao_genero',
        options=options_genero,
        value=[lista_genero[0], lista_genero[1]],  # Seleção inicial padrão
        inline=True
    ),
    html.Hr(),

    # Disposição dos 7 gráficos no layout
    html.Div([
        html.Div([dcc.Graph(id='id_histograma')], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='id_dispersao')], style={'width': '49%', 'display': 'inline-block'}),
    ]),
    
    html.Div([
        html.Div([dcc.Graph(id='id_heatmap')], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='id_barra')], style={'width': '49%', 'display': 'inline-block'}),
    ]),

    html.Div([
        html.Div([dcc.Graph(id='id_pizza')], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='id_densidade')], style={'width': '49%', 'display': 'inline-block'}),
    ]),

    html.Div([
        dcc.Graph(id='id_regressao')
    ], style={'width': '100%', 'marginTop': '20px'})
])

# 4. Callback para atualizar os 7 gráficos dinamicamente
@app.callback(
    Output('id_histograma', 'figure'),
    Output('id_dispersao', 'figure'),
    Output('id_heatmap', 'figure'),
    Output('id_barra', 'figure'),
    Output('id_pizza', 'figure'),
    Output('id_densidade', 'figure'),
    Output('id_regressao', 'figure'),
    Input('id_selecao_genero', 'value')
)
def cria_graficos(selecao_genero):
    # Filtragem do DataFrame
    if not selecao_genero:
        filtro_df = df
    else:
        filtro_df = df[df['Gênero'].isin(selecao_genero)]

    # 1. Gráfico de Histograma
    fig_hist = px.histogram(
        filtro_df, x='Preço', color='Gênero', nbins=20,
        title='1. Histograma: Distribuição de Preços'
    )
    fig_hist.update_layout(xaxis_title='Preço (R$)', yaxis_title='Frequência')

    # 2. Gráfico de Dispersão
    fig_scatter = px.scatter(
        filtro_df, x='Preço', y='N_Avaliações', color='Gênero',
        hover_data=['Título', 'Marca'],
        title='2. Dispersão: Preço vs. Número de Avaliações'
    )
    fig_scatter.update_layout(xaxis_title='Preço (R$)', yaxis_title='Nº de Avaliações')

    # 3. Mapa de Calor (Matriz de Correlação)
    cols_num = ['Nota', 'N_Avaliações', 'Desconto', 'Preço', 'Qtd_Vendidos_Cod']
    corr_matrix = filtro_df[cols_num].corr()
    fig_heatmap = px.imshow(
        corr_matrix, text_auto='.2f', color_continuous_scale='Blues',
        title='3. Mapa de Calor: Matriz de Correlação'
    )

    # 4. Gráfico de Barra
    df_bar = filtro_df.groupby('Gênero', as_index=False)['Preço'].mean()
    fig_bar = px.bar(
        df_bar, x='Gênero', y='Preço', color='Gênero',
        title='4. Gráfico de Barra: Preço Médio por Gênero'
    )
    fig_bar.update_layout(xaxis_title='Gênero', yaxis_title='Preço Médio (R$)')

    # 5. Gráfico de Pizza
    fig_pie = px.pie(
        filtro_df, names='Gênero',
        title='5. Gráfico de Pizza: Proporção de Produtos por Gênero'
    )

    # 6. Gráfico de Densidade
    fig_density = px.density_contour(
        filtro_df, x='Preço', y='Nota', color='Gênero',
        title='6. Gráfico de Densidade: Preço vs. Nota'
    )
    fig_density.update_layout(xaxis_title='Preço (R$)', yaxis_title='Nota')

    # 7. Gráfico de Regressão
    fig_reg = px.scatter(
        filtro_df, x='Desconto', y='Preço', color='Gênero', trendline='ols',
        title='7. Gráfico de Regressão: Desconto vs. Preço'
    )
    fig_reg.update_layout(xaxis_title='Desconto (%)', yaxis_title='Preço (R$)')

    return fig_hist, fig_scatter, fig_heatmap, fig_bar, fig_pie, fig_density, fig_reg


if __name__ == '__main__':
    app.run(debug=True, port=8050)