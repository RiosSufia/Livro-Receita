import customtkinter as ctk
from tkinter import messagebox
from receita import Receita
from livro_receitas import LivroDeReceitas

class InterfaceReceitas:
    def __init__(self):
        self.livro = LivroDeReceitas()
        
        # Cores do Design
        self.cor_fundo = "#1A120B"      # Marrom quase preto
        self.cor_card = "#2C1D12"       # Marrom escuro
        self.cor_laranja = "#F5912E"    # Laranja principal
        self.cor_texto_sec = "#A9907E"  # Texto bege/cinza

        ctk.set_appearance_mode("dark")
        self.root = ctk.CTk()
        self.root.title("Diário de Receitas")
        self.root.geometry("1000x750")
        self.root.configure(fg_color=self.cor_fundo)

        self.criar_tela_principal()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def criar_tela_principal(self):
        self.limpar_tela()

        # Header
        header = ctk.CTkFrame(self.root, fg_color="transparent")
        header.pack(fill="x", padx=60, pady=(40, 20))

        titulo_f = ctk.CTkFrame(header, fg_color="transparent")
        titulo_f.pack(side="left")
        ctk.CTkLabel(titulo_f, text="Minhas Receitas", font=("Arial Bold", 32), text_color="white").pack(anchor="w")
        ctk.CTkLabel(titulo_f, text="Gerencie suas criações culinárias favoritas", font=("Arial", 14), text_color=self.cor_texto_sec).pack(anchor="w")

        ctk.CTkButton(header, text="+ Adicionar Receita", fg_color=self.cor_laranja, text_color="black", 
                       font=("Arial Bold", 14), height=45, corner_radius=8, command=self.tela_adicionar).pack(side="right")

        # Container de Cards
        self.scroll = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=50, pady=10)
        
        # Configurar colunas do grid
        self.scroll.grid_columnconfigure((0, 1, 2), weight=1)

        for i, receita in enumerate(self.livro.obter_receitas()):
            self.criar_card(receita, i)

    def criar_card(self, receita, indice):
        card = ctk.CTkFrame(self.scroll, fg_color=self.cor_card, corner_radius=15, border_width=1, border_color="#3D2B1F")
        card.grid(row=indice//3, column=indice%3, padx=10, pady=10, sticky="nsew")

        # Placeholder da Foto
        foto = ctk.CTkFrame(card, height=150, fg_color="#3D2B1F", corner_radius=10)
        foto.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(foto, text="🍽️", font=("Arial", 40)).place(relx=0.5, rely=0.5, anchor="center")

        # Info
        ctk.CTkLabel(card, text=receita.nome, font=("Arial Bold", 18), text_color="white").pack(anchor="w", padx=15)
        ctk.CTkLabel(card, text=f"⏱ {receita.tempo}", font=("Arial", 12), text_color=self.cor_laranja).pack(anchor="w", padx=15)

        # Botões
        btn_ver = ctk.CTkButton(card, text="Ver Receita", fg_color="#432C1E", hover_color="#5D3D2A", 
                                 height=35, command=lambda i=indice: self.ver_receita(i))
        btn_ver.pack(fill="x", padx=15, pady=(15, 5))

        btn_f = ctk.CTkFrame(card, fg_color="transparent")
        btn_f.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(btn_f, text="Editar", fg_color="transparent", border_width=1, border_color="#5D3D2A",
                       height=30, command=lambda i=indice: self.editar_receita(i)).pack(side="left", expand=True, fill="x", padx=(0,5))
        
        ctk.CTkButton(btn_f, text="🗑", fg_color="transparent", text_color="#E74C3C", width=30, 
                       command=lambda i=indice: self.remover_receita(i)).pack(side="right")

    def tela_adicionar(self):
        self.limpar_tela()
        container = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=150, pady=20)

        ctk.CTkLabel(container, text="Nova Receita", font=("Arial Bold", 26)).pack(pady=20)

        self.in_nome = ctk.CTkEntry(container, placeholder_text="Nome da receita", height=45, fg_color=self.cor_card)
        self.in_nome.pack(fill="x", pady=10)

        f_extra = ctk.CTkFrame(container, fg_color="transparent")
        f_extra.pack(fill="x")
        self.in_tempo = ctk.CTkEntry(f_extra, placeholder_text="Tempo (ex: 1h 20min)", fg_color=self.cor_card)
        self.in_tempo.pack(side="left", fill="x", expand=True, padx=(0,5))
        self.in_porcao = ctk.CTkEntry(f_extra, placeholder_text="Porções (ex: 4 pessoas)", fg_color=self.cor_card)
        self.in_porcao.pack(side="right", fill="x", expand=True, padx=(5,0))

        self.in_ingredientes = ctk.CTkTextbox(container, height=120, fg_color=self.cor_card)
        self.in_ingredientes.pack(fill="x", pady=10)
        self.in_ingredientes.insert("0.0", "Ingredientes (um por linha)")

        self.in_preparo = ctk.CTkTextbox(container, height=120, fg_color=self.cor_card)
        self.in_preparo.pack(fill="x", pady=10)
        self.in_preparo.insert("0.0", "Modo de preparo (um por linha)")

        ctk.CTkButton(container, text="Salvar Receita", fg_color=self.cor_laranja, text_color="black", 
                       font=("Arial Bold", 16), height=50, command=self.salvar_receita).pack(fill="x", pady=20)
        
        ctk.CTkButton(container, text="Voltar", fg_color="transparent", command=self.criar_tela_principal).pack()

    def salvar_receita(self):
        nome = self.in_nome.get()
        ing = self.in_ingredientes.get("1.0", "end").strip().split("\n")
        prep = self.in_preparo.get("1.0", "end").strip().split("\n")
        t = self.in_tempo.get()
        p = self.in_porcao.get()

        nova = Receita(nome, ing, prep, t, p)
        self.livro.adicionar_receita(nova)
        self.criar_tela_principal()

    def ver_receita(self, indice):
        rec = self.livro.obter_receitas()[indice]
        self.limpar_tela()

        # Banner Superior
        banner = ctk.CTkFrame(self.root, height=200, fg_color=self.cor_card)
        banner.pack(fill="x", padx=60, pady=30)
        ctk.CTkLabel(banner, text=rec.nome, font=("Arial Bold", 40)).place(relx=0.05, rely=0.7, anchor="w")

        info = ctk.CTkTextbox(self.root, fg_color="transparent", font=("Arial", 16))
        info.pack(fill="both", expand=True, padx=60)
        info.insert("0.0", rec.texto_receita())
        info.configure(state="disabled")

        ctk.CTkButton(self.root, text="Voltar ao Dashboard", fg_color="#432C1E", 
                       command=self.criar_tela_principal).pack(pady=20)

    def remover_receita(self, indice):
        if messagebox.askyesno("Confirmar", "Deseja remover esta receita?"):
            self.livro.remover_receita(indice)
            self.criar_tela_principal()

    def editar_receita(self, indice):
        # Implementação similar à tela_adicionar, mas preenchendo os campos
        pass

    def executar(self):
        self.root.mainloop()