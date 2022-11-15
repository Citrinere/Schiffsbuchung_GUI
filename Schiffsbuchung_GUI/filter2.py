# ==================================================================================================================
# Datei zum Auslesen und Filtern der Excel Datei
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
print()
# ==================================================================================================================

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
print(df.head(21))
df_cleaned = df.dropna(how='all')


testValue = []
testValue.append(df.head(21))

print(testValue)
print("End of Excel reading with panda")
print()


# ==================================================================================================================

# Mögliche bessere Alternative mit openpyxl
# Quelle: https://bodo-schoenfeld.de/excel-daten-mit-pythons-openpyxl-modul-lesen/

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os.path import expanduser
import openpyxl
import sys

# Ich glaube hier wird auf den Pfad referenziert vom Home/User Directory, muss man noch schauen ob man das noch umändern kann
FILE_PATH = expanduser('~') + '\OneDrive\Dokumente\GitHub\Schiffsbuchung_GUI\Aufgabe 2 Reiseportal\Schiffreisen.xlsx'

try:
    excel_file = openpyxl.load_workbook(FILE_PATH)  # Laden der Excel Datei aus vorgegebenen Dateipfad
except IOError as e:                                # Bei Falschem Dateipfad Fehlermeldung
    print("ERROR: {0}".format(e))
    sys.exit()

# excel_file = openpyxl.load_workbook('G_IV_3_m1908_SH.xlsx')

excel_sheet = excel_file['Tabelle1']                # Excel Verknüpfung, welches Tabellen-Blatt verwendet werden soll

value = excel_sheet['F15'].value                    # Nur einen Einzelnen Wert auslesen
print("Ausgabe von einer einzelnen Zelle:\n""Der Wert von F15 lautet: {0}".format(value))

# Ganze Tabelle als Liste einfügen
cell_values = []                                    # Liste zum Speichern der Werte jeder einzelnen Excel Zelle

# Original Schleife !!! Nicht Verändern !!!
#for row_of_cells in excel_sheet['A1':'H22']:
 #   for cell in row_of_cells:
  #      cell_values.append(cell.value)

# Original Schleife liest alle Daten im ausgewählten Zellenbereich aus und packt diese in eine Liste als einzelne Werte
# Problem: Nach jedem 8tem Wert eine unterliste erzeugen für die Gesamt Liste
excelList = []                                      # Liste zum Speichern der Unterlisten der einzelnen Datenzeilen

for row_of_cells in excel_sheet['A1':'H22']:        # For-Schleife durchläuft angegebene Excel Bereich durch
    for cell in row_of_cells:                       # For-Schleife für jede Zelle führe Folgende aktion aus:
        cell_values.append(cell.value)              # Daten aus Zelle auslesen
        if cell_values.__len__() == 8:              # Nach jeder 8. Zelle, als Unterliste in excelList abspeichern
            excelList.append(cell_values)
            cell_values = []

#print(cell_values)
print("Komplette Excel Liste:", excelList)
counter = 0
while counter < excelList.__len__():
    print(excelList[counter])
    counter = counter + 1
    #end while
print("Beispiel Ausgabe von Datensatz 5", excelList[5])
print("Beispiel Ausgabe von Datensatz 2 & 3 (slicing)", excelList[2:4])
print()
print("End of Excel reading with openpyxl")
print()
#meerFilter = input("Geben Sie ein Reisegebiet an (Ostsee/Nordsee/Mittelmeer): ")
#listValues = ["Ostsee"]
#listValues.append()


#print("Hier Ihre möglichen Reisen gefiltert nach Ihrem Reisegebiet:")
counter = 0
#while counter < listValues.__len__():
 #   print(listValues[counter])
  #  counter = counter + 1
    #end while
counter = 0

# ==================================================================================================================
