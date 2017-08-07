#Import arcpy modules
import arcpy, arcinfo
import os
import glob
import arcgisscripting
import urllib

from arcpy import env
from arcpy.sa import *


# Set your workspace
arcpy.env.workspace = r"G:\Mississippi River Basin Disasters II Closeout\FAULT Program"

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")
arcpy.CheckOutExtension("3D")

#Turn overwrite function on
arcpy.env.overwriteOutput = True

#Make a new folder with the name that the user inputs  
folderName = raw_input("Please enter a name for a new folder to store your final products: ")
path = arcpy.env.workspace + "\\" + folderName

def makeFolder (folderName, path):
    path = arcpy.env.workspace + "\\" + folderName
    if os.path.exists(path):
        folderName = raw_input("That name is already in use. Please choose a new name: ")
        path = arcpy.env.workspace + "\\" + folderName
        makeFolder(folderName, path)
        
    else:  
        os.mkdir(path, 0777)
        print "Your folder \"%s\" has been created." %folderName

makeFolder(folderName, path)

# Local variables:
print "Getting Local Variables..."
All_Infrastructures = arcpy.env.workspace + "\Local_Variables" + r"\All_Infrastructures.shp"
NLCD_2011 = arcpy.env.workspace + "\Local_Variables" + r"\nlcd_2011_landcover_2011_edition_2014_10_10.img"
Lspop2014 = arcpy.env.workspace + "\Local_Variables" + r"\Lspop2014"
WaterMask_USA_tif = arcpy.env.workspace + "\Local_Variables" + r"\WaterMask_USA.tif"
NDWI_SignatureFile = arcpy.env.workspace + "\Local_Variables" + r"\ndwi_sigfil.gsg"
print "Setting Outputs..."
mosaic_b3 = arcpy.env.workspace + "\mosaic_b3.tif"
mosaic_b5 = arcpy.env.workspace + "\mosaic_b5.tif"
mosaic_b9 = arcpy.env.workspace + "\mosaic_b9.tif"
CloudMask = arcpy.env.workspace + "\CloudMask"
C3 = arcpy.env.workspace + "\C3"
C5 = arcpy.env.workspace + "\C5"
TOA_mosaic_b3 = arcpy.env.workspace + "\TOA_mosaic_b3"
TOA_mosaic_b5 = arcpy.env.workspace + "\TOA_mosaic_b5"
B3 = arcpy.env.workspace + "\B3"
B5 = arcpy.env.workspace + "\B5"
NDWI = arcpy.env.workspace + "\NDWI"
MLClass_NDWI = arcpy.env.workspace + "\MLClass_NDWI.tif"
Output_confidence_raster = ""
WaterMaskClip_tif = path + "\\" + "WaterMaskClip.tif"
Reclass_watermask_tif = arcpy.env.workspace + "\Reclass_watermask.tif"
Reclass_MLClass_NDWI_tif = arcpy.env.workspace + "\Reclass_MLClass_NDWI.tif"
NDWI_Extracted_WMask_tif = arcpy.env.workspace + "\NDWI_Extracted_WMask.tif"
Flood_Water_tif = path + "\\" + "Flood_Water.tif"
Landscan_Clp = arcpy.env.workspace + "\Landscan_Clp"
FloodMap_ExtentPolygon_shp = arcpy.env.workspace + "\FloodMap_ExtentPolygon.shp"
NLCD_Clp = arcpy.env.workspace + "\NLCD_Clp"
NLCD_Ag_Clp = arcpy.env.workspace + "\\" + "\NLCD_Ag_Clp"
Flooded_Lscan = path + "\\" + "Flooded_Lscan"
Flooded_Ag = path + "\\" + "Flooded_Ag"
Infra_Feature = arcpy.env.workspace + "\Infra_Feature"
Flooded_Infra = path + "\\" + "Flooded_Infra"
Infrastructure_Clp_shp = arcpy.env.workspace + "\\" + "\Infrastructure_Clp.shp"

