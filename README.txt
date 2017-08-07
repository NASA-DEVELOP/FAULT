FAULT - Flood Algorithm Utilizing Landsat and ArcMap Tools

Points of Contact regarding code
Mercedes Bartkovich - bartkovichm@gmail.com
Nicholas McVey      - nam0014@uah.edu
Helen Baldwin-Zook  - helenbluebaldwin@gmail.com
Dashiell Cruz       - cruzd@uah.edu


Part A - What the script accomplishes 


	This script serves as an automation of a flood mapping algorithm created previous by the Mississippi River Basin Disasters I project. The project follows a methodology that heavily relies on the ArcMap program to conduct analysis. This analysis will attempt to isolate flood water in a Normalized Difference Water Index calculation from satellite imagery.

	Firstly, the script needs to have its workplace set. This is where the user will store the local variables and where the user wants the all of the data and results to be place upon running the code. This is done manually by editing the code itself. Once the work space is set manually, the script can be ran. A prompt is presented to the user to name a folder where all the output will be placed upon the completion of the script. Then the local variables that are stored the workspace are set so that the script can draw from the data to conduct the necessary steps for flood analysis.

	After the workspace and output folder is set up, the script begins the processing of the data. Bands 3, 5, and 9 (The USGS cloud mask product) are mosaicked together. (If two or more landsat tiles are being analyzed, this allows for everything to be conducted together rather than multiple runs of the script on each tile individually). Next the cloud mask, or Band 9, is reclassified changing the multiple layers of clouds mapped into one extent of cloud coverage. This extent serves as the areas of clouds that need to be removed. The next step, Extract by mask, uses this reclassified Band 9 to remove areas of cloud coverage in both Band 3 and Band 5. 

	Once the clouds are removed, a Top of Atmosphere Reflectance conversion is conducted on both Bands 3 and 5, transforming the digital numbers into reflectance values for better interpretation. Next the negative values, largely the background layer behind the landsat tile after the TOA conversion, are removed from the scene. 

	Lastly the Normalized Difference Water Index calculation (NDWI) is conducted concluding the data processing section. 

	A Maximum Likelihood Classification is conducted on the NDWI that was created moments before using a signature file stored in the Local Variables section. This Maximum likelihood classification distinguishes the pixels in the NDWI image that are most likely water and which are most likely land. This serves as our water extent map. The next step gets the raster domain of that map. This will be utilized in order to clip the water mask to the same area that is being studied. The NDWI is then reclassified to a simple 1 for water and 2 for land. With the domain calculated, the NASA MODIS 250m Global Water Mask is used as a water mask for the water that is prevailing in areas during normal conditions. This mask subtracts the normal water from our water extent mask and leaves only a map of water that is not expected to be present in the image. This unexpected water is concluded to flood induced. This map is our Flood Extent Map. 

	The final step for the Flood Extent Map is to remove the land component of the dataset. The map is reclassified to map only the flood extent. 

	The next session is to conduct some impact analysis using this flood extent map

	With the domain that was calculated using the NDWI original image, the Landscan dataset, infrastructure dataset, and Landcover dataset are clipped to the study area. An intersection process is performed that determines the where the datasets and the flood extent map share pixels. This intersection produces maps of population impacts, agricultural fields damaged, and infrastructure affected by the flooding. The maps created are the components to our Flood Impact Map. 

	For area analysis, note that Landsat 8 is a 30m by 30m resolution. Mulitplying each pixel counted as being impacted by 900m^2 will give you area of flood impact. This can be converted to areas, miles, feet, anything you'd like via normal conversion methodology. 


Part B – Package or Software Dependencies

	This script imports Arcpy, and heavily relies on the ArcGIS Map software. The script itself is written in Python 2.7 shell. 
