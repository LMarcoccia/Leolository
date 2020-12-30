# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 10:32:53 2020

@author: lollo
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
    
    
    def __init__(self):
        pass
    
    
    def conta_corse_per_giorno(self, df, mese, args):
        
        dati_mese_zona=pd.DataFrame()
        for zona in df['Borough'].unique():
            df_temp = df[df['Borough'] == zona]
            dati_mese_zona[zona] = pd.Series(collections.Counter(df_temp['tpep_dropoff_datetime']))    
         
        andamento = pd.Series(collections.Counter(df['tpep_dropoff_datetime']))
        path = args.storage + f'Andamento_{mese}.csv'
        andamento.to_csv(path)
        
        return dati_mese_zona
    
    
    
    
    def crea_grafici_mese(self, df, dati_mese_zona, mese, i):
        
        dati_mese_zona = dati_mese_zona.sort_index()
        
        for zona in df['Borough'].unique():
            plt.figure()
            dati_mese_zona[zona].plot.bar()
            plt.title(zona)
            plt.savefig(f"./Results/2020-{mese}/{zona}.pdf", dpi=300)
            plt.close()
    
        gerarchia = pd.Series(collections.Counter(df['Borough']))
        plt.figure()
        gerarchia.plot.bar()
        plt.title(mese)
        plt.savefig(f"./Results/2020-{mese}/Gerarchia.pdf", dpi = 300)
        plt.close()

    
    
        
    def data_cleaner(self, df, i):
        
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

        df = df.dropna(axis = 0, how = 'any')
    
        df = df.loc[(df['tpep_dropoff_datetime'].dt.year == args.anno) & (df['tpep_dropoff_datetime'].dt.month  == int(i))]

        df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].dt.date
        
        return df




def principale(zone, i):
     
     df = pd.read_csv(f'./Data/yellow_tripdata_2020-0{i}.csv',usecols = ['tpep_dropoff_datetime', 'DOLocationID'])
        
     extractor=ExtractInfo()
     df=extractor.data_cleaner(df,i)
     
     mese = calendar.month_name[int(i)]
        
     df = pd.merge(df, zone, on=['DOLocationID'],how='left')
        
     #estrae il numero di corse per giorno nel mese dell'iterazione corrente
     dati_mese_zona=extractor.conta_corse_per_giorno(df, mese, args)
     
     #salva nella cartella Results i grafici relativi al numero di corse giornaliere per ogni mese
     extractor.crea_grafici_mese(df, dati_mese_zona, mese, i)

         


def crea_directories(args):
        
        #creo le cartelle per archiviare i file d'output se non esistono
        for i in args.mesi:
            mese = calendar.month_name[int(i)]
            path = args.radice + f'2020-{mese}/'
            if not os.path.exists(path): 
                os.makedirs(path)   
        
        if not os.path.exists(args.storage): 
             os.makedirs(args.storage)




def crea_andamento(andamento):
           
    plt.figure()
    andamento.plot(x = 'giorni', y = 'numero_viaggi')
    plt.title('Andamento dei Viaggi')
    plt.savefig("./Results/Andamento_lineplot.pdf", dpi = 300)
    plt.close() 
    
    
    
 
def riordina_e_grafica(args):
    
    files = glob.glob(os.path.join(args.storage, "Andamento_*.csv"))
    df_per_file = (pd.read_csv(f, sep=',') for f in files)
    andamento = pd.concat(df_per_file, ignore_index=True)
    
    andamento = andamento.rename({'Unnamed: 0' : 'giorni', '0': 'numero_viaggi'}, axis = 1)
    andamento['giorni'] = pd.to_datetime(andamento['giorni'])
    andamento['giorni'] = andamento['giorni'].dt.date
    andamento = andamento.sort_values(by=['giorni'])
    
    crea_andamento(andamento)



       
#============================================__main__==============================================#

start = time.perf_counter()


parser = argparse.ArgumentParser()

    
parser.add_argument("-i1", "--mesi", help = "Mesi da analizzare",
                 type = list, default = ['1', '2', '3', '4', '5', '6'])

parser.add_argument("-i2", "--zone", help = "Path del dataset delle zone",
                 type = str, default = './Data/taxi+_zone_lookup.csv')

parser.add_argument("-i3", "--anno", help = "Anno da analizzare",
                 type = int, default = 2020)

parser.add_argument("-o1", "--storage", help = "Cartella di posizionamento dei file csv temporanei",
                 type = str, default = './Storage/')

parser.add_argument("-o2", "--radice", help = "Cartella principale dei file di output",
                 type = str, default = './Results/')


args = parser.parse_args()

        
if __name__ == '__main__':
    
    
    zone = pd.read_csv(args.zone)
    zone = zone.rename({'LocationID': 'DOLocationID'}, axis = 1)


    crea_directories(args)
    
    
    thrs = [Process(target=principale,args=(zone,i+1)) for i in range(len(args.mesi))]
    for t in thrs:
        t.start()
        # aspetta che terminin
    for t, i in zip(thrs, range(len(args.mesi))):
        t.join()


    riordina_e_grafica(args)


elapsed = time.perf_counter() - start

#==========================================================================================#