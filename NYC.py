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

parser.add_argument("-i1", "--mesi", help = "Mesi da analizzare",
                     type = list, default = ['1', '2', '3', '4', '5', '6'])

parser.add_argument("-i2", "--zone", help = "Path del file dataset",
                     type = str, default = './Data/taxi+_zone_lookup.csv')

parser.add_argument("-i3", "--anno", help = "Anno da analizzare",
                     type = int, default = 2020)

args = parser.parse_args()

#==================================================================================================================#

start = time.perf_counter()


zone = pd.read_csv(args.zone)
zone = zone.rename({'LocationID': 'DOLocationID'}, axis=1)


for i in args.mesi: 
    df = pd.read_csv(f'./Data/yellow_tripdata_2020-0{i}.csv',usecols = ['tpep_dropoff_datetime', 'DOLocationID'])


    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])


    df = df.dropna(axis = 0, how = 'any')

    
    df = df.loc[(df['tpep_dropoff_datetime'].dt.year == args.anno) & (df['tpep_dropoff_datetime'].dt.month  == int(i))]


    df['tpep_dropoff_datetime'] = df['tpep_dropoff_datetime'].dt.date

    
    df = pd.merge(df, zone, on=['DOLocationID'],how='left')


    dati_mese_zona=pd.DataFrame()
    for zona in df['Borough'].unique():
        df_temp = df[df['Borough'] == zona]
        dati_mese_zona[zona] = pd.Series(collections.Counter(df_temp['tpep_dropoff_datetime']))
    

    dati_mese_zona = dati_mese_zona.sort_index()
    for zona in df['Borough'].unique():
        plt.figure()
        dati_mese_zona[zona].plot.bar()
        plt.title(zona)
        plt.savefig(f"./Results/2020-0{i}-{zona}.pdf", dpi=300)
        plt.close()


elapsed = time.perf_counter() - start
