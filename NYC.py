# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 10:32:53 2020

@author: lollo
"""

"""In quale periodo dell'anno i taxi vengono utilizzati di più? Creare un grafico che, per ogni mese, indichi il numero 
medio di viaggi registrati ogni giorno. A causa delle differenze tra le zone di New York, vogliamo visualizzare le stesse
informazioni per ogni borough. Notate qualche differenza tra di loro? Qual è il mese con la media giornaliera più alta? E 
invece quello con la media giornaliera più bassa?"""

#aumentare il contatore del giorno di partenza
#contatori messi in una serie
#togliere i viaggi non 2020-gennaio
#estrarre in automatico la lista dei giorni del mese a partire dal dataset
#timedelta per vedere come assegnare il viaggio al giorno di partenza o a quello di arrivo 

# =============================================================================
# #giorno-numero_viaggi
# #1 gennaio-x
# #2 gennaio-y, 
# =============================================================================

#mettere argparse
import pandas as pd
#import memory_usage, time_elapsed, generalmente misuriamo le prestazioni 
import matplotlib.pyplot as plt 
import time 
import collections
from datetime import date 

start = time.perf_counter()
#specifichiamo le colonne da leggere così da migliorare le prestazioni
#confrontiamo i tempi di caricamento con e senza le colonne superflue 
df = pd.read_csv("C:/Users/lollo/Downloads/yellow_tripdata_2020-01.csv",
                    usecols = ['tpep_pickup_datetime', 
                               'DOLocationID'])

zone = pd.read_csv("C:/Users/lollo/Downloads/taxi+_zone_lookup.csv")

df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
df['tpep_pickup_datetime'] = df['tpep_pickup_datetime'].dt.date

Giorno_NViaggi = pd.Series(collections.Counter(df['tpep_pickup_datetime']))
# for data in Giorno_NViaggi.index:
#     if date.year(data) != 2020 or date.month(data) != 1:
#        Giorno_NViaggi.index.drop(data,axis=0)


# plt.figure()
# plt.hist(Giorno_NViaggi)

elapsed = time.perf_counter() - start
