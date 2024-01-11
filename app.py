import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import os
import shutil
from threading import Thread

def browse_path(entry):
    folder_selected = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_selected)

def copy_files(source, destination, progress_bar, progress_label, text_widget):
    files = os.listdir(source)
    for index, file in enumerate(files):
        source_file = os.path.join(source, file)
        destination_file = os.path.join(destination, file)

        if not os.path.exists(destination_file) or os.path.getmtime(source_file) > os.path.getmtime(destination_file):
            try:
                shutil.copy2(source_file, destination_file)
                text_widget.insert(tk.END, f"Copiado: {file}\n")
            except PermissionError:
                text_widget.insert(tk.END, f"Erro de Permissão, não copiado: {file}\n")
            except Exception as e:
                text_widget.insert(tk.END, f"Erro ao copiar {file}: {e}\n")
        else:
            text_widget.insert(tk.END, f"Já existe e está atualizado: {file}\n")

        text_widget.see(tk.END)
        progress = (index + 1) / len(files) * 100
        progress_bar['value'] = progress
        progress_label.config(text=f"{progress:.2f}% Completo")
        window.update_idletasks()

def start_backup(source_entry, destination_entry, progress_bar, progress_label, text_widget):
    source = source_entry.get()
    destination = destination_entry.get()
    text_widget.delete('1.0', tk.END)
    try:
        thread = Thread(target=copy_files, args=(source, destination, progress_bar, progress_label, text_widget))
        thread.start()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def on_closing():
    if messagebox.askokcancel("Sair", "Interromper o backup pode resultar em perda de dados. Deseja realmente sair?"):
        window.destroy()

window = tk.Tk()
window.title("Backup App")
window.protocol("WM_DELETE_WINDOW", on_closing)

frame = tk.Frame(window)
frame.pack(padx=10, pady=10)

source_label = tk.Label(frame, text="Origem:")
source_label.grid(row=0, column=0, pady=(0, 5))

source_entry = tk.Entry(frame, width=50)
source_entry.grid(row=0, column=1, pady=(0, 5))

source_button = tk.Button(frame, text="Buscar", command=lambda: browse_path(source_entry))
source_button.grid(row=0, column=2, pady=(0, 5))

destination_label = tk.Label(frame, text="Destino:")
destination_label.grid(row=1, column=0)

destination_entry = tk.Entry(frame, width=50)
destination_entry.grid(row=1, column=1)

destination_button = tk.Button(frame, text="Buscar", command=lambda: browse_path(destination_entry))
destination_button.grid(row=1, column=2)

backup_button = tk.Button(frame, text="Iniciar a copia", command=lambda: start_backup(source_entry, destination_entry, progress_bar, progress_label, terminal_output))
backup_button.grid(row=2, column=1, pady=10)

progress_bar = ttk.Progressbar(frame, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(row=3, column=0, columnspan=3, pady=5)

progress_label = tk.Label(frame, text="0% Completo")
progress_label.grid(row=4, column=0, columnspan=3, pady=(0, 5))

terminal_output = scrolledtext.ScrolledText(frame, height=10)
terminal_output.grid(row=5, column=0, columnspan=3, pady=5)

window.mainloop()
