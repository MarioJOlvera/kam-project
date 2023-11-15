from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff 
import numpy as np 

from plotly.subplots import make_subplots 
from datetime import datetime
from tkinter import *
from itertools import groupby

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

file = ("LIDER - CO_V2.xlsx")

df = pd.read_excel(file)
datos = pd.DataFrame(df)

datos.rename(columns = {
    'Mes' : 'Period', 
    'Subdivision' : 'State', 
    'Metrica' : 'Metrics', 
    'Nivel' : 'Level', 
    'Valor' : 'Value'
}, inplace = True)

datos['State'].replace({
    'SANTANDER' : 'Santander', 
    'BOGOTA' : 'Bogota', 
    'VALLE DEL CAUCA' : 'Valle del Cauca',
    'CESAR' : 'Cesar',
    'N DE SANTANDER' : 'Santander', 
    'ATLANTICO' : 'Atlantico', 
    'N De Santander' : 'Santander', 
    'BOYACA' : 'Boyaca', 
    'BOLIVAR' : 'Bolivar', 
    'CUNDINAMARCA' : 'Cundinamarca', 
    'ANTIOQUIA' : 'Antioquia', 
    'BG' : 'Bogota', 
    'CALDAS' : 'Caldas', 
    'TOLIMA' : 'Tolima', 
    'CASANARE' : 'Casanare', 
    'SUCRE' : 'Sucre',
    'QUINTANA ROO' : 'Out of Country', 
    'Valle Del Cauca' : 'Valle del Cauca', 
    'ARAUCA' : 'Arauca', 
    'GUAYAS' : 'Guayas', 
    'MAGDALENA' : 'Magdalena', 
    'CAUCA' : 'Cauca', 
    'QUINDIO' : 'Quindio', 
    'CAQUETA' : 'Caqueta', 
    'META' : 'Meta', 
    'CORDOBA' : 'Cordoba', 
    'HUILA' : 'Huila', 
    'Norte de Santander' : 'Santander', 
    'UT' : 'Out of Country',
    'FL' : 'Out of Country',
    'WI' : 'Out of Country',
    'CDMX' : 'Out of Country', 
    'ST' : 'Out of Country', 
    'CU' : 'Out of Country', 
    'Quintana Roo' : 'Out of Country', 
    'TX' : 'Out of Country', 
    'Guayas' : 'Out of Country'
}, inplace = True)

datos.head()

states_df = pd.DataFrame(datos.iloc[:,[0,14]])

states_df.drop_duplicates(inplace = True)

series_states = pd.Series(states_df['State']).value_counts()

states_table = pd.DataFrame(series_states)

states_table.rename(columns = {
    'count' : 'Total'
}, inplace = True)

states_table.reset_index(inplace = True)

states_largest = pd.DataFrame(states_table.nlargest(5, columns = 'Total', keep = 'all'))

states_largest.rename(columns = {'Total' : 'Total States'}, inplace = True)

states_table_fig = ff.create_table(states_largest, height_constant = 50)


states_labels = states_largest['State']
states_values = states_largest['Total States']

colors_states = ['#3a93ba', '#fcc003', '#ff784f', '#8394c6', '#59aa9']


states_fig = make_subplots(rows = 1, cols = 2, 
                           shared_xaxes = True, 
                           specs = [[{'type' : 'domain'}, 
                                    {'type' : 'domain'}]]
                        )

states_fig.add_traces(go.Table(
    header = dict(values = list(states_largest.columns),
                  fill_color = 'royalblue', 
                  align = 'center', 
                  font = dict(color = 'white', size = 14), 
                  line_color = 'darkslategray'),
    cells = dict(values = [states_largest.State, states_largest['Total States']], 
                 fill_color = 'white', 
                 align = 'center',
                 font_size = 12, 
                 line_color = 'darkslategray')
), 1, 1)

states_fig.add_trace(
    go.Pie(
    labels= states_labels, 
    values = states_values, 
    name = 'States Summary', 
    hole = 0.4, 
    automargin = True
), 1, 2)

lvl_df = pd.DataFrame(datos.iloc[:,[0,9]])

lvl_df.drop_duplicates(inplace = True)

lvl_df.drop(0, inplace = True)

series_lvl = pd.Series(lvl_df['Level']).value_counts()

lvl = pd.DataFrame(series_lvl)

lvl.reset_index(inplace = True)

lvl.rename(columns = {'count' : 'Total Level'}, inplace = True)

lvl_largest = pd.DataFrame(lvl.nlargest(5, columns = 'Total Level', keep = 'all'))

lvl_largest.sort_values(by = 'Level', inplace = True)

ranks_df = pd.DataFrame(datos.drop(
    datos[
        (datos['Metrics'] != 'RangoMes')
    ].index
))

ranks_df['Value'] = ranks_df['Value'].astype(int)

ranks_df = pd.DataFrame(ranks_df.iloc[:,[0,11]])

ranks_df.drop_duplicates(inplace = True)

lst_rank = [
    (ranks_df['Value'] == -1),
    (ranks_df['Value'] == 0),
    (ranks_df['Value'] == 1),
    (ranks_df['Value'] == 2), 
    (ranks_df['Value'] == 3), 
    (ranks_df['Value'] == 4), 
    (ranks_df['Value'] == 5), 
    (ranks_df['Value'] == 6), 
    (ranks_df['Value'] == 7), 
    (ranks_df['Value'] == 8), 
    (ranks_df['Value'] == 9), 
    (ranks_df['Value'] == 10),
    (ranks_df['Value'] == 11), 
    (ranks_df['Value'] == 12)
]

