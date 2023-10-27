#!/usr/bin/python3.10

import math
import pandas as pd
from pprint import pprint


def time_avg(df):
    input_size = [int(i.split('x')[0]) for i in df['INPUT SIZE'].tolist()]
    SIZES = input_size[:input_size.index(max(input_size))+1]
    #create the same columns but with online SIEZES row and in TIME and PAGE FAULT do an average of values
    df_avg = pd.DataFrame(columns=df.columns)
    df_avg['INPUT SIZE'] = df['INPUT SIZE'][:len(SIZES)]
    df_avg['CONSTRAINTS'] = df['CONSTRAINTS'][:len(SIZES)]
    df_avg['MAX RAM BYTE (GB)'] = df['MAX RAM BYTE (GB)'][:len(SIZES)] / 10**9
    df_avg['NECESSARY BYTE (GB)'] = df['NECESSARY BYTE (GB)'][:len(SIZES)]

    #for time make an average on all the values of the same size
    for size in SIZES:
        df_avg.loc[df_avg['INPUT SIZE'] == f'{size}x{size}x3', 'TIME (s)'] = df[df['INPUT SIZE'] == f'{size}x{size}x3']['TIME (s)'].mean()
        df_avg.loc[df_avg['INPUT SIZE'] == f'{size}x{size}x3', 'PAGE FAULT'] = df[df['INPUT SIZE'] == f'{size}x{size}x3']['PAGE FAULT'].mean()


    #remove from df_agv colums with all NaN values
    return df_avg.dropna(axis=1,how='all'),SIZES
    


if __name__ == '__main__':
    CSV_PATH = './benchmark_pagefaults.csv'
    
    df = pd.read_csv(CSV_PATH)
    df,SIZES = time_avg(df)
    
    compare_time = dict()

    for start,size in enumerate(SIZES):
        compare_time[size] = {}
        base_time = df['TIME (s)'][start]

        for i in range(start + 1,len(SIZES)):
            original_time = df['TIME (s)'][i]
            tiled_time = float(f'{base_time * math.ceil(SIZES[i]**2 / size**2 ):.3f}')
            compare_time[size][SIZES[i]] = {'ORIG':original_time,'TILED':tiled_time}

    pprint(compare_time)
    pprint(df)