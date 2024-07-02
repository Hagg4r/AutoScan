Spiegazione del codice aggiuntivo

	1.	Funzione install_tools:
	•	Definisce i comandi di installazione per ffuf, amass, e uniscan usando sudo apt-get install -y.
	•	Controlla se ciascun tool è già installato utilizzando la funzione is_tool_installed.
	•	Se uno strumento non è installato, esegue il comando di installazione corrispondente.
	2.	Funzione is_tool_installed:
	•	Utilizza subprocess.call con il comando which per verificare se uno strumento è installato.

Note Importanti

	•	Privilegi di Amministratore: L’installazione dei pacchetti richiede privilegi di amministratore. Assicurati di eseguire questo script con i privilegi necessari (sudo).
	•	Distribuzione: Questo script utilizza apt-get per l’installazione, quindi è adatto per sistemi basati su Debian (ad esempio Ubuntu). Per altre distribuzioni, i comandi di installazione potrebbero variare.
	•	Prerequisiti: Il sistema deve avere accesso a Internet per scaricare i pacchetti.

Esecuzione del programma

Salva il codice in un file Python, ad esempio scanner.py, e eseguilo da terminale: sudo python AutoScan.py

Questo assicurerà che i tool necessari siano installati prima di eseguire le scansioni e salverà i risultati nel file scan_results.txt.
