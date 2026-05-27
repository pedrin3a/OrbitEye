
# =========================================================
# ORBITEYE
# =========================================================

import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime
import time

# =========================================================
# CONFIGURAÇÕES
# =========================================================

API_KEY = "c338b5700ae948e2b54205037262705"

BG_COLOR = "#050816"
PANEL_COLOR = "#0B1120"
NEON_BLUE = "#00F5FF"
TEXT_COLOR = "#E2E8F0"
ALERT_COLOR = "#FF4C4C"
GREEN_COLOR = "#00FFAA"

FONT_TITLE = ("Consolas", 24, "bold")
FONT_TEXT = ("Consolas", 12)
FONT_SMALL = ("Consolas", 10)

# =========================================================
# FUNÇÕES
# =========================================================

def salvar_log(mensagem):

    try:

        horario = datetime.now().strftime("%H:%M:%S")

        with open("logs.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(f"[{horario}] {mensagem}\n")

        logs_text.insert(tk.END, f"[{horario}] {mensagem}\n")
        logs_text.see(tk.END)

    except Exception as erro:
        print("Erro ao salvar log:", erro)

# =========================================================

def atualizar_relogio():

    horario = time.strftime("%H:%M:%S")

    relogio_label.config(
        text=f"Relógio: {horario}"
    )

    root.after(1000, atualizar_relogio)

# =========================================================

def animar_status():

    cores = ["#00F5FF", "#00FFAA"]

    atual = status.cget("fg")

    if atual == cores[0]:
        status.config(fg=cores[1])
    else:
        status.config(fg=cores[0])

    root.after(500, animar_status)

# =========================================================

def loading_satelite():

    status.config(
        text="CONECTANDO AO SATÉLITE..."
    )

    root.update()

# =========================================================

def analisar_risco(temp, humidity, weather):

    alerta = "✓ SEM ALERTAS"

    if temp >= 38 and humidity <= 30:
        alerta = "⚠ RISCO DE INCÊNDIO"

    elif "chuva" in weather.lower():
        alerta = "⚠ POSSÍVEL ENCHENTE"

    elif "tempestade" in weather.lower():
        alerta = "⚠ ALERTA DE TEMPESTADE"

    elif temp <= 5:
        alerta = "⚠ FRIO EXTREMO"

    return alerta

# =========================================================

def monitorar_cidade():

    cidade = cidade_entry.get()

    if cidade == "":
        messagebox.showwarning(
            "ATENÇÃO",
            "Digite uma cidade."
        )
        return

    try:

        loading_satelite()

        url = (
            f"http://api.weatherapi.com/v1/current.json?"
            f"key={API_KEY}&q={cidade},Brazil&lang=pt"
        )

        resposta = requests.get(url)

        dados = resposta.json()

        if "error" in dados:

            messagebox.showerror(
                "ERRO",
                "Cidade não encontrada."
            )

            salvar_log(
                "Erro ao localizar cidade"
            )

            return

        # =====================================================
        # DADOS CLIMÁTICOS
        # =====================================================

        temperatura = dados["current"]["temp_c"]
        umidade = dados["current"]["humidity"]
        vento = dados["current"]["wind_kph"]
        clima = dados["current"]["condition"]["text"]

        # =====================================================
        # ATUALIZA INTERFACE
        # =====================================================

        temperatura_label.config(
            text=f"{temperatura} °C"
        )

        umidade_label.config(
            text=f"{umidade}%"
        )

        vento_label.config(
            text=f"{vento} km/h"
        )

        clima_label.config(
            text=clima.upper()
        )

        # =====================================================
        # ALERTAS
        # =====================================================

        alerta = analisar_risco(
            temperatura,
            umidade,
            clima
        )

        if "⚠" in alerta:

            alerta_label.config(
                text=alerta,
                fg=ALERT_COLOR
            )

        else:

            alerta_label.config(
                text=alerta,
                fg=GREEN_COLOR
            )

        # =====================================================
        # STATUS
        # =====================================================

        status.config(
            text="SATÉLITES ONLINE | DADOS RECEBIDOS"
        )

        salvar_log(
            f"Monitoramento realizado em {cidade}"
        )

    except Exception as erro:

        messagebox.showerror(
            "ERRO",
            f"Erro no sistema:\n{erro}"
        )

        salvar_log(
            f"Erro no sistema: {erro}"
        )

# =========================================================
# JANELA PRINCIPAL
# =========================================================

root = tk.Tk()

root.title("OrbitEye")
root.geometry("950x700")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# =========================================================
# BARRA SUPERIOR
# =========================================================

barra_topo = tk.Frame(
    root,
    bg="#020617",
    height=25
)

barra_topo.pack(fill="x")

barra_texto = tk.Label(
    barra_topo,
    text="Satélite Fiap",
    bg="#020617",
    fg="#00FFAA",
    font=("Consolas", 9)
)

barra_texto.pack(
    side="left",
    padx=10
)

# =========================================================
# TÍTULO
# =========================================================

titulo = tk.Label(
    root,
    text="ORBITEYE",
    font=FONT_TITLE,
    bg=BG_COLOR,
    fg=NEON_BLUE
)

titulo.pack(pady=10)

subtitulo = tk.Label(
    root,
    text="CENTRAL ESPACIAL DE MONITORAMENTO CLIMÁTICO",
    font=("Consolas", 11),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

subtitulo.pack()

# =========================================================
# RELÓGIO
# =========================================================

relogio_label = tk.Label(
    root,
    text="UTC SPACE TIME",
    font=("Consolas", 11, "bold"),
    bg=BG_COLOR,
    fg="#00FFAA"
)

relogio_label.pack(pady=5)

# =========================================================
# FRAME SUPERIOR
# =========================================================

top_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

top_frame.pack(pady=20)

cidade_entry = tk.Entry(
    top_frame,
    font=("Consolas", 14),
    width=30,
    bg=PANEL_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat"
)

cidade_entry.grid(
    row=0,
    column=0,
    padx=10
)

monitorar_btn = tk.Button(
    top_frame,
    text="MONITORAR",
    font=("Consolas", 12, "bold"),
    bg=NEON_BLUE,
    fg="black",
    activebackground="#00FFAA",
    activeforeground="black",
    relief="flat",
    padx=25,
    pady=5,
    cursor="hand2",
    command=monitorar_cidade
)

monitorar_btn.grid(
    row=0,
    column=1
)

# =========================================================
# PAINEL DE DADOS
# =========================================================

dados_frame = tk.Frame(
    root,
    bg=PANEL_COLOR,
    width=820,
    height=260
)

dados_frame.pack(pady=10)
dados_frame.pack_propagate(False)

# =========================================================
# TEMPERATURA
# =========================================================

temp_title = tk.Label(
    dados_frame,
    text="TEMPERATURA",
    font=FONT_TEXT,
    bg=PANEL_COLOR,
    fg=NEON_BLUE
)

temp_title.place(x=50, y=30)

temperatura_label = tk.Label(
    dados_frame,
    text="-- °C",
    font=("Consolas", 22, "bold"),
    bg=PANEL_COLOR,
    fg=TEXT_COLOR
)

temperatura_label.place(x=50, y=70)

# =========================================================
# UMIDADE
# =========================================================

umidade_title = tk.Label(
    dados_frame,
    text="UMIDADE",
    font=FONT_TEXT,
    bg=PANEL_COLOR,
    fg=NEON_BLUE
)

umidade_title.place(x=300, y=30)

umidade_label = tk.Label(
    dados_frame,
    text="-- %",
    font=("Consolas", 22, "bold"),
    bg=PANEL_COLOR,
    fg=TEXT_COLOR
)

umidade_label.place(x=300, y=70)

# =========================================================
# VENTO
# =========================================================

vento_title = tk.Label(
    dados_frame,
    text="VENTO",
    font=FONT_TEXT,
    bg=PANEL_COLOR,
    fg=NEON_BLUE
)

vento_title.place(x=550, y=30)

vento_label = tk.Label(
    dados_frame,
    text="-- km/h",
    font=("Consolas", 22, "bold"),
    bg=PANEL_COLOR,
    fg=TEXT_COLOR
)

vento_label.place(x=550, y=70)

# =========================================================
# CLIMA
# =========================================================

clima_title = tk.Label(
    dados_frame,
    text="CLIMA",
    font=FONT_TEXT,
    bg=PANEL_COLOR,
    fg=NEON_BLUE
)

clima_title.place(x=50, y=160)

clima_label = tk.Label(
    dados_frame,
    text="---",
    font=("Consolas", 18, "bold"),
    bg=PANEL_COLOR,
    fg=TEXT_COLOR
)

clima_label.place(x=50, y=195)

# =========================================================
# ALERTAS
# =========================================================

alerta_title = tk.Label(
    dados_frame,
    text="STATUS DO SISTEMA",
    font=FONT_TEXT,
    bg=PANEL_COLOR,
    fg=NEON_BLUE
)

alerta_title.place(x=400, y=160)

alerta_label = tk.Label(
    dados_frame,
    text="✓ SEM ALERTAS",
    font=("Consolas", 18, "bold"),
    bg=PANEL_COLOR,
    fg=GREEN_COLOR
)

alerta_label.place(x=400, y=195)

# =========================================================
# LOGS
# =========================================================

logs_title = tk.Label(
    root,
    text="LOGS DO SISTEMA",
    font=FONT_TEXT,
    bg=BG_COLOR,
    fg=NEON_BLUE
)

logs_title.pack(pady=5)

logs_text = tk.Text(
    root,
    width=110,
    height=10,
    bg="#020617",
    fg=GREEN_COLOR,
    font=FONT_SMALL,
    relief="flat"
)

logs_text.pack(pady=10)

# =========================================================
# STATUS BAR
# =========================================================

status = tk.Label(
    root,
    text="SATÉLITES ONLINE | ORBITEYE v2.0",
    bg=BG_COLOR,
    fg=NEON_BLUE,
    font=("Consolas", 10)
)

status.pack(
    side="bottom",
    pady=10
)

# =========================================================
# INICIAR SISTEMA
# =========================================================

salvar_log("Sistema OrbitEye iniciado")

atualizar_relogio()
animar_status()

root.mainloop()

