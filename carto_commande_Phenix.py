import phenix_mgt as phnx
import off_mgt as off
import pandas as pd
import dask
import dask.dataframe as dd

# Do this only once to save SQL table into CSV files
# You will need to install Phenix SQL DB (.bak) into your local computer
phnx.extract_Phenix_SQLtable2CSV(path='./Phenix_DB/')

# List of Phenix tables
lst_table = ['CategorieProduits',
            'CommandeProduits',
            'Commandes',
            'Comptes',
            'OffreProduits',
            'Offres',
            'Produits']

# Import each table one by one
# 'Comptes' table is imported twice for both 'Emetteur' (EC_) and 'Receveur' (RC_)
df_catP = phnx.get_CategorieProduits('./Phenix_DB/' + lst_table[0] + '.csv', prefix='catP_')
df_CP   = phnx.get_CommandeProduits ('./Phenix_DB/' + lst_table[1] + '.csv', prefix='CP_')
df_CO   = phnx.get_Commandes        ('./Phenix_DB/' + lst_table[2] + '.csv', prefix='CO_')
df_EC   = phnx.get_Comptes          ('./Phenix_DB/' + lst_table[3] + '.csv', prefix='EC_')
df_RC   = phnx.get_Comptes          ('./Phenix_DB/' + lst_table[3] + '.csv', prefix='RC_')
df_OP   = phnx.get_OffreProduits    ('./Phenix_DB/' + lst_table[4] + '.csv', prefix='OP_')
df_O    = phnx.get_Offres           ('./Phenix_DB/' + lst_table[5] + '.csv', prefix='O_')
df_P    = phnx.get_Produits         ('./Phenix_DB/' + lst_table[6] + '.csv', prefix='P_')

# Add food group to Product table
df_P = phnx.add_foodgroup(df_P,csv_path='./OFF_DB/mehdi_phenix_foodgroup.csv')
df_P.to_csv('./Phenix_DB_clean/Produits.csv',sep='\t',encoding='utf-8')

# Add quantity to Product table
df_P = phnx.add_product_qty(df_P)
df_P = phnx.get_qty_from_PhenixCol(df_P)
df_P = phnx.extrapolate_qty_from_productvalue(df_P,df_OP,df_CP)
OFF_csv = './OFF_DB/fr.openfoodfacts.org.products.csv'
df_P = phnx.get_qty_from_OFF(df_P,OFF_csv=OFF_csv)
df_P.reset_index(drop=True,inplace=True)

# Correct GPS coordinates in Comptes
#df_geo_matrix = phnx.geotag_Compte(df_EC,prefix='EC_',IGN_API='YOUR_API_KEY')
#df_geo_matrix.to_csv('./Phenix_DB/df_geo_matrix.csv',sep='\t',encoding='utf-8')
# Manually correct geo coordinates (function manual_geotag())
df_geo_matrix = pd.read_csv('./Phenix_DB/df_geo_matrix.csv',sep='\t',encoding='utf-8',index_col=0)
df_geo_matrix = phnx.manual_geotag(df_geo_matrix)
# Apply correction into df_EC et df_RC
df_EC_corr = phnx.replace_geotag(df_EC,df_geo_matrix,prefix='EC_', threshold=1)
df_RC_corr = phnx.replace_geotag(df_RC,df_geo_matrix,prefix='RC_', threshold=1)

# Save the cleaned tables
phenix_clean_path = './Phenix_DB_clean/'
df_catP.to_csv(phenix_clean_path + lst_table[0] + '.csv',sep='\t',encoding='utf-8')
df_CP.to_csv  (phenix_clean_path + lst_table[1] + '.csv',sep='\t',encoding='utf-8')
df_CO.to_csv  (phenix_clean_path + lst_table[2] + '.csv',sep='\t',encoding='utf-8')
df_EC.to_csv  (phenix_clean_path + 'EC' + lst_table[3] + '.csv',sep='\t',encoding='utf-8')
df_RC.to_csv  (phenix_clean_path + 'RC' + lst_table[3] + '.csv',sep='\t',encoding='utf-8')
df_OP.to_csv  (phenix_clean_path + lst_table[4] + '.csv',sep='\t',encoding='utf-8')
df_O.to_csv   (phenix_clean_path + lst_table[5] + '.csv',sep='\t',encoding='utf-8')
df_P.to_csv   (phenix_clean_path + lst_table[6] + '.csv',sep='\t',encoding='utf-8')

