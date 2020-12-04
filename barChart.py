# this script needs proprietary software (ArcGIS) to run
import arcpy, os
import matplotlib.pyplot as plt

arcpy.env.overWriteOutput = True

# FIXME is it possible to use named parameters here?
# see https://python-docs.readthedocs.io/en/latest/writing/style.html
input_data = arcpy.GetParameterAsText(0)
fieldY = arcpy.GetParameterAsText(1)
fieldX = arcpy.GetParameterAsText(2)
#fieldLabel= arcpy.GetParameterAsText(3)
outGraphName = arcpy.GetParameterAsText(3)
out_graph = arcpy.GetParameterAsText(4)
title = arcpy.GetParameterAsText(5)

arcpy.env.workspace = os.getcwd()

# Create the graph
graph = arcpy.Graph()

# TODO add code to check valid input before doing anything with it!
graph.addSeriesBarVertical(input_data, fieldY, fieldX)
# Specify the title of the left axis
graph.graphAxis[0].title = fieldY

# Specify the title of the bottom axis
graph.graphAxis[2].title = fieldX

# Specify the title of the Graph
graph.graphPropsGeneral.title = title

# Output a graph, which is created in-memory
arcpy.MakeGraph_management(arcpy.GraphTemplate(), graph, outGraphName)

# Save the graph as an image
arcpy.SaveGraph_management(outGraphName, out_graph, 'MAINTAIN_ASPECT_RATIO')
