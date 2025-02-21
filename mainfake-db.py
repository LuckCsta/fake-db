import pandas as pd
import random
from faker import Faker

fake = Faker('pt_BR')

# Listas de valores possíveis
marcas_modelos = {
    "Toyota": ["Corolla", "Hilux", "Yaris", "Camry", "RAV4"],
    "Honda": ["Civic", "HR-V", "Fit", "Accord", "CR-V"],
    "Ford": ["Ka", "EcoSport", "Ranger", "Mustang", "Fusion"],
    "Chevrolet": ["Onix", "Tracker", "S10", "Cruze", "Equinox"],
    "Volkswagen": ["Gol", "Polo", "T-Cross", "Jetta", "Tiguan"],
    "Hyundai": ["HB20", "Creta", "Tucson", "Elantra", "Santa Fe"],
    "Fiat": ["Uno", "Mobi", "Argo", "Toro", "Cronos"],
    "Renault": ["Kwid", "Sandero", "Duster", "Logan", "Captur"],
    "Nissan": ["Versa", "Kicks", "Sentra", "March", "Altima"],
    "BMW": ["X1", "X3", "X5", "320i", "520i"],
}

formas_pagamento = ["A vista", "Financiamento", "Consórcio", "Leasing"]
cores = ["Preto", "Branco", "Prata", "Vermelho", "Azul"]
sexo_opcoes = ["Masculino", "Feminino"]

# Gerando os dados fictícios
dados = []
for i in range(1, 1001):
    sexo = random.choice(sexo_opcoes)
    nome = fake.first_name_male() if sexo == "Masculino" else fake.first_name_female()
    sobrenome = fake.last_name()
    nome_completo = f"{nome} {sobrenome}"
    idade = random.randint(18, 70)
    cpf = fake.cpf()
    email = fake.email()
    telefone = fake.phone_number()
    cidade = fake.city()
    estado = fake.state_abbr()

    marca = random.choice(list(marcas_modelos.keys()))
    modelo = random.choice(marcas_modelos[marca])
    ano_fabricacao = random.randint(2015, 2024)
    cor = random.choice(cores)
    valor_venda = round(random.uniform(30000, 250000), 2)
    data_venda = fake.date_between(start_date="-2y", end_date="today")
    forma_pagamento = random.choice(formas_pagamento)

    dados.append({
        "ID_CLIENTE": i, "NOME": nome_completo, "IDADE": idade, "CPF": cpf, "SEXO": sexo, "EMAIL": email,
        "TELEFONE": telefone, "CIDADE": cidade, "ESTADO": estado, "MARCA_VEICULO": marca,
        "MODELO_VEICULO": modelo, "ANO_FABRICACAO": ano_fabricacao, "COR": cor, "VALOR_VENDA": valor_venda,
        "DATA_VENDA": data_venda, "FORMA_PAGAMENTO": forma_pagamento
    })

# Criando o DataFrame
colunas = [
    "ID_CLIENTE", "NOME", "IDADE", "CPF", "SEXO", "EMAIL", "TELEFONE", "CIDADE", "ESTADO",
    "MARCA_VEICULO", "MODELO_VEICULO", "ANO_FABRICACAO", "COR", "VALOR_VENDA", "DATA_VENDA",
    "FORMA_PAGAMENTO"
]
df_vendas = pd.DataFrame(dados, columns=colunas)

# Exibindo as primeiras linhas
print(df_vendas)