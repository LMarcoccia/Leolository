# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 10:32:53 2020

@author: lollo
"""

"""In quale periodo dell'anno i taxi vengono utilizzati di più? Creare un grafico che, per ogni mese, indichi il numero 
medio di viaggi registrati ogni giorno. A causa delle differenze tra le zone di New York, vogliamo visualizzare le stesse
informazioni per ogni borough. Notate qualche differenza tra di loro? Qual è il mese con la media giornaliera più alta? E 
invece quello con la media giornaliera più bassa?"""


#mettere argparse
import pandas as pd
#import memory_usage, time_elapsed, generalmente misuriamo le prestazioni 
import matplotlib.pyplot as plt 
import time 
import collections
from datetime import date,datetime
import argparse
import tqdm
from abc import ABC, abstractmethod

        
   

class Extractor(ABC):
    '''
    interface class
    '''
    @abstractmethod
    def conta_corse_per_giorno(self):
        pass
    
    @abstractmethod
    def crea_grafici(self):
        pass
    
    @abstractmethod
    def data_cleaner(self):
        pass
    

    


class ExtractInfo(Extractor):
    
    def __init__(self):
        pass
    
    def conta_corse_per_giorno(self,df):
        
        dati_mese_zona=pd.DataFrame()
        for zona in df['Borough'].unique():
            df_temp = df[df['Borough'] == zona]
            dati_mese_zona[zona] = pd.Series(collections.Counter(df_temp['tpep_dropoff_datetime']))
            
        return dati_mese_zona
    
    
    def crea_grafici(self,df,dati_mese_zona):
        
        dati_mese_zona = dati_mese_zona.sort_index()
        for zona in df['Borough'].unique():
            plt.figure()
            dati_mese_zona[zona].plot.bar()
            plt.title(zona)
            plt.savefig(f"./Results/2020-0{i}-{zona}.pdf", dpi=300)
            plt.close()
    
    def data_cleaner(self,df):
        
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

args = parser.parse_args()

        
zone = pd.read_csv(args.zone)
zone = zone.rename({'LocationID': 'DOLocationID'}, axis=1)


for i in args.mesi: 
    #preparazione dati
    df = pd.read_csv(f'./Data/yellow_tripdata_2020-0{i}.csv',usecols = ['tpep_dropoff_datetime', 'DOLocationID'])
    
    extractor=ExtractInfo()
    df=extractor.data_cleaner(df)
    
    df = pd.merge(df, zone, on=['DOLocationID'],how='left')
    
    #estrae il numero di corse per giorno nel mese dell'iterazione corrente
    dati_mese_zona=extractor.conta_corse_per_giorno(df)
    
    
    #salva nella cartella Results i grafici relativi al numero di corse giornaliere per ogni mese
    extractor.crea_grafici(df,dati_mese_zona)
   

elapsed = time.perf_counter() - start

#==========================================================================================#