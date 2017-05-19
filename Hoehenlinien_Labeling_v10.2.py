# -*- coding: cp1252 -*-
# ---------------------------------------------------------------------------
# HoehenlinienToolbox.py
# Created on: Mo Jan 16, 2012
# Lisag AG, 6460 Altdorf, Hanskaspar Frei
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
import arcinfo

arcpy.AddMessage("")
arcpy.AddMessage("*******************************************************************************")
arcpy.AddMessage("LISAG, 6460 ALTDORF.")
arcpy.AddMessage("SKRIPT ZUM ERSTELLEN UND GLAETTEN VON HOEHENKURVEN")
arcpy.AddMessage("Anschliessend Export nach DXF mit Labeling und Hoehenangabe in Attribut Elevation")
arcpy.AddMessage("*******************************************************************************")
arcpy.AddMessage("")
try:
    arcpy.AddMessage("arcpy importiert und Lizenz auf arcinfo gesetzt")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")

    # Check out any necessary licenses
    extension = arcpy.CheckOutExtension("Spatial")
    arcpy.AddMessage("Spatial Analyst Lizenz aktiviert, Antwort des Programms: " + extension)
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")

    # Overwrite existing Output
    arcpy.env.overwriteOutput = True

    #get the Installation Path Variables to access the Tooboxes
    installInfo = arcpy.GetInstallInfo()
    InstPath = installInfo["InstallDir"]

    # Load required toolboxes...

    arcpy.ImportToolbox(InstPath + "ArcToolbox\\Toolboxes\\Spatial Analyst Tools.tbx")
    arcpy.AddMessage("Spatial Analyst Toolbox geladen ")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")


    # Local variables...
    cont_orig1 = "Y:\\Projekte\\Geodaten\\Hoehen\\DTM_DOM_AWG\\Scratch\\Scratch.gdb\\cont_orig1"

    OutputSmoothLine = "Y:\\Projekte\\Geodaten\\Hoehen\\DTM_DOM_AWG\\Scratch\\Scratch.gdb\\ContSmoo_orig1"

    OutputEndPoints = "Y:\\Projekte\\Geodaten\\Hoehen\\DTM_DOM_AWG\\Scratch\\Scratch.gdb\\hkurvEndPoints"

    OutputMidPoints = "Y:\\Projekte\\Geodaten\\Hoehen\\DTM_DOM_AWG\\Scratch\\Scratch.gdb\\hkurvMidPoints"

    DTM_GRID_2m_Uri = "Y:\\Projekte\\Geodaten\\Hoehen\\DTM_AKTUELL.gdb\\DTM_KOMBINIERT"

    ScratchRaster1 = "Y:\\Projekte\\Geodaten\\Hoehen\\DTM_AKTUELL.gdb\\DTMscratch"

    projectedOutputLines = "Y:\\Projekte\\Geodaten\\Hoehen\\DTM_DOM_AWG\\Scratch\\Scratch.gdb\\ContSmoo_lv95"

    projectedOutputPoints = "Y:\\Projekte\\Geodaten\\Hoehen\\DTM_DOM_AWG\\Scratch\\Scratch.gdb\\Points_lv95"

