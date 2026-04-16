import pandas as pd
import numpy as np

# Citire fisier local
df = pd.read_csv('student-mat.csv', sep=';')

# Eliminare coloane direct din df
coloane_de_eliminat = [
    'Mjob', 'Fjob', 'reason', 'guardian',
    'famsize', 'Pstatus', 'Medu', 'Fedu',
    'traveltime', 'activities', 'nursery',
    'higher', 'famrel', 'health'
]

df.drop(columns=coloane_de_eliminat, inplace=True)

df.rename(columns={
    'school'    : 'Scoala',
    'sex'       : 'Sex',
    'age'       : 'Varsta',
    'address'   : 'Mediu',
    'studytime' : 'Ore_Studiu',
    'failures'  : 'Materii_Picate',
    'schoolsup' : 'Meditatii_Scoala',
    'famsup'    : 'Ajutor_Familie',
    'paid'      : 'Meditatii_Private',
    'internet'  : 'Internet',
    'romantic'  : 'Relatie',
    'freetime'  : 'Timp_Liber',
    'goout'     : 'Iesiri',
    'Dalc'      : 'Alcool_Saptamana',
    'Walc'      : 'Alcool_Weekend',
    'absences'  : 'Absente',
    'G1'        : 'Nota_T1',
    'G2'        : 'Nota_T2',
    'G3'        : 'Nota_Finala'
}, inplace=True)

# Verificare
print("Coloane rămase:", df.columns.tolist())
print("Dimensiune dataset:", df.shape)
print(df.head())
df[['Nota_T1', 'Nota_T2', 'Nota_Finala']] = df[['Nota_T1', 'Nota_T2', 'Nota_Finala']].replace(0, np.nan)


df.to_csv('student_procesat.csv', index=False)
print("Salvat cu succes!")