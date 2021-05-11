#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker, dates
import datetime as dt
import locale
import argparse
import twitter
import os

urls = {'primera': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSK4kksU2hLQ3yZQSYkFErYrzYIiv4zhUmIM6ZZFmz1dU9QLf9QrcpAbHW9r6LevIg4hqevNGwbhGS8/pub?gid=0&single=true&output=csv',
        'segunda': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSK4kksU2hLQ3yZQSYkFErYrzYIiv4zhUmIM6ZZFmz1dU9QLf9QrcpAbHW9r6LevIg4hqevNGwbhGS8/pub?gid=314213353&single=true&output=csv'}
colores = {'primera':'#b8cbce', 'segunda':'#4b6169', 'anotaciones_suaves':'#a0b1c0', 'anotaciones': '#2d2b2b', 'fondo': '#fcfcfc'}
departamentos = ['Santa Cruz', 'La Paz', 'Cochabamba', 'Tarija', 'Oruro', 'Chuquisaca', 'Potosi', 'Pando', 'Beni']

def any_updates(respuestas):
    if sum([updated_dfi(tipo_dosis, respuestas[tipo_dosis]) for tipo_dosis in respuestas.keys()]) == len(respuestas.keys()):
        return True
    else:
        return False

def updated_dfi(tipo_dosis, dfi):
    if (len(dfi) - pd.concat([pd.read_csv('datos/{}.csv'.format(tipo_dosis), parse_dates=['fecha']), dfi]).duplicated().sum()) > 0:
        return True
    else:
        return False

def format_dfi(tipo_dosis, dfi):
    dfi.to_csv('datos/{}.csv'.format(tipo_dosis), index=False)
    dfi = dfi.set_index('fecha').unstack().reset_index()
    dfi['dosis'] = tipo_dosis
    return dfi

def format_dfs(dfs):
    dfs = pd.concat(dfs)
    dfs = dfs[['fecha', 'level_0', 0, 'dosis']]
    dfs.columns = ['fecha', 'departamento', 'cantidad', 'dosis']
    return dfs

def make_days(df, desde_hoy=0):
    df_days = pd.DataFrame(pd.date_range(df.fecha.min(), dt.datetime.now() - dt.timedelta(days=desde_hoy)), columns=['fecha'])
    df_days['cantidad'] = 0
    return df_days

def format_df(dfc, all_days):
    dfi = dfc[['fecha', 'cantidad']].groupby('fecha').cantidad.sum().reset_index()
    dfi.cantidad = pd.concat([pd.Series(dfi.iloc[0].cantidad), dfi.cantidad.diff(1).fillna(0)[1:]])
    dfi = pd.concat([dfi, all_days], axis=0).drop_duplicates(subset=['fecha']).set_index('fecha').sort_index()
    dfi['cumulativo'] = dfi.cantidad.cumsum()
    return dfi

def plot_ticks(ax):
    ax.xaxis.set_minor_formatter(dates.DateFormatter('%-d'))
    ax.xaxis.set_major_formatter(dates.DateFormatter('%B'))
    ax.xaxis.set_minor_locator(dates.DayLocator(bymonthday=[5, 25]))
    ax.xaxis.set_major_locator(dates.MonthLocator(bymonthday=15))
    ax.tick_params(axis='x', which='major', labelsize=15)
    for tick in ax.get_xticklabels(which='both'):
        tick.set_verticalalignment('center')

def dosis_plot(ax, df):
    all_days = make_days(df, 1)
    ax.set_facecolor(colores['fondo'])
    dfc = df.copy()
    dosis = pd.concat([format_df(dfc[dfc.dosis == tipo_dosis], all_days).rename(columns={'cantidad':tipo_dosis})[tipo_dosis] for tipo_dosis in ['segunda', 'primera']], axis=1)
    ax.stackplot(dosis.index, dosis.T.values, colors=[colores['segunda'], colores['primera']], alpha=.9)
    ax.set_xticks([])
    ax.grid(axis='y')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(3, prune='lower'))
    ax.set_xlim(dosis.index.min(), dosis.index.max())
    ax.tick_params(which='both', rotation=0, labelcolor=colores['anotaciones_suaves'])
    for label in ax.get_yticklabels():
        label.set_fontfamily('NYTFranklin')
        label.set_alpha(.9)
        label.set_horizontalalignment('left')
        label.set_bbox(dict(color=colores['fondo'], pad=.5))
        label.set_alpha(.9)
    ax.annotate('Dosis\nDiarias', xy=(.07, .5), xycoords='axes fraction', va='center', ha='left', color=colores['anotaciones'], fontsize=20, weight='bold', fontfamily='NYTFranklin', bbox=dict(color=colores['fondo'], pad=.5))

