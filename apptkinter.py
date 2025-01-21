import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt


class FinanceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Finanças Pessoais")
        self.root.geometry("400x500")
        self.data = pd.DataFrame(columns=["Tipo", "Categoria", "Valor", "Data"])
        
        # Elementos da interface
        self.create_widgets()
    
    def create_widgets(self):
        # Títulos
        tk.Label(self.root, text="Adicionar Transação", font=("Arial", 14)).pack(pady=10)
        
        # Tipo
        tk.Label(self.root, text="Tipo:").pack(anchor="w")
        self.type_var = tk.StringVar(value="Receita")
        tk.Radiobutton(self.root, text="Receita", variable=self.type_var, value="Receita").pack(anchor="w")
        tk.Radiobutton(self.root, text="Despesa", variable=self.type_var, value="Despesa").pack(anchor="w")
        
        # Categoria
        tk.Label(self.root, text="Categoria:").pack(anchor="w")
        self.category_entry = tk.Entry(self.root)
        self.category_entry.pack(fill="x", pady=5)
        
        # Valor
        tk.Label(self.root, text="Valor (R$):").pack(anchor="w")
        self.value_entry = tk.Entry(self.root)
        self.value_entry.pack(fill="x", pady=5)
        
        # Data
        tk.Label(self.root, text="Data (AAAA-MM-DD):").pack(anchor="w")
        self.date_entry = tk.Entry(self.root)
        self.date_entry.pack(fill="x", pady=5)
        
        # Botão de adicionar
        tk.Button(self.root, text="Adicionar", command=self.add_transaction).pack(pady=10)
        
        # Botões extras
        tk.Button(self.root, text="Exibir Resumo", command=self.show_summary).pack(fill="x", pady=5)
        tk.Button(self.root, text="Exportar Dados", command=self.export_data).pack(fill="x", pady=5)
        tk.Button(self.root, text="Gráfico de Despesas", command=self.plot_expenses).pack(fill="x", pady=5)
    
    def add_transaction(self):
        tipo = self.type_var.get()
        categoria = self.category_entry.get()
        valor = self.value_entry.get()
        data = self.date_entry.get()
        
        if not categoria or not valor or not data:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
        
        try:
            valor = float(valor)
        except ValueError:
            messagebox.showerror("Erro", "O valor deve ser numérico.")
            return
        
        self.data = pd.concat([self.data, pd.DataFrame([[tipo, categoria, valor, data]], 
                                                       columns=["Tipo", "Categoria", "Valor", "Data"])],
                              ignore_index=True)
        messagebox.showinfo("Sucesso", "Transação adicionada com sucesso!")
        self.category_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
    
    def show_summary(self):
        if self.data.empty:
            messagebox.showinfo("Resumo", "Nenhuma transação registrada.")
            return
        
        total_receitas = self.data[self.data["Tipo"] == "Receita"]["Valor"].sum()
        total_despesas = self.data[self.data["Tipo"] == "Despesa"]["Valor"].sum()
        saldo = total_receitas - total_despesas
        
        resumo = (f"Total de Receitas: R$ {total_receitas:.2f}\n"
                  f"Total de Despesas: R$ {total_despesas:.2f}\n"
                  f"Saldo Atual: R$ {saldo:.2f}")
        
        messagebox.showinfo("Resumo Financeiro", resumo)
    
    def export_data(self):
        if self.data.empty:
            messagebox.showinfo("Exportar Dados", "Nenhuma transação registrada para exportar.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                 filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.data.to_csv(file_path, index=False)
            messagebox.showinfo("Exportar Dados", "Dados exportados com sucesso!")
    
    def plot_expenses(self):
        despesas = self.data[self.data["Tipo"] == "Despesa"]
        if despesas.empty:
            messagebox.showinfo("Gráfico", "Nenhuma despesa registrada para exibir.")
            return
        
        categorias = despesas.groupby("Categoria")["Valor"].sum()
        categorias.plot(kind="bar", title="Despesas por Categoria", xlabel="Categoria", ylabel="Valor (R$)")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceManager(root)
    root.mainloop()
