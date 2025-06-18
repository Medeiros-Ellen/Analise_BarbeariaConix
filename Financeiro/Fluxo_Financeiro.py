from google.colab import files
import pandas as pd
import plotly.express as px
from io import StringIO
import plotly.io as pio
import requests, gzip, shutil, unicodedata
from io import StringIO
import plotly.io as pio
import requests, gzip, shutil, unicodedata

uploaded = files.upload()
file_name = list(uploaded.keys())[0]

with open(file_name, encoding='latin1') as f:
    lines = f.readlines()

data_lines = [line for line in lines if line.count(';') > 10 and 'Total' not in line]
df = pd.read_csv(StringIO(''.join(data_lines)), sep=';', encoding='latin1')
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('ç', 'c')
df['data_atendimento/venda'] = pd.to_datetime(df['data_atendimento/venda'], dayfirst=True, errors='coerce')

for col in ['valor_pago', 'valor_a_ser_recebido']:
    df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

df['semana'] = df['data_atendimento/venda'].dt.isocalendar().week
meses_pt = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
df['mes'] = df['data_atendimento/venda'].dt.month
ano = df['data_atendimento/venda'].dt.year.astype(str)
df['mes_numero'] = df['data_atendimento/venda'].dt.month
ano = df['data_atendimento/venda'].dt.year.astype(str)
df['mes_nome'] = df['mes_numero'].apply(lambda x: meses_pt[x-1])
df['mes'] = df['mes_numero'].astype(str).str.zfill(2) + '-' + ano + ' - ' + df['mes_nome']
df['dia_da_semana'] = df['data_atendimento/venda'].dt.dayofweek.map({
    0: 'segunda-feira',
    1: 'terça-feira',
    2: 'quarta-feira',
    3: 'quinta-feira',
    4: 'sexta-feira',
    5: 'sábado',
    6: 'domingo'
})
df['dia_da_semana'] = pd.Categorical(df['dia_da_semana'], categories=[
    'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo'
], ordered=True)

def format_brl(val):
    return 'R$ ' + f'{val:,.2f}'.replace(',', 'v').replace('.', ',').replace('v', '.')

pio.templates.default = "plotly_dark"

# Baixar base de nomes
url = "https://data.brasil.io/dataset/genero-nomes/nomes.csv.gz"
compactado = "nomes.csv.gz"
extraido = "nomes.csv"

r = requests.get(url)
with open(compactado, 'wb') as f:
    f.write(r.content)
