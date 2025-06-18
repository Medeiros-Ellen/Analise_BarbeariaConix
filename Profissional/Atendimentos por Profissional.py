# @title Gráfico - Atendimentos por Profissional {"vertical-output":true,"display-mode":"form"}

df_qtd = df.groupby("Profissional").size().reset_index(name="Atendimentos")
df_qtd["Texto"] = df_qtd["Atendimentos"].astype(str)

fig = px.bar(
    df_qtd,
    x="Profissional",
    y="Atendimentos",
    title="Atendimentos por Profissional",
    template="plotly_dark",
    text="Texto"
)

fig.update_traces(
    textposition="outside",
    textfont_size=11,
    texttemplate="%{text}"
)

# Garantir espaço suficiente para os rótulos
fig.update_yaxes(range=[0, df_qtd["Atendimentos"].max() * 1.2])
fig.update_layout(bargap=0.3)

fig.show()