Band3 = glob.glob(arcpy.env.workspace + r"\LC80*\*B3.tif")
Band5 = glob.glob(arcpy.env.workspace + r"\LC80*\*B5.tif")
Band9 = glob.glob(arcpy.env.workspace + r"\LC80*\*B9.tif")


#Mosaic Landsat data
for mosaic3 in iter(Band3):
    band = mosaic3[-5]
    print " "
    print "Mosaicking band 3..."
    
    arcpy.MosaicToNewRaster_management(Band3, arcpy.env.workspace, "mosaic_b" + band + ".tif", "#", "16_BIT_UNSIGNED", "#", "1", "MAXIMUM", "FIRST")
    break

for mosaic5 in iter(Band5):
    band = mosaic5[-5]
    PR = mosaic5[-25:-19]
    print "Mosaicking band 5..."
    
    arcpy.MosaicToNewRaster_management(Band5, arcpy.env.workspace, "mosaic_b" + band + ".tif", "#", "16_BIT_UNSIGNED", "#", "1", "MAXIMUM", "FIRST")
    break

#Mosaic Landsat data Band 9
for mosaic5 in iter(Band5):
    print "Mosaicking band 9..."
    print " "
    arcpy.MosaicToNewRaster_management(Band9, arcpy.env.workspace, "mosaic_b9.tif", "#", "16_BIT_UNSIGNED", "#", "1", "MAXIMUM", "FIRST")
    break

# Process: Reclassify (7)
print "Reclassifying B9..."
arcpy.gp.Reclassify_sa(mosaic_b9, "Value", "0 1;0 5325 1", CloudMask, "NODATA")

# Process: Extract by Mask - Removing Cloud Coverage
print "Extracting Clouds from B3..."
arcpy.gp.ExtractByMask_sa(mosaic_b3, CloudMask, C3)

# Process: Extract by Mask (2)- Removing Cloud Coverage
print "Extracting Clouds from B5..."
arcpy.gp.ExtractByMask_sa(mosaic_b5, CloudMask, C5)

# Process: Raster Calculator - Completing Top of Atmosphere Conversion
print "Converting B3 to TOA..."
arcpy.gp.RasterCalculator_sa("\"C3\" * (2.0000E-5) + (-0.10000)", TOA_mosaic_b3)
                             
# Process: Raster Calculator (4) - Removing Background Image Space
print "Removing negative values TOA B3..."
arcpy.gp.RasterCalculator_sa("Con(\"TOA_mosaic_b3\" < 0,0,\"TOA_mosaic_b3\")", B3)

# Process: Raster Calculator (3)- Completing Top of Atmosphere Conversion
print "Converting B5 to TOA..."                             
arcpy.gp.RasterCalculator_sa("\"C5\" * (2.0000E-5) + (-0.10000)", TOA_mosaic_b5)

# Process: Raster Calculator (5) - Removing Background Image Space
print "Removing negative values TOA B5..."
arcpy.gp.RasterCalculator_sa("Con(\"TOA_mosaic_b5\" < 0,0,\"TOA_mosaic_b5\")", B5)

# Process: Raster Calculator (2)
print "Performing NDWI..."
arcpy.gp.RasterCalculator_sa("Float(\"B3\" - \"B5\") / Float(\"B3\" + \"B5\")", NDWI)

print " "
print " "
print "Data Processing Complete!"
print " "
print " "

# Process: Maximum Likelihood Classification - Distinguishing Water from Land
print "Performing Maximum Likelihood Classification..."
print " "
print " "
arcpy.gp.MLClassify_sa(NDWI, NDWI_SignatureFile, MLClass_NDWI, "0.0", "EQUAL", "", Output_confidence_raster)

print "Data Analysis Pt. 1 - Maximum Likelihood Classification Complete!"
print " "
print " "