###############################################
# Built json for geo plot
###############################################

# Join all tables of Commande
dict_merge = [{'df2':df_CP, 'on_col': ['Id','CP_Id'],                   'col_name':'CP_Id'  , 'how':'right','del_col':False},
              {'df2':df_CO, 'on_col': ['Commande_Id','CO_Id'],          'col_name':'temp_Id', 'how':'left', 'del_col':True},
              {'df2':df_RC, 'on_col': ['Recepteur_Id','RC_Id'],         'col_name':'RC_Id'  , 'how':'left', 'del_col':False},
              {'df2':df_O,  'on_col': ['Offre_Id','O_Id'],              'col_name':'temp_Id', 'how':'left', 'del_col':True},
              {'df2':df_EC, 'on_col': ['Compte_Id','EC_Id'],            'col_name':'EC_Id'  , 'how':'left', 'del_col':False},
              {'df2':df_OP, 'on_col': ['OffreProduit_Id','OP_Id'],      'col_name':'temp_Id', 'how':'left', 'del_col':True},
              {'df2':df_P,  'on_col': ['Produit_Id','P_Id'],            'col_name':'temp_Id', 'how':'left', 'del_col':True},]
df_Phenix = phnx.merge_loop_tables(dict_merge)

# Filter Commande status 1 (accepted) and 4 (completed)
df_Phenix = df_Phenix[(df_Phenix.CO_Statut==1) | (df_Phenix.CO_Statut==4)]
# Add distance column between Emetteur and Recepteur
# df_Phenix = phnx.calc_distance(df_Phenix)

# Prepare JSON data
geo_hubs = df_Phenix[['EC_Latitude','EC_Longitude','EC_Nom','RC_Latitude','RC_Longitude','RC_Nom']]

geo_EC = df_Phenix[['EC_Latitude','EC_Longitude','EC_Nom']].drop_duplicates()
geo_EC['Coordinates'] = geo_EC.apply(lambda row: [row.EC_Latitude, row.EC_Longitude],axis=1)
geo_EC = geo_EC.drop(['EC_Latitude','EC_Longitude'],axis=1)
geo_EC = geo_EC_1.rename(columns={'EC_Nom':'Nom'},)

geo_RC = df_Phenix[['RC_Latitude','RC_Longitude','RC_Nom']].drop_duplicates()
geo_RC['Coordinates'] = geo_RC.apply(lambda row: [row.RC_Latitude, row.RC_Longitude],axis=1)
geo_RC = geo_RC.drop(['RC_Latitude','RC_Longitude'],axis=1)
geo_RC = geo_RC_1.rename(columns={'RC_Nom':'Nom'},)

lst_line = []
geo_hubs = geo_hubs.groupby(geo_hubs.columns.tolist(),as_index=False).size()
for index, count in geo_hubs[geo_hubs.values>10].iteritems(): # print line if there are minimum 10 commands
    dict_line = {
        'from'   : ([index[0],index[1]]),
        'to'     : ([index[3],index[4]]),
        'count'  : count,
        'text'   : index[2]+' >> '+ index[5]+ ' ('+str(count)+')'
    }
    lst_line.append(dict_line)
geo_line = pd.DataFrame(lst_line)

# Save into json files for graph
now = (pd.datetime.now().date())
geo_EC.to_json  ('./json/%s_EC_coordinates.json' % now)
geo_RC.to_json  ('./json/%s_RC_coordinates.json' % now)
geo_line.to_json('./json/%s_geo_commandes.json' % now)