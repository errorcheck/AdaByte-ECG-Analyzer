import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import sys
import os

# -------------------------------------------------
def analizar_ecg(ruta_archivo):
    """Analiza el CSV de ECG y genera un PDF sin abrir ventanas."""
    try:
        df = pd.read_csv(ruta_archivo)
    except Exception as e:
        print(f"ERROR al leer el CSV: {e}")
        return

    # PDF de salida
    nombre = os.path.splitext(os.path.basename(ruta_archivo))[0]
    pdf_path = nombre + "_informe.pdf"

    with PdfPages(pdf_path) as pdf:

        # --- Página 1: estadísticas ---
        fig1 = plt.figure(figsize=(8, 6))
        plt.title("Estadísticas descriptivas")
        plt.text(0.01, 0.99, str(df.describe()), fontsize=10, va='top')
        pdf.savefig(fig1)
        plt.close(fig1)

        # --- Página 2: Histograma de BPM ---
        fig2 = plt.figure(figsize=(10, 5))
        sns.histplot(df['heart_rate'], kde=True, color='blue')
        plt.title("Distribución de Frecuencia Cardíaca")
        plt.xlabel("BPM")
        plt.ylabel("Frecuencia")
        pdf.savefig(fig2)
        plt.close(fig2)

        # --- Página 3: Boxplot QRS ---
        fig3 = plt.figure(figsize=(8, 5))
        sns.boxplot(x='arrhythmia_detected', y='qrs_duration', data=df)
        plt.title("Duración del QRS según Arritmia")
        plt.xlabel("Arritmia (0 = No, 1 = Sí)")
        plt.ylabel("Duración QRS (ms)")
        pdf.savefig(fig3)
        plt.close(fig3)

    print(f"Informe generado: {pdf_path}")

# -------------------------------------------------
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Uso: python ecg.py archivo.csv")
        sys.exit(1)

    ruta = sys.argv[1]

    if not os.path.exists(ruta):
        print(f"ERROR: No existe el archivo {ruta}")
        sys.exit(1)

    analizar_ecg(ruta)