# Process: Raster Domain - Determining Study Area Size
print "Getting Raster Domain..."
arcpy.RasterDomain_3d(mosaic_b3, FloodMap_ExtentPolygon_shp, "POLYGON")

# Process: Clip - Shrinking Water Mask Down to Study Area
print "Clipping Water Mask..."
arcpy.gp.ExtractByMask_sa(WaterMask_USA_tif, FloodMap_ExtentPolygon_shp, WaterMaskClip_tif)

# Process: Reclassify (2) - Changing Values of Classified Image to Facilitate Simpler Mathematical Operations in the Future
print "Reclassifying NDWI Classification..."
arcpy.gp.Reclassify_sa(MLClass_NDWI, "Value", "1 0;1 151 1", Reclass_MLClass_NDWI_tif, "DATA")

# Process: Reclassify - Changing Values of Water Mask to Facilitate Simpler Mathematical Operations in the Future
print "Reclassifying Water Mask..."
arcpy.gp.Reclassify_sa(path + "\\" + "WaterMaskClip.tif", "Value", "0 NODATA;1 2;2 1", Reclass_watermask_tif, "DATA")

# Process: Raster Calculator - Removing Expected Prevailing Water Features From the Water Extent Mask
print "Subtracting Water Mask from NDWI Classification..."
arcpy.gp.RasterCalculator_sa("\"Reclass_watermask.tif\" - \"Reclass_MLClass_NDWI.tif\"", NDWI_Extracted_WMask_tif)

# Process: Reclassify (3) - Changing the Map to Only Depict Areas of Flood Water
print "Identifying Flood Water..."
print " "
print " "
arcpy.gp.Reclassify_sa(NDWI_Extracted_WMask_tif, "Value", "2 1", Flood_Water_tif, "NODATA")

print "Data Analysis Pt. 2 - Flood Extent Map Complete"
print "Your final product 'Flood_Water' is located within %s." %path
print " "
print " "


# Process: Clip - Shrinking Dataset to Study Area
print "Clipping Landscan..."
arcpy.gp.ExtractByMask_sa(Lspop2014, FloodMap_ExtentPolygon_shp, Landscan_Clp)

# Process: Extract by Mask (2) - Determining Impact of Flooding on Dataset
print "Extracting Flooded Landscan by water mask..."
arcpy.gp.ExtractByMask_sa(Landscan_Clp, Flood_Water_tif, Flooded_Lscan)

# Process: Clip (2) - Shrinking Dataset to Study Area
print "Clipping Infrastructures..."
arcpy.Clip_analysis(All_Infrastructures, FloodMap_ExtentPolygon_shp, Infrastructure_Clp_shp, "")

# Process: Feature to Raster
print "Converting Infrastructures from a feature to a raster..."
arcpy.FeatureToRaster_conversion(Infrastructure_Clp_shp, "STRUCTURE", Infra_Feature, "0.002")

# Process: Extract by Mask - Determining Impact of Flooding on Dataset
print "Extracting Flooded Infrastructure by mask..."
print " "
print " "
arcpy.gp.ExtractByMask_sa(Infra_Feature, Flood_Water_tif, Flooded_Infra)

# Process: Clip (3) - Shrinking Dataset to Study Area
print "Clipping NLCD..."
arcpy.gp.ExtractByMask_sa(NLCD_2011, FloodMap_ExtentPolygon_shp, NLCD_Clp)

# Process: Reclassify
print "Reclassify NLCD data..."
arcpy.gp.Reclassify_sa(NLCD_Clp, "Value", "81 1;82 2", NLCD_Ag_Clp, "NODATA")

# Process: Extract by Mask (2) - Determining Impact of Flooding on Dataset
print "Extracting Flooded NLCD by water mask..."
arcpy.gp.ExtractByMask_sa(NLCD_Ag_Clp, Flood_Water_tif, Flooded_Ag)


print "Data Analysis Pt. 3 - Flood Impact Map Complete"
print "Your final product is located within %s." %path
print "Full Flood Analysis Completed! You rock!"
