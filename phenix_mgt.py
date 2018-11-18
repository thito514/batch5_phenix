#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Preparing Phenix data for visualisation
'''

__author__ = 'Thierry HA'
__license__ = 'MIT License'
__version__ = '0.1'
__maintainer__ = 'Thierry HA'
__status__ = 'Development'

import pandas as pd

def extract_Phenix_SQLtable2CSV(path='./Phenix_DB/'):
    """
    Save all Phenix SQL tables into raw CSV files
    Args:
        path (str): folder path where the csv will be saved
    Returns:
        done (bool): True if no errors
    """
    import pyodbc
    import pandas as pd
    con = pyodbc.connect(Trusted_Connection='yes', driver = '{SQL Server}',server = 'localhost\SQLEXPRESS' , database = 'PHX_D4G')
    
    lst_table = ['CategorieProduits',
                'CommandeProduits',
                'Commandes',
                'Comptes',
                'OffreProduits',
                'Offres',
                'Produits']
    
    for str_table in lst_table:
        data = pd.read_sql('select * from ' + str_table,con)
        data.to_csv(path+str_table+'.csv',sep='\t',encoding='utf-8')
        print(str_table + ' >> Done')
        
    return True

def get_CategorieProduits(path, prefix='CatP_'):
    """
    Read CSV (CategorieProduits) into Dataframe. All relevant columns are kept and renamed with prefix.
    Args:
        path (str): file path to CategorieProduits.csv
        prefix (str): All relevant columns are renamed with prefix
    Returns:
        df (Dataframe): Resulting dataframe
    """
    col = {'Id':prefix+'Id',
           'Compte_Id':'Compte_Id',
           'IsAlimentaire':prefix+'IsAlimentaire',
           'IsDangereux':prefix+'IsDangereux',
           'IsFresh':prefix+'IsFresh',
           'IsFrozen':prefix+'IsFrozen',
           'IsPerishable':prefix+'IsPerishable',
           'Nom':prefix+'Nom',
           'Descriptif':prefix+'Desc'}
    dt = {'Id': 'int64',
          'Compte_Id': 'float64',
          'IsAlimentaire': 'bool',
          'IsDangereux': 'bool',
          'IsFresh': 'bool',
          'IsFrozen': 'bool',
          'IsPerishable': 'bool',
          'Nom': 'object',
          'Descriptif': 'object'}
    df = pd.read_csv(path, sep='\t', encoding='utf-8', usecols=list(col.keys()), dtype=dt)
    df = df.rename(index=str, columns=col)
    return df

def get_CommandeProduits(path, prefix='CP_'):
    """
    Read CSV (CommandeProduits) into Dataframe. All relevant columns are kept and renamed with prefix.
    Args:
        path (str): file path to CommandeProduits.csv
        prefix (str): All relevant columns are renamed with prefix
    Returns:
        df (Dataframe): Resulting dataframe
    """
    col = {'Id':prefix+'Id',
           'Commande_Id':'Commande_Id',
           'OffreProduit_Id':'OffreProduit_Id',
           'QuantiteTotale':prefix+'QuantiteTotale',
           'QuantiteUnite':prefix+'QuantiteUnite',
           'QuantiteValeur':prefix+'QuantiteValeur',
           'MontantTotal':prefix+'MontantTotal',
           'Weight':prefix+'Weight'}
    dt = {'Id': 'int64',
          'Commande_Id': 'int64',
          'OffreProduit_Id':'int64',
          'QuantiteTotale':'float64',
          'QuantiteUnite':'object',
          'QuantiteValeur':'float64',
          'MontantTotal':'float64',
          'Weight':'float64'}
    df = pd.read_csv(path, sep='\t', encoding='utf-8', usecols=list(col.keys()), dtype=dt)
    df = df.rename(index=str, columns=col)
    return df

def get_Commandes(path, prefix = 'CO_'):
    """
    Read CSV (Commandes) into Dataframe. All relevant columns are kept and renamed with prefix.
    Args:
        path (str): file path to Commandes.csv
        prefix (str): All relevant columns are renamed with prefix
    Returns:
        df (Dataframe): Resulting dataframe
    """
    col = {'Id':prefix+'Id',
           'DateCommande':prefix+'DateCommande',
           'EstReceptionne':prefix+'EstReceptionne',
           'Statut':prefix+'Statut',
           'Offre_Id':'Offre_Id',
           'Recepteur_Id':'Recepteur_Id'}
    dt = {'Id':'int64',
           'DateCommande':'object',
           'EstReceptionne':'bool',
           'Statut':'int64',
           'Offre_Id':'int64',
           'Recepteur_Id':'int64'}
    date = ['DateCommande']
    df = pd.read_csv(path, sep='\t', encoding='utf-8', usecols=list(col.keys()), dtype=dt, parse_dates=date)
    df = df.rename(index=str, columns=col)
    return df

def get_Comptes(path, prefix = 'C_'):
    """
    Read CSV (Comptes) into Dataframe. All relevant columns are kept and renamed with prefix.
    Args:
        path (str): file path to Comptes.csv
        prefix (str): All relevant columns are renamed with prefix
    Returns:
        df (Dataframe): Resulting dataframe
    """
    col = {'Id':prefix+'Id',
           'Adresse_CodePostal':prefix+'Adresse_CodePostal',
           'Adresse_Ville':prefix+'Adresse_Ville',
           'Adresse_AdresseLigne1':prefix+'Adresse_AdresseLigne1',
           'Adresse_AdresseLigne2':prefix+'Adresse_AdresseLigne2',
           'Adresse_AdresseLigne3':prefix+'Adresse_AdresseLigne3',
           'Latitude':prefix+'Latitude',
           'Longitude':prefix+'Longitude',
           'Nom':prefix+'Nom',
           'TypeCompte':prefix+'TypeCompte'}
    dt = {'Id':'int64',
           'Adresse_CodePostal':'object',
           'Adresse_Ville':'object',
           'Latitude':'float64',
           'Longitude':'float64',
           'Nom':'object',
           'TypeCompte':'int64'}
    df = pd.read_csv(path, sep='\t', encoding='utf-8', usecols=list(col.keys()), dtype=dt)
    df = df.rename(index=str, columns=col)
    return df

def get_OffreProduits(path, prefix = 'OP_'):
    """
    Read CSV (OffreProduits) into Dataframe. All relevant columns are kept and renamed with prefix.
    Args:
        path (str): file path to OffreProduits.csv
        prefix (str): All relevant columns are renamed with prefix
    Returns:
        df (Dataframe): Resulting dataframe
    """
    col = {'Id':prefix+'Id',
           'Offre_Id':'Offre_Id',
           'Produit_Id':'Produit_Id',
           'EstInsecable':prefix+'EstInsecable',
           'EstUnDon':prefix+'EstUnDon',
           'QuantiteUnite':prefix+'QuantiteUnite',
           'QuantiteValeur':prefix+'QuantiteValeur',
           'QuantiteValeurParLot':prefix+'QuantiteValeurParLot'}
    dt = {'Id':'int64',
           'Offre_Id':'int64',
           'Produit_Id':'int64',
           'EstInsecable':'bool',
           'EstUnDon':'bool',
           'QuantiteUnite':'object',
           'QuantiteValeur':'float64',
           'QuantiteValeurParLot':'float64'}
    df = pd.read_csv(path, sep='\t', encoding='utf-8', usecols=list(col.keys()), dtype=dt)
    df = df.rename(index=str, columns=col)
    return df

def get_Offres(path, prefix = 'O_'):
    """
    Read CSV (Offres) into Dataframe. All relevant columns are kept and renamed with prefix.
    Args:
        path (str): file path to Offres.csv
        prefix (str): All relevant columns are renamed with prefix
    Returns:
        df (Dataframe): Resulting dataframe
    """
    col = {'Id':prefix+'Id',
           'Compte_Id':'Compte_Id'}
    dt = {'Id':'int64',
          'Compte_Id':'int64'}
    df = pd.read_csv(path, sep='\t', encoding='utf-8', usecols=list(col.keys()), dtype=dt)
    df = df.rename(index=str, columns=col)
    return df

def get_Produits(path, prefix = 'P_'):
    """
    Read CSV (Produits) into Dataframe. All relevant columns are kept and renamed with prefix.
    Args:
        path (str): file path to Produits.csv
        prefix (str): All relevant columns are renamed with prefix
    Returns:
        df (Dataframe): Resulting dataframe
    """
    col = {'Id':prefix+'Id',
           'Categorie_CategorieProduit_Id':'CategorieProduit_Id',
           'Compte_Compte_Id':'Compte_Id',
           'Ean':prefix+'EAN',
           'Nom':prefix+'Nom',
           'PoidsUnitaire':prefix+'PoidsUnitaire'}
    dt = {'Id':'int64',
          'Categorie_CategorieProduit_Id':'int64',
          'Compte_Compte_Id':'float64',
          'Ean':'object',
          'Nom':'object',
          'PoidsUnitaire':'float64'}
    df = pd.read_csv(path, sep='\t', encoding='utf-8', usecols=list(col.keys()), dtype=dt)
    df = df.rename(index=str, columns=col)
    return df


def merge_tables(df1, df2, on_col=[], col_name='', how='inner', del_col=True):
    """
    Merge two DataFrames on different column names
    Args:
        df1 (Dataframe): file path to Produits.csv
        df2 (Dataframe): 
        on_col (list)  : Name of the columns in df1 and df2 to merge on [df1_colname, df2_colname]
        col_name (str) : Rename the column used for merging
        how (str)      : type of merge ('inner', 'outer', 'left', 'right')
        del_col (bool) : Delete the columns used for merging (True or False)
    Returns:
        df (Dataframe): Resulting merged dataframe
    """
    # merge tables with different column names
    df1 = df1.rename(index=str, columns={on_col[0]:col_name})
    df2 = df2.rename(index=str, columns={on_col[1]:col_name})
    df = pd.merge(df1, df2, how=how)
    if del_col:
        df.drop(col_name, axis=1, inplace=True)
    return df

def merge_loop_tables(dict_merge):
    """
    Merge multiple DataFrame in sequence
    Args:
        dict_merge (list of dict): Merge sequence
            dict: {df2      = Dataframe to merge,
                   on_col   = Name of columns to merge on
                   col_name = Rename the column used for merging
                   how      = Type of merge ('inner', 'outer', 'left', 'right')
                   del_col  = Delete the columns used for merging (True or False)
    Returns:
        df (Dataframe): Resulting merged dataframe
    """
    # Starting with empty DataFrame
    df = pd.DataFrame(columns=['Id'])
    
    # Merge loop using merge_tables() function
    for merge_step in dict_merge:
        df = merge_tables(df,merge_step['df2'] ,
                             on_col=merge_step['on_col'], 
                             col_name=merge_step['col_name'],
                             how=merge_step['how'], 
                             del_col=merge_step['del_col'])
        print('----> STEP ---->')
        print(list(df.columns))
        print(len(df))
    return df

##############################################################
### List of functions used for cleaning Comptes table and 
### geo positionning data (Longitidue and Latitude)
##############################################################
def geotag_Compte(df, prefix='', IGN_API=''):
    """
    This function corrects Phenix original geo coordinates (longitude and latitude).
    This function uses IGN geocoding API to convert adresses into Longitude and Latitude coordinates. 
    Args:
        df (DataFrame): 'Comptes' DataFrame
        prefix (str): Prefix used in the 'Comptes' DataFrame
        IGN_API (str): IGN API key needed to access to IGN geocoding API
    Returns:
        df_matrix (DataFrame): Simplified version of 'Comptes' DataFrame with the following columns
            Nom              = Account name as in PhenixDB
            AdresseLigne3    = Account address as in PhenixDB
            Ville            = Account city as in PhenixDB
            CodePostal       = Account postal code as in PhenixDB
            old_lon, old_lat = Account original geo coordinate as in PhenixDB
            new_lon, new_lat = Account recalculated geo coordinate from IGN
            delta            = Distance (km) between old and new geo coordinates
    """
    from geopy.geocoders import Nominatim, IGNFrance
    from geopy.distance import lonlat, distance

    geolocator = IGNFrance(api_key=IGN_API, referer='localhost', user_agent='Agent_tests')
    matrix = []
    
    for index, value in df.iterrows():
        i = value[prefix+'Id']
        adresse1 = '' if str(value[prefix+'Adresse_AdresseLigne1'])=='nan' else str(value[prefix+'Adresse_AdresseLigne1'])
        adresse2 = '' if str(value[prefix+'Adresse_AdresseLigne2'])=='nan' else str(value[prefix+'Adresse_AdresseLigne2'])
        adresse3 = '' if str(value[prefix+'Adresse_AdresseLigne3'])=='nan' else str(value[prefix+'Adresse_AdresseLigne3'])
        ville = '' if str(value[prefix+'Adresse_Ville'])=='nan' else str(value[prefix+'Adresse_Ville'])
        CP = '' if str(value[prefix+'Adresse_CodePostal'])=='nan' else str(value[prefix+'Adresse_CodePostal'])
        query = adresse3 + ',' + ville + ',' + CP
        
        # check if geolocation is found
        try:
            location = geolocator.geocode(query,maximum_responses=1,exactly_one=True)
        except:
            print('(%s) %s --> location not found' % (i, query))
            element= dict(Id = value[prefix+'Id'],
                      delta=None,
                      Nom=value[prefix+'Nom'],
                      adresse1=value[prefix+'Adresse_AdresseLigne1'],
                      adresse2=value[prefix+'Adresse_AdresseLigne2'],
                      adresse3=value[prefix+'Adresse_AdresseLigne3'],
                      ville=value[prefix+'Adresse_Ville'],
                      CP=value[prefix+'Adresse_CodePostal'],
                      old_lon=value[prefix+'Longitude'],
                      old_lat=value[prefix+'Latitude'],
                      new_lon=None,
                      new_lat=None)
            matrix.append(element)
            continue
            
        # calculate distance old vs new geolocation
        old_lonlat = (value[prefix+'Longitude'], value[prefix+'Latitude'])
        new_lonlat = (location.longitude, location.latitude)
        delta = calc_geodistance(lonlat1=old_lonlat, lonlat2=new_lonlat)
        #### delta = distance(lonlat(*old_lonlat), lonlat(*new_lonlat)).km 
                                   
        element = dict(Id = value[prefix+'Id'],
                      delta=delta,
                      Nom=value[prefix+'Nom'],
                      adresse1=value[prefix+'Adresse_AdresseLigne1'],
                      adresse2=value[prefix+'Adresse_AdresseLigne2'],
                      adresse3=value[prefix+'Adresse_AdresseLigne3'],
                      ville=value[prefix+'Adresse_Ville'],
                      CP=value[prefix+'Adresse_CodePostal'],
                      old_lon=value[prefix+'Longitude'],
                      old_lat=value[prefix+'Latitude'],
                      new_lon=location.longitude,
                      new_lat=location.latitude)
        matrix.append(element)
    df_matrix = pd.DataFrame.from_dict(matrix)
    return df_matrix

def calc_geodistance(lonlat1=(), lonlat2=()):
    from geopy.distance import lonlat, distance
    
    dist = distance(lonlat(*lonlat1), lonlat(*lonlat2)).km 
    return dist

def manual_geotag(df_matrix):
    '''
    This function manually corrects geotags of Phenix accounts
    Args:
        df_matrix (DataFrame): DataFrame resulting of geotag_Comptes()
    Returns:
        df_matrix (DataFrame): Corrected geotags
    '''
    dict_manual = [
                   dict(Id=1880,new_lon=0.09723,new_lat=48.43538), # Carrefour Market - Alençon
                   dict(Id=2418,new_lon=2.35436,new_lat=48.84016), # Franprix SEBASTOPOL 5651
                   dict(Id=2438,new_lon=2.35781,new_lat=48.87406), # Franprix MAGENTA DISTR 5200
                   dict(Id=2440,new_lon=2.4097477,new_lat=48.8554594), # Franprix SOGI VINGT 5209
                   dict(Id=2468,new_lon=2.37312,new_lat=48.84913), # Franprix SUPERANT 6241
                   dict(Id=1970,new_lon=2.0014673,new_lat=43.45391), # Restos du coeur 31 - Centre de Revel
                   dict(Id=2555,new_lon=2.409748,new_lat=48.855459), # Intermarché Baratier
                   dict(Id=1983,new_lon=0.09723,new_lat=48.43538), # Banque Alimentaire 87o
                   dict(Id=2074,new_lon=2.001467,new_lat=43.45391), # SCF 78 Maisons Lafitte
                   dict(Id=2533,new_lon=2.35436,new_lat=48.84016), # RDC 25 Valdahon
                   dict(Id=2553,new_lon=2.35781,new_lat=48.87406), # CHU Altho
                   dict(Id=2583,new_lon=2.37312,new_lat=48.84913), # RdC 37 Joué-les-Tours
                   ]
    for c in dict_manual:
        # Apply manual correction to df_matrix
        index = df_matrix[df_matrix.Id == c['Id']].index[0]
        df_matrix.loc[(index),['new_lat']] = c['new_lat']
        df_matrix.loc[(index),['new_lon']] = c['new_lon']

        # Calculate distance
        old_lat = df_matrix.loc[(index)].get_value('old_lat')
        old_lon = df_matrix.loc[(index)].get_value('old_lon')
        delta = calc_geodistance(lonlat1=(old_lon, old_lat), lonlat2=(c['new_lon'], c['new_lat']))
        df_matrix.loc[(index),['delta']] = delta
    return df_matrix

def replace_geotag(df, df_matrix, prefix='', threshold=1):
    """
    Using the df_matrix from geotag_Compte(), this function replaces old to new geo coordinates.
    It uses a threshold distance over which the old are replaced by new coordinates
    Args:
        df (DataFrame): 'Comptes' DataFrame
        df_matrix (DataFrame): DataFrame resulting of geotag_Comptes()
        prefix (str): Prefix used in the 'Comptes' DataFrame
        threshold (int): Threshold distance over which the old are replaced by new coordinates
    Returns:
        df (DataFrame): Simplified Comptes DataFrame with the following columns
    """
    # loop on geocoded elements that are further than the threshold
    for index, value in df_matrix[df_matrix.delta > threshold].iterrows():
        df_index = df[(df[prefix+'Id']==value.Id)].index

        df.loc[list(df_index),[prefix+'Longitude']] = value.new_lon
        df.loc[list(df_index),[prefix+'Latitude']] = value.new_lat
    
    # loop on elements that couldn't be geocoded
    for index, value in df_matrix[df_matrix.delta.isnull()].iterrows():
        df_index = df[(df[prefix+'Id']==value.Id)].index

        df.loc[list(df_index),[prefix+'Longitude']] = value.old_lon
        df.loc[list(df_index),[prefix+'Latitude']] = value.old_lat
    print('%d coordinates has been updated of %d' % (len(df_matrix[df_matrix.delta > threshold]), len(df_matrix)))
    
    return df

def plot_df_matrix(df_matrix):
    """
    Plot a map of all Phenix accounts before and after geocoding.
    This function requires plotly.
    Args:
        df_matrix (DataFrame): DataFrame resulting of geotag_Comptes()
    Returns:
        Map plot from Plotly
    """
    import plotly
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    init_notebook_mode()
    
    trace_new = {
        'type':'scattergeo',
        'lat':df_matrix.new_lat.values.tolist(),
        'lon':df_matrix.new_lon.values.tolist(),
        'text':df_matrix.Nom.values.tolist(),
        'name':'NEW',
        'marker':{
            'color': 'blue',
        },
        'mode':'markers'
    }
    trace_old = {
        'type':'scattergeo',
        'lat':df_matrix.old_lat.values.tolist(),
        'lon':df_matrix.old_lon.values.tolist(),
        'text':df_matrix.Nom.values.tolist(),
        'name': 'OLD',
        'marker':{
            'color': 'red',
            'symbol':'x'
        },
        'mode':'markers'
    }
    layout = dict(
            title = 'Comparaison des positions des comptes (avant/après correction par geocoding)',
            width = 800,
            geo = dict(
                scope='europe',
                resolution=50,
                center= {'lon':2,'lat':46.5},
                framewidth=700,
                showland = True,
                landcolor = 'rgb(243, 243, 243)',
                countrycolor = 'rgb(204, 204, 204)'
                ),
        )

    fig = dict( data=[trace_old, trace_new], layout=layout)
    plotly.offline.iplot(fig) 
    return fig