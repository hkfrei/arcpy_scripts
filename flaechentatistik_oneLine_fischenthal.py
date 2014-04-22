#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Test with multidimensional arrays
#
# Author:      Hanskaspar
#
# Created:     19.04.2014
# Copyright:   (c) Hanskaspar 2014
#-------------------------------------------------------------------------------
import arcpy
arcpy.env.workspace = "D:\\gis\\fischenthal\\flaechenstatistikTest_Hoerndli\\scratch.gdb"

featureClass = "StatistikResult2"
fieldList = "HL_Neigung;Code;Nummer_1;Shape_Area;NeigungInt;KEY"

outFile = open("D:\\gis\\fischenthal\\flaechenstatistikTest_Hoerndli\\statResult.txt","w")
outFile.write("PrzNummer;" + "Code;" + "kl_18%;" + "18-35%;" + "gr_35-50%;" + "gr_50%;" + "\n" )

#===============================================================================
# Wichtig: maximale Anzahl Features die es im Resultat hat
#===============================================================================
anzahlMoeglichkeiten = 9

#===============================================================================
# Funktionsdefinitionen
#===============================================================================
def getArrayValues(pCursor, pRow, pKey, pArray):
    """Put the values from a row element in a array"""
    pArray[0] = pRow.Nummer_1
    pArray[1] = str(pRow.Code)


    while pRow is not None and pKey == pRow.KEY:
        print(pRow.NeigungInt)
        if pRow.NeigungInt == 1:
            print("<18% " + str(pRow.Shape_Area)[0:8])
            pArray[2] = str(pRow.Shape_Area)[0:8]
        elif pRow.NeigungInt == 2:
            print("18-35% "+ str(pRow.Shape_Area)[0:8])
            pArray[3] = str(pRow.Shape_Area)[0:8]
        elif pRow.NeigungInt == 3:
            print("35-50% "+ str(pRow.Shape_Area)[0:8])
            pArray[4] = str(pRow.Shape_Area)[0:8]
        elif pRow.NeigungInt == 4 :
            print(">50% "+ str(pRow.Shape_Area)[0:8])
            pArray[5] = str(pRow.Shape_Area)[0:8]
        pRow = pCursor.next()
    print("=================")
    outFile.write(str(pArray[0]) + ";" + str(pArray[1]) + ";"+ str(pArray[2]) + ";"+ str(pArray[3]) + ";"+ str(pArray[4]) + ";" +  str(pArray[5]) + ";"  + "\n")

#===============================================================================
def test(pCursor, pRow, pKey):
    while pRow is not None and pKey == pRow.KEY:
        print(pRow.KEY + ": " + str(pRow.NeigungInt))
        pRow = pCursor.next()



#===============================================================================
# Search Cursor
#===============================================================================
searchCur = arcpy.SearchCursor(featureClass,"","",fieldList,"KEY A, NeigungInt A")
row = searchCur.next()
i = 1
while i <= anzahlMoeglichkeiten and row:
    key = row.KEY
    array = [0]*6
    getArrayValues(searchCur, row, key, array)
##    test(searchCur,row,key)
    i = i+1
    print i
#print(array)



#===============================================================================
# AUFRAEUMEN
#===============================================================================
outFile.close
del outFile
#del multiArray
#del array

print("finished")


