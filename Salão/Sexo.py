# @title Gráfico - Sexo {"vertical-output":true,"display-mode":"form"}
# Gráfico 1: Distribuição por Sexo
sexo_df = clientes_df["SEXO"].value_counts().reset_index()
sexo_df.columns = ["SEXO", "count"]

color_map = {
    "M": "#1877F2",
    "F": "#C13584"
}

fig1 = px.pie(
    sexo_df,
    values="count", names="SEXO",
    # x="SEXO", y="count",
    # labels={"SEXO": "Sexo", "count": "Número de Clientes"},
    title="Distribuição por Sexo",
    template="plotly_dark",
    color="SEXO",
    color_discrete_map=color_map
)
fig1.show()
