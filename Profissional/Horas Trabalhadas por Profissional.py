# @title Gráfico - Horas Trabalhadas por Profissional {"vertical-output":true,"display-mode":"form"}

# Calcular horas a partir de minutos
horas_trabalhadas = df.groupby("Profissional")["Duracao_min"].sum().reset_index()
horas_trabalhadas["Horas"] = (horas_trabalhadas["Duracao_min"] / 60).round(0)

# Adicionar coluna de texto com "h"
horas_trabalhadas["Horas_str"] = horas_trabalhadas["Horas"].astype(int).astype(str) + "h"


# Criar gráfico
fig = px.bar(
    horas_trabalhadas.sort_values("Horas", ascending=False),
    x="Profissional", y="Horas",
    title="Horas Trabalhadas por Profissional",
    labels={"Horas": "Horas Trabalhadas"},
    text=horas_trabalhadas["Horas_str"],  # Usar string personalizada
    template="plotly_dark"
)

fig.update_layout(bargap=0.3)
fig.show()
