# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 10:32:53 2020

@author: Leonardo Furia - Lorenzo Marcoccia 
"""


"""In quale periodo dell'anno i taxi vengono utilizzati di più? Creare un grafico che, per ogni mese, indichi il numero 
medio di viaggi registrati ogni giorno. A causa delle differenze tra le zone di New York, vogliamo visualizzare le stesse
informazioni per ogni borough. Notate qualche differenza tra di loro? Qual è il mese con la media giornaliera più alta? E 
invece quello con la media giornaliera più bassa?"""


import pandas as pd
import matplotlib.pyplot as plt 
import time 
import collections
import argparse
from abc import ABC, abstractmethod
import calendar
import os
from multiprocessing import Process
import glob    


   

class Extractor(ABC):
    '''
    interface class
    '''
    @abstractmethod
    def conta_corse_per_giorno(self):
        pass
    
    @abstractmethod
    def crea_grafici_mese(self):
        pass
    
    @abstractmethod
    def data_cleaner(self):
        pass
    

    

class ExtractInfo(Extractor):
    '''la classe contiene i metodi che svolgono le operazioni proncipali sul dataset'''
    
    def __init__(self):
        pass
    
    
    def conta_corse_per_giorno(self, df, mese, args):
        
        '''Metodo che estrapola le informazioni dal dataset: viene calcolato il numero di viaggi giornaliero per
           ogni zona e mese, che verrà utilizzato per i grafici. Dato che questa funzione viene chiamata in processi 
           contemporanei, le informazioni per la creazione dell'andamento vengono salvate in file .csv e poste in una
           cartella apposita.'''
        
        dati_mese_zona=pd.DataFrame()
        for zona in df['Borough'].unique():
            df_temp = df[df['Borough'] == zona]
            dati_mese_zona[zona] = pd.Series(collections.Counter(df_temp['tpep_dropoff_datetime']))    
         
        andamento = pd.Series(collections.Counter(df['tpep_dropoff_datetime']))
        path = args.storage + f'/Andamento_{mese}-{args.anno}.csv'
        andamento.to_csv(path)
        
        return dati_mese_zona
    
    
    
    
    def crea_grafici_mese(self, df, dati_mese_zona, mese, i, args):
        
        '''Il metodo crea dei barplot per ogni zona della città: sull'ascissa sono posti i giorni del mese,
           sull'ordinata il numero di corse giornaliero. Inoltre, i plot 'gerarchici' mostrano l'importanza, in termini
           di corse, di ciascuna zona nel mese considerato. I grafici vengono salvati nella cartella specifica del mese
           nella directory designata come output.'''
        
        dati_mese_zona = dati_mese_zona.sort_index()
        
        for zona in df['Borough'].unique():
            plt.figure()
            dati_mese_zona[zona].plot.bar()
            plt.title(zona)
            plt.savefig(args.radice + f"/{args.anno}-{mese}/{zona}.pdf", dpi=300)
            plt.close()
    
        gerarchia = pd.Series(collections.Counter(df['Borough']))
        plt.figure()
        gerarchia.plot.bar()
        plt.title(mese)
        plt.savefig(args.radice + f"/{args.anno}-{mese}/Gerarchia.pdf", dpi = 300)
        plt.close()

    
    
        
    def data_cleaner(self, df, i):
        
        '''Il metodo pulisce e rende utilizzabile i dataset importati. Vengono scartate le righe con valori NaN e
           selezionate le informazioni richieste. Inoltre, il dtype delle colonne contenenti date viene settato a 
           date.'''
        
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

        df = df.dropna(axis = 0, how = 'any')
    
        df = df.loc[(df['tpep_dropoff_datetime'].dt.year == args.anno) & (df['tpep_dropoff_datetime'].dt.month  == int(i))]

        df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].dt.date
        
        return df




def principale(zone, i, args):
    
    '''La function è il corpo principale del programma ed è necessaria parallelizzazione dei processi: chiama tutti i sottoprogrammi ed i metodi necessari al corretto 
       svolgimento del singolo processo. La function verrà eseguita tante volte quanti sono i processi. Il numero di processi dipende dal numero di mesi che sui quali 
       si vuole effettuare l'analisi. Di default il programma effettua l'analisi su 6 mesi (da gennaio 2020 a giugno 2020)  '''
     
    df = pd.read_csv(args.dati + f'/yellow_tripdata_{args.anno}-0{i}.csv', usecols = ['tpep_dropoff_datetime', 'DOLocationID'])
     
    extractor=ExtractInfo()
    df=extractor.data_cleaner(df, i)
    
    mese = calendar.month_name[int(i)]
       
    df = pd.merge(df, zone, on=['DOLocationID'],how='left')
       
    #estrae il numero di corse per giorno nel mese dell'iterazione corrente
    dati_mese_zona=extractor.conta_corse_per_giorno(df, mese, args)
    
    #salva nella cartella Results i grafici relativi al numero di corse giornaliere per ogni mese
    extractor.crea_grafici_mese(df, dati_mese_zona, mese, i, args)

         


def crea_directories(args):
    
    '''La function crea le directories necessarie per il funzionamento del programma.'''
        
    #creo le cartelle per archiviare i file d'output se non esistono
    for i in args.mesi:
        mese = calendar.month_name[int(i)]
        path = args.radice + f'/{args.anno}-{mese}/'
        if not os.path.exists(path): 
            os.makedirs(path)   
    
    if not os.path.exists(args.storage): 
         os.makedirs(args.storage)




def crea_andamento(andamento, args):
           
    '''La function crea il grafico dell'andamento del numero delle corse, utilizzando la variabile ottenuta dalla
       fusione dei dataset mensili temporanei creati durante i processi.'''
    
    plt.figure()
    andamento.plot(x = 'giorni', y = 'numero_viaggi')
    plt.title('Andamento dei Viaggi')
    plt.savefig(args.radice + f"/Andamento_lineplot_{args.anno}.pdf", dpi = 300)
    plt.close() 
    
    
    
 
def riordina_e_grafica(args):
    
    '''La function trova nella cartella Storage tutti i file creati durante i processi e li fonde nella variabile
       unica 'andamento', che poi viene ordinata e passata alla funzione crea_andamento.'''
    
    files = glob.glob(os.path.join(args.storage, "Andamento_*.csv"))
    df_per_file = (pd.read_csv(f, sep=',') for f in files)
    andamento = pd.concat(df_per_file, ignore_index=True)
    
    andamento = andamento.rename({'Unnamed: 0' : 'giorni', '0': 'numero_viaggi'}, axis = 1)
    andamento['giorni'] = pd.to_datetime(andamento['giorni'])
    andamento['giorni'] = andamento['giorni'].dt.date
    andamento = andamento.sort_values(by=['giorni'])
    
    crea_andamento(andamento, args)



       
#============================================__main__==============================================#

#avvio contatore
start = time.perf_counter()


parser = argparse.ArgumentParser()

    
parser.add_argument("-i1", "--mesi", help = "Mesi da analizzare",
                 type = list, default = '123456')

parser.add_argument("-i2", "--zone", help = "Path del dataset delle zone",
                 type = str, default = './Data/taxi+_zone_lookup.csv')

parser.add_argument("-i3", "--anno", help = "Anno da analizzare",
                 type = int, default = 2020)

parser.add_argument("-i4", "--dati", help = "Cartella di posizionamento dei dataset iniziali",
                 type = str, default = './Data')

parser.add_argument("-o1", "--storage", help = "Cartella di posizionamento dei file csv temporanei",
                 type = str, default = './Storage')

parser.add_argument("-o2", "--radice", help = "Cartella principale dei file di output",
                 type = str, default = './Results')


args = parser.parse_args()

        
if __name__ == '__main__':
    
    
    zone = pd.read_csv(args.zone)
    zone = zone.rename({'LocationID': 'DOLocationID'}, axis = 1)


    crea_directories(args)
    
    
    #definizione dei processi paralleli
    thrs = [Process(target=principale,args=(zone, i, args)) for i in args.mesi]
    for t in thrs:
        t.start()
        # aspetta che termini
    for t in thrs:
        t.join()


    riordina_e_grafica(args)


elapsed = time.perf_counter() - start

#==========================================================================================#