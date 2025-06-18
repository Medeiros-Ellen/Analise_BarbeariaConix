# @title Gráfico - Faturamento por Profissional por Semana % (sem a última semana) {"vertical-output":true,"display-mode":"form"}
# Garantir o tipo datetime correto
df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")

# Extrair ano e semana ISO
df["Ano"] = df["Data"].dt.isocalendar().year
df["Semana"] = df["Data"].dt.isocalendar().week
df["Ano_Semana"] = df["Ano"].astype(str) + "-S" + df["Semana"].astype(str).str.zfill(2)

# Remover a última semana do ano mais recente
ultima_semana = df["Semana"].max()
ultimo_ano = df["Ano"].max()
df_filtrado = df[~((df["Ano"] == ultimo_ano) & (df["Semana"] == ultima_semana))]

# Agrupar por semana e profissional
faturamento_semana = df_filtrado.groupby(["Ano_Semana", "Profissional"])["Valor"].sum().reset_index()


total_por_semana = faturamento_semana.groupby("Ano_Semana")["Valor"].transform("sum")
faturamento_semana["Percentual"] = (faturamento_semana["Valor"] / total_por_semana) * 100
faturamento_semana["Texto"] = faturamento_semana["Percentual"].round(1).astype(str) + "%"

# Criar gráfico
fig = px.bar(
    faturamento_semana,
    x="Ano_Semana",
    y="Percentual",
    color="Profissional",
    barmode="group",
    text="Texto",
    title="Faturamento por Profissional por Semana (%)",
    labels={"Percentual": "Faturamento (%)", "Ano_Semana": "Semana"},
    template="plotly_dark"
)

# Ajustes visuais
fig.update_traces(
    textposition="outside",
    textfont_size=10,
    texttemplate="%{text}"
)

fig.update_layout(
    bargap=0.2,
    xaxis_title="Semana (Ano-Semana)",
    yaxis_title="Faturamento (%)"
)
fig.update_yaxes(range=[0, 100])  # Percentuais de 0% a 100%

fig.show()
