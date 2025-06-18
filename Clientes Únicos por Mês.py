# @title Gráfico - Clientes Únicos por Mês {"vertical-output":true,"display-mode":"form"}


# Valido alterar - Usando rankingDeClientes.csv , distribuir clientes novos e antigos por semana
clientes_mes = df.groupby('mes')['cliente'].nunique().reset_index(name='quantidade')
fig = px.bar(clientes_mes, x='mes', y='quantidade', title='Clientes Únicos por Mês', labels={'quantidade': 'Clientes'})
fig.show()
