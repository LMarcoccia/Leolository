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


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--in_data", help = "path del file dataset",
                     type = str, default = './Data/yellow_tripdata_2020-01.csv')

parser.add_argument("-i1", "--zone", help = "path del file dataset",
                     type = str, default = './Data/taxi+_zone_lookup.csv')

#SISTEMARE IL PATH IN USCITA E CREARE LA CARTELLA RESULTS 
parser.add_argument("-o", "--out_file", help = "cartella di deposito del file di uscita",
                     type = str, default = './Results/{MESE}.csv')

args = parser.parse_args()


start = time.perf_counter()

 
df = pd.read_csv(args.in_data,usecols = ['tpep_dropoff_datetime', 'DOLocationID'])


zone = pd.read_csv(args.zone)


df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])


#elimino tutte le date diverse da 01/2020
df = df.loc[(df['tpep_dropoff_datetime'].dt.year == 2020) & (df['tpep_dropoff_datetime'].dt.month  == 1)]


df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].dt.date


zone = zone.rename({'LocationID': 'DOLocationID'}, axis=1)
df = pd.merge(df, zone, on=['DOLocationID'],how='left')


dati_mese_zona=pd.DataFrame()
for zona in df['Borough'].unique():
    df_temp=df[df['Borough']==zona]
    dati_mese_zona[zona] = pd.Series(collections.Counter(df_temp['tpep_dropoff_datetime']))
    

dati_mese_zona = dati_mese_zona.sort_index()
for zona in df['Borough'].unique():
    dati_mese_zona[zona].plot.bar()
    plt.title(zona)
    #plt.savefig(args.out_data) 


elapsed = time.perf_counter() - start
