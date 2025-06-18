# @title Gráfico - Evolução de Agendamentos por Semana {"vertical-output":true,"display-mode":"form"}
# Agrupar por semana e extrair o início da semana como data
agendamentos_semanais = df.groupby(df["Data"].dt.to_period("W")).size().reset_index(name="Qtd")
agendamentos_semanais["Data"] = agendamentos_semanais["Data"].apply(lambda x: x.start_time)
agendamentos_semanais["Semana"] = agendamentos_semanais["Data"].dt.strftime("S%W/%y")

fig = px.line(
    agendamentos_semanais,
    x="Data", y="Qtd",
    title="Evolução de Agendamentos por Semana",
    labels={"Data": "Semana", "Qtd": "Agendamentos"},
    template="plotly_dark"
)

fig.update_traces(
    mode="lines+markers+text",
    texttemplate="%{customdata[0]}<br>Q: %{y}",
    textposition="top center",
    textfont_size=10,
    customdata=agendamentos_semanais[["Semana"]]
)

fig.update_yaxes(range=[0, agendamentos_semanais["Qtd"].max() * 1.2])
fig.show()
