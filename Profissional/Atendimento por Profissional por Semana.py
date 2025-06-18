# @title Gráfico - Atendimento por Profissional por Semana (sem a última semana) {"vertical-output":true,"display-mode":"form"}


df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")

# Extrair ano e semana ISO
df["Ano"] = df["Data"].dt.isocalendar().year
df["Semana"] = df["Data"].dt.isocalendar().week
df["Ano_Semana"] = df["Ano"].astype(str) + "-S" + df["Semana"].astype(str).str.zfill(2)

# Remover a última semana
ultima_semana = df["Semana"].max()
ultimo_ano = df["Ano"].max()
df_filtrado = df[~((df["Ano"] == ultimo_ano) & (df["Semana"] == ultima_semana))]

# Agrupar novamente por semana e profissional
df_semana = df_filtrado.groupby(["Ano_Semana", "Profissional"]).size().reset_index(name="Atendimentos")
df_semana["Texto"] = df_semana["Atendimentos"].astype(str)

# Criar gráfico
fig = px.bar(
    df_semana,
    x="Ano_Semana",
    y="Atendimentos",
    color="Profissional",
    barmode="group",
    text="Texto",
    title="Atendimentos por Profissional por Semana (sem a última semana)",
    template="plotly_dark"
)

fig.update_traces(
    textposition="outside",
    textfont_size=10,
    texttemplate="%{text}"
)

fig.update_layout(
    bargap=0.2,
    xaxis_title="Semana (Ano-Semana)",
    yaxis_title="Atendimentos"
)
fig.update_yaxes(range=[0, df_semana["Atendimentos"].max() * 1.2])

fig.show()
