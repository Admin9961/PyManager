import psutil
import threading
import tkinter as tk
import tkinter
from tkinter import ttk
from ttkthemes import ThemedStyle
import platform
import subprocess
import locale
import os
import wmi

def monitorare_prestazioni():
    percentuale_cpu = psutil.cpu_percent(interval=1)
    informazioni_memoria = psutil.virtual_memory()
    utilizzo_disco = psutil.disk_usage('/')

    etichetta_cpu.config(text=f'Utilizzo CPU: {percentuale_cpu}%', foreground='blue')
    etichetta_memoria.config(text=f'Utilizzo Memoria: {informazioni_memoria.percent}%', foreground='green')
    etichetta_disco.config(text=f'Utilizzo Disco: {utilizzo_disco.percent}%', foreground='red')

    root.after(1000, monitorare_prestazioni)

def avviare_thread_monitoraggio():
    thread = threading.Thread(target=monitorare_prestazioni)
    thread.daemon = True
    thread.start()

def monitorare_processi():
    processi = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'username', 'create_time'])

    for child in albero_processi.get_children():
        albero_processi.delete(child)

    for processo in processi:
        informazioni_processo = processo.info
        albero_processi.insert("", "end", values=(
            informazioni_processo['pid'],
            informazioni_processo['name'],
            f"{informazioni_processo['cpu_percent']:.2f}%",
            f"{informazioni_processo['memory_percent']:.2f}%",
            informazioni_processo['status'],
            informazioni_processo['username'],
            informazioni_processo['create_time'],
            informazioni_processo['pid'],
            informazioni_processo.get('exe', 'N/A'),
        ))

    albero_processi.bind("<Button-3>", termina_processo)
    root.after(2000, monitorare_processi)

def termina_processo_specifica(entry_pid):
    pid = entry_pid.get()
    if pid:
        try:
            processo = psutil.Process(int(pid))
            processo.terminate()
            monitorare_processi()
        except Exception as e:
            tkinter.messagebox.showerror("Errore", f'Errore durante la terminazione del processo: {e}')
    else:
        tkinter.messagebox.showerror("Attenzione", "Inserisci un PID valido!")

def mostra_interfaccia_terminazione():
    finestra_terminazione = tk.Toplevel(root)
    finestra_terminazione.title('Termina Processo Specifico')
    finestra_terminazione.geometry('300x100')

    label_pid = ttk.Label(finestra_terminazione, text='Inserisci il PID del processo da terminare:')
    label_pid.pack(pady=5)

    entry_pid = ttk.Entry(finestra_terminazione)
    entry_pid.pack(pady=5)

    button_termina = ttk.Button(finestra_terminazione, text='Termina', command=lambda: termina_processo_specifica(entry_pid))
    button_termina.pack(pady=10)

def avviare_thread_monitoraggio_processi():
    thread = threading.Thread(target=monitorare_processi)
    thread.daemon = True
    thread.start()

def monitorare_disco():
    informazioni_disco = psutil.disk_usage('/')
    testo = f'Utilizzo Disco: {informazioni_disco.percent}% - Spazio Totale: {informazioni_disco.total / (1024**3):.2f} GB - Spazio Disponibile: {informazioni_disco.free / (1024**3):.2f} GB'
    colore = 'green' if informazioni_disco.percent < 50 else ('orange' if informazioni_disco.percent < 80 else 'red')
    etichetta_disco.config(text=testo, foreground=colore)
    root.after(5000, monitorare_disco)

