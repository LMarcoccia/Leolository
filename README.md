# Leolository
Repository per gli esercizi del Prof. Guarrasi

Progetto Taxi
Il programma riceve una lista di mesi e analizza i dataset in formato csv a essi riferiti, contenuti nella cartella Data. Ad esempio l'utente può inserire in input la seguente lista ['1','2','3','4'] ed il programma importa i dataset associati ad i mesi specificati nella lista effettuando le analisi nel periodo che va da Gennaio ad Aprile.
Viene inoltre importato un dataset contenente le informazioni per il riconoscimento degli ID delle zone, che verranno aggiunte tramite merge al dataframe contenente le informazioni sui viaggi. 
L'utente può infine specificare in input le seguenti informazioni:
-anno sul quale si vuole effettuare l'analisi
-path del dataset delle zone
-path della cartella contenente i dataset relativi alle corse dei taxi
-path di output dei dati

Prima della fase iniziale di pulizia dati il codice crea delle directories nella cartella Results, al fine di rendere l'organizzazione degli output ordinata. Viene creato unfolder per ogni mese qualora non fosse già stato creato. 
Viene creata anche una cartella per il posizionamento dei dataset intermedi (creati in ogni processo), chiamata Storage. Questi dataset contengono le informazioni sui viaggi giornalieri per ciascun mese.

In uscita vengono prodotti dei grafici che aiutano l'utente a visualizzare graficamente le informazioni estratte dai dataset: 
- in ogni cartella mensile, viene creato un grafico per ogni zona che riporta i viaggi per ciascun giorno del mese; 
- viene creato un file, denominato 'Gerarchia', che riporta l'ordine di importanza (in termini di numero di viaggi totali per mese) dei Boroughs di New York.
- Nella cartella Results vengono salvati anche i grafici che riportano l'andamento dei viaggi nell'intervallo di tempo considerato (di default da Gennaio a fine Giugno).
- Nella cartella Storage, vengono salvati i dataset intermedi: questi file vengono utilizzati per creare l'andamento delle corse dei taxi nel periodo specificato dall'utente. 


L'ANALISI VIENE IMPOSTATA SUI SEGUENTI PARAMETRI DI DEFAULT:

-mesi da Gennaio a Giugno (['1','2','3','4','5','6'])

-anno 2020

-path del dataset di test relativo alle corse dei taxi: ./Data_test

-path del dataset delle zone: './Data_test/taxi+_zone_lookup.csv'

-path di output dei dati: cartella ./Results 

-path di output della cartella di posizionamento dei dataset intermedi: ./Storage


MODULI UTILIZZATI:

-pandas as pd: pulizia dati, creazione dataframe, creazione grafici, import/export from/to csv

-matplotlib.pyplot as plt: creazione grafici 

-time: misurazione tempo di esecuzione 

-collections: conteggio dei viaggi giornalieri

-argparse: definizione dei parametri di default

-from abc imported ABC, abstractmethod: creazione metodi astratti e classe interfaccia

-calendar: estrazione nome del mese a partire dal numero

-os: creazione cartelle

-from multiprocessing imported Process: gestione della parallelizzazione

-glob: ricerca dei files in formato csv che iniziano con gli stessi caratteri    