with gzip.open(compactado, 'rb') as f_in:
    with open(extraido, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

# Normalizar nomes
def normalizar_nome(nome):
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    return nome.strip().upper()

# Extrair primeiro nome do cliente e normalizar
df["primeiro_nome"] = df["cliente"].str.split().str[0]
df["nome_normalizado"] = df["primeiro_nome"].apply(normalizar_nome)

# Preparar base de gêneros
df_nomes = pd.read_csv(extraido)
df_nomes = df_nomes[["first_name", "classification"]].dropna().drop_duplicates()
df_nomes["first_name"] = df_nomes["first_name"].apply(str.upper)

# Mesclar com base principal
df = df.merge(df_nomes, how="left", left_on="nome_normalizado", right_on="first_name")
df["genero"] = df["classification"].map({"M": "Masculino", "F": "Feminino"}).fillna("Desconhecido")

cores_sexo = {
    "Masculino": "#1E88E5",
    "Feminino": "#EC407A",
    "Desconhecido": "#EF5350"
}


# @title Gráfico - Total por Tipo de Pagamento %{"vertical-output":true,"display-mode":"form"}
# Agrupar total por tipo
agrupado_tipo = df.groupby('tipo_de_forma_de_pagamento')['valor_pago'].sum().reset_index()


total_geral = agrupado_tipo['valor_pago'].sum()

agrupado_tipo['percentual'] = (agrupado_tipo['valor_pago'] / total_geral) * 100
agrupado_tipo['texto'] = agrupado_tipo['percentual'].round(1).astype(str) + "%"

fig1 = px.bar(
    agrupado_tipo.sort_values(by='percentual', ascending=False),
    x='tipo_de_forma_de_pagamento',
    y='percentual',
    title='Total por Tipo de Pagamento (%)',
    labels={'tipo_de_forma_de_pagamento': 'Tipo', 'percentual': 'Percentual (%)'}
)


fig1.update_traces(text=agrupado_tipo['texto'], textposition='outside')
fig1.update_layout(yaxis_range=[0, 100])  # Limita eixo Y de 0 a 100%

fig1.show()

# @title Gráfico - Total por Forma Específica %{"vertical-output":true,"display-mode":"form"}

formas = df.groupby('forma_de_pagamento')['valor_pago'].sum().sort_values(ascending=False).reset_index()

# Calcular total geral
total_geral = formas['valor_pago'].sum()

formas['percentual'] = (formas['valor_pago'] / total_geral) * 100
formas['texto'] = formas['percentual'].round(1).astype(str) + "%"

fig2 = px.bar(
    formas,
    x='forma_de_pagamento',
    y='percentual',
    title='Total por Forma Específica (%)',
    labels={'forma_de_pagamento': 'Forma', 'percentual': 'Percentual (%)'}
)

# Adicionar texto nas barras
fig2.update_traces(text=formas['texto'], textposition='outside')
fig2.update_layout(xaxis_tickangle=-45, yaxis_range=[0, 100])  # Deixar eixo Y até 100%

fig2.show()

# @title Gráfico - Faturamento por Semana %{"vertical-output":true,"display-mode":"form"}

df_semana = df.groupby('semana', as_index=False)['valor_pago'].sum()

# Calcular o total geral
total_geral = df_semana['valor_pago'].sum()


df_semana['percentual'] = (df_semana['valor_pago'] / total_geral) * 100


df_semana['texto'] = df_semana['percentual'].round(1).astype(str) + '%'


fig3 = px.line(
    df_semana,
    x='semana', y='percentual',
    title='Faturamento por Semana (%)',
    labels={'semana': 'Semana', 'percentual': 'Percentual (%)'}
)


fig3.update_traces(mode='lines+markers+text', text=df_semana['texto'], textposition='top center')
fig3.update_layout(yaxis_range=[0, 100])  # Ajuste do eixo Y para 0–100%

fig3.show()

# @title Gráfico - Faturamento por Dia da Semana % {"vertical-output":true,"display-mode":"form"}

dias = df.groupby('dia_da_semana')['valor_pago'].sum().reset_index()


dias['ordem'] = dias['dia_da_semana'].map({
    'segunda-feira': 0,
    'terça-feira': 1,
    'quarta-feira': 2,
    'quinta-feira': 3,
    'sexta-feira': 4,
    'sábado': 5,
    'domingo': 6
})
dias = dias.sort_values('ordem')


total = dias['valor_pago'].sum()
dias['percentual'] = (dias['valor_pago'] / total) * 100
dias['texto'] = dias['percentual'].round(1).astype(str) + '%'


fig5 = px.bar(
    dias,
    x='dia_da_semana', y='percentual',
    title='Faturamento por Dia da Semana (%)',
    labels={'dia_da_semana': 'Dia', 'percentual': 'Percentual (%)'}
)
fig5.update_layout(margin=dict(l=40, r=40, t=50, b=40))
fig5.update_traces(text=dias['texto'], textposition='outside')

fig5.show()

# @title Gráfico - Distribuição por Tipo de Pagamento (Agrupado) {"vertical-output":true,"display-mode":"form"}


import plotly.express as px

# Criar uma cópia da coluna com categorias agrupadas
df_grafico = df.copy()
df_grafico['categoria'] = df_grafico['tipo_de_forma_de_pagamento'].replace({
    'PIX': 'PIX / À Vista',
    'À Vista': 'PIX / À Vista'
})

# Agrupar com base na nova categoria
agrupado_categoria = df_grafico.groupby('categoria')['valor_pago'].sum()

# Criar o gráfico de pizza
fig_pizza = px.pie(
    agrupado_categoria.reset_index(),
    names='categoria',
    values='valor_pago',
    title='Distribuição por Tipo de Pagamento (Agrupado)',
    hole=0
)

fig_pizza.update_traces(
    textinfo='label+percent',
    textposition='inside',
    showlegend=False
)

fig_pizza.show()

# @title Gráfico - % (novo) de Cada Forma de Pagamento {"vertical-output":true,"display-mode":"form"}
import plotly.express as px


porcent_forma = (
    df.groupby('forma_de_pagamento')['valor_pago']
    .sum()
    .reset_index()
    .sort_values(by='valor_pago', ascending=True)
)

# Calcular o total geral
total_pago = porcent_forma['valor_pago'].sum()


porcent_forma['percentual'] = (porcent_forma['valor_pago'] / total_pago) * 100


fig_forma_barra = px.bar(
    porcent_forma,
    x='percentual',
    y='forma_de_pagamento',
    orientation='h',
    title='% de Cada Forma de Pagamento',
    template='plotly_dark',
    labels={'percentual': 'Percentual (%)', 'forma_de_pagamento': 'Forma de Pagamento'}
)


fig_forma_barra.update_traces(
    text=porcent_forma['percentual'].apply(lambda x: f'{x:.1f}%'),
    textposition='outside'
)

fig_forma_barra.update_layout(
    yaxis_title='Forma de Pagamento',
    xaxis_title='Percentual (%)',
    margin=dict(l=100, r=50, t=50, b=50)
)

fig_forma_barra.show()

# @title Gráfico - Total de Taxas Pagas por Forma de Pagamento %{"vertical-output":true,"display-mode":"form"}

import plotly.express as px
import pandas as pd

# Processar coluna de taxa
coluna_taxa = (
    df['valor_de_desconto_da_operadora_(r$)']
    .astype(str)
    .str.replace('R$', '', regex=False)
    .str.replace('.', '', regex=False)
    .str.replace(',', '.', regex=False)
    .astype(float)
    .abs()
)


formas_pagamento = df['tipo_de_forma_de_pagamento']


df_temp = pd.DataFrame({
    'Forma de Pagamento': formas_pagamento,
    'Taxa (R$)': coluna_taxa
})


agrupado_taxa = (
    df_temp.groupby('Forma de Pagamento')['Taxa (R$)']
    .sum()
    .loc[lambda x: x > 0]
    .sort_values(ascending=False)
)


total_taxa = agrupado_taxa.sum()
df_percentual = agrupado_taxa.reset_index()
df_percentual['Percentual'] = (df_percentual['Taxa (R$)'] / total_taxa) * 100


fig_taxa = px.bar(
    df_percentual,
    x='Percentual',
    y='Forma de Pagamento',
    orientation='h',
    title='Percentual de Taxas Pagas por Forma de Pagamento',
    labels={
        'Forma de Pagamento': 'Forma de Pagamento',
        'Percentual': 'Percentual (%)'
    },
    template='plotly_dark'
)

# Adicionar rótulos em porcentagem
fig_taxa.update_traces(
    text=df_percentual['Percentual'].apply(lambda x: f'{x:.1f}%'),
    textposition='outside'
)

fig_taxa.update_layout(
    xaxis_title='Percentual (%)',
    margin=dict(l=100, r=50, t=50, b=50)
)

fig_taxa.show()

# @title Gráfico - Clientes Únicos por Mês {"vertical-output":true,"display-mode":"form"}


# Valido alterar - Usando rankingDeClientes.csv , distribuir clientes novos e antigos por semana
clientes_mes = df.groupby('mes')['cliente'].nunique().reset_index(name='quantidade')
fig = px.bar(clientes_mes, x='mes', y='quantidade', title='Clientes Únicos por Mês', labels={'quantidade': 'Clientes'})
fig.show()

# @title Gráfico - Valor Total Pago Por Gênero {"vertical-output":true,"display-mode":"form"}


import plotly.graph_objects as go

# Cores por gênero
cores_sexo = {
    "Masculino": "#1E88E5",
    "Feminino": "#EC407A",
    "Desconhecido": "#EF5350"
}

# Dados
pagamento_por_genero = (
    df.groupby("genero")["valor_pago"]
    .sum()
    .reset_index()
    .sort_values(by="valor_pago", ascending=True)
)

# Legenda formatada
total = pagamento_por_genero["valor_pago"].sum()
pagamento_por_genero["percentual"] = (pagamento_por_genero["valor_pago"] / total * 100).round(1)
pagamento_por_genero["legenda"] = pagamento_por_genero.apply(
    lambda row: f"{row['percentual']}% | R$ {row['valor_pago']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
    axis=1
)

# Gráfico
fig = go.Figure()

for _, row in pagamento_por_genero.iterrows():
    cor = cores_sexo.get(row["genero"], "#888888")
    fig.add_trace(go.Bar(
        x=[row["valor_pago"]],
        y=[row["genero"]],
        orientation='h',
        text=row["legenda"],
        textposition='outside',
        marker=dict(color=cor),
        name=row["genero"]
    ))

# Calcular o limite superior do eixo X (10% acima do maior valor)
x_max = pagamento_por_genero["valor_pago"].max() * 1.1

fig.update_layout(
    title='Valor Total Pago por Gênero',
    template='plotly_dark',
    yaxis_title='Gênero',
    xaxis_title='Valor Pago',
    showlegend=False,
    margin=dict(r=10),  # margem pode ser pequena agora
    uniformtext_minsize=10,
    uniformtext_mode='hide',
    xaxis=dict(
        tickformat=',.0f',
        tickprefix='R$ ',
        separatethousands=True,
        range=[0, x_max]  # <<< define o range manualmente
    )
)


fig.show()
