# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:25:32 2024

@author: Николай
"""
# Подключение библиотек
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Выбор каталога работы
os.chdir('c:/work/scripts')

# Чтение датасета
df = pd.read_csv('../data/googleplaystore.csv')

# Удаление неанализируемых столбцов
df = df.drop(columns=['Last Updated', 'Current Ver', 'Android Ver'])

## Подготовка данных 
## Для концентрации проверяющего на умение строить графики, было принято решение не расписывать каждый шаг подготвки данных

# Преобразование 'Installs' в целочисленный тип 
df['Installs'] = df['Installs'].apply(lambda x : x.replace('+',"") if '+' in str(x) else x)
df['Installs'] = df['Installs'].apply(lambda x : x.replace(',',"") if ',' in str(x) else x)
df = df[df['Installs']!='Free']
df['Installs'] = df['Installs'].astype(int)

# Преобразование 'Size' в вещественный тип
def convert_size_to_bytes(size_str):
    if size_str == 'Varies with device':
        return np.nan 
    elif size_str.endswith('M'):
        return float(size_str[:-1]) * 1024 * 1024  
    elif size_str.endswith('k'):
        return float(size_str[:-1]) * 1024 
    else:
        return np.nan
    

df['Size'] = df['Size'].apply(convert_size_to_bytes)

# Преобразование 'Reviews' в целочисленный тип
df['Reviews'] = df['Reviews'].astype(int)

# Преобразование 'Price' в целочисленный тип
df['Price'] = df['Price'].apply(lambda x : float(x.replace('$',"")) if '$' in str(x) else float(x))

# Переименование столбцов
df.rename(columns = {'Size': 'Size_in_bytes'}, inplace=True)
df.rename(columns = {'Content Rating': 'Content_rating'}, inplace=True)
df.rename(columns = {'Price': 'Price_in_dollars'}, inplace=True)

qualitatives_at = ['Type', 'Content_rating']
quantitatives_at = ['Rating', 'Reviews', 'Size_in_bytes', 'Installs', 'Price_in_dollars']

# Создание кластеризованных столбчатых диаграмм
def cluster_bar_chart_make1(quantitative, k):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Content_rating', y=quantitative, hue='Type', data=df, width=0.6)
    plt.xlabel('Content_rating')
    plt.ylabel(quantitative)
    # plt.ticklabel_format(style='plain', axis='y')
    plt.title('Кластеризованная столбчатая диаграмма')
    plt.savefig(f'../graphics/Clustered_Bar_Chart{k}.png')
    plt.show()


for i in range(len(quantitatives_at)):
    cluster_bar_chart_make1(quantitatives_at[i], i+1)
    

def cluster_bar_chart_make2(quantitative, k):
    plt.figure(figsize=(10, 7))
    sns.barplot(x='Category', y=quantitative, hue='Type', data=df, width=0.6)
    plt.xlabel('Category')
    plt.xticks(rotation=90, fontsize=6)
    plt.ylabel(quantitative)
    # plt.ticklabel_format(style='plain', axis='y')
    plt.title('Кластеризованная столбчатая диаграмма')
    plt.subplots_adjust(top=0.92, bottom=0.22) 
    plt.savefig(f'../graphics/Clustered_Bar_Chart{k}.png', dpi=300)
    plt.show()


for i in range(len(quantitatives_at)):
    cluster_bar_chart_make2(quantitatives_at[i], i+6)

# Создание категоризированных гистограмм
def categorized_histogram_make(qualitative, quantitative, k):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=quantitative, hue=qualitative, multiple="dodge", bins=10)
    plt.title('Категоризированная гистограмма')
    plt.xlabel(quantitative)
    plt.ylabel('Количество')
    plt.savefig(f'../graphics/Categorized_Histogram{k}.png')
    plt.show()


k=1
for qualitative in qualitatives_at:
    for quantitative in quantitatives_at:
        categorized_histogram_make(qualitative, quantitative, k)
        k+=1
        
# Создание категоризированных диаграмм box-and-whiskers
def categorized_box_and_whisker_plot_make1(qualitative, quantitative, k):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=qualitative, y=quantitative, data=df)    
    plt.title('Категоризированная диаграмма box-and-whiskers')
    plt.xlabel(qualitative)
    plt.ylabel(quantitative)
    plt.savefig(f'../graphics/Categorized_Box_and_Whisker_Plot{k}.png')
    plt.show()


k=1
for qualitative in qualitatives_at:
    for quantitative in quantitatives_at:
        categorized_box_and_whisker_plot_make1(qualitative, quantitative, k)
        k+=1


def categorized_box_and_whisker_plot_make2(quantitative, k):
    plt.figure(figsize=(10, 7))
    sns.boxplot(x='Category', y=quantitative, data=df)    
    plt.title('Категоризированная диаграмма box-and-whiskers')
    plt.xlabel('Category')
    plt.xticks(rotation=90, fontsize=6)
    plt.ylabel(quantitative)
    plt.subplots_adjust(top=0.92, bottom=0.22) 
    plt.savefig(f'../graphics/Categorized_Box_and_Whisker_Plot{k}.png', dpi=300)
    plt.show()


k=11
for quantitative in quantitatives_at:
    categorized_box_and_whisker_plot_make2(quantitative, k)
    k+=1
        
# Создание категоризированных диаграмм рассеивания
def categorized_scatterplot_make(qualitative, quantitative1, quantitative2, k):
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=quantitative1, y=quantitative2, hue=qualitative, data=df)    
    plt.title('Категоризированная диаграмма рассеивания')
    plt.xlabel(quantitative1)
    plt.ylabel(quantitative2)
    plt.subplots_adjust(left=0.07, right=0.82, top=0.95, bottom=0.1) 
    if qualitative == 'Category':
        plt.legend(loc='center left', bbox_to_anchor=(1.01, 0.58), fontsize=8)
    if qualitative == 'Content_rating':
        plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.82))
    if qualitative == 'Type':
        plt.legend(loc='center left', bbox_to_anchor=(1.01, 0.9))
        plt.subplots_adjust(left=0.07, right=0.9, top=0.95, bottom=0.1) 
    plt.savefig(f'../graphics/Categorized_Scatterplot{k}.png', dpi=300)
    plt.show()


k=1
for qualitative in (qualitatives_at + ['Category']):
    for i in range(len(quantitatives_at)-1):
        for j in range(i+1, len(quantitatives_at)):
            categorized_scatterplot_make(qualitative, quantitatives_at[i],
                                         quantitatives_at[j], k)
            k+=1
