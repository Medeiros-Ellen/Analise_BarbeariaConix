# @title Gráfico - Agendamentos por Dia da Semana e Mês {"vertical-output":true,"display-mode":"form"}


# Criar colunas auxiliares
df["mes"] = df["Data"].dt.strftime("%m/%y")  # Formato MM/AA
df["dia_da_semana_en"] = df["Data"].dt.day_name()

# Traduzir dias da semana manualmente
traducao_dias = {
    'Monday': 'segunda-feira',
    'Tuesday': 'terça-feira',
    'Wednesday': 'quarta-feira',
    'Thursday': 'quinta-feira',
    'Friday': 'sexta-feira',
    'Saturday': 'sábado',
    'Sunday': 'domingo'
}
df["dia_da_semana"] = df["dia_da_semana_en"].map(traducao_dias)

# Contar agendamentos
heatmap_data = df.groupby(['mes', 'dia_da_semana']).size().reset_index(name='agendamentos')
heatmap_pivot = heatmap_data.pivot(index='dia_da_semana', columns='mes', values='agendamentos').fillna(0)

# Ordenar os dias da semana
dias_ordem = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
heatmap_pivot = heatmap_pivot.reindex(dias_ordem)

# Criar gráfico
fig_heatmap = px.imshow(
    heatmap_pivot,
    labels=dict(x='Mês', y='Dia da Semana', color='Qtd. Agendamentos'),
    x=heatmap_pivot.columns,
    y=heatmap_pivot.index,
    color_continuous_scale='YlOrRd',
    text_auto='.0f',
    aspect='auto',
    title='Agendamentos por Dia da Semana e Mês'
)

fig_heatmap.update_layout(margin=dict(l=40, r=40, t=50, b=40))
fig_heatmap.show()
