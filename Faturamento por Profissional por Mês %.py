# @title Gráfico - Faturamento por Profissional por Mês % (sem o último Mês) {"vertical-output":true,"display-mode":"form"}

# Garantir o tipo datetime correto
df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")

# Extrair ano e mês
df["Ano"] = df["Data"].dt.year
df["Mes"] = df["Data"].dt.month
df["Ano_Mes_dt"] = df["Data"].dt.to_period("M").dt.to_timestamp()
df["Ano_Mes"] = df["Ano_Mes_dt"].dt.strftime("%b/%Y")  # Ex: Jan/2025

# Remover o último mês detectado
ultimo_ano = df["Ano"].max()
ultimo_mes = df[df["Ano"] == ultimo_ano]["Mes"].max()
df_filtrado = df[~((df["Ano"] == ultimo_ano) & (df["Mes"] == ultimo_mes))]

# Agrupar faturamento por mês e profissional
faturamento_mes = df_filtrado.groupby(["Ano_Mes", "Profissional"])["Valor"].sum().reset_index()

total_por_mes = faturamento_mes.groupby("Ano_Mes")["Valor"].transform("sum")
faturamento_mes["Percentual"] = (faturamento_mes["Valor"] / total_por_mes) * 100
faturamento_mes["Texto"] = faturamento_mes["Percentual"].round(1).astype(str) + "%"

fig = px.bar(
    faturamento_mes,
    x="Ano_Mes",
    y="Percentual",
    color="Profissional",
    barmode="group",
    text="Texto",
    title="Faturamento por Profissional por Mês (%)",
    labels={"Percentual": "Faturamento (%)", "Ano_Mes": "Mês"},
    template="plotly_dark",
    category_orders={"Ano_Mes": sorted(faturamento_mes["Ano_Mes"].unique(), key=lambda x: pd.to_datetime(x, format="%b/%Y"))}
)


fig.update_traces(
    textposition="outside",
    textfont_size=10,
    texttemplate="%{text}"
)

fig.update_layout(
    bargap=0.2,
    xaxis_title="Mês (Abrev./Ano)",
    yaxis_title="Faturamento (%)"
)
fig.update_yaxes(range=[0, 100])

fig.show()