condition_ranks = [
    'Customer', 
    'PremiumCustomer', 
    'Consultant',
    'Senior Consultant',
    'Director', 
    'Director 3K', 
    'Director 6K',
    'Executive 12K', 
    'Executive 25K',
    'Executive 50K',
    'Presidential 100K',
    'Presidential Elite 200K', 
    'Chairman Club 500K',
    'Chairman Club Elite 1M'
]

ranks_df['Rank'] = np.select(lst_rank, condition_ranks, default = 'Not Specified')

ranks = pd.DataFrame(ranks_df.drop(
    ranks_df[
        (ranks_df['EBSAccountNumber'] == 11971)
    ].index
))

ranks_df.drop_duplicates(subset = 'EBSAccountNumber', inplace = True)

series_ranks = pd.Series(ranks['Rank']).value_counts()

df_ranks = pd.DataFrame(series_ranks)

df_ranks.reset_index(inplace = True)

df_ranks.rename(columns = {'count' : 'Total Ranks', 'Rank' : 'Ranks'}, inplace = True)

ranks_largest = pd.DataFrame(df_ranks.nlargest(5, columns = 'Total Ranks', keep = 'all'))

lvl_labels = lvl_largest['Level']
lvl_values = lvl_largest['Total Level']

ranks_label = ranks_largest['Ranks']
ranks_value = ranks_largest['Total Ranks']

colors_level = ['#2661a9', '#88c7bd', '#78b0fd', '#fe9339', '#61bfd1']

colors_ranks = ['#0c1a1a', '#254a49', '#356461', '#427e7a', '#53a098']

lvl_fig = make_subplots(
    rows = 1, cols = 2, 
    shared_xaxes = True, 
    vertical_spacing = 0.03,
    specs = [
        [{'type' : 'table'},
         {'type' : 'domain'}]
    ]
)

ranks_fig = make_subplots(
    rows = 1, cols = 2, 
    shared_xaxes = True,
    vertical_spacing = 0.03,
    specs = [
        [
            {'type' : 'table'},
            {'type' : 'domain'}
        ]
    ]
)

lvl_fig.add_trace(
    go.Table(
        header = dict(
            values = list(lvl_largest.columns),
            fill_color = 'royalblue',
            align = 'center',
            font = dict(color = 'white', size = 14),
            line_color = 'darkslategray'
        ),
        cells = dict(
            values = [lvl_largest.Level, lvl_largest['Total Level']],
            fill_color = 'white',
            align = 'center',
            font_size = 12,
            line_color = 'darkslategray'
        )
    ), 1, 1
)

lvl_fig.add_trace(
    go.Pie(
        labels = lvl_labels,
        values = lvl_values, 
        name = 'Level Summary',
        hole = 0.5, 
        automargin = True
    ), 1, 2
)

ranks_fig.add_trace(
    go.Table(
        header = dict(
            values = list(ranks_largest.columns),
            fill_color = 'royalblue',
            font = dict(color = 'white', size = 14), 
            line_color = 'darkslategray'
        ),
        cells = dict(
            values = [ranks_largest.Ranks, ranks_largest['Total Ranks']],
            fill_color = 'white',
            align = 'center',
            font_size = 12, 
            line_color = 'darkslategray'
        )
    ), 1, 1
)

ranks_fig.add_trace(
    go.Pie(
        labels = ranks_label,
        values = ranks_value,
        name = 'Ranks Summary',
        hole = 0.3, 
        automargin = True 
    ), 1, 2
)

# HISTORICO DE RANGOS Y REGLA DE BALANCE ---------------------- 

datos_ranks = pd.DataFrame(datos.iloc[:,[0,1,10,11,12]])

historic_ranks = pd.DataFrame(datos_ranks.drop(
    datos_ranks[
        (datos_ranks['Metrics'] != 'RangoMes') & (datos_ranks['Metrics'] != 'TOV') &
        (datos_ranks['Metrics'] != 'TOVFuerte') & (datos_ranks['Metrics'] != 'GV') &
        (datos_ranks['Metrics'] != 'ConsultoresL1') | (datos_ranks['EBSAccountNumber'] != 11971)
    ].index
))

historic_ranks.replace(
    {
        'ConsultoresL1' : 'Senior Consultant',
        'RangoMes' : 'Current Rank',
        'TOVFuerte' : 'Balance'
    }, inplace = True
)

historic_ranks = pd.DataFrame(historic_ranks.drop(
    historic_ranks[
        (historic_ranks['Period'] < '2022-09-01')
    ].index
))

ranks_pivot = historic_ranks.pivot(
    index = 'Period',
    columns = 'Metrics',
    values = 'Value'
)

ranks_pivot['Current Rank'] = ranks_pivot['Current Rank'].astype(int)

lst_rank = [
    (ranks_pivot['Current Rank'] == -1),
    (ranks_pivot['Current Rank'] == 0),
    (ranks_pivot['Current Rank'] == 1),
    (ranks_pivot['Current Rank'] == 2), 
    (ranks_pivot['Current Rank'] == 3), 
    (ranks_pivot['Current Rank'] == 4), 
    (ranks_pivot['Current Rank'] == 5), 
    (ranks_pivot['Current Rank'] == 6), 
    (ranks_pivot['Current Rank'] == 7), 
    (ranks_pivot['Current Rank'] == 8), 
    (ranks_pivot['Current Rank'] == 9), 
    (ranks_pivot['Current Rank'] == 10),
    (ranks_pivot['Current Rank'] == 11), 
    (ranks_pivot['Current Rank'] == 12)
]

