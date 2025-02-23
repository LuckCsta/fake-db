import pandas as pd
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from faker import Faker
from datetime import datetime, timedelta

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


def gerar_dados_clientes(qtd):
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

        dados.append({
            "ID_CLIENTE": i,
            "NOME": nome_completo,
            "IDADE": idade,
            "CPF": cpf,
            "SEXO": sexo,
            "EMAIL": email,
            "TELEFONE": telefone,
            "CIDADE": cidade,
            "ESTADO": estado
        })
    return pd.DataFrame(dados)


def gerar_dados_veiculos(qtd):
    dados = []
    for _ in range(qtd):
        marca = random.choice(list(marcas_modelos.keys()))
        modelo = random.choice(marcas_modelos[marca])
        ano_fabricacao = random.randint(2015, 2024)
        cor = random.choice(cores)
        valor_venda = round(random.uniform(30000, 250000), 2)
        data_venda = fake.date_between(start_date="-2y", end_date="today")
        forma_pagamento = random.choice(formas_pagamento)

        dados.append({
            "MARCA_VEICULO": marca,
            "MODELO_VEICULO": modelo,
            "ANO_FABRICACAO": ano_fabricacao,
            "COR": cor,
            "VALOR_VENDA": valor_venda,
            "DATA_VENDA": data_venda,
            "FORMA_PAGAMENTO": forma_pagamento
        })
    return pd.DataFrame(dados)


def gerar_dados_pagamentos(df_clientes, df_veiculos):
    dados = []
    for i in range(len(df_clientes)):
        forma_pagamento = df_veiculos.iloc[i]["FORMA_PAGAMENTO"]
        valor_total = df_veiculos.iloc[i]["VALOR_VENDA"]
        data_pagamento = df_veiculos.iloc[i]["DATA_VENDA"]

        pagamento = {
            "ID_PAGAMENTO": i + 1,
            "CPF_CLIENTE": df_clientes.iloc[i]["CPF"],
            "FORMA_PAGAMENTO": forma_pagamento,
            "VALOR_TOTAL": valor_total,
            "DATA_PAGAMENTO": data_pagamento
        }

        if forma_pagamento == "Financiamento":
            pagamento.update({
                "PARCELAS": random.randint(12, 60),
                "TAXA_JUROS": round(random.uniform(0.5, 2.5), 2)
            })

        dados.append(pagamento)
    return pd.DataFrame(dados)


def gerar_perfis_consumidores(df_clientes, df_veiculos):
    dados = []
    for i in range(len(df_clientes)):
        historico_compras = random.randint(1, 5)
        marcas_preferidas = random.sample(list(marcas_modelos.keys()), k=random.randint(1, 3))

        dados.append({
            "ID_CONSUMIDOR": df_clientes.iloc[i]["ID_CLIENTE"],
            "NOME": df_clientes.iloc[i]["NOME"],
            "IDADE": df_clientes.iloc[i]["IDADE"],
            "EMAIL": df_clientes.iloc[i]["EMAIL"],
            "CIDADE": df_clientes.iloc[i]["CIDADE"],
            "ESTADO": df_clientes.iloc[i]["ESTADO"],
            "HISTORICO_COMPRAS": historico_compras,
            "MARCAS_PREFERIDAS": ", ".join(marcas_preferidas),
            "ULTIMA_COMPRA": df_veiculos.iloc[i]["DATA_VENDA"]
        })
    return pd.DataFrame(dados)


def gerar_todos_dados(qtd):
    df_clientes = gerar_dados_clientes(qtd)
    df_veiculos = gerar_dados_veiculos(qtd)
    df_pagamentos = gerar_dados_pagamentos(df_clientes, df_veiculos)
    df_perfis = gerar_perfis_consumidores(df_clientes, df_veiculos)

    return {
        "clientes": df_clientes,
        "veiculos": df_veiculos,
        "pagamentos": df_pagamentos,
        "perfis_consumidores": df_perfis
    }


