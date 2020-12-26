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
    
    @abstractmethod
    def crea_andamento(self):
        pass
    
    @abstractmethod
    def crea_directories(self): 
        pass

    

class ExtractInfo(Extractor):
    
    
    def __init__(self):
        pass
    
    
    def crea_directories(self, args):
        
        #creo le cartelle per archiviare i file d'output se non esistono
        for i in args.mesi:
            mese = calendar.month_name[int(i)]
            path = args.radice + f'2020-{mese}/'
            if not os.path.exists(path): 
                os.makedirs(path)   


    
    
    def conta_corse_per_giorno(self, df, andamento, paragone_mesi):
        
        dati_mese_zona=pd.DataFrame()
        for zona in df['Borough'].unique():
            df_temp = df[df['Borough'] == zona]
            dati_mese_zona[zona] = pd.Series(collections.Counter(df_temp['tpep_dropoff_datetime']))    
        
        andamento = pd.concat([andamento,pd.Series(collections.Counter(df['tpep_dropoff_datetime']))])
        
        paragone_mesi[mese] = pd.Series(len(df))
            
        return dati_mese_zona, andamento, paragone_mesi
    
    
    
    
    def crea_grafici_mese(self, df, dati_mese_zona, mese):
        
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


    
    
    def crea_andamento(self, paragone_mesi, andamento):
        
         plt.figure()
         paragone_mesi.plot.bar()
         plt.title('Andamento dei Viaggi')
         plt.xlabel('Mesi')
         plt.savefig("./Results/Andamento_barplot.pdf", dpi = 300)
         plt.close()
   
         plt.figure()
         andamento.plot(x = 'Index', y = '0')
         plt.title('Andamento dei Viaggi')
         plt.savefig("./Results/Andamento_lineplot.pdf", dpi = 300)
         plt.close() 
    
    
    
    
    def data_cleaner(self, df):
        
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

        df = df.dropna(axis = 0, how = 'any')
    
        df = df.loc[(df['tpep_dropoff_datetime'].dt.year == args.anno) & (df['tpep_dropoff_datetime'].dt.month  == int(i))]

        df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].dt.date
        
        return df




#============================================__main__==============================================#

start = time.perf_counter()


parser = argparse.ArgumentParser()

parser.add_argument("-i1", "--mesi", help = "Mesi da analizzare",
                     type = list, default = ['1', '2', '3', '4', '5', '6'])

parser.add_argument("-i2", "--zone", help = "Path del file dataset",
                     type = str, default = './Data/taxi+_zone_lookup.csv')

parser.add_argument("-i3", "--anno", help = "Anno da analizzare",
                     type = int, default = 2020)

parser.add_argument("-i4", "--cores", help = "Core da utilizzare",
                     type = int, default = os.cpu_count())

parser.add_argument("-o1", "--radice", help = "Cartella principale dei file di output",
                     type = str, default = './Results/')

args = parser.parse_args()

        
zone = pd.read_csv(args.zone)
zone = zone.rename({'LocationID': 'DOLocationID'}, axis = 1)


paragone_mesi = pd.DataFrame()
andamento = pd.Series(dtype = object)


extractor = ExtractInfo()
extractor.crea_directories(args)


for i in args.mesi: 
    #preparazione dati
    df = pd.read_csv(f'./Data/yellow_tripdata_2020-0{i}.csv',usecols = ['tpep_dropoff_datetime', 'DOLocationID'])
    
    mese = calendar.month_name[int(i)]
      
    df = extractor.data_cleaner(df)
    
    df = pd.merge(df, zone, on=['DOLocationID'], how = 'left')
    
    #estrae il numero di corse per giorno nel mese dell'iterazione corrente
    dati_mese_zona, andamento, paragone_mesi = extractor.conta_corse_per_giorno(df, andamento, paragone_mesi)
    
    #salva nella cartella Results i grafici relativi al numero di corse giornaliere per ogni mese
    extractor.crea_grafici_mese(df, dati_mese_zona, mese)
 

extractor.crea_andamento(paragone_mesi, andamento)


elapsed = time.perf_counter() - start

#==========================================================================================#