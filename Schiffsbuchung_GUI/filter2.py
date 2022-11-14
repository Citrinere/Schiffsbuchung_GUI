# Excel Datei einlesen
# Quelle: https://bodo-schoenfeld.de/excel-daten-mit-python-einlesen/

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

DATA_FILE = "../Aufgabe 2 Reiseportal/Schiffreisen.xlsx"

# Create a Pandas Dataframe
# (read the Excel data with Pandas)
df = pd.read_excel(DATA_FILE)

# print the first five rows
print(df.head(20))

#df_cleaned = df.dropna(how='all')
#df_years = df_cleaned['Jahr'].astype(np.uint16)

#x = df_years.values
#y = df_cleaned['Arbeitslose'].values  # no value for 1993

#fig, ax = plt.subplots()

#plt.title("Arbeitslose in Kiel\n(1989 - 2016)", size="x-large")
#plt.ylabel("Arbeitslose", size="x-large")
#plt.xlabel("Jahr", size="x-large")

#plt.plot(y, "r*-", markersize=6, linewidth=1, color='r')

#ax.set_xticks(range(len(x)))
#ax.set_xticklabels(x, rotation='vertical')

plt.show()
print()
print("End of Excel reading with panda")
print()
# Mögliche bessere Alternative mit openpyxl
# Quelle: https://bodo-schoenfeld.de/excel-daten-mit-pythons-openpyxl-modul-lesen/

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import expanduser
import openpyxl
import sys

FILE_PATH = expanduser('~') + '\OneDrive\Dokumente\GitHub\Schiffsbuchung_GUI\Aufgabe 2 Reiseportal\Schiffreisen.xlsx'

try:
    excel_file = openpyxl.load_workbook(FILE_PATH)
except IOError as e:
    print("ERROR: {0}".format(e))
    sys.exit()

# excel_file = openpyxl.load_workbook('G_IV_3_m1908_SH.xlsx')

excel_sheet = excel_file['Tabelle1']

# Nur einen Einzelnen Wert auslesen
value = excel_sheet['F15'].value
print("Der Wert von F15 lautet: {0}".format(value))

# Ganze Tabelle als Liste einfügen
cell_values = []

#Original Schleife
#for row_of_cells in excel_sheet['A2':'H22']:
 #   for cell in row_of_cells:
  #      cell_values.append(cell.value)

# Original Schleife liest alle Daten im ausgewälten Zellenbereich aus und packt diese in eine Liste als einzelne Werte
# Problem: Nach jedem 8tem Wert eine unterliste erzeugen für die Gesamt Liste
helpList = []
for row_of_cells in excel_sheet['A2':'H22']:
    for cell in row_of_cells:
        cell_values.append(cell.value)
        for cell in range(8):
            helpList.append(cell_values)
            cell_values = []

print(cell_values)
print(helpList)
print()
print("End of openpyxl")
print()
# ==================================================================================================================
# Verkettete Listen mit List Typen erstellen

# 1. Test Versuch
excelDateien = list
excelDateien = ["Das", "ist", "ein", "Test"]
reisenListe = list
reisenListe = [["Mein Schiff", "Mittelmeer", "10", "Innenkabine"], ["Aida", "Ostsee", "8", "Außenkabine"]]

print(excelDateien)
print(reisenListe)

reisenListe.append(excelDateien)
print(reisenListe)
print(reisenListe[-1])