##    Perimeter = "Y:\\Projekte\\tmp\\converted_Graphics_2.shp"
##    Aequidistanz ="1"
##    SmoothToleranz = "2"
##    OutputDXF = "D:\\gaga\\Test_lv95.DXF"
    Perimeter       = arcpy.GetParameterAsText(0)
    Aequidistanz    = arcpy.GetParameterAsText(1)
    SmoothToleranz  = arcpy.GetParameterAsText(2)
    OutputDXF       = arcpy.GetParameterAsText(3)

    arcpy.AddMessage("Perimeter aus DTM ausschneiden")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Process: Extract by Mask...
    arcpy.ExtractByMask_sa(DTM_GRID_2m_Uri, Perimeter, ScratchRaster1)

    arcpy.AddMessage("Original Hoehenlinien erstellen")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Process: Contour...
    arcpy.Contour_sa(ScratchRaster1, cont_orig1, Aequidistanz, "450", "1")

    arcpy.AddMessage("Hoehenlinien glaetten")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Process: Smooth Line...
    arcpy.SmoothLine_cartography(cont_orig1, OutputSmoothLine, "PAEK", SmoothToleranz + " Meters", "NO_FIXED", "NO_CHECK")

    arcpy.AddMessage("Linien End- und Mittelpunkte in Punkte Feature Class konvertieren")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Process: Feature Vertices To Points (End Points)...
    arcpy.FeatureVerticesToPoints_management(OutputSmoothLine, OutputEndPoints, "BOTH_ENDS")

    # Process: Feature Vertices To Points (Mid Points)...
    arcpy.FeatureVerticesToPoints_management(OutputSmoothLine, OutputMidPoints, "MID")

    # Process: Append...
    arcpy.Append_management(OutputMidPoints, OutputEndPoints,"TEST", "", "")

    arcpy.AddMessage("Transformation nach LV95")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Projektionsobjekte definieren
    lv95 = arcpy.SpatialReference(2056)
    ch1903 = arcpy.SpatialReference(21781)
    transformation = "CH1903_To_CH1903+_1_NTv2"

    #Geodaten transformieren nach LV95
    arcpy.Project_management(OutputSmoothLine, projectedOutputLines, lv95, transformation, ch1903)
    arcpy.Project_management(OutputEndPoints, projectedOutputPoints, lv95, transformation, ch1903)

    arcpy.AddMessage("Feld CADType hinzufuegen")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Process: Add Field...
    arcpy.AddField_management(projectedOutputPoints, "CADType", "TEXT", "", "", "20", "", "NULLABLE", "NON_REQUIRED", "")

    arcpy.AddMessage("Feld CADType berechnen")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Process: Calculate Field...
    arcpy.CalculateField_management(projectedOutputPoints, "CADType", "\"TEXT\"", "VB", "")

    arcpy.AddMessage("Feld TxtValue hinzufuegen")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Process: Add Field (2)...
    arcpy.AddField_management(projectedOutputPoints, "TxtValue", "TEXT", "", "", "20", "", "NULLABLE", "NON_REQUIRED", "")

    arcpy.AddMessage("Feld TxtValue berechnen")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Process: Calculate Field (2)...
    arcpy.CalculateField_management(projectedOutputPoints, "TxtValue", "[CONTOUR]", "VB", "")

    arcpy.AddMessage("CAD spezifische Felder hinzufuegen")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Process Set CAD Alias.....
    arcpy.AddCADFields_conversion(projectedOutputLines, "ADD_ENTITY_PROPERTIES","NO_LAYER_PROPERTIES","NO_TEXT_PROPERTIES","NO_DOCUMENT_PROPERTIES","NO_XDATA_PROPERTIES")

    arcpy.AddMessage("Feld Elevation berechnen")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Process: Calculate Field (2)...
    arcpy.CalculateField_management(projectedOutputLines, "Elevation", "[CONTOUR]", "VB", "")

    arcpy.AddMessage("Feld Width berechnen")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Process: Calculate Field (2)...
    arcpy.CalculateField_management(projectedOutputLines, "Width", "[Shape_Length]", "VB", "")



    arcpy.AddMessage("Export to CAD")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    # Process: Export to CAD...
    arcpy.ExportCAD_conversion("Y:\\Projekte\\Geodaten\\Hoehen\\DTM_DOM_AWG\\Scratch\\Scratch.gdb\\ContSmoo_lv95;Y:\\Projekte\\Geodaten\\Hoehen\\DTM_DOM_AWG\\Scratch\\Scratch.gdb\\Points_lv95", "DXF_R14", OutputDXF, "Use_Filenames_in_Tables", "Overwrite_Existing_Files", "")

    arcpy.AddMessage("Loeschen der Zwischenresultate")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
    arcpy.Delete_management(ScratchRaster1)
    arcpy.Delete_management(cont_orig1)
    arcpy.Delete_management(OutputSmoothLine)
    arcpy.Delete_management(OutputEndPoints)
    arcpy.Delete_management(OutputMidPoints)
    arcpy.Delete_management(projectedOutputLines)
    arcpy.Delete_management(projectedOutputPoints)

    del ScratchRaster1
    del cont_orig1
    del OutputSmoothLine
    del OutputEndPoints
    del OutputMidPoints
    del OutputDXF
    del Perimeter
    del Aequidistanz
    del SmoothToleranz
    del DTM_GRID_2m_Uri
    del projectedOutputLines
    del projectedOutputPoints

    arcpy.AddMessage("Prozess beendet")
    arcpy.AddMessage("*******************************************************************************")
    arcpy.AddMessage("")
except:
    print arcpy.GetMessages()

