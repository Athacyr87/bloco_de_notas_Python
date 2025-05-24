import tkinter as tk
from tkinter import filedialog, messagebox

class BlocoDeNotas:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloco de Notas")
        self.root.geometry("600x400")  # Tamanho inicial da janela
        self.root.configure(bg="#F0F0F0")  # Fundo cinza claro, similar ao Windows

        # Configurar ícone (opcional, pode não funcionar em todos os sistemas)
        try:
            self.root.iconbitmap("notepad.ico")  # Necessita de um arquivo .ico
        except:
            pass  # Ignora se o ícone não estiver disponível

        # Área de texto com barra de rolagem
        self.texto_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.texto_frame.pack(expand=True, fill="both", padx=5, pady=5)

        self.scrollbar = tk.Scrollbar(self.texto_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.texto = tk.Text(
            self.texto_frame,
            wrap="word",
            font=("Consolas", 11),  # Fonte padrão do Bloco de Notas do Windows
            bg="#FFFFFF",  # Fundo branco
            fg="#000000",  # Texto preto
            insertbackground="#000000",  # Cursor preto
            relief="sunken",  # Borda estilo Windows
            borderwidth=2,
            yscrollcommand=self.scrollbar.set
        )
        self.texto.pack(expand=True, fill="both")
        self.scrollbar.config(command=self.texto.yview)

        # Menu principal
        self.menu_bar = tk.Menu(self.root, bg="#F0F0F0", relief="flat")
        self.root.config(menu=self.menu_bar)

        # Menu Arquivo
        self.menu_arquivo = tk.Menu(self.menu_bar, tearoff=0, bg="#FFFFFF", font=("Segoe UI", 9))
        self.menu_bar.add_cascade(label="Arquivo", menu=self.menu_arquivo)
        self.menu_arquivo.add_command(label="Novo", command=self.novo_arquivo, accelerator="Ctrl+N")
        self.menu_arquivo.add_command(label="Abrir...", command=self.abrir_arquivo, accelerator="Ctrl+O")
        self.menu_arquivo.add_command(label="Salvar", command=self.salvar_arquivo, accelerator="Ctrl+S")
        self.menu_arquivo.add_command(label="Salvar como...", command=self.salvar_como)
        self.menu_arquivo.add_separator()
        self.menu_arquivo.add_command(label="Sair", command=self.sair)

        # Menu Editar
        self.menu_editar = tk.Menu(self.menu_bar, tearoff=0, bg="#FFFFFF", font=("Segoe UI", 9))
        self.menu_bar.add_cascade(label="Editar", menu=self.menu_editar)
        self.menu_editar.add_command(label="Desfazer", command=self.desfazer, accelerator="Ctrl+Z")
        self.menu_editar.add_separator()
        self.menu_editar.add_command(label="Cortar", command=self.cortar, accelerator="Ctrl+X")
        self.menu_editar.add_command(label="Copiar", command=self.copiar, accelerator="Ctrl+C")
        self.menu_editar.add_command(label="Colar", command=self.colar, accelerator="Ctrl+V")
        self.menu_editar.add_command(label="Selecionar tudo", command=self.selecionar_tudo, accelerator="Ctrl+A")

        # Atalhos de teclado
        self.root.bind("<Control-n>", lambda event: self.novo_arquivo())
        self.root.bind("<Control-o>", lambda event: self.abrir_arquivo())
        self.root.bind("<Control-s>", lambda event: self.salvar_arquivo())
        self.root.bind("<Control-z>", lambda event: self.desfazer())
        self.root.bind("<Control-x>", lambda event: self.cortar())
        self.root.bind("<Control-c>", lambda event: self.copiar())
        self.root.bind("<Control-v>", lambda event: self.colar())
        self.root.bind("<Control-a>", lambda event: self.selecionar_tudo())

        self.arquivo_atual = None  # Para rastrear o arquivo aberto

    def novo_arquivo(self):
        if self.texto.get("1.0", tk.END).strip():
            if messagebox.askyesno("Salvar", "Deseja salvar o arquivo atual antes de criar um novo?"):
                self.salvar_arquivo()
        self.texto.delete("1.0", tk.END)
        self.arquivo_atual = None
        self.root.title("Bloco de Notas - Novo Arquivo")

    def abrir_arquivo(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")])
        if arquivo:
            try:
                with open(arquivo, "r", encoding="utf-8") as f:
                    self.texto.delete("1.0", tk.END)
                    self.texto.insert("1.0", f.read())
                self.arquivo_atual = arquivo
                self.root.title(f"Bloco de Notas - {arquivo}")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")

    def salvar_arquivo(self):
        if self.arquivo_atual:
            try:
                with open(self.arquivo_atual, "w", encoding="utf-8") as f:
                    f.write(self.texto.get("1.0", tk.END).strip())
                self.root.title(f"Bloco de Notas - {self.arquivo_atual}")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")
        else:
            self.salvar_como()

    def salvar_como(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")])
        if arquivo:
            self.arquivo_atual = arquivo
            self.salvar_arquivo()

    def desfazer(self):
        try:
            self.texto.edit_undo()
        except:
            pass  # Ignora se não houver ação para desfazer

    def cortar(self):
        self.texto.event_generate("<<Cut>>")

    def copiar(self):
        self.texto.event_generate("<<Copy>>")

    def colar(self):
        self.texto.event_generate("<<Paste>>")

    def selecionar_tudo(self):
        self.texto.tag_add(tk.SEL, "1.0", tk.END)
        self.texto.mark_set(tk.INSERT, "1.0")
        self.texto.see(tk.INSERT)

    def sair(self):
        if self.texto.get("1.0", tk.END).strip():
            if messagebox.askyesno("Sair", "Deseja salvar antes de sair?"):
                self.salvar_arquivo()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlocoDeNotas(root)
    root.mainloop()