def progreso_departamento(ax, i, df, departamento):
    
    ax.set_facecolor(colores['fondo'])
    locale.setlocale(locale.LC_TIME, "es_US.UTF8")
    dfc = df.copy()
    all_days = make_days(dfc, 1)
    
    anotaciones = [{'tipo': 'segunda', 'mensaje': 'con dos dosis', 'vertical': .35, 'color': 'segunda'},
                    {'tipo': 'primera', 'mensaje': 'con al menos\nuna dosis', 'vertical': .65, 'color': 'primera'}]
    poblacion = {}
    
    for dose in ['primera', 'segunda']:
        dfi = format_df(dfc[(dfc.dosis.isin([dose, 'ambas'])) & (dfc.departamento == departamento)], all_days)
        poblacion[dose] = dfi.cumulativo.max()
        ax.bar(x=dfi[dfi.cantidad != 0].index, height=dfi[dfi.cantidad != 0].cumulativo, color=colores[dose], alpha=1., width=.7, zorder=2)
        ax.bar(x=dfi[dfi.cantidad == 0].index, height=dfi[dfi.cantidad == 0].cumulativo, color=colores[dose], alpha=.6, width=.7, zorder=2)
        
    ax.set_ylim(0, poblacion['primera'] * 1.1)
    ax.set_xlim(all_days.fecha.min() - dt.timedelta(hours=12), all_days.fecha.max() + dt.timedelta(hours=12))
    ax.grid(axis='y', zorder=1, alpha=.5)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(3, prune='lower'))
    
    if i == 0 :
        plot_ticks(ax)
        ax.tick_params(axis='x', which='both', labeltop=True, labelbottom=False)
        ax.tick_params(axis='x', which='major', pad=1)
    elif i == 8:
        plot_ticks(ax)
        ax.tick_params(axis='x', which='minor', pad=20)
        ax.tick_params(axis='x', which='major', pad=17)
    else:
        ax.set_xticks([])

    ax.tick_params(which='both', rotation=0, labelcolor=colores['anotaciones_suaves'])
    ax.tick_params(axis='y', direction="in", pad=-2)
    
    for label in ax.get_yticklabels():
        label.set_horizontalalignment('left')
        label.set_bbox(dict(color=colores['fondo'], pad=.5))
        
    for axis in [ax.get_yticklabels(), ax.get_xticklabels()]:
        for label in axis:
            label.set_fontfamily('NYTFranklin')
            label.set_alpha(.9)

    dimension = len(str(dfc.sort_values('fecha').groupby(['dosis', 'departamento'])['cantidad'].cumsum().max()))
    
    for anotacion in anotaciones:
        
        ax.annotate(int(poblacion[anotacion['tipo']]), xy=(1.015 + (dimension * .012), anotacion['vertical']), xycoords='axes fraction', va='center', ha='right', color=colores[anotacion['color']], fontfamily='NYTFranklin', fontsize=15, weight='bold')
        ax.annotate(anotacion['mensaje'], xy=(1.025 + (dimension * .012), anotacion['vertical']), xycoords='axes fraction', va='center', ha='left', color=colores[anotacion['color']], fontfamily='NYTFranklin', fontsize=10)
    
    ax.annotate(departamento, xy=(-.02, .5), xycoords='axes fraction', va='center', ha='right', color=colores['anotaciones'], fontsize=20, weight='bold', fontfamily='NYTFranklin')

