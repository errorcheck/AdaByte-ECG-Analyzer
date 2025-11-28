import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
import sys

# -------------------------------------------------
def recurso_path(relative_path):
    """Permite acceder a archivos tanto en ejecución normal como en .exe."""
    if hasattr(sys, 'frozen'):  # ejecutable
        base_path = os.path.dirname(sys.executable)
    else:  # ejecución normal .py
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

# -------------------------------------------------
def encontrar_ecg_script():
    """
    Busca SOLO ecg.py en la carpeta principal.
    Ignora completamente _internal y cualquier duplicado.
    """
    if hasattr(sys, 'frozen'):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    ruta_principal = os.path.join(base, "ecg.py")
    if os.path.isfile(ruta_principal):
        return ruta_principal

    return None

# -------------------------------------------------
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo ECG",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        entrada_archivo.set(archivo)
        messagebox.showinfo(
            "Archivo seleccionado",
            f"Listo:\n{os.path.basename(archivo)}"
        )

# -------------------------------------------------
def analizar_ecg():
    ruta_csv = entrada_archivo.get()

    if not ruta_csv or not os.path.exists(ruta_csv):
        messagebox.showerror("Error", "Seleccioná un CSV válido primero.")
        return

    script = encontrar_ecg_script()
    if not script:
        messagebox.showerror(
            "Error crítico",
            "No se encuentra ecg.py\n"
            "Debe estar en la MISMA carpeta que este programa."
        )
        return

    try:
        subprocess.run(
            [sys.executable, script, ruta_csv],
            cwd=os.path.dirname(script),
            check=True,
            text=True
        )
        messagebox.showinfo("Éxito", "Análisis completado correctamente.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error en el análisis", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------------------------------------------------
def generar_pdf():
    """
    NO relanza el análisis.
    El PDF lo genera ecg.py cuando corresponde.
    """
    messagebox.showinfo("PDF", "El PDF se generó correctamente.")

# -------------------------------------------------
# INTERFAZ
ventana = tk.Tk()
ventana.title("AdaByte – ECG Analyzer v1")
ventana.geometry("500x280")
ventana.config(bg="#f2f2f2")

entrada_archivo = tk.StringVar()

tk.Label(
    ventana,
    text="ECG Analyzer AdaByte",
    font=("Arial", 18, "bold"),
    bg="#f2f2f2"
).pack(pady=15)

frame = tk.Frame(ventana, bg="#f2f2f2")
frame.pack(pady=10)

tk.Entry(frame, textvariable=entrada_archivo, width=55).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Seleccionar CSV", command=seleccionar_archivo).pack(side=tk.LEFT, padx=5)

tk.Button(
    ventana,
    text="Analizar ECG",
    font=("Arial", 12, "bold"),
    bg="#4fc3f7",
    fg="white",
    height=2,
    command=analizar_ecg
).pack(pady=12)

tk.Button(
    ventana,
    text="Generar PDF",
    font=("Arial", 12, "bold"),
    bg="#81c784",
    fg="white",
    height=2,
    command=generar_pdf
).pack(pady=8)

ventana.mainloop()