condition_ranks = [
    'Customer', 
    'PremiumCustomer', 
    'Consultant',
    'Senior Consultant',
    'Director', 
    'Director 3K', 
    'Director 6K',
    'Executive 12K', 
    'Executive 25K',
    'Executive 50K',
    'Presidential 100K',
    'Presidential Elite 200K', 
    'Chairman Club 500K',
    'Chairman Club Elite 1M'
]

ranks_pivot['Current Rank'] = np.select(lst_rank, condition_ranks, default = 'Not Specified')

ranks_pivot.reset_index(inplace = True)

ranks_pivot[['Balance', 'GV', 'Senior Consultant', 'TOV']] = ranks_pivot[['Balance', 'GV', 'Senior Consultant', 'TOV']].astype(int)

table_data = [['Period', 'Balance', 'Current<br>Rank', 'GV', 'Senior<br>Consultant', 'TOV'],
              ['2022-09-01', 9209.94, 'Executive 12K', 595.75, 4, 16524.39],
              ['2022-10-01', 9215.38, 'Executive 12K', 898.99, 4, 17296.06],
              ['2022-11-01', 9186.78, 'Executive 12K', 845.30, 4, 16117.94],
              ['2022-12-01', 6559.07, 'Executive 12K', 333.16, 4, 12559.83],
              ['2023-01-01', 8739.09, 'Executive 12K', 500.89, 4, 16107.62],
              ['2023-02-01', 10345.02, 'Executive 12K', 417.51, 8, 16362.69],
              ['2023-03-01', 11852.62, 'Executive 12K', 890.95, 6, 18719.43],
              ['2023-04-01', 6688.96, 'Director 6K', 502.05, 5, 10749.80],
              ['2023-05-01', 5861.04, 'Director 6K', 339.08, 5, 10827.62],
              ['2023-06-01', 7826.97, 'Executive 12K', 459.17, 6, 12997.03],
              ['2023-07-01', 8673.04, 'Executive 12K', 314.70, 4, 15242.77],
              ['2023-08-01', 9165.55, 'Executive 12K', 421.25, 6, 15663.82]]

historic_ranks_fig = ff.create_table(table_data, height_constant=50)

period = ['2022-09-01','2022-10-01', '2022-11-01', '2022-12-01',
          '2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01',
          '2023-06-01', '2023-07-01', '2023-08-01']

GFPG = [16524.39, 17296.06, 16117.94, 12559.83, 16107.62, 16362.69, 18719.43, 10749.80, 10827.62, 12997.03, 15242.77, 15663.82]
GAPG = [9209.94, 9215.38, 9186.78, 6559.07, 8739.09, 10345.02, 11852.62, 6688.96, 5861.04, 7826.97, 8673.04, 9165.55]

trace1 = go.Bar(x=period, y=GFPG,
                    marker=dict(color='#0099ff'),
                    name='TOV<br>Per Period',
                    xaxis='x2', yaxis='y2')
trace2 = go.Scatter(x=period, y=GAPG,
                    marker=dict(color='#404040'),
                    name='Balance<br>Per Period',
                    xaxis='x2', yaxis='y2')


historic_ranks_fig.add_traces([trace1, trace2])

historic_ranks_fig['layout']['xaxis2'] = {}
historic_ranks_fig['layout']['yaxis2'] = {}

historic_ranks_fig.layout.xaxis.update({'domain' : [0, .55]})
historic_ranks_fig.layout.xaxis2.update({'domain' : [0.6, 1]})

historic_ranks_fig.layout.yaxis2.update({'anchor' : 'x2'})
historic_ranks_fig.layout.yaxis2.update({'title' : 'TOV'})

historic_ranks_fig.layout.margin.update({'t' : 50, 'b' : 100})

# ------------------ TOV x Lider --------------------


tov_general = pd.DataFrame(datos.drop(
    datos[
        (datos['Metrics'] != 'TOV')  & (datos['Metrics'] != 'RangoMes') | (datos['Level'] != 1)
    ].index 
))


tov_general.drop(columns = ['EnrollmentDate', 'AccountType', 'CountryISO', 
                            'Sponsor_EBSAccountNumber', 'Sponsor_AccountType',
                            'Sponsor_CountryISO', 'City', 'State'], inplace = True)


tov_lvl_1 = pd.DataFrame(tov_general.drop(
    tov_general[
        (tov_general['Period'] < '2022-09-01')
    ].index
))

tov_lvl_1.dropna(inplace = True)

tov_lvl_1 = pd.DataFrame(tov_lvl_1.drop(
    tov_lvl_1[
        (tov_lvl_1['Value'] < 2)
    ].index
))

tov_lvl_1.drop(columns = ['SponsorName', 'Level'], inplace = True)

tov_lvl_1.rename(columns = {
    'EBSAccountNumber' : 'AccountNumber'
}, inplace = True)

tov_pivot = tov_lvl_1.pivot(index = ['AccountNumber', 'Name', 'Metrics'], columns = 'Period', values = 'Value')


tov_pivot.dropna(inplace = True)

tov_pivot.reset_index(inplace = True)

