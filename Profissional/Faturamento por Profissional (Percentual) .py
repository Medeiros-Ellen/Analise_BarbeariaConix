# Valido - Mostrar total de cada servico
# @title Gráfico - Faturamento por Profissional (Percentual) {"vertical-output":true,"display-mode":"form"}

df_fat = df.groupby("Profissional")["Valor"].sum().reset_index()
df_fat["Valor_Label"] = "R$: " + df_fat["Valor"].round(2).astype(str)


df_fat["Percentual"] = (df_fat["Valor"] / df_fat["Valor"].sum()) * 100
df_fat["Percentual_Label"] = df_fat["Percentual"].round(2).astype(str) + "%"

fig = px.bar(
    df_fat,
    x="Profissional",
    y="Percentual",
    title="Faturamento por Profissional (%)",
    template="plotly_dark",
    text="Percentual_Label"
)

fig.update_traces(
    textposition="outside",
    textfont_size=11,
    texttemplate="%{x}<br>%{text}"
)

fig.update_yaxes(range=[0, df_fat["Percentual"].max() * 1.3])
fig.update_layout(bargap=0.3, height=500)
