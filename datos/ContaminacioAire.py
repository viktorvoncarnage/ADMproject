# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 16:53:08 2022

@author: sergi
"""

import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
##client = Socrata("analisi.transparenciacatalunya.cat", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(analisi.transparenciacatalunya.cat,
#                  MyAppToken,
#                  username="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
##results = client.get("tasf-thgu", limit=550000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df = results_df.loc[:510758, :]
results_Barcelones = results_df.loc[(results_df['nom_comarca'].str.startswith('Barcelon'))]

r_PM = results_Barcelones.loc[(results_Barcelones['contaminant'].str.startswith('PM'))]

r_NO2 = results_Barcelones.loc[(results_Barcelones['contaminant'].str.startswith('NO2'))]

r_O3 = results_Barcelones.loc[(results_Barcelones['contaminant'].str.startswith('O3'))]

r_SO2 = results_Barcelones.loc[(results_Barcelones['contaminant'].str.startswith('SO2'))]

pathH = 'C:\\Users\\sergi\\OneDrive\\Escritorio\\Sergi\\Masters\\Analisi Dades Masives\\'
r_PM.to_csv(pathH + 'datosPM.csv', encoding='utf-8', index=False)
r_NO2.to_csv(pathH + 'datosNO2.csv', encoding='utf-8', index=False)
r_O3.to_csv(pathH + 'datosO3.csv', encoding='utf-8', index=False)
r_SO2.to_csv(pathH + 'datosSO2.csv', encoding='utf-8', index=False)