tov = pd.DataFrame(tov_pivot.drop(
    tov_pivot[
        (tov_pivot['Metrics'] == 'RangoMes')
    ].index
))

tov.columns = tov.columns.astype(str)

tov.rename(columns = {
    '2022-09-01 00:00:00' : 'Sep 2022', 
    '2022-10-01 00:00:00' : 'Oct 2022', 
    '2022-11-01 00:00:00' : 'Nov 2022', 
    '2022-12-01 00:00:00' : 'Dec 2022', 
    '2023-01-01 00:00:00' : 'Jan 2023', 
    '2023-02-01 00:00:00' : 'Feb 2023', 
    '2023-03-01 00:00:00' : 'Mar 2023', 
    '2023-04-01 00:00:00' : 'Apr 2023', 
    '2023-05-01 00:00:00' : 'May 2023', 
    '2023-06-01 00:00:00' : 'Jun 2023', 
    '2023-07-01 00:00:00' : 'Jul 2023', 
    '2023-08-01 00:00:00' : 'Aug 2023'
}, inplace = True )

tov['Account'] = tov['AccountNumber'].astype(int)

series_name = pd.Series(tov['Name'])

tov[['LastName', 'Name']] = tov['Name'].str.split(r",", expand = True)

cols = ['AccountNumber', 'LastName', 'Name', 'Metrics', 'Sep 2022', 
        'Oct 2022', 'Nov 2022', 'Dec 2022', 'Jan 2023', 'Feb 2023', 
        'Mar 2023', 'Apr 2023', 'May 2023', 'Jun 2023', 'Jul 2023', 'Aug 2023']

tov = tov[cols]

tov.drop(columns = ['Name', 'Metrics'], inplace = True)

tov_general_2022 = pd.DataFrame(tov_general.drop(
    tov_general[
        (tov_general['Period'] < '2022-01-01') | (tov_general['Period'] > '2022-08-01') | (tov_general['Value'] < 3)
    ].index
))

tov_general_2022.drop(columns = ['SponsorName', 'Level'], inplace = True)

tov_general_2022 = pd.DataFrame(tov_general_2022.drop(
    tov_general_2022[
        (tov_general_2022['Metrics'] == 'RangoMes')
    ].index
))

tov_general_2022['Year_2022'] = tov_general_2022['Period'].dt.year

tov_general_2022.drop(columns = ['Metrics', 'Period'], inplace= True)

tov_2022 = pd.DataFrame(tov_general_2022.groupby(['Year_2022', 'EBSAccountNumber', 'Name']).sum())

tov_2022.reset_index(inplace = True)

tov_2022.rename(columns = {'EBSAccountNumber' : 'AccountNumber',
                           'Value' : 'TOV_2022'}, inplace = True)


tov_general_2023 = pd.DataFrame(tov_general.drop(
    tov_general[
        (tov_general['Period'] < '2023-01-01') | (tov_general['Period'] > '2023-08-01') | (tov_general['Value'] < 3)
    ].index
))

tov_general_2023.drop(columns = ['SponsorName', 'Level'], inplace = True)

tov_general_2023 = pd.DataFrame(tov_general_2023.drop(
    tov_general_2023[
        (tov_general_2023['Metrics'] == 'RangoMes')
    ].index
))

tov_general_2023['Year_2023'] = tov_general_2023['Period'].dt.year

tov_general_2023.drop(columns = ['Metrics', 'Period'], inplace= True)

tov_2023 = pd.DataFrame(tov_general_2023.groupby(['Year_2023', 'EBSAccountNumber', 'Name']).sum())

tov_2023.reset_index(inplace = True)

tov_2023.rename(columns = {'EBSAccountNumber' : 'AccountNumber',
                           'Value' : 'TOV_2023'}, inplace = True)

tov_acumulado = tov_2022.merge(tov_2023, on = 'AccountNumber', how = 'left')

tov_acumulado.dropna(inplace = True)

tov_acumulado = pd.DataFrame(tov_acumulado.nlargest(5, columns = ['TOV_2022', 'TOV_2023'], keep = 'all'))

tov_acumulado.drop(columns = {'Year_2022', 'Year_2023', 'Name_y'}, inplace = True)

tov_acumulado[['LastName', 'Name_x']] = tov_acumulado['Name_x'].str.split(r",", expand = True)

tov_acumulado.rename(columns = {'Name_x' : 'Name'}, inplace = True)

cols_acumulado = ['AccountNumber', 'LastName', 'Name', 'TOV_2022', 'TOV_2023']

tov_acumulado = tov_acumulado[cols_acumulado]

tov_acumulado.drop(columns = {'Name'}, inplace = True)

tov_acumulado['Var_YTD'] = round(((tov_acumulado['TOV_2023'] - tov_acumulado['TOV_2022']) / (tov_acumulado['TOV_2022'])) * 100.00, 2)

tov_acumulado['TOV_2022'] = tov_acumulado['TOV_2022'].astype(int)
tov_acumulado['TOV_2023'] = tov_acumulado['TOV_2023'].astype(int)

fig_acumulado = ff.create_table(tov_acumulado, height_constant = 60)

names = list(tov_acumulado['LastName'])

GFPG2 = list(tov_acumulado['TOV_2022'])
GAPG2 = list(tov_acumulado['TOV_2023'])

