Questo progetto è una versione del Task Manager di Windows scritta interamente in Python. Il programma ha problemi di prestazioni ed è leggermente buggato, ma funziona.

Include inoltre la chicca che mi contraddistingue (dato che sono un hacker - lo so è cringissimo dirlo così), ossia chiamo una funzione che verifica se la security policy di Powershell è sconfigurata.

Abilità di visualizzare dati sullo stato dell'HD, informazioni su scheda di rete, processi e servizi, utilizzo memoria e CPU. Possibilità di terminare un processo tramite PID dall'opzione "Termina Processo Specifico" nel menù a tendina.

L'.exe è stato compilato con Python 3.12 e Pyinstaller 6.1.0 (pyinstaller --onefile --uac-admin taskmanager.py)
Dato che è un Task Manager, dovrai eseguirlo con i privilegi dell'amministratore, o non funzionerà correttamente.

![tmanager](https://github.com/Admin9961/PyManager/assets/121270287/dd364cc6-3cbd-431f-af09-6cca91c5b0fd)
