# Leolository
Repository per gli esercizi del Prof. Guarrasi

Progetto Taxi
Il programma riceve una lista di mesi e analizza i dataset in formato csv a essi riferiti, contenuti nella cartella Data.Viene anche importato un dataset contenente le informazioni 
per il riconoscimento degli ID delle zone, che verranno aggiunte tramite merge al dataframe contenente le informazioni sui viaggi. 
Prima della fase iniziale di pulizia dati il codice crea delle directories nella cartella Results, al fine di rendere l'organizzazione degli output ordinata. Viene creato un
folder per ogni mese qualora non fosse già stato creato. 
In uscita vengono prodotti dei grafici che aiutano l'utente a visualizzare graficamente le informazioni estratte dai dataset: in ogni cartella mensile, viene creato un grafico per 
ogni zona che riporta i viaggi per ciascun giorno del mese; viene anche creato un file, denominato 'Gerarchia', che riporta l'ordine di importanza (in termini di numero di viaggi 
totali per mese) dei Boroughs di New York. Nella cartella Results vengono salvati anche i grafici che riportano l'andamento dei viaggi da Gennaio a fine Giugno.
L'analisi è impostata su parametri di default (mesi da Gennaio a Giugno, anno 2020, path del dataset delle zone, path di output dei dati) cambiabili dall'utente.