trace1_acumulado = go.Bar(x=names, y=GFPG2,
                    marker=dict(color='#0099ff'),
                    name='TOV<br>2022',
                    xaxis='x2', yaxis='y2')
trace2_acumulado = go.Bar(x=names, y=GAPG2,
                    marker=dict(color='#404040'),
                    name='TOV<br>2023',
                    xaxis='x2', yaxis='y2')

fig_acumulado.add_traces([trace1_acumulado, trace2_acumulado])

# initialize xaxis2 and yaxis2
fig_acumulado['layout']['xaxis2'] = {}
fig_acumulado['layout']['yaxis2'] = {}

# Edit layout for subplots
fig_acumulado.layout.xaxis.update({'domain': [0, .5]})
fig_acumulado.layout.xaxis2.update({'domain': [0.6, 1.]})

# The graph's yaxis MUST BE anchored to the graph's xaxis
fig_acumulado.layout.yaxis2.update({'anchor': 'x2'})
fig_acumulado.layout.yaxis2.update({'title': 'TOV'})

# Update the margins to add a title and see graph x-labels.
fig_acumulado.layout.margin.update({'t':50, 'b':100})

tov = pd.DataFrame(tov.nlargest(5, columns= ['Aug 2023'], keep = 'all'))

tov_test = [['Account<br>Number', 'LastName', 'Sep 2022', 'Oct 2022', 'Nov 2022', 'Dec 2022', 'Jan 2023', 'Feb 2023', 'Mar 2023', 'Apr 2023', 'May 2023', 'Jun 2023', 'Jul 2023', 'Aug 2023'], 
            [10367, 'Taboada<br>Jimenes', 7314.45, 8080.68, 6937.16, 6000.76, 7368.53, 6017.67, 6866.81, 4060.84, 4966.58, 5170.06, 6569.73, 6498.27],
            [60689558, 'Ramirez<br>Leal', 2385.16, 2333.13, 2239.8, 1138.4, 2000.25, 1697.6, 2537.75, 1596.76, 690.36, 2152.91, 2251.97, 2381.84],
            [65931, 'Jaimes<br>Garcia', 2933.54, 2487.77, 2377.32, 1635.66, 2724.38, 1997.77, 2416.22, 1690.51, 1666.92, 1507.2, 2400.74, 2247.95],
            [132883, 'Camacho<br>Gomez', 671.50, 535.34, 1496.92, 1006.72, 825.08, 2250.59, 1037.34, 873.98, 1379.17, 1211.52, 1787.95, 1388.31],
            [60632444, 'Macias<br>Fierro',	1359.80, 1817.04, 1090.36, 898.82, 1495.75, 1752.96, 3036.69, 973.56, 933.73, 1010.26, 1142.18, 1107.12]]

fig_table = ff.create_table(tov_test, height_constant=60)

# ----------------------- RANGOS POR NIVEL ---------------

buyers = pd.DataFrame(datos.drop(
    datos[
        (datos['Metrics'] != 'RangoMes') & (datos['Metrics'] != 'PV') | (datos['Period'] < '2022-01-01') 
    ].index
))


buyers.drop(columns = ['EnrollmentDate', 'AccountType', 'CountryISO', 'Sponsor_EBSAccountNumber', 
                       'SponsorName', 'Sponsor_AccountType', 'Sponsor_CountryISO', 'Level', 'City', 'State'], inplace = True)


buyers_pivot = buyers.pivot(index = ['Period', 'EBSAccountNumber', 'Name'], columns = 'Metrics', values = 'Value')

buyers_pivot['RangoMes'] = buyers_pivot['RangoMes'].astype(int)

lst_rank = [
    (buyers_pivot['RangoMes'] == -1),
    (buyers_pivot['RangoMes'] == 0),
    (buyers_pivot['RangoMes'] == 1),
    (buyers_pivot['RangoMes'] == 2), 
    (buyers_pivot['RangoMes'] == 3), 
    (buyers_pivot['RangoMes'] == 4), 
    (buyers_pivot['RangoMes'] == 5), 
    (buyers_pivot['RangoMes'] == 6), 
    (buyers_pivot['RangoMes'] == 7), 
    (buyers_pivot['RangoMes'] == 8), 
    (buyers_pivot['RangoMes'] == 9), 
    (buyers_pivot['RangoMes'] == 10),
    (buyers_pivot['RangoMes'] == 11), 
    (buyers_pivot['RangoMes'] == 12)
]

condition_ranks = [
    'Customer', 
    'PremiumCustomer', 
    'Consultant',
    'Senior Consultant',
    'Director', 
    'Director 3K', 
    'Director 6K',
    'Executive 12K', 
    'Executive 25K',
    'Executive 50K',
    'Presidential 100K',
    'Presidential Elite 200K', 
    'Chairman Club 500K',
    'Chairman Club Elite 1M'
]

buyers_pivot['Rank'] = np.select(lst_rank, condition_ranks, default = 'Not Specified')

buyers_df = pd.DataFrame(buyers_pivot.drop(
    buyers_pivot[
        (buyers_pivot['PV'] == 0)
    ].index
))

buyers_df.reset_index(inplace = True)

buyers_test = pd.DataFrame(buyers_df.iloc[:,[0, 5]])

buyers_group_general = pd.DataFrame(buyers_test.groupby(['Period', 'Rank']).value_counts())

buyers_group_general.reset_index(inplace = True)

buyers_group = pd.DataFrame(buyers_group_general.drop(
    buyers_group_general[
        (buyers_group_general['Period'] < '2022-09-01')
    ].index
))

