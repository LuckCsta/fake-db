import pandas as pd
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from faker import Faker

fake = Faker('pt_BR')

# Listas de marcas e modelos disponíveis
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
    "Mercedes": ["A200", "CLA-45", "Classe A", "Classe C", "GLE 400"],
    "Audi": ["A1", "A3", "Q3", "A5", "TT"],
    "Volvo": ["XC40", "XC60", "S90"],
    "Jeep": ["Renegade", "Compass", "Cherokee", "Defender"]
}

formas_pagamento = ["A vista", "Financiamento", "Consórcio", "Leasing"]
cores = ["Preto", "Branco", "Prata", "Vermelho", "Azul"]
sexo_opcoes = ["Masculino", "Feminino"]


def gerar_dados(qtd):
    dados = []
    for i in range(1, qtd + 1):
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
    return pd.DataFrame(dados)


def salvar_arquivo(df, formato):
    caminho = filedialog.asksaveasfilename(defaultextension=f".{formato}",
                                           filetypes=[(f"{formato.upper()} files", f"*.{formato}")])
    if caminho:
        if formato == "csv":
            df.to_csv(caminho, index=False)
        elif formato in ["xlsx", "excel"]:
            df.to_excel(caminho, index=False)
        elif formato == "json":
            df.to_json(caminho, orient="records", indent=4)
        elif formato == "sql":
            from sqlalchemy import create_engine
            engine = create_engine(f"sqlite:///{caminho}")
            df.to_sql("vendas", con=engine, if_exists="replace", index=False)
        messagebox.showinfo("Sucesso", f"Arquivo salvo em {caminho}")


def visualizar_dados():
    try:
        qtd = int(entry_qtd.get())
        df = gerar_dados(qtd)
        text_preview.delete("1.0", tk.END)
        text_preview.insert(tk.END, df.head().to_string())
        return df
    except ValueError:
        messagebox.showerror("Erro", "Digite um número válido de vendas.")
        return None


def exportar():
    df = visualizar_dados()
    if df is not None:
        formato = formato_var.get()
        salvar_arquivo(df, formato)


# Interface Gráfica
root = tk.Tk()
root.title("Exportação de Vendas")
root.geometry("500x400")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Quantidade de Vendas:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
entry_qtd = tk.Entry(root, font=("Arial", 12))
entry_qtd.pack(pady=5)

formato_var = tk.StringVar(value="csv")
tk.Label(root, text="Formato de Exportação:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
formatos = ["csv", "xlsx", "json", "sql"]
ttk.Combobox(root, textvariable=formato_var, values=formatos, state="readonly", font=("Arial", 12)).pack(pady=5)

tk.Button(root, text="Gerar Prévia", command=visualizar_dados, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(
    pady=5)
tk.Button(root, text="Gerar e Exportar", command=exportar, bg="#008CBA", fg="white", font=("Arial", 12)).pack(pady=5)

text_preview = tk.Text(root, height=8, width=60, font=("Courier", 10))
text_preview.pack(pady=10)

root.mainloop()
