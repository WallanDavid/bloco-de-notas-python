from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
from fpdf import FPDF
import os
import time

class SecureNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Notes App")

        # Configurar o estilo para uma aparência moderna
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Pode ser "clam", "alt", "default", "classic", etc.

        # Barra de ferramentas
        self.toolbar = ttk.Frame(root)
        self.toolbar.pack(side=TOP, fill=X)

        # Botões da barra de ferramentas
        ttk.Button(self.toolbar, text="Salvar", command=self.save_note).grid(row=0, column=0, padx=5)
        ttk.Button(self.toolbar, text="Exportar", command=self.export_note).grid(row=0, column=1, padx=5)
        ttk.Button(self.toolbar, text="Criar Pasta", command=self.create_folder).grid(row=0, column=2, padx=5)

        # Textbox para inserir notas
        self.note_entry = Text(root, wrap=WORD, width=40, height=10)
        self.note_entry.pack(pady=10)
        self.note_entry.bind("<KeyRelease>", self.update_word_count)

        # Variáveis para controle
        self.current_folder = None

        # Contador de palavras
        self.word_count_label = Label(root, text="Contador de Palavras: 0")
        self.word_count_label.pack()

        # Adicionando funcionalidades adicionais
        self.setup_additional_features()

    def setup_additional_features(self):
        # Implementação de funcionalidades adicionais
        self.add_auto_backup()
        self.add_search_notes()

    def add_auto_backup(self):
        # Configuração do backup automático a cada 5 minutos
        self.root.after(300000, self.auto_backup)

    def auto_backup(self):
        try:
            # Salva a nota em um arquivo de backup
            backup_filename = f"backup_{time.strftime('%Y%m%d%H%M%S')}.txt"
            with open(backup_filename, "w") as backup_file:
                backup_file.write(self.note_entry.get("1.0", "end-1c"))

            messagebox.showinfo("Backup Automático", "Backup realizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro ao fazer Backup", f"Ocorreu um erro: {str(e)}")

        # Configura o próximo backup automático
        self.root.after(300000, self.auto_backup)

    def add_search_notes(self):
        # Barra de pesquisa
        self.search_var = StringVar()
        self.search_entry = Entry(self.root, textvariable=self.search_var, width=20)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.search_notes)

    def search_notes(self, event):
        # Filtra as notas com base na pesquisa
        search_term = self.search_var.get().lower()
        all_text = self.note_entry.get("1.0", "end-1c").lower()

        if search_term:
            start_pos = "1.0"
            while True:
                start_pos = all_text.find(search_term, start_pos)
                if start_pos:
                    end_pos = f"{start_pos}+{len(search_term)}c"
                    self.note_entry.tag_add("search", start_pos, end_pos)
                    start_pos = end_pos
                else:
                    break

            self.note_entry.tag_configure("search", background="yellow")
        else:
            self.note_entry.tag_remove("search", "1.0", "end-1c")

    def create_folder(self):
        # Cria uma pasta para organizar notas
        folder_name = filedialog.askdirectory(title="Criar Pasta")
        if folder_name:
            self.current_folder = folder_name
            messagebox.showinfo("Pasta Criada", f"Pasta '{os.path.basename(folder_name)}' criada com sucesso!")

    def save_note(self):
        # Salva a nota em um arquivo de texto
        file_types = [("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")]
        if self.current_folder:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=file_types, initialdir=self.current_folder)
        else:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=file_types)

        if file_path:
            with open(file_path, "w") as file:
                file.write(self.note_entry.get("1.0", "end-1c"))

            messagebox.showinfo("Nota Salva", f"Nota salva com sucesso em '{os.path.basename(file_path)}'!")

    def export_note(self):
        # Exporta a nota atual para um arquivo de texto
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.note_entry.get("1.0", "end-1c"))

            messagebox.showinfo("Exportação", f"Nota exportada com sucesso para '{os.path.basename(file_path)}'!")

    def import_note(self):
        # Importa uma nota de um arquivo de texto
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.note_entry.delete("1.0", "end")
                self.note_entry.insert("1.0", content)

            messagebox.showinfo("Importação", f"Nota importada com sucesso de '{os.path.basename(file_path)}'!")

    def update_word_count(self, event):
        # Atualiza o contador de palavras em tempo real
        words = self.note_entry.get("1.0", "end-1c").split()
        word_count = len(words)
        self.word_count_label.config(text=f"Contador de Palavras: {word_count}")

if __name__ == "__main__":
    root = Tk()
    app = SecureNotesApp(root)
    root.mainloop()