buyers_group = buyers_group.pivot(index = 'Rank', columns = 'Period', values = 'count')

buyers_group.fillna(0, inplace = True)

buyers_group.reset_index(inplace = True)

buyers_group.columns = buyers_group.columns.astype(str)

buyers_group.rename(columns = {
        '2022-09-01 00:00:00' : 'Sep 2022',
        '2022-10-01 00:00:00' : 'Oct 2022', 
        '2022-11-01 00:00:00' : 'Nov 2022',
        '2022-12-01 00:00:00' : 'Dec 2022', 
        '2023-01-01 00:00:00' : 'Jan 2023',
        '2023-02-01 00:00:00' : 'Feb 2023', 
        '2023-03-01 00:00:00' : 'Mar 2023',
        '2023-04-01 00:00:00' : 'Apr 2023',
        '2023-05-01 00:00:00' : 'May 2023',
        '2023-06-01 00:00:00' : 'Jun 2023',
        '2023-07-01 00:00:00' : 'Jul 2023',
        '2023-08-01 00:00:00' : 'Aug 2023'}, inplace = True
)

lst_month = ['Sep 2022', 'Oct 2022', 'Nov 2022', 'Dec 2022', 'Jan 2023', 'Feb 2023', 'Mar 2023', 'Apr 2023', 'May 2023', 'Jun 2023', 'Jul 2023', 'Aug 2023']

buyers_group[lst_month] = buyers_group[lst_month].astype(int)

buyers_group.rename(columns = {
    'Sep 2023' : '09-23',
    'Aug 2023' : '08-23', 
    'Jul 2023' : '07-23', 
    'Jun 2023' : '06-23', 
    'May 2023' : '05-23', 
    'Apr 2023' : '04-23',
    'Mar 2023' : '03-23', 
    'Feb 2023' : '02-23', 
    'Jan 2023' : '01-23', 
    'Dec 2022' : '12-22', 
    'Nov 2022' : '11-22', 
    'Oct 2022' : '10-22'
}, inplace = True)

buyers_lst_month = ['08-23', '07-23', '06-23', '05-23', '04-23', '03-23', '02-23', '01-23', '12-22', '11-22', '10-22']

buyers_melt = pd.melt(buyers_group, id_vars = 'Rank', value_vars= buyers_lst_month)

buyers_melt['Period'] = pd.to_datetime(buyers_melt['Period'], format = '%m-%y')

buyers_melt.rename(columns = {'value' : 'Total'}, inplace = True)

cols = ['Period', 'Rank', 'Total']

buyers_melt = buyers_melt[cols]

buyers_2023 = pd.DataFrame(buyers_melt.drop(
    buyers_melt[
        (buyers_melt['Period'] < '2023-01-01')
    ].index
))

buyers_2023.sort_values(by = 'Period', ascending = True, inplace = True)

buyers_2023['Year_2023'] = buyers_2023['Period'].dt.year

buyers_2022 = pd.DataFrame(buyers_group_general.drop(
    buyers_group_general[
        (buyers_group_general['Period'] > '2022-08-01')
    ].index
))

buyers_2022.sort_values(by = 'Period', ascending = True, inplace = True)

buyers_2022['Year_2022'] = buyers_2022['Period'].dt.year

buyers_2022.drop(columns = 'Period', inplace = True)

buyers_2022.rename(columns = {'count' : 'Total_2022'}, inplace = True)

buyers_2023.drop(columns = 'Period', inplace = True)

buyers_year_2022 = pd.DataFrame(buyers_2022.groupby(['Year_2022', 'Rank']).sum())

buyers_year_2023 = pd.DataFrame(buyers_2023.groupby(['Year_2023', 'Rank']).sum())

buyers_year_2023.reset_index(inplace = True)
buyers_year_2022.reset_index(inplace = True)

buyers_year_2023.rename(columns = {'Total' : 'Total_2023'}, inplace = True)

buyers_ytd = buyers_year_2022.merge(buyers_year_2023, on = 'Rank', how = 'left')

buyers_ytd.drop(columns = ['Year_2022', 'Year_2023'], inplace = True)

buyers_group.rename(columns = {
    '10-22' : 'Oct 2022', 
    '11-22' : 'Nov 2022', 
    '12-22' : 'Dec 2022',
    '01-23' : 'Jan 2023',
    '02-23' : 'Feb 2023',
    '03-23' : 'Mar 2023',
    '04-23' : 'Apr 2023',
    '05-23' : 'May 2023',
    '06-23' : 'Jun 2023',
    '07-23' : 'Jul 2023',
    '08-23' : 'Aug 2023'
}, inplace = True)

buyers_ytd.sort_values(by = ['Total_2022', 'Total_2023'], ascending = False, inplace = True)

buyers_group_table = ff.create_table(buyers_ytd, height_constant = 60)

ranks_lst = list(buyers_ytd['Rank'])

GFPG3 = list(buyers_ytd['Total_2022'])
GAPG3 = list(buyers_ytd['Total_2023'])

trace1_buyers = go.Bar(x = ranks_lst, 
                y = GFPG3, 
                marker = dict(color = '#0099ff'),
                name = 'Ranks<br>2022',
                xaxis = 'x2', 
                yaxis = 'y2')

trace2_buyers = go.Bar(x = ranks_lst,
                y = GAPG3,
                marker = dict(color = '#404040'),
                name = 'Ranks<br>2023', 
                xaxis = 'x2',
                yaxis = 'y2')

