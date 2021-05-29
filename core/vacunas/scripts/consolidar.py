#!/usr/bin/env python3

import pandas as pd

def consolidar():
    "Descarga datos, agrega columnas de observaciones a los metadatos y almacena todo en `directory`"
    
    directory = 'datos'
    url = {'metadata': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSqqrgZIoiGkbpHHT9Zh8dm1UYHANI8qgVa_4CK7SrvZMMCElwTFoWjmKl8TtpRLSunl5mW_zQySiiX/pub?gid=0&single=true&output=csv',
           'primera': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSqqrgZIoiGkbpHHT9Zh8dm1UYHANI8qgVa_4CK7SrvZMMCElwTFoWjmKl8TtpRLSunl5mW_zQySiiX/pub?gid=1225256068&single=true&output=csv',
           'segunda': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSqqrgZIoiGkbpHHT9Zh8dm1UYHANI8qgVa_4CK7SrvZMMCElwTFoWjmKl8TtpRLSunl5mW_zQySiiX/pub?gid=1683596885&single=true&output=csv'}
    orden = ['Beni', 'Chuquisaca', 'Cochabamba', 'La Paz', 'Oruro', 'Pando', 'Potosi', 'Santa Cruz', 'Tarija', 'Total']
    
    meta = pd.read_csv(url['metadata'], parse_dates=['fecha'], index_col=['fecha'])
    for dosis in ['primera', 'segunda']:
        df = pd.read_csv(url[dosis], parse_dates=['fecha'], index_col=['fecha'])
        meta['observaciones_{}'.format(dosis)] = crear_observaciones(df)
        df[orden].to_csv('{}/{}.csv'.format(directory, dosis), float_format='%.0f')
    meta.to_csv('{}/metadata.csv'.format(directory))

def crear_observaciones(df):
    "Define y aplica pruebas a `df`, y devuelve una serie con mensajes de observación."
    
    total = 'Total'
    mensaje = {'suma': 'la suma de valores por departamento no coincide con el total reportado',
               'disminuye': 'el número de dosis disminuye respecto al valor reportado el día anterior',
               'noreportado': 'no existe un reporte publicado y transcrito'}

    def test(tipo, df):
        "Función de ayuda para acceder a pruebas"

        tipos = {'suma': test_suma(df),
                 'disminuye': test_disminuye(df),
                 'noreportado': test_noreportado(df)}

        return tipos[tipo]

    def test_suma(df):
        "En qué fechas la suma de los valores por departamento no coincide con el total reportado."

        departamentos = df.columns[:-1]
        return df[(df[departamentos].sum(axis=1) != df[total]) & 
                  (df[total].notna())].index

    def test_disminuye(df):
        "En qué fechas el número de dosis disminuye respecto al valor reportado el día anterior."

        return df[(df.diff() < 0).sum(axis=1) > 0].index

    def test_noreportado(df):
        "En qué fechas no existe un reporte publicado y transcrito."

        return df[df[total].isna()].index

    def evaluar(df):
        "Aplica pruebas a `df` y devuelve resultados como una serie de mensajes"

        pruebas = mensaje.keys()
        resultados = pd.DataFrame(columns=pruebas, index=df.index)
        for prueba in pruebas:
            rows = test(prueba, df)
            resultados.loc[rows, prueba] = mensaje[prueba]
        return resultados.apply(lambda columns: ' y '.join([col for col in columns if type(col) == str]), axis=1)
    
    return evaluar(df)

consolidar()
