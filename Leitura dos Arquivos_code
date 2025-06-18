import pandas as pd
import plotly.express as px
from gender_guesser_br import Genero
import unicodedata

# Leitura do arquivo
# df = pd.read_csv("/content/Agendamentos_Tratados_Python.csv")
df = pd.read_csv(nome_arquivo, sep=",")

# Garantir conversões corretas
df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
df["Cadastramento"] = pd.to_datetime(df["Cadastramento"], dayfirst=True)
df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")


# Extrair duração numérica em minutos
df["Duracao_min"] = df["Duração"].str.extract(r"(\d+)").astype(float)

# Extrair primeiro nome e identificar sexo
# df["PrimeiroNome"] = df["Cliente"].str.split().str[0].str.strip().str.title()
# df["Sexo"] = df["PrimeiroNome"].apply(lambda nome: Genero(nome)())
# Normalização do nome
def normalizar_nome(nome):
    nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    return nome.strip().upper()

# Extrair primeiro nome do cliente e normalizar
df["PrimeiroNome"] = df["Cliente"].str.split().str[0]
df["Nome_Normalizado"] = df["PrimeiroNome"].apply(normalizar_nome)

# Preparar dataframe de nomes
nomes_mapeados = df_nomes[["first_name", "classification"]].dropna().drop_duplicates()
nomes_mapeados["first_name"] = nomes_mapeados["first_name"].apply(str.upper)

# Mesclar os dados com o gênero estimado
df = df.merge(nomes_mapeados, how="left", left_on="Nome_Normalizado", right_on="first_name")
df["Sexo"] = df["classification"].map({"M": "masculino", "F": "feminino"}).fillna("desconhecido")