def progreso(df):
    with plt.rc_context(fname='update/clean.mplstyle'):
        f = plt.figure(figsize=(15,17), facecolor=colores['fondo'])
        gs = f.add_gridspec(ncols=150, nrows=110)
        plt.subplots_adjust(wspace=.1, hspace=.1)
        ax1 = f.add_subplot(gs[0:11, :-50])
        dosis_plot(ax1, df)
        ax1.annotate('Vacunaciones', xy=(0.5,1.8), xycoords='axes fraction', fontsize=40, ha='center', va='bottom', fontweight='bold', color=colores['anotaciones'])
        ax1.annotate('en Bolivia', xy=(0.5,1.7), xycoords='axes fraction', fontsize=25, ha='center', va='top', fontweight='bold', color=colores['anotaciones'])
        for i, departamento in enumerate(departamentos):
            ax = f.add_subplot(gs[((i+1)*10)+5:((i+1)*10)+14, :-50])
            progreso_departamento(ax, i, df, departamento)
        ax.annotate('Líneas suaves indican que ese día no se registraron públicamente nuevas vacunaciones', xy=(.5, -.8), xycoords='axes fraction', color=colores['anotaciones_suaves'], ha='center', va='bottom')
        ax.annotate('Datos: Ministerio de Salud\nElaboración: @mauforonda', xy=(.5, -1.1), xycoords='axes fraction', color=colores['anotaciones_suaves'], ha='center', va='top')
        f.savefig('plots/progreso.jpg', bbox_inches='tight', dpi=80, pad_inches=.3)
        f.savefig('plots/progreso_twitter.jpg', bbox_inches='tight', dpi=300, pad_inches=.3)

def twitter_access():
    parser = argparse.ArgumentParser(description='Credenciales de Twitter')

    parser.add_argument('consumer_key', type=str)
    parser.add_argument('consumer_secret', type=str)
    parser.add_argument('access_token_key', type=str)
    parser.add_argument('access_token_secret', type=str)

    args = parser.parse_args()

    return twitter.Api(consumer_key=args.consumer_key, 
    consumer_secret=args.consumer_secret, 
    access_token_key=args.access_token_key, 
    access_token_secret=args.access_token_secret)

def mensaje(dfs):
    
    poblacion_objetivo = pd.read_csv('update/poblacion_objetivo.csv', index_col='departamento').sum().sum()
    poblacion_total = pd.read_csv('update/poblacion_total.csv', index_col='departamento')['poblacion']
    dosis = pd.concat([format_df(dfs[dfs.dosis == tipo_dosis], make_days(dfs, 1)).rename(columns={'cantidad':tipo_dosis})[tipo_dosis].astype(int) for tipo_dosis in ['primera', 'segunda']], axis=1)
    ayer = pd.concat([dfs[dfs.dosis == tipo_dosis].pivot(index='fecha', columns='departamento', values='cantidad').diff(1).iloc[-1].astype(int) for tipo_dosis in ['primera', 'segunda']], axis=1).sum(axis=1).sort_values()
    ayer = pd.concat([ayer, poblacion_total], axis=1)
    ayer.columns = ['dosis', 'poblacion']
    ayer['por_mil'] = ((ayer.dosis / ayer.poblacion) * 1000)
    ayer = ayer.sort_values('por_mil')
    vacunados = dfs[dfs.dosis == 'segunda'].groupby('departamento').cantidad.max().sum()
    
    template = '💉 Vacunación en Bolivia ({}) 💉\n\nAyer se colocaron\n\n1⃣💉 {} primeras y\n2⃣💉 {} segundas dosis\n\n👍 {} administró {:.2f} dosis por 1000 personas ({:.0f})\n\n📈 {:.2%} de la población nacional total y\n📈 {:.2%} de la población vacunable recibieron ambas dosis'
    return template.format(dfs.fecha.max().strftime('%-d/%-m'), dosis.iloc[-1]['primera'], int(dosis.iloc[-1]['segunda']), ayer.index[-1], ayer.iloc[-1]['por_mil'], ayer.iloc[-1]['dosis'], vacunados/poblacion_total.sum().sum(), vacunados/poblacion_objetivo)

def tweet(dfs):
    api = twitter_access()
    text = mensaje(dfs)
    api.PostUpdate(text, media='plots/progreso_twitter.jpg')
    os.remove('plots/progreso_twitter.jpg')

def init():
    dfs = []
    respuestas = {tipo_dosis: pd.read_csv(urls[tipo_dosis], parse_dates=['fecha'], usecols=list(range(10))) for tipo_dosis in urls.keys()}
    if any_updates(respuestas):
        for tipo_dosis in respuestas.keys():
            dfs.append(format_dfi(tipo_dosis, respuestas[tipo_dosis]))
        dfs = format_dfs(dfs)
        progreso(dfs)
        tweet(dfs)

init()