buyers_group_table.add_traces([trace1_buyers, trace2_buyers])

buyers_group_table['layout']['xaxis2'] = {}
buyers_group_table['layout']['yaxis2'] = {}

# Edit layout for subplots
buyers_group_table.layout.xaxis.update({'domain': [0, .5]})
buyers_group_table.layout.xaxis2.update({'domain': [0.6, 1.]})

# The graph's yaxis MUST BE anchored to the graph's xaxis
buyers_group_table.layout.yaxis2.update({'anchor': 'x2'})
buyers_group_table.layout.yaxis2.update({'title': 'Ranks'})

# Update the margins to add a title and see graph x-labels.
buyers_group_table.layout.margin.update({'t':50, 'b':100})

table_buyers = [['Rank', 'Sep 2022', 'Oct 2022', 'Nov 2022', 'Dec 2022', 'Jan 2023', 'Feb 2023', 'Mar 2023', 'Apr 2023', 'May 2023', 'Jun 2023', 'Jul 2023', 'Aug 2023'],
                ['Customer', 2, 0, 0, 1, 0,	0, 1, 0, 1, 1, 2, 3],
                ['Premium<br>Customer', 103, 75, 56, 70, 66, 66, 65, 30, 51, 25, 51, 60],
                ['Consultant', 60, 104, 50, 71, 62, 61, 62, 49, 55, 59, 59, 98],
                ['Senior<br>Consultant', 20, 20, 18, 14, 23, 18, 19, 12, 13, 17, 19, 16],
                ['Director', 2, 4, 4, 3, 3, 2, 3, 3, 2, 2, 2, 3],
                ['Director 3K', 0, 0, 0, 1, 0, 1, 1, 2, 1, 2, 1, 1],
                ['Director 6K', 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
                ['Executive<br>12K', 0,	0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1]]

fig_buyers_general = ff.create_table(table_buyers, height_constant = 60)

# ------------------------- PV por NIVEL --------------------

pv_general = pd.DataFrame(datos.drop(
    datos[
        (datos['Metrics'] != 'PV')
    ].index
))

pv_df = pd.DataFrame(pv_general.iloc[:,[9, 11, 12]])

pv_group = pd.DataFrame(pv_df.groupby(['Period', 'Level']).sum())

pv_group.reset_index(inplace = True)

pv_pivot = pd.DataFrame(pv_group.drop(
    pv_group[
        (pv_group['Period'] < '2022-09-01')
    ].index
))

pv_pivot = pv_pivot.pivot(index = 'Level', columns = 'Period', values = 'Value')

pv_pivot.fillna(0, inplace = True)

pv_pivot.drop([0, 7], inplace = True)

pv_pivot.reset_index(inplace = True)

pv_pivot.columns = pv_pivot.columns.astype(str)

pv_pivot.rename(columns = {
    '2022-09-01 00:00:00' : 'Sep 2022', 
    '2022-10-01 00:00:00' : 'Oct 2022', 
    '2022-11-01 00:00:00' : 'Nov 2022', 
    '2022-12-01 00:00:00' : 'Dec 2022', 
    '2023-01-01 00:00:00' : 'Jan 2023', 
    '2023-02-01 00:00:00' : 'Feb 2023', 
    '2023-03-01 00:00:00' : 'Mar 2023', 
    '2023-04-01 00:00:00' : 'Apr 2023', 
    '2023-05-01 00:00:00' : 'May 2023', 
    '2023-06-01 00:00:00' : 'Jun 2023', 
    '2023-07-01 00:00:00' : 'Jul 2023', 
    '2023-08-01 00:00:00' : 'Aug 2023'
}, inplace = True )

pv1 = pd.DataFrame(pv_group.drop(
    pv_group[
        (pv_group['Level'] != 1) | (pv_group['Period'] < '2022-09-01')
    ].index
))

pv2 = pd.DataFrame(pv_group.drop(
    pv_group[
        (pv_group['Level'] != 2) | (pv_group['Period'] < '2022-09-01')
    ].index
))

pv3 = pd.DataFrame(pv_group.drop(
    pv_group[
        (pv_group['Level'] != 3) | (pv_group['Period'] < '2022-09-01')
    ].index
))

pv4 = pd.DataFrame(pv_group.drop(
    pv_group[
        (pv_group['Level'] != 4) | (pv_group['Period'] < '2022-09-01')
    ].index
))

pv5 = pd.DataFrame(pv_group.drop(
    pv_group[
        (pv_group['Level'] != 5) | (pv_group['Period'] < '2022-09-01')
    ].index
))

pv6 = pd.DataFrame(pv_group.drop(
    pv_group[
        (pv_group['Level'] != 6) | (pv_group['Period'] < '2022-09-01')
    ].index
))

cols = ['Sep 2022', 'Oct 2022', 'Nov 2022', 'Dec 2022', 'Jan 2023', 'Feb 2023', 'Apr 2023', 'Mar 2023', 'May 2023', 'Jun 2023', 'Jul 2023', 'Aug 2023']

pv_pivot[cols] = pv_pivot[cols].astype(int)

pv_table = ff.create_table(pv_pivot, height_constant = 60)


trace1 = go.Scatter(
    x = pv1['Period'], 
    y = pv1['Value'], 
    name = 'Level 1', 
    marker = dict(color = '#8394c6'),
    xaxis = 'x2', 
    yaxis = 'y2'
)

trace2 = go.Scatter(
    x = pv2['Period'], 
    y = pv2['Value'], 
    name = 'Level 2', 
    marker = dict(color = '#fcc003'),
    xaxis = 'x2', 
    yaxis = 'y2'
)

trace3 = go.Scatter(
    x = pv3['Period'], 
    y = pv3['Value'], 
    name = 'Level 3', 
    marker = dict(color = '#3a93ba'),
    xaxis = 'x2', 
    yaxis = 'y2'
)

trace4 = go.Scatter(
    x = pv4['Period'], 
    y = pv4['Value'], 
    name = 'Level 4', 
    marker = dict(color = '#ff784f'),
    xaxis = 'x2', 
    yaxis = 'y2'
)

trace5 = go.Scatter(
    x = pv5['Period'], 
    y = pv5['Value'], 
    name = 'Level 5', 
    marker = dict(color = '#16325c'),
    xaxis = 'x2', 
    yaxis = 'y2'
)

trace6 = go.Scatter(
    x = pv6['Period'], 
    y = pv6['Value'], 
    name = 'Level 6', 
    marker = dict(color = '#59aaa9'),
    xaxis = 'x2', 
    yaxis = 'y2'
)

pv_table.add_traces([trace1, trace2, trace3, trace4, trace5, trace6])

pv_table['layout']['xaxis2'] = {}
pv_table['layout']['yaxis2'] = {}

pv_table.layout.yaxis.update({'domain': [0, .45]})
pv_table.layout.yaxis2.update({'domain': [.6, 1]})

# The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
pv_table.layout.yaxis2.update({'anchor': 'x2'})
pv_table.layout.xaxis2.update({'anchor': 'y2'})
pv_table.layout.yaxis2.update({'title': 'PV'})

# Update the margins to add a title and see graph x-labels.
pv_table.layout.margin.update({'t': 70, 'l':60})

# Update the height because adding a graph vertically will interact with
# the plot height calculated for the table
pv_table.layout.update({'height':800})


# ----------------------------------------------------

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    'margin-left' : '18rem', 
    'margin-right' : '2rem',
    'padding' : '2rem 1rem'
}