def salvar_arquivo(dfs, formato):
    caminho = filedialog.asksaveasfilename(
        defaultextension=f".{formato}",
        filetypes=[(f"{formato.upper()} files", f"*.{formato}")]
    )

    if caminho:
        try:
            if formato == "csv":
                # Salva cada DataFrame em uma pasta com nome específico
                for nome, df in dfs.items():
                    nome_arquivo = f"{caminho.rsplit('.', 1)[0]}_{nome}.csv"
                    df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')

            elif formato == "xlsx":
                # Salva todos os DataFrames em diferentes abas do mesmo arquivo Excel
                with pd.ExcelWriter(caminho, engine='openpyxl') as writer:
                    for nome, df in dfs.items():
                        df.to_excel(writer, sheet_name=nome, index=False)

            elif formato == "json":
                # Converte todos os DataFrames para JSON e salva em um único arquivo
                json_data = {nome: df.to_dict('records') for nome, df in dfs.items()}
                pd.DataFrame([json_data]).to_json(
                    caminho,
                    orient='records',
                    force_ascii=False,
                    indent=4
                )

            messagebox.showinfo("Sucesso", f"Arquivo(s) salvo(s) com sucesso em {caminho}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo: {str(e)}")


def visualizar_dados():
    try:
        qtd = int(entry_qtd.get())
        if qtd <= 0:
            raise ValueError("A quantidade deve ser maior que zero")

        dfs = gerar_todos_dados(qtd)

        # Cria uma nova janela para visualização
        preview_window = tk.Toplevel(root)
        preview_window.title("Prévia dos Dados")
        preview_window.geometry("800x600")

        # Cria um notebook (abas) para mostrar diferentes conjuntos de dados
        notebook = ttk.Notebook(preview_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Cria uma aba para cada DataFrame
        for nome, df in dfs.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=nome.replace('_', ' ').title())

            # Cria um widget Text com scrollbar
            text_widget = tk.Text(frame, wrap=tk.NONE)
            scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=text_widget.yview)
            scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=text_widget.xview)
            text_widget.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

            # Posiciona os widgets
            scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
            scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Insere os dados
            text_widget.insert(tk.END, df.head().to_string())
            text_widget.configure(state='disabled')

        return dfs
    except ValueError as e:
        messagebox.showerror("Erro", str(e))
        return None
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
        return None


def exportar():
    dfs = visualizar_dados()
    if dfs is not None:
        formato = formato_var.get()
        salvar_arquivo(dfs, formato)


# Interface Gráfica
root = tk.Tk()
root.title("Gerador de Dados de Vendas")
root.geometry("600x600")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))

# Frame principal
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Título
title_label = ttk.Label(
    main_frame,
    text="Gerador de Dados de Vendas",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=(0, 20))

# Frame para controles
controls_frame = ttk.Frame(main_frame)
controls_frame.pack(fill=tk.X, pady=10)

# Quantidade de registros
ttk.Label(controls_frame, text="Quantidade de Registros:").pack(pady=5)
entry_qtd = ttk.Entry(controls_frame, font=("Arial", 12))
entry_qtd.pack(pady=5)
entry_qtd.insert(0, "10")

# Formato de exportação
ttk.Label(controls_frame, text="Formato de Exportação:").pack(pady=5)
formato_var = tk.StringVar(value="csv")
formatos = ["csv", "xlsx", "json"]
formato_combo = ttk.Combobox(
    controls_frame,
    textvariable=formato_var,
    values=formatos,
    state="readonly",
    font=("Arial", 12)
)
formato_combo.pack(pady=5)

# Frame dos botões
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=20)

# Botões
ttk.Button(
    button_frame,
    text="Visualizar Dados",
    command=visualizar_dados,
    style="TButton"
).pack(side=tk.LEFT, padx=5)

ttk.Button(
    button_frame,
    text="Gerar e Exportar",
    command=exportar,
    style="TButton"
).pack(side=tk.LEFT, padx=5)

# Informações
info_frame = ttk.Frame(main_frame)
info_frame.pack(fill=tk.X, pady=20)

info_text = """
Dados Gerados:
• Informações de clientes
• Detalhes de veículos
• Dados de pagamentos
• Perfis de consumidores

Formatos Suportados:
• CSV (separado por vírgulas)
• XLSX (Excel)
• JSON (dados estruturados)
"""

info_label = ttk.Label(
    info_frame,
    text=info_text,
    justify=tk.LEFT,
    font=("Arial", 10)
)
info_label.pack(pady=10)

root.mainloop()