def mostra_stato_network():
    stato_network = psutil.net_if_stats()
    indirizzi_ip = psutil.net_if_addrs()

    finestra_stato_network = tk.Toplevel(root)
    finestra_stato_network.title('Stato del Network')
    finestra_stato_network.geometry('800x600')

    canvas = tk.Canvas(finestra_stato_network)
    canvas.pack(side="left", fill="both", expand=True)

    frame = ttk.Frame(canvas)
    scrollbar = ttk.Scrollbar(finestra_stato_network, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    for interfaccia, stato in stato_network.items():
        indirizzo_ip = ', '.join([addr.address for addr in indirizzi_ip.get(interfaccia, [])])
        gateway = stato.gateway if hasattr(stato, 'gateway') else 'N/A'

        colore = 'green' if stato[0] == psutil.CONN_ESTABLISHED else 'red'
        label = ttk.Label(frame, text=f'Interfaccia: {interfaccia}, Stato: {stato[0]}, Velocità: {stato[1]} Mbps, IP: {indirizzo_ip}, Gateway: {gateway}', foreground=colore)
        label.pack()

def mostra_stato_hard_disk():
    informazioni_hard_disk = psutil.disk_io_counters(perdisk=True)
    finestra_stato_hard_disk = tk.Toplevel(root)
    finestra_stato_hard_disk.title('Stato dell\'Hard Disk')
    finestra_stato_hard_disk.geometry('800x600')

    canvas = tk.Canvas(finestra_stato_hard_disk)
    canvas.pack(side="left", fill="both", expand=True)

    frame = ttk.Frame(canvas)
    scrollbar = ttk.Scrollbar(finestra_stato_hard_disk, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    for disco, informazioni in informazioni_hard_disk.items():
        label = ttk.Label(frame, text=f'Disco: {disco}, Operazioni di lettura (TOTALI): {informazioni.read_count}, Operazioni di scrittura (TOTALI): {informazioni.write_count}')
        label.pack()

def mostra_applicazioni_installate():
    finestra_applicazioni = tk.Toplevel(root)
    finestra_applicazioni.title('Applicazioni Installate')
    finestra_applicazioni.geometry('800x600')

    canvas = tk.Canvas(finestra_applicazioni)
    canvas.pack(side="left", fill="both", expand=True)

    frame = ttk.Frame(canvas)
    scrollbar = ttk.Scrollbar(finestra_applicazioni, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    elenco_applicazioni = []

    if platform.system() == 'Windows':
        elenco_applicazioni = [app for app in os.listdir(os.environ['ProgramFiles']) if os.path.isdir(os.path.join(os.environ['ProgramFiles'], app))]

    for app in elenco_applicazioni:
        label = ttk.Label(frame, text=app)
        label.pack()

def mostra_servizi_di_sistema():
    finestra_servizi = tk.Toplevel(root)
    finestra_servizi.title('Servizi di Sistema Attivi')
    finestra_servizi.geometry('800x600')

    canvas = tk.Canvas(finestra_servizi)
    canvas.pack(side="left", fill="both", expand=True)

    frame = ttk.Frame(canvas)
    scrollbar = ttk.Scrollbar(finestra_servizi, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    try:
        c = wmi.WMI()
        servizi = c.Win32_Service()

        for servizio in servizi:
            label = ttk.Label(frame, text=f"{servizio.DisplayName} - {servizio.State}")
            label.pack()

    except Exception as e:
        label_errore = ttk.Label(frame, text=f'Errore nel recuperare i servizi: {e}')
        label_errore.pack()

def selezione_menu(event):
    opzione_selezionata = opzioni_menu.get()
    if opzione_selezionata == "Networking Status":
        mostra_stato_network()
    elif opzione_selezionata == "Monitor Disk":
        mostra_stato_hard_disk()
    elif opzione_selezionata == "Applicazioni Installate":
        mostra_applicazioni_installate()
    elif opzione_selezionata == "Servizi di Sistema":
        mostra_servizi_di_sistema()
    elif opzione_selezionata == "Termina Processo Specifico":
        mostra_interfaccia_terminazione()

def rilevare_specifiche_os():
    specifiche_os = platform.platform()
    
    try:
        lingua_predefinita = locale.getdefaultlocale()[0]
        specifiche_os += f'\nLingua predefinita: {lingua_predefinita}'
    except Exception as e:
        print(f'Errore nel rilevare lingua: {e}')

    try:
        versione_powershell = subprocess.run(["powershell", "$PSVersionTable.PSVersion"], capture_output=True, text=True)
        specifiche_os += f'\nVersione di PowerShell: {versione_powershell.stdout.strip()}'
    except Exception as e:
        print(f'Errore nel rilevare la versione di PowerShell: {e}')
    
    try:
        sicurezza_powershell = subprocess.run(["powershell", "Get-ExecutionPolicy"], capture_output=True, text=True)
        
        if "RemoteSigned" in sicurezza_powershell.stdout:
            specifiche_os += '\nPowershell: enforced security policy'
        else:
            specifiche_os += f'\nPowershell: at risk\nDettagli vulnerabilità: {sicurezza_powershell.stdout.strip()}'
    except Exception as e:
        print(f'Errore nel rilevare la sicurezza di PowerShell: {e}')
    
    label_specifiche_os.config(text=f'Sistema Operativo: {specifiche_os}')

def avviare_thread_monitoraggio_os():
    thread_os = threading.Thread(target=rilevare_specifiche_os)
    thread_os.daemon = True
    thread_os.start()

def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

root = tk.Tk()
root.title('Monitor Prestazioni')
root.geometry('800x600')

style = ThemedStyle(root)
style.set_theme("equilux")

etichetta_cpu = ttk.Label(root, text='Utilizzo CPU: ', font=('Arial', 12, 'bold'))
etichetta_cpu.pack()

etichetta_memoria = ttk.Label(root, text='Utilizzo Memoria: ', font=('Arial', 12, 'bold'))
etichetta_memoria.pack()

etichetta_disco = ttk.Label(root, text='Utilizzo Disco: ', font=('Arial', 12, 'bold'))
etichetta_disco.pack()

albero_processi = ttk.Treeview(root, columns=('PID', 'Nome', 'CPU %', 'Memoria %', 'Stato', 'Utente', 'Tempo Creazione', 'PID', 'Esecutabile'), show='headings', style='mystyle.Treeview')
style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Arial', 10))
albero_processi.heading('PID', text='PID')
albero_processi.heading('Nome', text='Nome')
albero_processi.heading('CPU %', text='CPU %')
albero_processi.heading('Memoria %', text='Memoria %')
albero_processi.heading('Stato', text='Stato')
albero_processi.heading('Utente', text='Utente')
albero_processi.heading('Tempo Creazione', text='Tempo Creazione')
albero_processi.heading('PID', text='PID')
albero_processi.heading('Esecutabile', text='Esecutabile')

scrollbar_y = ttk.Scrollbar(root, orient='vertical', command=albero_processi.yview)
scrollbar_x = ttk.Scrollbar(root, orient='horizontal', command=albero_processi.xview)
albero_processi.configure(yscroll=scrollbar_y.set, xscroll=scrollbar_x.set)

scrollbar_y.pack(side='right', fill='y')
scrollbar_x.pack(side='bottom', fill='x')

albero_processi.pack(expand=True, fill=tk.BOTH)

label_specifiche_os = ttk.Label(root, text='Sistema Operativo: ', font=('Arial', 12, 'italic'))
label_specifiche_os.pack()

opzioni_menu = ttk.Combobox(root, values=["Networking Status", "Monitor Disk", "Applicazioni Installate", "Servizi di Sistema", "Termina Processo Specifico"], font=('Arial', 12))
opzioni_menu.set("Scegli un'opzione")
opzioni_menu.bind("<<ComboboxSelected>>", selezione_menu)
opzioni_menu.pack()

avviare_thread_monitoraggio()
avviare_thread_monitoraggio_processi()
monitorare_disco()
avviare_thread_monitoraggio_os()

root.mainloop()