sidebar = html.Div(
    [
        html.H2('Send Out', className = 'display-3'),
        html.Hr(),
        html.P(
            'Stats data by Leader'
        ),
        dbc.Nav(
            [
                dbc.NavLink('States', href = '/states-page', active = 'exact'),
                dbc.NavLink('Level', href = '/level-page', active = 'exact'),
                dbc.NavLink('Ranks', href = '/ranks-page', active = 'exact'),
                dbc.NavLink('Historic Ranks', href = '/historic-ranks', active = 'exact'),
                dbc.NavLink('TOV', href = '/tov-historic', active = 'exact'),
                dbc.NavLink('Buyers by Rank', href = '/buyers-rank', active = 'exact'),
                dbc.NavLink('PV by Level', href = '/pv-level', active = 'exact')
            ], 
            vertical = True,
            pills = True
        ),
    ],
    style = SIDEBAR_STYLE,
)

content = html.Div(id = 'page-content', children = [], style = CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id = 'url'),
    sidebar, 
    content
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)

def render_page_content(pathname):
    if pathname == '/states-page':
        return [
            html.H1("Total Customer by State", 
            style = {
                'text-align' : 'center'
            }),
            dcc.Graph(
                id = 'state-pie', 
                figure = states_fig
            )
        ]
    elif pathname == '/level-page':
        return [
            html.H1('Total Customer by Level',
                style = {
                'text-align' : 'center'
                }
            ), 
            dcc.Graph(id = 'level-pie',
                      figure = lvl_fig)
        ]
    elif pathname == '/ranks-page':
        return [
            html.H1(
                'Total Customer by Rank',
                style = {
                'text-align' : 'center'
                }   
            ),
            dcc.Graph(
                id = 'rank-pie',
                figure = ranks_fig
            )
        ]
    elif pathname == '/historic-ranks':
        return [
            html.H1(
                'Historic Ranks Stats by Leader',
                style = {'text-align' : 'center'}
            ),
            dcc.Graph(id = 'historic-ranks',
                      figure = historic_ranks_fig
            )
        ]
    elif pathname == '/tov-historic':
        return [
            html.H1(
                'TOV by Leader', 
                style = {'text-align' : 'center'}
            ), 
            dcc.Graph(
                id = 'table-bar-ytd',
                figure = fig_acumulado
            ),
            html.Br(),
            dcc.Graph(
                id = 'tov-by-leader',
                figure = fig_table
            )
        ]
    elif pathname == '/buyers-rank':
        return [
            html.H1(
                'Buyers By Rank YTD (2022-2023)',
                style = {'text-align' : 'center'}
            ),
            html.Br(),
            dcc.Graph(
                id = 'buyers-table-bar',
                figure = buyers_group_table
            ),
            html.Br(),
            dcc.Graph(
                id = 'buyers-table',
                figure = fig_buyers_general
            )
        ]
    elif pathname == '/pv-level':
        return [
            html.H1(
                'PV Stats by Level (2022-2023)',
                style = {'text-align' : 'center'}
            ),
            html.Br(),
            dcc.Graph(
                id = 'pv-level',
                figure = pv_table
            )
        ]

if __name__ == '__main__':
    app.run_server(debug = True)
