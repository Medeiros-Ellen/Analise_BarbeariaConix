# @title Gráfico - Contato {"vertical-output":true,"display-mode":"form"}
# Gráfico 3: Primeiro Contato
contato_df = clientes_df["PRIMEIRO CONTATO"].value_counts().reset_index()
contato_df.columns = ["Canal", "count"]

color_map = {
    "Whatsapp": "#25D366",
    "Instagram": "#C13584",
    "Facebook": "#1877F2",
    "Google": "#DB4437",
    "Indicação": "#00BFFF",
    "Shopping": "#FFA500",
    "Site": "#A9A9A9"
}

fig3 = px.pie(
    contato_df,
    values="count", names="Canal",
    title="Origem do Primeiro Contato",
    template="plotly_dark",
    color="Canal",
    color_discrete_map=color_map
)
# fig3.update_traces(textinfo="label+percent")
fig3.update_traces(
    texttemplate="%{label}<br>%{percent} (%{value})",
    textposition="inside"
)
fig3.show()
