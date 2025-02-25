import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedTk
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import json
import sqlite3
import os

# Configuração do Faker para pt_BR
fake = Faker('pt_BR')

# Constantes
BRANDS_AND_MODELS = {
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

PAYMENT_METHODS = ["A vista", "Financiamento", "Consórcio", "Leasing"]
COLORS = ["Preto", "Branco", "Prata", "Vermelho", "Azul"]
GENDERS = ["Masculino", "Feminino"]
STATES = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
    "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]


class DataGenerator:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("Gerador de Dados de Vendas")
        self.root.geometry("800x900")
        self.setup_ui()
        self.current_data = None
        self.current_tab = "customers"
        self.is_dark_theme = False

    def setup_ui(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Título e botão de tema
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(
            title_frame,
            text="Gerador de Dados de Vendas",
            font=("Helvetica", 18, "bold")
        ).pack(side=tk.LEFT)

        self.theme_button = ttk.Button(
            title_frame,
            text="🌙 Tema Escuro",
            command=self.toggle_theme
        )
        self.theme_button.pack(side=tk.RIGHT)

        # Quantidade de registros
        ttk.Label(
            self.main_frame,
            text="Quantidade de Registros:",
            font=("Helvetica", 10)
        ).pack(pady=(0, 5))

        self.count_var = tk.StringVar(value="10")
        self.count_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.count_var,
            width=10
        )
        self.count_entry.pack(pady=(0, 15))

        # Seleção de datas
        dates_frame = ttk.Frame(self.main_frame)
        dates_frame.pack(fill=tk.X, pady=(0, 15))

        # Data inicial
        start_date_frame = ttk.Frame(dates_frame)
        start_date_frame.pack(side=tk.LEFT, expand=True, padx=5)

        ttk.Label(
            start_date_frame,
            text="Data Inicial:",
            font=("Helvetica", 10)
        ).pack()

        self.start_date = ttk.Entry(start_date_frame)
        self.start_date.insert(0, "2022-01-01")
        self.start_date.pack()

        # Data final
        end_date_frame = ttk.Frame(dates_frame)
        end_date_frame.pack(side=tk.LEFT, expand=True, padx=5)

        ttk.Label(
            end_date_frame,
            text="Data Final:",
            font=("Helvetica", 10)
        ).pack()

        self.end_date = ttk.Entry(end_date_frame)
        self.end_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.end_date.pack()

        # Formato de exportação
        ttk.Label(
            self.main_frame,
            text="Formato de Exportação:",
            font=("Helvetica", 10)
        ).pack(pady=(0, 5))

        self.format_var = tk.StringVar(value="csv")
        formats = ["csv", "xlsx", "json", "sql"]
        self.format_combo = ttk.Combobox(
            self.main_frame,
            textvariable=self.format_var,
            values=formats,
            state="readonly"
        )
        self.format_combo.pack(pady=(0, 15))

        # Botões de ação
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(pady=(0, 20))

        ttk.Button(
            buttons_frame,
            text="👁 Visualizar",
            command=self.preview_data
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            buttons_frame,
            text="💾 Exportar",
            command=self.export_data
        ).pack(side=tk.LEFT, padx=5)

        self.copy_button = ttk.Button(
            buttons_frame,
            text="📋 Copiar",
            command=self.copy_data,
            state="disabled"
        )
        self.copy_button.pack(side=tk.LEFT, padx=5)

        # Área de visualização
        self.preview_frame = ttk.LabelFrame(
            self.main_frame,
            text="Prévia dos Dados",
            padding="10"
        )
        self.preview_frame.pack(fill=tk.BOTH, expand=True)

        # Tabs para diferentes conjuntos de dados
        self.tabs_frame = ttk.Frame(self.preview_frame)
        self.tabs_frame.pack(fill=tk.X, pady=(0, 10))

        # Treeview para exibição dos dados
        self.tree_frame = ttk.Frame(self.preview_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        self.vsb = ttk.Scrollbar(self.tree_frame, orient="vertical")
        self.hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal")

        # Treeview
        self.tree = ttk.Treeview(
            self.tree_frame,
            selectmode="extended",
            yscrollcommand=self.vsb.set,
            xscrollcommand=self.hsb.set
        )

        # Configuração das scrollbars
        self.vsb.config(command=self.tree.yview)
        self.hsb.config(command=self.tree.xview)

        # Posicionamento dos elementos
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.hsb.pack(fill=tk.X)

        # Informações
        info_frame = ttk.LabelFrame(
            self.main_frame,
            text="Informações",
            padding="10"
        )
        info_frame.pack(fill=tk.X, pady=(20, 0))

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
• SQL (banco de dados SQLite)
        """

        ttk.Label(
            info_frame,
            text=info_text,
            justify=tk.LEFT
        ).pack()

    def generate_customer(self, id):
        gender = random.choice(GENDERS)
        first_name = fake.first_name_male() if gender == "Masculino" else fake.first_name_female()
        last_name = fake.last_name()

        return {
            "ID": id,
            "Nome": f"{first_name} {last_name}",
            "Idade": random.randint(18, 70),
            "CPF": fake.cpf(),
            "Sexo": gender,
            "Email": fake.email(),
            "Telefone": fake.phone_number(),
            "Cidade": fake.city(),
            "Estado": random.choice(STATES)
        }

    def generate_vehicle(self):
        brand = random.choice(list(BRANDS_AND_MODELS.keys()))
        model = random.choice(BRANDS_AND_MODELS[brand])

        start_date = datetime.strptime(self.start_date.get(), "%Y-%m-%d")
        end_date = datetime.strptime(self.end_date.get(), "%Y-%m-%d")
        sale_date = fake.date_between(start_date=start_date, end_date=end_date)

        return {
            "Marca": brand,
            "Modelo": model,
            "Ano": random.randint(2015, 2024),
            "Cor": random.choice(COLORS),
            "Valor": round(random.uniform(30000, 250000), 2),
            "Data_Venda": sale_date.strftime("%Y-%m-%d"),
            "Forma_Pagamento": random.choice(PAYMENT_METHODS)
        }

    def generate_payment(self, customer, vehicle):
        payment = {
            "ID": random.randint(1000, 9999),
            "CPF_Cliente": customer["CPF"],
            "Forma_Pagamento": vehicle["Forma_Pagamento"],
            "Valor_Total": vehicle["Valor"],
            "Data_Pagamento": vehicle["Data_Venda"]
        }

        if vehicle["Forma_Pagamento"] == "Financiamento":
            payment.update({
                "Parcelas": random.randint(12, 60),
                "Taxa_Juros": round(random.uniform(0.5, 2.5), 2)
            })

        return payment

    def generate_consumer_profile(self, customer, vehicle):
        return {
            "ID": customer["ID"],
            "Nome": customer["Nome"],
            "Idade": customer["Idade"],
            "Email": customer["Email"],
            "Cidade": customer["Cidade"],
            "Estado": customer["Estado"],
            "Historico_Compras": random.randint(1, 5),
            "Marcas_Preferidas": ", ".join(random.sample(list(BRANDS_AND_MODELS.keys()), k=random.randint(1, 3))),
            "Ultima_Compra": vehicle["Data_Venda"]
        }

    def generate_all_data(self):
        try:
            count = int(self.count_var.get())
            if count <= 0:
                raise ValueError("A quantidade deve ser maior que zero")

            customers = [self.generate_customer(i + 1) for i in range(count)]
            vehicles = [self.generate_vehicle() for _ in range(count)]
            payments = [self.generate_payment(c, v) for c, v in zip(customers, vehicles)]
            profiles = [self.generate_consumer_profile(c, v) for c, v in zip(customers, vehicles)]

            return {
                "Clientes": customers,
                "Veículos": vehicles,
                "Pagamentos": payments,
                "Perfil de consumidor": profiles
            }
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
            return None
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            return None

    def update_treeview(self, data_dict, tab_name):
        # Limpar dados anteriores
        for item in self.tree.get_children():
            self.tree.delete(item)

        for col in self.tree["columns"]:
            self.tree.heading(col, text="")

        if not data_dict or tab_name not in data_dict:
            return

        data = data_dict[tab_name]
        if not data:
            return

        # Configurar colunas
        columns = list(data[0].keys())
        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Inserir dados
        for item in data:
            values = [str(item[col]) for col in columns]
            self.tree.insert("", "end", values=values)

    def create_tab_buttons(self):
        for widget in self.tabs_frame.winfo_children():
            widget.destroy()

        for tab_name in self.current_data.keys():
            btn = ttk.Button(
                self.tabs_frame,
                text=tab_name,
                command=lambda t=tab_name: self.change_tab(t)
            )
            btn.pack(side=tk.LEFT, padx=2)

    def change_tab(self, tab_name):
        self.current_tab = tab_name
        self.update_treeview(self.current_data, tab_name)

    def preview_data(self):
        self.current_data = self.generate_all_data()
        if self.current_data:
            self.create_tab_buttons()
            self.update_treeview(self.current_data, list(self.current_data.keys())[0])
            self.copy_button.config(state="normal")

    def export_data(self):
        data = self.current_data or self.generate_all_data()
        if not data:
            return

        format_type = self.format_var.get()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        try:
            if format_type == "csv":
                folder = filedialog.askdirectory()
                if folder:
                    for name, df in data.items():
                        df = pd.DataFrame(df)
                        filepath = os.path.join(folder, f"{name}_{timestamp}.csv")
                        df.to_csv(filepath, index=False, encoding='utf-8-sig')

            elif format_type == "xlsx":
                filepath = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx")],
                    initialfile=f"dados_vendas_{timestamp}.xlsx"
                )
                if filepath:
                    with pd.ExcelWriter(filepath) as writer:
                        for name, df in data.items():
                            pd.DataFrame(df).to_excel(writer, sheet_name=name, index=False)

            elif format_type == "json":
                filepath = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json")],
                    initialfile=f"dados_vendas_{timestamp}.json"
                )
                if filepath:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)

            elif format_type == "sql":
                filepath = filedialog.asksaveasfilename(
                    defaultextension=".db",
                    filetypes=[("SQLite files", "*.db")],
                    initialfile=f"dados_vendas_{timestamp}.db"
                )
                if filepath:
                    conn = sqlite3.connect(filepath)
                    for name, records in data.items():
                        df = pd.DataFrame(records)
                        df.to_sql(name, conn, if_exists='replace', index=False)
                    conn.close()

            messagebox.showinfo("Sucesso", "Dados exportados com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar dados: {str(e)}")

    def copy_data(self):
        if not self.current_data or not self.current_tab:
            return

        data = self.current_data[self.current_tab]
        text = json.dumps(data, ensure_ascii=False, indent=2)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Sucesso", "Dados copiados para a área de transferência!")

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        theme = "equilux" if self.is_dark_theme else "arc"
        self.root.set_theme(theme)
        self.theme_button.config(
            text="☀️ Tema Claro" if self.is_dark_theme else "🌙 Tema Escuro"
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = DataGenerator()
    app.run()