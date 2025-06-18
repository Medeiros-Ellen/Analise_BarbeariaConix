# @title Gráfico - Cadastros {"vertical-output":true,"display-mode":"form"}
# Agrupa por mês e formata para MM/YY
cadastros_mensais = clientes_df.groupby(clientes_df["CADASTRO"].dt.to_period("M")).size().reset_index(name="Qtd")
cadastros_mensais["CADASTRO"] = pd.to_datetime(cadastros_mensais["CADASTRO"].astype(str))
cadastros_mensais["label"] = cadastros_mensais["CADASTRO"].dt.strftime("%m/%y")

fig = px.line(
    cadastros_mensais,
    x="CADASTRO", y="Qtd",
    title="Evolução de Cadastros por Mês",
    labels={"CADASTRO": "Mês", "Qtd": "Cadastros"},
    markers=True,
    text="label",  # 👈 MM/YY acima dos pontos
    template="plotly_dark"
)

fig.update_traces(
    textposition="top center"
)
fig.update_traces(textfont_size=10)
fig.show()
